DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def get_segment_of_day(datetime, to_combine_with_day_name=False):
    """Return the part of the day for a datetime object."""
    hour = datetime.hour
    if 4 <= hour < 8:
        return "Morning" if to_combine_with_day_name else "Early Morning"
    elif 8 <= hour < 12:
        return "Morning" if to_combine_with_day_name else "Late Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    elif 21 <= hour < 24:
        return "Night" if to_combine_with_day_name else "Nighttime"
    else:  # 0:00 to 4:59
        return "Night" if to_combine_with_day_name else "Late Night"


def get_day_of_week(datetime):
    """Return the weekday name, e.g. 'Monday'."""
    return DAY_NAMES[datetime.weekday()]


def get_day_and_segment(datetime):
    """Return the weekday and part of day, e.g. 'Monday Early Morning'."""
    return f"{get_day_of_week(datetime)} {get_segment_of_day(datetime, to_combine_with_day_name=True)}"


def get_month(datetime):
    """Return the month name, e.g. 'January'."""
    return MONTH_NAMES[datetime.month - 1]


def get_segment_of_week(datetime):
    """Return 'Weekend', 'Midweek', or 'Weekday'."""
    weekday = datetime.weekday()  # Monday = 0, Sunday = 6
    if weekday >= 5:  # Saturday or Sunday
        return "Weekend"
    elif weekday in (2, 3):  # Wednesday or Thursday
        return "Midweek"
    else:  # Monday, Tuesday, Friday
        return "Weekday"


word_creator_registry = {
    "SEGMENT_OF_WEEK": get_segment_of_week,
    "MONTH": get_month,
    "DAY_OF_WEEK_AND_SEGMENT_OF_DAY": get_day_and_segment,
    "DAY_OF_WEEK": get_day_of_week,
    "SEGMENT_OF_DAY": get_segment_of_day,
}
