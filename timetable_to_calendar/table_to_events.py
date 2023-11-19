from datetime import datetime
from typing import NamedTuple

import pytz
from paths import EXAMPLE_DATA_FOLDER
from dateutil.parser import parse, ParserError

from cell_type_classifier import CellTypeClassifier, CellType
from constants import EVENT_ID_TO_EVENT_NAME
from timetable_to_calendar.hot_fix import fix_date, fix_date_range, fix_time

List2D = list[list[str]]  # first row is date, some column is time slot


class Event(NamedTuple):
    datetime_start: datetime
    datetime_end: datetime
    event_name: str
    event_short_name: str

    @staticmethod
    def _temp(date: str, start_time: str, end_time: str, event_name: str):
        # Get the timezone
        tz = pytz.timezone("Europe/Madrid")

        # Parse the date and time and make them timezone aware
        start = fix_time(start_time)
        end = fix_time(end_time)
        name, date = event_name, fix_date(date)

        if not date:
            raise ValueError(f"Date is empty for event_name={event_name}")

        try:
            start_date_time = tz.localize(parse(f"{date} {start}"))
            end_date_time = tz.localize(parse(f"{date} {end}"))
        except ValueError:
            raise ValueError(f"Error parsing datetime for event_name={event_name}")

        return Event(start_date_time, end_date_time, name, name)

    def __str__(self) -> str:
        date = self.datetime_start.strftime("%Y-%m-%d")
        start = self.datetime_start.strftime("%H:%M:%S")
        end = self.datetime_end.strftime("%H:%M:%S")
        return f"Ev({date} {start[:2]}-{end[:2]} {self.event_name})"


def extract_events(table: List2D, clf: CellTypeClassifier) -> list[Event]:
    events = []
    for row in table:
        start_time, end_time = "", ""
        for ic, cell_val in enumerate(row):
            date = table[0][ic]
            if clf(cell_val) == CellType.TIME_SLOT:
                start_time, end_time = cell_val.split("-")
            elif clf(cell_val) == CellType.EVENT_ID:
                if not start_time or not end_time:
                    raise ValueError(f"Wrong time slot in {row=}, {ic=}, {cell_val=}")
                _event_name = EVENT_ID_TO_EVENT_NAME.get(cell_val)
                event_name = _event_name.full if _event_name else cell_val
                events.append(Event._temp(date, start_time, end_time, event_name))
    events.sort(key=lambda x: x.datetime_start)
    return events


# Sample CSV data (the first four lines of your data, as an example)
def test(show: bool = False) -> list[Event]:
    with open(EXAMPLE_DATA_FOLDER / "manual-fix.csv") as f:
        table = [line.split(",") for line in f.read().splitlines()]

    all_cell_values = set(cell or None for row in table for cell in row)
    # `or None` for https://github.com/microsoft/pylance-release/issues/497
    clf = CellTypeClassifier(all_cell_values)
    extracted_events = extract_events(table, clf)

    # Print or process the extracted events
    if show:
        print("Extracted events:")
        for event in extracted_events:
            print(event)

    return extracted_events


if __name__ == "__main__":
    test(show=True)
