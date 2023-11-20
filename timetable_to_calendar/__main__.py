from datetime import timedelta
from pathlib import Path
from cell_type_classifier import CellTypeClassifier
from doc_to_table import extract_tables_from_docx
from event_lint import merge_events
from i_calendar import create_ics_file, ics_to_event_list
from paths import EXAMPLE_DATA_FOLDER, TEST_OUTPUT_FOLDER
from table_to_events import Event, extract_events


def docx_to_events(docx_path: Path) -> list[Event]:
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
    return events


def app(docx_path: Path, export_ics_path: Path):
    events = docx_to_events(docx_path)

    # list[Event] to ics
    create_ics_file(events, export_ics_path)

    # make sure the ics file is correct
    ics_events = ics_to_event_list(export_ics_path)
    assert len(ics_events) == len(events)
    if events == ics_events:
        return events

    for ev, iev in zip(events, ics_events):
        if ev != iev:
            print("events not equal")
            print(ev.__repr__())
            print(iev.__repr__())
            print()
    return events


if __name__ == "__main__":
    events = app(
        EXAMPLE_DATA_FOLDER / "timetable.docx", TEST_OUTPUT_FOLDER / "timetable.ics"
    )
    print("Extracted events:")
    count = 0
    for event in events:
        ...
        # print(event)

        # to generate filenames
        yymmdd = event.datetime_start.strftime("%y%m%d")
        start = event.datetime_start.strftime("%H%M")
        end = event.datetime_end.strftime("%H%M")
        duration = event.datetime_end - event.datetime_start
        if event.summary == "DAODM":
            count += 1
            count_str = f"{count:02}"
            if duration == timedelta(hours=4):
                count += 1
                count_str += f",{count:02}"
            # print(
            #     f"_{event.summary.lower()}-{count_str}-{yymmdd} , class given on 20{yymmdd} {event.datetime_start.strftime('%H%M')}-{event.datetime_end.strftime('%H%M')} by @"
            # )
            # generate a string like this:
            # mkdir _cadm-01-240129 && echo "class given on 20240129 1700-1900 by @" > _cadm-01-240129/cadm-01.note-240129.md && mkdir _cadm-01-240129/cadm-01.files && touch _cadm-01-240129/cadm-01.files/.placeholder
            # mkdir _cadm-01-240129 && echo "class given on 20240129 1700-1900 by @" > _cadm-01-240129/cadm-01.note-240129.md && mkdir _cadm-01-240129/cadm-01.files && touch _cadm-01-240129/cadm-01.files/.placeholder
            # cmd = f'mkdir _{event.summary.lower()}-{count_str}-{yymmdd} && echo "class given on 20{yymmdd} {start}-{end} by @" > _{event.summary.lower()}-{count_str}-{yymmdd}/{event.summary.lower()}-{count_str}.note-{yymmdd}.md && mkdir _{event.summary.lower()}-{count_str}-{yymmdd}/{event.summary.lower()}-{count_str}.files && touch _{event.summary.lower()}-{count_str}-{yymmdd}/{event.summary.lower()}-{count_str}.files/.placeholder'
            # print(cmd)
