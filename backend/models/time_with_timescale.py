import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys

sys.path.append("models")
sys.path.append("utils")

import utils.date_utils as date_utils

# from utils.date_utils import weeks_between_dates, get_quarter_by_month
from timescale import TimeScale


# (TODO: implement in UI (e.g. dropdown selection from... to... -> output list of time in UI as a table (need a api call to time_w_timescale to output corresponding list ) -> user fill in table))
class TimeWithTimescale:

    def __init__(self, year: int, time: int, timescale: TimeScale):
        self.year = year
        self.time = time
        self.timescale = timescale

    # return start date with datetime as the type

    def to_start_date(self) -> datetime:

        # print(f"in to_start_date() - self.timescale: {self.timescale}")
        # print(f"in to_start_date() - self.time: {self.time}")
        # print((self.timescale == TimeScale.MONTH))
        # print(type(self.timescale))
        # print(type(TimeScale.MONTH))
        if self.timescale == TimeScale.WEEK:
            start_date = datetime.fromisocalendar(self.year, self.time, 1)
        elif self.timescale == TimeScale.MONTH:
            start_date = datetime(self.year, self.time, 1)
        elif self.timescale == TimeScale.QUARTER:
            start_month = (self.time - 1) * 3 + 1
            start_date = datetime(self.year, start_month, 1)
        elif self.timescale == TimeScale.YEAR:
            start_date = datetime(self.year, 1, 1)
        else:
            start_date = None

        return start_date

    def to_end_date(self) -> datetime:
        if self.timescale == TimeScale.WEEK:
            end_date = datetime.fromisocalendar(self.year, self.time, 7)
        elif self.timescale == TimeScale.MONTH:
            _, last_day = calendar.monthrange(self.year, self.time)
            end_date = datetime(self.year, self.time, last_day)
        elif self.timescale == TimeScale.QUARTER:
            end_month = (self.time - 1) * 3 + 3
            _, last_day = calendar.monthrange(self.year, end_month)
            end_date = datetime(self.year, self.time, last_day)
        elif self.timescale == TimeScale.YEAR:
            end_date = datetime(self.year, 12, 31)
        else:
            end_date = None
        return end_date

    def to_start_calendar_week(self):
        from calendar_week import CalendarWeek

        if self.timescale == TimeScale.WEEK:
            cw = CalendarWeek(self.year, self.time)
        elif self.timescale == TimeScale.MONTH:
            cw = CalendarWeek.get_start_cw_of_month(self.year, self.time)
        elif self.timescale == TimeScale.QUARTER:
            cw = CalendarWeek.get_start_cw_of_quarter(self.year, self.time)
        elif self.timescale == TimeScale.YEAR:
            cw = CalendarWeek(self.year, 1)
        return cw

    def to_end_calendar_week(self):
        from calendar_week import CalendarWeek

        if self.timescale == TimeScale.WEEK:
            cw = CalendarWeek(self.year, self.time)
        elif self.timescale == TimeScale.MONTH:
            cw = CalendarWeek.get_end_cw_of_month(self.year, self.time)
        elif self.timescale == TimeScale.QUARTER:
            cw = CalendarWeek.get_end_cw_of_quarter(self.year, self.time)
        elif self.timescale == TimeScale.YEAR:
            cw = CalendarWeek.get_end_cw_of_year(self.year)
        return cw

    # return the end date with datetime as the type
    def get_end_date_by_duration(
        self,
        duration: int,
    ) -> datetime:
        if self.timescale == TimeScale.MONTH:
            start_date = datetime(self.year, self.time, 1)
            end_date = start_date + relativedelta(months=duration)

        elif self.timescale == TimeScale.QUARTER:
            start_month = (self.time - 1) * 3 + 1
            start_date = datetime(self.year, start_month, 1)
            end_date = start_date + relativedelta(months=duration * 3)

        elif self.timescale == TimeScale.YEAR:
            start_date = datetime(self.year, self.time, 1)
            end_date = start_date + relativedelta(years=duration)

        elif self.timescale == TimeScale.WEEK:
            start_date = datetime.fromisocalendar(self.year, self.time, 7)
            end_date = start_date + relativedelta(weeks=duration)
        return end_date

    # return the duration with week as the timescale
    def get_number_of_week_by_duration(
        self,
        duration: int,
    ) -> int:  # duration_as_week
        if self.timescale == TimeScale.MONTH:
            start_date = datetime(self.year, self.time, 1)
            end_date = start_date + relativedelta(months=duration)
            delta_week = date_utils.weeks_between_dates(start_date, end_date)
        elif self.timescale == TimeScale.QUARTER:
            start_month = (self.time - 1) * 3 + 1
            start_date = datetime(self.year, start_month, 1)
            end_date = start_date + relativedelta(months=duration * 3)
            delta_week = date_utils.weeks_between_dates(start_date, end_date)
        elif self.timescale == TimeScale.YEAR:
            start_date = datetime(self.year, self.time, 1)
            end_date = start_date + relativedelta(years=duration)
            delta_week = date_utils.weeks_between_dates(start_date, end_date)
        elif self.timescale == TimeScale.WEEK:
            delta_week = duration
        return delta_week

    # return start quarter
    def get_start_quarter(self) -> int:
        _date = self.to_start_date()
        return date_utils.get_quarter_by_month(_date.month)

    # return end quarter
    def get_end_quarter(self) -> int:
        _date = self.to_end_date()
        return date_utils.get_quarter_by_month(_date.month)

    # return start month
    def get_start_month(self) -> int:
        _date = self.to_start_date()
        return _date.month

    # return end month
    def get_end_month(self) -> int:
        _date = self.to_end_date()
        return _date.month
