# output a spreadsheet based on given ramp start time, duration, containing all the other relavant data from user input

# week-base calculation
import pandas as pd
from datetime import datetime
import sys

sys.path.append("models")

from product_detail import ProductDetail


from calendar_week import CalendarWeek
from utils.date_utils import *


class ProductPlan:
    def __init__(self, product_detail: ProductDetail) -> None:
        self.product_detail = product_detail
        self.generate_weekly_df()

    def generate_weekly_wspw_row(self) -> list[int]:
        import math
        from timescale import TimeScale

        # WSPW formula: wspw=math.ceil((demand/cpw)*0.995)
        row = [0] * self.product_detail.sheet_duration_in_week
        # zero-index + cws between function is inclusive
        start_col_of_row = self.product_detail.cws_between_sheet_and_plan_start
        cpw = self.product_detail.chip_per_wafer

        start_year = self.product_detail.demands[0].dst_time.year
        start_time = self.product_detail.demands[0].dst_time.time
        end_year = self.product_detail.demands[-1].dst_time.year
        end_time = self.product_detail.demands[-1].dst_time.time
        if self.product_detail.demands[0].dst_time.timescale == TimeScale.WEEK:
            row[
                start_col_of_row : start_col_of_row
                + self.product_detail.request_duration
            ] = [
                math.ceil(demand.quantity / cpw * 0.995)
                for demand in self.product_detail.demands
            ]
        if self.product_detail.demands[0].dst_time.timescale == TimeScale.MONTH:
            cur_index = 0
            row_index = start_col_of_row
            for year, month in iterate_months(
                start_year, start_time, end_year, end_time
            ):
                cw_list = CalendarWeek.get_cw_list_by_month(year, month)
                # number of cw of current month
                num_of_cw = len(cw_list)
                weekly_demand = math.ceil(
                    self.product_detail.demands[cur_index].quantity / cpw * 0.995
                )
                weekly_demand_list = [weekly_demand] * num_of_cw
                row[row_index : row_index + num_of_cw] = weekly_demand_list
                row_index += num_of_cw
                cur_index += 1

        if self.product_detail.demands[0].dst_time.timescale == TimeScale.QUARTER:
            cur_index = 0
            row_index = start_col_of_row
            for year, quarter in iterate_quarters(
                start_year, start_time, end_year, end_time
            ):
                cw_list = CalendarWeek.get_cw_list_by_quarter(year, quarter)
                # number of cw of current quarter
                num_of_cw = len(cw_list)
                weekly_demand = math.ceil(
                    self.product_detail.demands[cur_index].quantity / cpw * 0.995
                )
                weekly_demand_list = [weekly_demand] * num_of_cw
                row[row_index : row_index + num_of_cw] = weekly_demand_list
                row_index += num_of_cw
                cur_index += 1

        if self.product_detail.demands[0].dst_time.timescale == TimeScale.YEAR:
            cur_index = 0
            row_index = start_col_of_row
            for year in range(start_year, end_year):
                # number of cw of current year
                num_of_cw = datetime(year=year, month=12, day=28).isocalendar()[1]
                weekly_demand = math.ceil(
                    self.product_detail.demands[cur_index].quantity / cpw * 0.995
                )
                weekly_demand_list = [weekly_demand] * num_of_cw
                row[row_index : row_index + num_of_cw] = weekly_demand_list
                row_index += num_of_cw
                cur_index += 1
            pass
        return row

    def generate_weekly_demand_row(self):
        from timescale import TimeScale

        row = [0] * self.product_detail.sheet_duration_in_week
        # zero-index + cws between function is inclusive
        start_col_of_row = self.product_detail.cws_between_sheet_and_request_start
        start_year = self.product_detail.demands[0].dst_time.year
        start_time = self.product_detail.demands[0].dst_time.time
        end_year = self.product_detail.demands[-1].dst_time.year
        end_time = self.product_detail.demands[-1].dst_time.time

        if self.product_detail.demands[0].dst_time.timescale == TimeScale.WEEK:
            row[
                start_col_of_row : start_col_of_row
                + self.product_detail.request_duration
            ] = [demand.quantity for demand in self.product_detail.demands]

        if self.product_detail.demands[0].dst_time.timescale == TimeScale.MONTH:
            cur_index = 0
            row_index = start_col_of_row
            for year, month in iterate_months(
                start_year, start_time, end_year, end_time
            ):
                cw_list = CalendarWeek.get_cw_list_by_month(year, month)
                # number of cw of current month
                num_of_cw = len(cw_list)
                weekly_demand = self.product_detail.demands[cur_index].quantity
                weekly_demand_list = [weekly_demand] * num_of_cw
                row[row_index : row_index + num_of_cw] = weekly_demand_list
                row_index += num_of_cw
                cur_index += 1

        if self.product_detail.demands[0].dst_time.timescale == TimeScale.QUARTER:
            cur_index = 0
            row_index = start_col_of_row
            for year, quarter in iterate_quarters(
                start_year, start_time, end_year, end_time
            ):
                cw_list = CalendarWeek.get_cw_list_by_quarter(year, quarter)
                # number of cw of current quarter
                num_of_cw = len(cw_list)
                weekly_demand = self.product_detail.demands[cur_index].quantity
                weekly_demand_list = [weekly_demand] * num_of_cw
                row[row_index : row_index + num_of_cw] = weekly_demand_list
                row_index += num_of_cw
                cur_index += 1

        if self.product_detail.demands[0].dst_time.timescale == TimeScale.YEAR:
            cur_index = 0
            row_index = start_col_of_row
            for year in range(start_year, end_year):
                # number of cw of current year
                num_of_cw = datetime(year=year, month=12, day=28).isocalendar()[1]
                weekly_demand = self.product_detail.demands[cur_index].quantity
                weekly_demand_list = [weekly_demand] * num_of_cw
                row[row_index : row_index + num_of_cw] = weekly_demand_list
                row_index += num_of_cw
                cur_index += 1
            pass
        self.demand_row = row

    def generate_tester_per_week(self, sort_row: list[int]):

        self.tester_per_week = [
            round(
                (
                    self.product_detail.t_base
                    * x
                    / 60
                    * (1 + self.product_detail.rework_percentage / 100)
                )
                / 168
                * 100
                / self.product_detail.pr,
                2,
            )
            for x in sort_row
        ]

    def generate_shipout_balance_row(self):
        self.shipout_balance_row = [self.DC_row[0] - self.demand_row[0]]

        # Iterate over the supply and demand lists starting from the second element
        for i in range(1, len(self.DC_row)):
            # Calculate the current week's balance and append to the balance list
            self.shipout_balance_row.append(
                self.DC_row[i - 1]
                + self.shipout_balance_row[i - 1]
                - self.demand_row[i]
            )

    def generate_weekly_df(
        self,
    ):

        import math

        # use multi-index:
        col_index = pd.MultiIndex.from_tuples(
            self.product_detail.sheet_month_cw_list, names=("MONTH", "CW")
        )

        rows = []
        cur_row = []
        start_col_of_row = self.product_detail.cws_between_sheet_and_plan_start
        prev_start_col_of_row = 0
        prev_row = self.generate_weekly_wspw_row()
        prev_process_step = None
        row_index = []

        for cur_process_step in self.product_detail.process_steps:
            cur_row = [0] * (self.product_detail.sheet_duration_in_week)
            if cur_process_step.is_first_step:
                # if is first step: move parallely by multiplying CPW to each WSPW cell
                cur_row[
                    start_col_of_row : start_col_of_row
                    + self.product_detail.request_duration
                ] = [
                    math.ceil(
                        x
                        # * self.product_detail.chip_per_wafer
                        * cur_process_step.step_yield
                    )
                    for x in prev_row[
                        start_col_of_row : start_col_of_row
                        + self.product_detail.request_duration
                    ]
                ]
                # print(len(cur_row))

            else:
                if (
                    cur_process_step.step_type
                    == ProductDetail.ProcessStep.TypeOfProcessStep.DPS
                ):

                    cur_row[
                        start_col_of_row : start_col_of_row
                        + self.product_detail.request_duration
                    ] = [
                        math.ceil(x * cur_process_step.step_yield)
                        * self.product_detail.chip_per_wafer
                        for x in prev_row[
                            prev_start_col_of_row : prev_start_col_of_row
                            + self.product_detail.request_duration
                        ]
                    ]

                else:
                    cur_row[
                        start_col_of_row : start_col_of_row
                        + self.product_detail.request_duration
                    ] = [
                        math.ceil(x * cur_process_step.step_yield)
                        for x in prev_row[
                            prev_start_col_of_row : prev_start_col_of_row
                            + self.product_detail.request_duration
                        ]
                    ]

                if (
                    cur_process_step.step_type
                    == ProductDetail.ProcessStep.TypeOfProcessStep.Sort
                ):
                    self.generate_tester_per_week(cur_row)

            # save DC row for calculation of ShipoutBalance
            if (
                cur_process_step.step_type
                == ProductDetail.ProcessStep.TypeOfProcessStep.DC
            ):
                self.DC_row = cur_row

            rows.append(cur_row)
            row_index.append(cur_process_step.step_type)
            if (
                cur_process_step.step_type
                == ProductDetail.ProcessStep.TypeOfProcessStep.Sort
            ):
                rows.append(self.tester_per_week)
                row_index.append(
                    ProductDetail.ProcessStep.TypeOfProcessStep.TesterQuantityRow
                )
            prev_start_col_of_row = start_col_of_row
            start_col_of_row += (
                cur_process_step.transit_time + cur_process_step.cycle_time
            )

            prev_row = cur_row.copy()
            prev_process_step = cur_process_step

        self.generate_weekly_demand_row()
        row_index.append(ProductDetail.ProcessStep.TypeOfProcessStep.DemandRow)
        rows.append(self.demand_row)

        self.generate_shipout_balance_row()
        row_index.append(ProductDetail.ProcessStep.TypeOfProcessStep.ShipoutBalance)
        rows.append(self.shipout_balance_row)

        # NOTE: logic for reach lvl and ort leadtime - treated like trasist time and cycle time, showing in last row
        row_index.append(ProductDetail.ProcessStep.TypeOfProcessStep.ReachLevelRow)
        rows.append([self.product_detail.reach_level])
        row_index.append(ProductDetail.ProcessStep.TypeOfProcessStep.StockBufferRow)
        rows.append([self.product_detail.stock_buffer])
        row_index.append(ProductDetail.ProcessStep.TypeOfProcessStep.ORT_levelRow)
        rows.append([self.product_detail.ORT_level])

        self.df_all = pd.DataFrame(columns=col_index, index=row_index, data=rows)
        # use multi-index
        self.df_monthly = self.df_all.groupby(level=["MONTH"], axis=1, sort=False).sum()
        # self.df_monthly = self.df_monthly.loc[:, (self.df_monthly != 0).any(axis=0)]
        self.sheet_month_list = col_index.get_level_values(0).values
        self.sheet_cw_list = col_index.get_level_values(1).values
        self.sheet_year_list = [cw.year for cw in self.sheet_cw_list]

        month_abbr_list = [
            get_month_abbr(int(year_month.split("-")[1]))
            for year_month in self.sheet_month_list
        ]

        self.combined_month_year_list = []
        for month, year in zip(month_abbr_list, self.sheet_year_list):
            self.combined_month_year_list.append(month + str(year)[-2:])
