from pathlib import Path
from cell_type_classifier import CellTypeClassifier
from doc_to_table import extract_tables_from_docx
from event_lint import merge_events
from i_calendar import create_ics_file, ics_to_event_list
from paths import EXAMPLE_DATA_FOLDER, TEST_OUTPUT_FOLDER
from table_to_events import Event, extract_events


def app(docx_path: Path, export_ics_path: Path):
    # doc to list[Event]
    tables = extract_tables_from_docx(docx_path)

    # overwrite table[1] with externally edited table_1.csv
    with open(EXAMPLE_DATA_FOLDER / "manual-fix.csv") as f:
        tables[0] = [line.split(",") for line in f.read().splitlines()]

    # table to list[Event]
    all_cell_values = set(cell or None for t in tables for r in t for cell in r)
    # `or None` for https://github.com/microsoft/pylance-release/issues/497
    clf = CellTypeClassifier(all_cell_values)

    events: list[Event] = []
    for table in tables:
        events.extend(extract_events(table, clf))

    # lint_events
    events = merge_events(events)

    # list[Event] to ics
    create_ics_file(events, export_ics_path)

    # convert back for better format
    events = ics_to_event_list(export_ics_path)
    events = sorted(events, key=lambda x: (x.datetime_start))

    return events


if __name__ == "__main__":
    events = app(
        EXAMPLE_DATA_FOLDER / "timetable.docx", TEST_OUTPUT_FOLDER / "timetable.ics"
    )
    print("Extracted events:")
    for event in events:
        print(event)
