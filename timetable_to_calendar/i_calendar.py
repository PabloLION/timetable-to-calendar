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

        # Add properties to the event
        cal_event.add("summary", event.summary)
        cal_event.add("dtstart", event.datetime_start)
        cal_event.add("dtend", event.datetime_end)
        cal_event.add("dtstamp", datetime.now(event.datetime_start.tzinfo))
        # Timestamp should be in UTC
        cal_event.add("description", event.description)

        # Add event to the calendar
        cal.add_component(cal_event)

    # Write to file
    with open(file_path, "wb") as f:
        f.write(cal.to_ical())


def ics_to_event_list(ics_file_path) -> list[Event]:
    with open(ics_file_path, "rb") as ics_file:
        # Load the ICS file
        cal = Calendar.from_ical(ics_file.read())

        # List to hold Event objects
        events_list = []

        for component in cal.walk():
            if component.name != "VEVENT":
                continue
            # Extract event details
            short_name = str(component.get("summary"))
            full_name = str(component.get("description"))
            start = component.get("dtstart").dt
            end = component.get("dtend").dt

            # Convert to timezone-aware datetime objects
            if isinstance(start, datetime) and start.tzinfo is None:
                start = pytz.timezone("Europe/Madrid").localize(start)
            if isinstance(end, datetime) and end.tzinfo is None:
                end = pytz.timezone("Europe/Madrid").localize(end)

            # Create an Event object and add it to the list
            event = Event(
                start,
                end,
                short_name,
                full_name,
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
