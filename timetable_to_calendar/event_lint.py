from datetime import datetime
from table_to_events import Event


def merge_events(events: list[Event]) -> list[Event]:
    """
    Lint the events list. Merge the consecutive events with the same event_id.
    """
    grouped_events = dict[tuple[datetime, str], list[Event]]()  # key:date+time_end+name
    events_by_end = sorted(events, key=lambda x: (x.datetime_end))

    for event in events_by_end:
        searching_key = (event.datetime_start, event.summary)
        new_key = (event.datetime_end, event.summary)
        if new_key in grouped_events:
            raise ValueError(
                f"Duplicate events in {grouped_events=}: {event=} and {grouped_events[new_key]=} with key {new_key=}"
            )
        if searching_key in grouped_events:
            grouped_events[new_key] = grouped_events.pop(searching_key) + [event]
            continue
        grouped_events[new_key] = [event]

    merged_events = []

    for group in grouped_events.values():
        start = group[0].datetime_start
        end = group[-1].datetime_end
        short = group[0].summary
        full = group[0].description

        merged_events.append(Event(start, end, short, full))
    return merged_events


def test(show=False):
    from table_to_events import test as test_list_to_event

    events = test_list_to_event()
    merged = merge_events(events)
    if show:
        print("Merged events:")
        for event in merged:
            print(event)

    return merged


if __name__ == "__main__":
    test(show=True)
