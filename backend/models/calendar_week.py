import calendar
import datetime
import isoweek
from datetime import datetime

import sys

sys.path.append("models")
import time_with_timescale
from utils.date_utils import *


class CalendarWeek:
    def __init__(self, year: int, week: int) -> None:
        self.year = year
        self.week = week
        self.set_month_of_cw()

    def __str__(self) -> str:
        return f"CW({self.year}-{self.week})"

    def __eq__(self, other):
        if not isinstance(other, CalendarWeek):
            return NotImplemented
        return self.year == other.year and self.week == other.week

    def __hash__(self) -> int:
        return hash((self.year, self.week))

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, CalendarWeek):
            return NotImplemented
        return (self.year, self.week) < (other.year, other.week)

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)

    def __repr__(self):
        return str(self)

    def add_week(self, week: int):
        last_week = datetime(year=self.year, month=12, day=28).isocalendar()[1]
        _week = self.week + week
        if _week > last_week:
            return CalendarWeek(self.year + 1, _week - last_week)
        else:
            return CalendarWeek(self.year, _week)

    def subtract_week(self, week: int):
        last_week_prev_year = datetime(
            year=self.year - 1, month=12, day=28
        ).isocalendar()[1]
        _week = self.week - week
        if _week <= 0:
            return CalendarWeek(self.year - 1, _week + last_week_prev_year)
        else:
            return CalendarWeek(self.year, _week)

    # Monday as the start day of the week
    def to_cw_start_date(self) -> datetime:
        start_date = datetime.fromisocalendar(self.year, self.week, 1)
        return start_date

    def to_cw_end_date(self):
        end_date = datetime.fromisocalendar(self.year, self.week, 7)
        return end_date

    # use as a iterator
    def range_to(self, end_cw):
        current_cw = CalendarWeek(self.year, self.week)
        while current_cw.year < end_cw.year or (
            current_cw.year == end_cw.year and current_cw.week < end_cw.week
        ):
            yield current_cw
            next_cw = current_cw.add_week(1)
            current_cw = CalendarWeek(next_cw.year, next_cw.week)

    def set_month_of_cw(self):
        cw_start_date = self.to_cw_start_date()
        cw_start_month = cw_start_date.month
        cw_end_date = self.to_cw_end_date()
        cw_end_month = cw_end_date.month
        self.month = cw_end_month

    @classmethod
    # if any 1st day of the next month is in a week, then this week goes to the next month, without overlap
    # return list[CalendarWeek]
    def get_cw_list_by_month(cls, year: int, month: int) -> list:
        start_date = datetime(year, month, 1)
        _, cur_month_last_day = calendar.monthrange(year, month)
        cur_month_end_date = datetime(year, month, cur_month_last_day)
        cur_month_start_week = start_date.isocalendar()[1]
        cur_month_end_week = cur_month_end_date.isocalendar()[1]
        if month == 12:
            next_month_start_date = datetime(year + 1, 1, 1)
        else:
            next_month_start_date = datetime(year, month + 1, 1)
        next_month_start_week = next_month_start_date.isocalendar()[1]
        if (
            cur_month_end_week == next_month_start_week
        ):  # that means the 1st day of the next month is in the last week of cur month
            # -> remove it from the list as it should belong to the next month:
            cur_month_end_week = cur_month_end_week - 1
        if cur_month_end_week == 0:
            cur_month_end_week = isoweek.Week.last_week_of_year(year).week
        cw_list = []
        last_week = datetime(year=year, month=12, day=28).isocalendar()[1]
        if last_week == cur_month_start_week:
            cur_month_start_week = 0
        cw_list = [
            CalendarWeek(year, week)
            for week in range(cur_month_start_week, cur_month_end_week + 1)
        ]
        if last_week == cur_month_start_week:
            cw_list.insert(0, CalendarWeek(year - 1, last_week))
        return cw_list

    @classmethod
    # if any 1st day of the next month is in a week, then this week goes to the next month, without overlap
    # return list[CalendarWeek]
    def get_cw_list_by_quarter(cls, year: int, quarter: int):
        start_month = get_start_month_of_quarter(quarter)
        end_month = get_end_month_of_quarter(quarter)
        cw_list = []
        for month in range(start_month, end_month + 1):
            monthly_cw_list = cls.get_cw_list_by_month(year, month)
            cw_list.extend(monthly_cw_list)
        return cw_list

    @classmethod
    def get_cw_by_date(cls, date: datetime):
        cw = cls(date.isocalendar()[0], date.isocalendar()[1])
        return cw

    @classmethod
    def get_start_cw_of_month(cls, year: int, month: int):
        return cls.get_cw_list_by_month(year, month)[0]

    @classmethod
    def get_end_cw_of_month(cls, year: int, month: int):
        return cls.get_cw_list_by_month(year, month)[-1]

    @classmethod
    def get_start_cw_of_quarter(cls, year: int, quarter: int):
        return cls.get_cw_list_by_quarter(year, quarter)[0]

    @classmethod
    def get_end_cw_of_quarter(cls, year: int, quarter: int):
        return cls.get_cw_list_by_quarter(year, quarter)[-1]

    @classmethod
    def get_end_cw_of_year(cls, year):
        from isoweek import Week

        return cls(year, Week.last_week_of_year(year).week)

    @staticmethod
    # To iterate over every (year, month) tuple given a start year/month and an end year/month
    def iterate_cw(start_cw, end_cw):
        current_cw = start_cw
        while current_cw <= end_cw:
            yield (current_cw)
            current_cw = current_cw.add_week(1)

    @classmethod
    def cw_list_between_cws(cls, start_cw, end_cw):
        return [cw for cw in cls.iterate_cw(start_cw, end_cw)]

    @classmethod
    def cw_list_between_timewithtimescale(
        cls,
        start_time: time_with_timescale.TimeWithTimescale,
        end_time: time_with_timescale.TimeWithTimescale,
    ):
        # need to make sure the 2 timescales are the same
        start_cw = start_time.to_start_calendar_week()
        end_cw = end_time.to_end_calendar_week()
        return cls.cw_list_between_cws(start_cw, end_cw)

    @staticmethod
    # including starting week itself
    def weeks_between_cws(start_cw, end_cw) -> int:
        from isoweek import Week

        # If the start week is greater than the end week, and the years
        # are the same, it means there are no weeks between them.
        if start_cw > end_cw:
            return -1
        # If the start and end are the same, there's effectively 0 week between them.
        if start_cw == end_cw:
            return 1
        if start_cw.year == end_cw.year:
            return end_cw.week - start_cw.week + 1
        weeks_in_start_year = Week.last_week_of_year(start_cw.year).week
        weeks_in_between_years = sum(
            Week.last_week_of_year(y).week
            for y in range(start_cw.year + 1, end_cw.year)
        )
        num_of_weeks = (
            (weeks_in_start_year - start_cw.week) + weeks_in_between_years + end_cw.week
        )

        return num_of_weeks + 1

    @classmethod
    def get_month_cw_tuple_list(
        cls, start_year, start_month, end_year, end_month
    ) -> list[tuple]:

        combined_list = []
        for year, month in iterate_months(start_year, start_month, end_year, end_month):
            month_cw_list = cls.get_cw_list_by_month(year, month)
            month_cw_tuples = [(f"{year}-{month}", cw) for cw in month_cw_list]
            combined_list.extend(month_cw_tuples)
        return combined_list
