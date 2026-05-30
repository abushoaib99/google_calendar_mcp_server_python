import json

from mcp.server.fastmcp import FastMCP

from calendar_mcp.calendar import CalendarDateInput, get_events_by_date

mcp = FastMCP("Souyeb's Calendar")


@mcp.tool()
async def get_my_calendar_data_by_date_tool(date: str) -> str:
    """Fetch Google Calendar events for a specific date."""
    try:
        validated = CalendarDateInput(date=date)
        result = get_events_by_date(validated.date)
    except ValueError as err:
        result = {"error": str(err)}

    return json.dumps(result)
