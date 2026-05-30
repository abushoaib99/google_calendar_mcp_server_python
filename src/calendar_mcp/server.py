import json

from mcp.server.fastmcp import FastMCP

from calendar_mcp.calendar import CalendarDateInput, get_events_by_date

mcp = FastMCP("Google Calendar")


@mcp.tool()
async def get_my_calendar_data_by_date_tool(date: str) -> str:
    """
    Fetch Google Calendar events for a specific date from the signed-in user's calendar.

    Requires credentials.json (Desktop OAuth client) in the project root before first use.
    """
    try:
        validated = CalendarDateInput(date=date)
        result = get_events_by_date(validated.date)
    except ValueError as err:
        result = {"error": str(err)}
    except (FileNotFoundError, OSError) as err:
        result = {"error": str(err)}

    return json.dumps(result)
