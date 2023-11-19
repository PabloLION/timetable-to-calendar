from datetime import datetime


def fix_date(date_str: str) -> str:
    # suppose the date is in the format similar to "dd-mmm"
    translations = {
        "dic": "dec 2023",  # Assuming "dic" is for December
        "des": "dec 2023",
        "ene": "jan 2024",
        "gen": "jan 2024",
        "febr": "feb 2024",
        "març": "mar 2024",
        "abr": "apr 2024",
        "maig": "may 2024",
        "juny": "jun 2024",
    }

    for cat_month, eng_month in translations.items():
        date_str = date_str.replace(cat_month, eng_month)

    date_str = date_str.rstrip(".")  # remove trailing dot

    if not date_str:
        raise ValueError("Date string is empty")

    return date_str


def fix_time(time_str: str) -> str:
    if not time_str:
        raise ValueError("Time string is empty")
    if ":" not in time_str:
        return f"{time_str}:00"
    return time_str


def fix_date_range(date_time: datetime) -> datetime:
    # #TODO: paramaterize the start and end dates
    # assert that both the start and the end are between sept 2023 and jun 2024
    if date_time.tzinfo is None:
        raise ValueError(f"Error: {date_time=} is not timezone aware")
    if datetime(2023, 9, 1, tzinfo=date_time.tzinfo) > date_time:
        date_time = date_time.replace(year=2024)
    elif date_time > datetime(2024, 6, 30, tzinfo=date_time.tzinfo):
        date_time = date_time.replace(year=2023)
    if not (
        datetime(2023, 9, 1, tzinfo=date_time.tzinfo)
        <= date_time
        <= datetime(2024, 6, 30, tzinfo=date_time.tzinfo)
    ):
        raise ValueError(
            f"Error: {date_time=} is not between 2023-09-01 and 2024-06-30"
        )

    return date_time
