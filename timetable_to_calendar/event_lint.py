from table_to_events import Event
from hot_fix import fix_date, fix_time


def merge_events(events: list[Event]) -> list[Event]:
    """
    Lint the events list. Merge the consecutive events with the same event_id.
    """
    grouped_events = dict[tuple[str, ...], list[Event]]()  # key:date+time_end+name
    events_by_end = sorted(events, key=lambda x: (x.date, x.time_end))

    for event in events_by_end:
        searching_key = (event.date, event.time_start, event.event_name)
        new_key = (event.date, event.time_end, event.event_name)
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
        start = group[0].time_start
        end = group[-1].time_end
        name, date = group[0].event_name, group[0].date

        if not date:
            raise ValueError(f"Date is empty in {group=}")

        start, end, date = fix_time(start), fix_time(end), fix_date(date)
        merged_events.append(Event(date, start, end, name))
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
