import re

def parse_opening_hours(opening_hours: str):
    """
    Analysis openingHours string to (weekday, open_time, close_time) 。

    Args:
        opening_hours (str): e.g. "Mon, Wed, Fri 08:00 - 12:00 / Tue, Thur 14:00 - 18:00"

    Returns:
        List[Tuple[str, str, str]]: e.g. [("Monday", "08:00", "12:00"), ("Tuesday", "14:00", "18:00")]
    """
    time_slots = []
    # Mapping for abbreviated day names.
    days_map = {
        "Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday",
        "Thu": "Thursday", "Thur": "Thursday",
        "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"
    }
    # Ordered list of full day names.
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def get_full_day(day_str):
        """Return the full day name given an abbreviation or full day name."""
        day_str = day_str.strip()
        if day_str in days_map:
            return days_map[day_str]
        elif day_str in weekdays:
            return day_str
        elif day_str[:3] in days_map:
            return days_map[day_str[:3]]
        else:
            return None

    parts = opening_hours.split(" / ")

    for part in parts:
        match = re.search(r"([\w\s,-]+)\s+(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})", part)
        if not match:
            print(f"Can't analyze openingHours: {part}")
            continue

        days_part, open_time, close_time = match.groups()

        # Handle day ranges (e.g., "Mon - Wednesday")
        if " - " in days_part:
            start_day, end_day = days_part.split(" - ")
            start_day_full = get_full_day(start_day)
            end_day_full = get_full_day(end_day)
            if not start_day_full or not end_day_full:
                print(f"Can't analyze start_day and end_day: {days_part}")
                continue
            start_index = weekdays.index(start_day_full)
            end_index = weekdays.index(end_day_full)
            if start_index <= end_index:
                day_list = weekdays[start_index:end_index + 1]
            else:
                day_list = weekdays[start_index:] + weekdays[:end_index + 1]
        else:
            # Handle comma-separated days.
            day_list = []
            for day in days_part.split(","):
                full_day = get_full_day(day)
                if full_day:
                    day_list.append(full_day)
                else:
                    print(f"Unknown weekday: {day}")

        # Process the time ranges.
        if close_time < open_time:  # Overnight case.
            for day in day_list:
                # For the current day, open_time to midnight.
                time_slots.append((day, open_time, "24:00"))
                # For the next day, midnight to close_time.
                current_index = weekdays.index(day)
                next_day = weekdays[(current_index + 1) % 7]
                time_slots.append((next_day, "00:00", close_time))
        else:
            for day in day_list:
                time_slots.append((day, open_time, close_time))

    return time_slots
