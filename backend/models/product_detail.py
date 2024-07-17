import enum
import sys

sys.path.append("models")

from time_with_timescale import TimeWithTimescale
from calendar_week import CalendarWeek
from utils.date_utils import *


# User input from form in terms of each product
class ProductDetail:

    class ProcessStep:
        class TypeOfProcessStep(enum.Enum):
            FE = 1
            Bumping = 2
            Sort = 3
            DPS = 4
            DC = 5
            TesterQuantityRow = 6
            DemandRow = 7
            ShipoutBalance = 8
            ReachLevelRow = 9
            StockBufferRow = 10
            ORT_levelRow = 11

        def __init__(
            self,
            step_name: str,
            step_type: TypeOfProcessStep,
            transit_time=0,
            cycle_time=0,
            step_yield=1.0,
            is_first_step=False,
        ) -> None:
            self.step_name = step_name
            self.step_type = step_type
            self.transit_time = transit_time if transit_time != 0 else 0
            self.cycle_time = cycle_time if cycle_time != 0 else 0
            self.step_yield = step_yield if step_yield != 1.0 else 1.0
            self.is_first_step = is_first_step if is_first_step == True else False

        def __str__(self) -> str:
            return self.step_type.name

    class Demand:
        quantity: int
        dst_time: TimeWithTimescale

        def __init__(self, quantity: int, dst_time: TimeWithTimescale) -> None:
            self.quantity = quantity
            self.dst_time = dst_time

    def __init__(
        self,
        demands: list[Demand],
        parallelity: int,
        t_base: float,
        basic_type: str,
        salescode: str,
        chip_per_wafer: int,
        process_steps: list[ProcessStep],
        reach_level: int,
        stock_buffer: int,
        ORT_level: int,
        rework_percentage: int,
        pr: int,
    ) -> None:
        self.demands = demands
        self.parallelity = parallelity
        self.t_base = t_base
        self.basic_type = basic_type
        self.salescode = salescode
        self.chip_per_wafer = chip_per_wafer
        self.process_steps = process_steps
        self.reach_level = reach_level
        self.stock_buffer = stock_buffer
        self.ORT_level = ORT_level
        self.rework_percentage = rework_percentage
        self.pr = pr
        self.set_plan_duration()
        # self.tester_capacity = tester_capacity

    def set_plan_duration(self):
        self.total_tt = sum(
            process_step.transit_time for process_step in self.process_steps
        )
        self.total_ct = sum(
            process_step.cycle_time for process_step in self.process_steps
        )
        self.total_interval_time = (
            self.total_ct
            + self.total_tt
            + self.reach_level
            + self.stock_buffer
            + self.ORT_level
        )
        self.request_start_cw = self.demands[0].dst_time.to_start_calendar_week()

        self.request_end_cw = self.demands[-1].dst_time.to_end_calendar_week()

        self.request_duration = CalendarWeek.weeks_between_cws(
            self.request_start_cw, self.request_end_cw
        )

        ## plan data
        self.plan_start_cw = self.request_start_cw.subtract_week(
            self.total_interval_time
        )
        self.plan_start_year = self.plan_start_cw.year
        self.plan_start_month = self.plan_start_cw.month
        self.plan_start_week = self.plan_start_cw.week

        ## plan end
        self.plan_end_cw = self.plan_start_cw.add_week(
            self.request_duration + self.total_interval_time - 1
        )
        self.plan_end_month = self.plan_end_cw.month
        # self.plan_end_week = self.plan_end_cw.week

        self.plan_end_week = self.plan_end_cw.week

        ## plan duration
        self.plan_duration = CalendarWeek.weeks_between_cws(
            self.plan_start_cw, self.plan_end_cw
        )
        self.plan_duration_list_of_weeks = CalendarWeek.cw_list_between_cws(
            self.plan_start_cw, self.plan_end_cw
        )

        # sheet data
        ## sheet start
        # start CW = month start
        # sheet and actual plan aligned by month - since in the VRFC table need to be group by month
        self.sheet_start_year = self.plan_start_year
        self.sheet_start_month = self.plan_start_month
        self.sheet_start_cw = CalendarWeek.get_start_cw_of_month(
            self.sheet_start_year, self.sheet_start_month
        )

        ## sheet end
        # change accordingly to generate shipout quantity up to end of request
        self.sheet_end_year = self.request_end_cw.year
        self.sheet_end_month = self.request_end_cw.month

        self.sheet_end_cw = CalendarWeek.get_end_cw_of_month(
            self.sheet_end_year, self.sheet_end_month
        )

        ## sheet duration

        self.sheet_month_cw_list = CalendarWeek.get_month_cw_tuple_list(
            self.sheet_start_year,
            self.sheet_start_month,
            self.sheet_end_year,
            self.sheet_end_month,
        )

        self.sheet_duration_in_week = len(self.sheet_month_cw_list)

        self.cws_between_sheet_and_plan_start = (
            CalendarWeek.weeks_between_cws(self.sheet_start_cw, self.plan_start_cw) - 1
        )

        self.cws_between_sheet_and_request_start = (
            CalendarWeek.weeks_between_cws(self.sheet_start_cw, self.request_start_cw)
            - 1
        )
