import calendar
import datetime
import isoweek
from datetime import datetime, timedelta
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from models.timescale import TimeScale


# month start: 1st of month
# week start: monday
# from week to month: if any of the weekday in a week contains next month's 1st day - > next week -> which month does it belongs to can be determined by weekend number


# convert weekend to the next nearest monday
def ensure_date_is_weekday(date: datetime):
    if date.weekday() >= 5:
        date += timedelta(days=7 - date.weekday())
    return date


# unused
# function to calculate the weeks between 2 dates
def weeks_between_dates(start_date, end_date):
    weeks = rrule.rrule(
        rrule.WEEKLY,
        dtstart=start_date,
        until=end_date,
    )
    return weeks.count() - 1


# unused
# return start date with datetime as the type
def convert_time_scale_to_start_date(
    time_scale: TimeScale, start_year: int, input_start_time: int
) -> datetime:
    """
    Converts a time scale and start time into a corresponding start date.

    Based on the specified `time_scale` (e.g., YEAR, MONTH, QUARTER, WEEK), this function calculates
    the start date of that period for the given `start_year`.

    Parameters:
    - time_scale (TimeScale): An enum indicating the scale of time (YEAR, MONTH, QUARTER, WEEK).
    - start_year (int): The year in which the time scale is situated.
    - input_start_time (int): The specific time unit within the year corresponding to the `time_scale`
                              (e.g., month number for MONTH, quarter number for QUARTER, etc.).

    Returns:
    - datetime: A datetime object representing the start date of the specified time period.

    Raises:
    - ValueError: If `input_start_time` is not within the valid range for the given `time_scale`.

    Note:
    - This function assumes that the `TimeScale` enum is defined and available in the scope.
    - For WEEK scale, the `input_start_time` is expected to be the ISO week number.

    Examples:
    >>> convert_time_scale_to_start_date(TimeScale.MONTH, 2024, 5)
    datetime.datetime(2024, 5, 1)

    >>> convert_time_scale_to_start_date(TimeScale.QUARTER, 2024, 2)
    datetime.datetime(2024, 4, 1)

    >>> convert_time_scale_to_start_date(TimeScale.YEAR, 2024, 1)
    datetime.datetime(2024, 1, 1)

    >>> convert_time_scale_to_start_date(TimeScale.WEEK, 2024, 22)
    datetime.datetime(2024, 5, 27)
    """
    if time_scale == TimeScale.MONTH:
        start_date = datetime(start_year, input_start_time, 1)
    elif time_scale == TimeScale.QUARTER:
        start_month = (input_start_time - 1) * 3 + 1
        start_date = datetime(start_year, start_month, 1)
    elif time_scale == TimeScale.YEAR:
        start_date = datetime(start_year, 1, 1)
    elif time_scale == TimeScale.WEEK:
        start_date = datetime.fromisocalendar(start_year, input_start_time, 1)
    return start_date


# unused
def convert_time_scale_to_end_date(
    time_scale: TimeScale, end_year: int, input_end_time: int
) -> datetime:
    """
    Converts a time scale and end time into a corresponding end date.

    Based on the specified `time_scale` (e.g., MONTH, QUARTER, YEAR, WEEK), this function calculates
    the end date of that period for the given `end_year`.

    Parameters:
    - time_scale (TimeScale): An enum indicating the scale of time (MONTH, QUARTER, YEAR, WEEK).
    - end_year (int): The year in which the time scale is situated.
    - input_end_time (int): The specific time unit within the year corresponding to the `time_scale`
                            (e.g., month number for MONTH, quarter number for QUARTER, etc.).

    Returns:
    - datetime: A datetime object representing the end date of the specified time period.

    Raises:
    - ValueError: If `input_end_time` is not within the valid range for the given `time_scale`.

    Note:
    - This function assumes that the `TimeScale` enum is defined and available in the scope.
    - For the QUARTER scale, the `input_end_time` should be the quarter number (1-4).
    - For the WEEK scale, the `input_end_time` is expected to be the ISO week number and the date returned will be the last day of that week (Sunday).

    Examples:
    >>> convert_time_scale_to_end_date(TimeScale.MONTH, 2023, 5)
    datetime.datetime(2023, 5, 31)

    >>> convert_time_scale_to_end_date(TimeScale.QUARTER, 2023, 2)
    datetime.datetime(2023, 6, 30)

    >>> convert_time_scale_to_end_date(TimeScale.YEAR, 2023, 1)
    datetime.datetime(2023, 12, 31)

    >>> convert_time_scale_to_end_date(TimeScale.WEEK, 2023, 22)
    datetime.datetime(2023, 6, 4)
    """
    if time_scale == TimeScale.MONTH:
        _, last_day = calendar.monthrange(end_year, input_end_time)
        end_date = datetime(end_year, input_end_time, last_day)
    elif time_scale == TimeScale.QUARTER:
        end_month = (input_end_time - 1) * 3 + 3
        _, last_day = calendar.monthrange(end_year, end_month)
        end_date = datetime(end_year, input_end_time, last_day)
    elif time_scale == TimeScale.YEAR:
        end_date = datetime(end_year, 12, 31)
    elif time_scale == TimeScale.WEEK:
        end_date = datetime.fromisocalendar(end_year, input_end_time, 7)
    return end_date


# unused
# return the end date with datetime as the type
def duration_to_end_date(
    time_scale: TimeScale, start_year: int, input_start_time: int, input_duration: int
) -> datetime:
    if time_scale == TimeScale.MONTH:
        start_date = datetime(start_year, input_start_time, 1)
        end_date = start_date + relativedelta(months=input_duration)
    elif time_scale == TimeScale.QUARTER:
        start_month = (input_start_time - 1) * 3 + 1
        start_date = datetime(start_year, start_month, 1)
        end_date = start_date + relativedelta(months=input_duration * 3)
    elif time_scale == TimeScale.YEAR:
        start_date = datetime(start_year, input_start_time, 1)
        end_date = start_date + relativedelta(years=input_duration)
    elif time_scale == TimeScale.WEEK:
        start_date = datetime.fromisocalendar(start_year, input_start_time, 7)
        end_date = start_date + relativedelta(weeks=input_duration)

    return end_date


# unused
# return the duration with week as the timescale
def duration_to_week(
    time_scale: TimeScale, start_year: int, input_start_time: int, input_duration: int
) -> int:  # duration_as_week
    if time_scale == TimeScale.MONTH:
        start_date = datetime(start_year, input_start_time, 1)
        end_date = start_date + relativedelta(months=input_duration)
        delta_week = weeks_between_dates(start_date, end_date)
    elif time_scale == TimeScale.QUARTER:
        start_month = (input_start_time - 1) * 3 + 1
        start_date = datetime(start_year, start_month, 1)
        end_date = start_date + relativedelta(months=input_duration * 3)
        delta_week = weeks_between_dates(start_date, end_date)
    elif time_scale == TimeScale.YEAR:
        start_date = datetime(start_year, input_start_time, 1)
        end_date = start_date + relativedelta(years=input_duration)
        delta_week = weeks_between_dates(start_date, end_date)
    elif time_scale == TimeScale.WEEK:
        delta_week = input_duration
    return delta_week


# unused
# return list of week numbers given start time and duration
def duration_to_week_list_in_datetime(
    start_date: datetime, duration_in_week: int
) -> list[datetime]:
    week_list = []
    for week in range(duration_in_week):
        week_date = start_date + timedelta(weeks=week)
        week_list.append(week_date)
    return week_list


# unused
# return list of months given start time and duration
def duration_to_month_list(start_date: datetime, duration_in_month: int) -> list[int]:
    month_list = []
    for month in range(duration_in_month):
        month_date = start_date + relativedelta(months=month)
        month_list.append(month_date)
    return month_list


# return quarter of given year and week/date
def get_quarter_by_date_or_week(
    input_date=None, is_datetime=True, input_year=0, input_week=0
) -> int:
    if is_datetime:
        date = input_date
    else:
        date = datetime.fromisocalendar(input_year, input_week, 7)
    quarter = (date.month - 1) // 3 + 1
    return quarter


# return quarter of given month
def get_quarter_by_month(input_month=0) -> int:
    quarter = (input_month - 1) // 3 + 1
    return quarter


# return the start month of the quarter
def get_start_month_of_quarter(quarter: int) -> int:
    start_month_of_quarter = (quarter - 1) * 3 + 1
    return start_month_of_quarter


# return the end month of the quarter
def get_end_month_of_quarter(quarter: int) -> int:
    return get_start_month_of_quarter(quarter) + 2


# return the last week of the quarter
def get_last_week_of_quarter(year: int, quarter: int) -> int:
    month = get_end_month_of_quarter(quarter)
    _, last_day = calendar.monthrange(year, month)
    date = datetime(year, month, last_day)
    week = date.isocalendar()[1]
    return week


# return the starting week of the month
def get_start_week_of_month(year: int, month: int) -> int:
    date = datetime(year, month, 1)
    week = date.isocalendar()[1]
    return week


# return the last week of the month
def get_end_week_of_month(year: int, month: int) -> int:
    _, last_day = calendar.monthrange(year, month)
    date = datetime(year, month, last_day)
    week = date.isocalendar()[1]
    return week


# if any 1st day in a week, then this week goes to the next month, without overlap
def get_week_list_by_month(
    input_year=0, input_month=0, is_datetime=False, input_datetime=None
) -> list[int]:
    if is_datetime:
        month = input_datetime.month
        year = input_datetime.year
    else:
        month = input_month
        year = input_year
    start_date = datetime(year, month, 1)
    _, last_day = calendar.monthrange(year, month)
    end_date = datetime(year, month, last_day)
    start_week = start_date.isocalendar()[1]
    end_week = end_date.isocalendar()[1]
    if month == 12:
        start_date_of_next_month = datetime(year + 1, 1, 1)
    else:
        start_date_of_next_month = datetime(year, month + 1, 1)
    start_week_of_next_month = start_date_of_next_month.isocalendar()[1]
    if end_week == start_week_of_next_month:
        end_week = end_week - 1
    if end_week == 0:
        end_week = isoweek.Week.last_week_of_year(input_year).week
    week_list = list(range(start_week, end_week + 1))
    return week_list


# unused
def get_year_quarter_month_week_tuple(
    input_year=0, input_month=0, is_datetime=False, input_datetime=None
) -> list[tuple]:
    """
    Generates a list of tuples, each containing the year, quarter, month, and ISO week number for a specific month, without any overlapping weeks.

    Depending on the arguments provided, the function can calculate the list based on an explicitly given year and month or
    derive the year and month from a provided datetime object. The function handles edge cases such as the end of the year and
    correctly calculates the last week of the year based on ISO standards. If any 1st day of a month is in a week, then this week goes to the next month to avoid overlappings.

    Parameters:
    - input_year (int): The year for which the ISO week numbers list is to be generated. Ignored if `is_datetime` is True.
    - input_month (int): The month for which the ISO week numbers list is to be generated. Ignored if `is_datetime` is True.
    - is_datetime (bool): Flag indicating whether the `input_datetime` should be used to determine the month and year.
    - input_datetime (datetime, optional): If `is_datetime` is True, this is used to extract the month and year.

    Returns:
    - list[tuple]: A list of tuples where each tuple contains the year, quarter, month, and ISO week number.

    Raises:
    - ValueError: If `is_datetime` is True but `input_datetime` is None.

    Examples:
        >>> get_iso_weeks_by_month_and_quarter(input_year=2023, input_month=5)
    [(2023, 2, 5, 18), (2023, 2, 5, 19), ..., (2023, 2, 5, 22)]

        >>> get_iso_weeks_by_month_and_quarter(is_datetime=True, input_datetime=datetime(2023, 5, 15))
    [(2023, 2, 5, 18), (2023, 2, 5, 19), ..., (2023, 2, 5, 22)]
    """
    if is_datetime and input_datetime:
        month = input_datetime.month
        year = input_datetime.year
    else:
        month = input_month
        year = input_year
    start_date = datetime(year, month, 1)
    _, last_day = calendar.monthrange(year, month)
    end_date = datetime(year, month, last_day)
    start_week = start_date.isocalendar()[1]
    end_week = end_date.isocalendar()[1]
    if month == 12:
        start_date_of_next_month = datetime(year + 1, 1, 1)
    else:
        start_date_of_next_month = datetime(year, month + 1, 1)
    start_week_of_next_month = start_date_of_next_month.isocalendar()[1]
    if end_week == start_week_of_next_month:
        end_week = end_week - 1
    if end_week == 0:
        end_week = isoweek.Week.last_week_of_year(input_year).week
    tuple_list = [
        (year, get_quarter_by_month(month), month, week)
        for week in range(start_week, end_week + 1)
    ]
    return tuple_list


# unused
def generate_iso_weeks_for_date_range(
    start_year, start_month, end_year, end_month
) -> list[tuple]:
    """
    Creates a list of tuples with year, quarter, month, and ISO week numbers for each week within a given date range.

    This function iterates over each month within the specified start and end dates, generating tuples that represent
    all ISO week numbers within each month. It is dependent on the helper functions 'iterate_months' which yields each
    month in the range and 'get_year_quarter_month_week_tuple' which generates the ISO week numbers for a given month.

    Parameters:
    - start_year (int): The starting year of the date range.
    - start_month (int): The starting month of the date range.
    - end_year (int): The ending year of the date range.
    - end_month (int): The ending month of the date range.

    Returns:
    - list[tuple]: A list of tuples, each containing:
        - year (int): The year of the week.
        - quarter (int): The fiscal quarter of the week.
        - month (int): The month of the week.
        - week (int): The ISO week number.

    Raises:
    - ValueError: If the start date is after the end date, or if invalid month and year values are provided.

    Examples:
    >>> generate_iso_weeks_for_date_range(2023, 1, 2023, 3)
    [(2023, 1, 1, 1), (2023, 1, 1, 2), ..., (2023, 1, 3, 13)]

    Note:
    - The function assumes that 'iterate_months' and 'get_year_quarter_month_week_tuple' are defined elsewhere and are
      used to perform the iteration of months and the calculation of week numbers respectively.
    - The function does not perform validation on the input parameters; this validation should be handled externally.
    """
    combined_list = []
    for year, month in iterate_months(start_year, start_month, end_year, end_month):
        month_week_tuples = get_year_quarter_month_week_tuple(year, month)
        combined_list.extend(month_week_tuples)
    return combined_list


# To iterate over every (year, month) tuple given a start year/month and an end year/month
def iterate_months(start_year, start_month, end_year, end_month):
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)

    current_date = start_date
    while current_date <= end_date:
        yield (current_date.year, current_date.month)
        current_date += relativedelta(months=1)


def iterate_quarters(start_year, start_quarter, end_year, end_quarter):
    current_year = start_year
    current_quarter = start_quarter
    while current_year < end_year or (
        current_year == end_year and current_quarter <= end_quarter
    ):
        yield (current_year, current_quarter)
        current_quarter += 1
        if current_quarter > 4:
            current_year += 1
            current_quarter = 1


def get_month_abbr(month_number):
    if 1 <= month_number <= 12:
        return calendar.month_abbr[month_number].upper()
    else:
        return "Invalid month number"
