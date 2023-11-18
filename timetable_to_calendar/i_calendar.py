from pathlib import Path
from icalendar import Calendar, Event as iCalEvent
from datetime import datetime
from dateutil.parser import parse, ParserError
import pytz

from table_to_events import Event


def create_ics_file(events: list[Event], file_path: Path):
    cal = Calendar()

    for event in events:
        # Create an iCalendar event
        cal_event = iCalEvent()

        # Get the timezone
        tz = pytz.timezone(event.timezone)

        # Parse the date and time and make them timezone aware
        try:
            start_date_time = tz.localize(parse(f"{event.date} {event.time_start}"))
            end_date_time = tz.localize(parse(f"{event.date} {event.time_end}"))
        except ParserError:
            print(f"Error parsing datetime in {event.date=} {event.time_start=}")
            continue
        # Add properties to the event
        cal_event.add("summary", event.event_name)
        cal_event.add("dtstart", start_date_time)
        cal_event.add("dtend", end_date_time)
        cal_event.add("dtstamp", datetime.now(pytz.utc))  # Timestamp should be in UTC

        # Add event to the calendar
        cal.add_component(cal_event)

    # Write to file
    with open(file_path, "wb") as f:
        f.write(cal.to_ical())


def ics_to_event_list(ics_file_path):
    with open(ics_file_path, "rb") as ics_file:
        # Load the ICS file
        cal = Calendar.from_ical(ics_file.read())

        # List to hold Event objects
        events_list = []

        for component in cal.walk():
            if component.name != "VEVENT":
                continue
            # Extract event details
            summary = str(component.get("summary"))
            start = component.get("dtstart").dt
            end = component.get("dtend").dt

            # Convert to timezone-aware datetime objects
            if isinstance(start, datetime) and start.tzinfo is None:
                start = pytz.timezone("Europe/Madrid").localize(start)
            if isinstance(end, datetime) and end.tzinfo is None:
                end = pytz.timezone("Europe/Madrid").localize(end)

            # Format date and time
            date_str = start.strftime("%Y-%m-%d")
            time_start_str = start.strftime("%H:%M:%S")
            time_end_str = end.strftime("%H:%M:%S")

            # Create an Event object and add it to the list
            event = Event(
                date=date_str,
                time_start=time_start_str,
                time_end=time_end_str,
                event_name=summary,
            )
            events_list.append(event)

        return events_list


def test(show=False):
    from event_lint import test as test_event_lint

    test_path = Path("test.ics")
    events = test_event_lint()
    create_ics_file(events, test_path)
    events_list = ics_to_event_list(test_path)
    if show:
        print("Events list:")
        for event in events_list:
            print(event)
    return events_list


if __name__ == "__main__":
    test(show=True)
