from datetime import datetime, timedelta, timezone

from googleapiclient.discovery import build
from pydantic import BaseModel, Field, field_validator

from calendar_mcp.auth import get_credentials


class CalendarDateInput(BaseModel):
    date: str = Field(
        ..., description="The date to fetch calendar events for (e.g., '2026-05-30')"
    )

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: str) -> str:
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    "Invalid date format. Please provide a valid date string."
                )
        return value


def get_events_by_date(date_str: str) -> dict:
    """Fetch up to 10 events from the primary calendar for the given date."""
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds, cache_discovery=False)

        try:
            parsed_date = datetime.fromisoformat(
                date_str.replace("Z", "+00:00")
            ).astimezone(timezone.utc)
        except ValueError:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )

        start = parsed_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start.isoformat(),
                timeMax=end.isoformat(),
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        meetings = []
        for event in events_result.get("items", []):
            start_time = event["start"].get("dateTime", event["start"].get("date"))
            meetings.append(f"{event.get('summary', 'No Title')} at {start_time}")

        return {"meetings": meetings}

    except Exception as e:
        print("ERROR:: ", e)
        return {"error": str(e)}
