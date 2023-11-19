from typing import NamedTuple
from paths import REPO_ROOT

from cell_type_classifier import CellTypeClassifier, CellType
from constants import EVENT_ID_TO_EVENT_NAME

List2D = list[list[str]]  # first row is date, some column is time slot


class Event(NamedTuple):
    date: str
    time_start: str  # hour if not specified
    time_end: str
    event_name: str
    timezone: str = "Europe/Madrid"


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
                events.append(Event(date, start_time, end_time, event_name))
    events.sort(key=lambda x: x.date)
    return events


# Sample CSV data (the first four lines of your data, as an example)
def test(show: bool = False) -> list[Event]:
    with open(REPO_ROOT / "table_2.csv") as f:
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
