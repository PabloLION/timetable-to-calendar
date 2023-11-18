def fix_date(date_str: str) -> str:
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

    return date_str.rstrip(".")


def fix_time(time_str: str) -> str:
    if not time_str:
        raise ValueError("Time string is empty")
    if ":" not in time_str:
        return f"{time_str}:00"
    return time_str
