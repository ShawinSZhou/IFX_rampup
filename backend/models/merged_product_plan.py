# merged all product plan dfs into one df
import pandas as pd
from datetime import datetime
import sys

sys.path.append("models")

from product_plan import ProductPlan
from product_detail import ProductDetail


from calendar_week import CalendarWeek
from utils.date_utils import *


class MergedProductPlan:
    def __init__(self, list_of_product_plans: list[ProductPlan]):
        self.list_of_product_plans = list_of_product_plans
        self.df = pd.DataFrame()
        self.get_sheet_start_week()
        self.get_sheet_end_week()
        self.get_mergerd_col_index()

        self.merge_dfs()

        self.df.to_excel("./debug/shipout_debug.xlsx")

    def get_sheet_start_week(self):
        # self.list_of_product_plans[1].product_detail.sheet_start_cw
        self.start_cw: CalendarWeek = min(
            [
                product_plan.product_detail.sheet_start_cw
                for product_plan in self.list_of_product_plans
            ]
        )

    def get_sheet_end_week(self):
        self.end_cw: CalendarWeek = max(
            [
                product_plan.product_detail.sheet_end_cw
                for product_plan in self.list_of_product_plans
            ]
        )

    def get_sheet_duration(self):
        self.duration = CalendarWeek.weeks_between_cws(self.start_cw, self.end_cw)
        self.duration_list_of_weeks = CalendarWeek.cw_list_between_cws(
            self.start_cw, self.end_cw
        )

    def get_mergerd_col_index(self):
        month_cw_list = CalendarWeek.get_month_cw_tuple_list(
            self.start_cw.year,
            self.start_cw.month,
            self.end_cw.year,
            self.end_cw.month,
        )
        self.col_index = pd.MultiIndex.from_tuples(month_cw_list, names=("MONTH", "CW"))

    def get_row_len(self):
        total_row_len = [
            len(product_plan.df_all.index)
            for product_plan in self.list_of_product_plans
        ]

    def get_plan_row_by_type(
        self,
        product_plan: ProductPlan,
        process_step_type: ProductDetail.ProcessStep.TypeOfProcessStep,
    ) -> pd.DataFrame:
        row = product_plan.df_all.loc[
            product_plan.df_all.index == process_step_type
        ].head(1)
        return row

    def move_non_zero(self, row: pd.Series):

        # Identify the first non-zero value in the row
        non_zero_value = row[row != 0]

        if len(non_zero_value) != 0:
            new_row = pd.Series(
                [non_zero_value.values[0]] + [0] * (len(row) - 1), index=row.index
            )
            print(new_row)
            return new_row
        else:
            return row

    def normalize_df(self, product_plan: ProductPlan) -> pd.DataFrame:

        start_col = self.col_index.get_level_values(1).get_loc(
            product_plan.product_detail.sheet_start_cw
        )
        end_col = self.col_index.get_level_values(1).get_loc(
            product_plan.product_detail.sheet_end_cw
        )
        new_df = pd.DataFrame(columns=self.col_index, index=product_plan.df_all.index)
        new_df.iloc[:, start_col : end_col + 1] = product_plan.df_all.iloc[:, :].values
        new_df = new_df.fillna(0)
        return new_df

    def merge_dfs(self):
        combined_list = []
        FE = []
        Bumping = []
        Sort = []
        DPS = []
        DC = []
        DemandRow = []
        ShipoutBalanceRow = []
        TesterQuantityRow = []
        ReachLevelRow = []
        StockBufferRow = []
        ORT_levelRow = []

        step_list = [
            "FE",
            "Bumping",
            "Sort",
            "Tester Quantity",
            "DPS",
            "DC",
            "Weekly Demand",
            "ShipoutBalance",
            "Reach Level",
            "Stock Buffer",
            "ORT Level",
        ]

        for product in self.list_of_product_plans:
            df = self.normalize_df(product)
            FE.append((df.loc[ProductDetail.ProcessStep.TypeOfProcessStep.FE]))
            Bumping.append(df.loc[ProductDetail.ProcessStep.TypeOfProcessStep.Bumping])
            Sort.append(df.loc[ProductDetail.ProcessStep.TypeOfProcessStep.Sort])
            TesterQuantityRow.append(
                df.loc[ProductDetail.ProcessStep.TypeOfProcessStep.TesterQuantityRow]
            )
            DPS.append(df.loc[ProductDetail.ProcessStep.TypeOfProcessStep.DPS])
            DC.append(df.loc[ProductDetail.ProcessStep.TypeOfProcessStep.DC])
            DemandRow.append(
                df.loc[ProductDetail.ProcessStep.TypeOfProcessStep.DemandRow]
            )
            ShipoutBalanceRow.append(
                df.loc[ProductDetail.ProcessStep.TypeOfProcessStep.ShipoutBalance]
            )

            ReachLevelRow.append(
                self.move_non_zero(
                    df.loc[ProductDetail.ProcessStep.TypeOfProcessStep.ReachLevelRow]
                )
            )

            StockBufferRow.append(
                self.move_non_zero(
                    df.loc[ProductDetail.ProcessStep.TypeOfProcessStep.StockBufferRow]
                )
            )
            ORT_levelRow.append(
                self.move_non_zero(
                    df.loc[ProductDetail.ProcessStep.TypeOfProcessStep.ORT_levelRow]
                )
            )

            product_step_list = [
                step + "-" + product.product_detail.basic_type for step in step_list
            ]
            combined_list.append(product_step_list)

        zipped_lists = zip(*combined_list)
        row_index_list = [element for tuple in zipped_lists for element in tuple]

        list_of_lists = [
            FE,
            Bumping,
            Sort,
            TesterQuantityRow,
            DPS,
            DC,
            ShipoutBalanceRow,
            DemandRow,
            ReachLevelRow,
            StockBufferRow,
            ORT_levelRow,
        ]

        FE_df = pd.concat(FE, axis=1).transpose()
        Bumping_df = pd.concat(Bumping, axis=1).transpose()
        Sort_df = pd.concat(Sort, axis=1).transpose()
        TesterQuantityRow_df = pd.concat(TesterQuantityRow, axis=1).transpose()
        DPS_df = pd.concat(DPS, axis=1).transpose()
        DC_df = pd.concat(DC, axis=1).transpose()
        DemandRow_df = pd.concat(DemandRow, axis=1).transpose()
        ShipoutBalanceRow_df = pd.concat(ShipoutBalanceRow, axis=1).transpose()
        ReachLevelRow_df = pd.concat(ReachLevelRow, axis=1).transpose()
        StockBufferRow_df = pd.concat(StockBufferRow, axis=1).transpose()
        ORT_levelRow_df = pd.concat(ORT_levelRow, axis=1).transpose()

        self.df = pd.concat(
            [
                FE_df,
                Bumping_df,
                Sort_df,
                TesterQuantityRow_df,
                DPS_df,
                DC_df,
                DemandRow_df,
                ShipoutBalanceRow_df,
                ReachLevelRow_df,
                StockBufferRow_df,
                ORT_levelRow_df,
            ]
        )
        self.df.index = row_index_list

        print(self.df)


if __name__ == "__main__":
    from time_with_timescale import TimeWithTimescale
    from timescale import TimeScale
    from product_detail import ProductDetail
    from product_plan import ProductPlan
    import pandas as pd

    # process steps
    process_step_1 = ProductDetail.ProcessStep(
        step_name="FE",
        step_type=ProductDetail.ProcessStep.TypeOfProcessStep.FE,
        cycle_time=8,
        transit_time=0,
        step_yield=0.995,
        is_first_step=True,
    )
    process_step_2 = ProductDetail.ProcessStep(
        step_name="Bumping",
        step_type=ProductDetail.ProcessStep.TypeOfProcessStep.Bumping,
        cycle_time=2,
        transit_time=0,
        step_yield=0.998,
        is_first_step=False,
    )
    process_step_3 = ProductDetail.ProcessStep(
        step_name="Sort",
        step_type=ProductDetail.ProcessStep.TypeOfProcessStep.Sort,
        cycle_time=1,
        transit_time=0,
        step_yield=0.95,
        is_first_step=False,
    )
    process_step_4 = ProductDetail.ProcessStep(
        step_name="DPS",
        step_type=ProductDetail.ProcessStep.TypeOfProcessStep.DPS,
        cycle_time=2,
        transit_time=0,
        step_yield=0.995,
        is_first_step=False,
    )
    process_step_5 = ProductDetail.ProcessStep(
        step_name="DC",
        step_type=ProductDetail.ProcessStep.TypeOfProcessStep.DC,
        cycle_time=1,
        transit_time=0,
        step_yield=1.0,
        is_first_step=False,
    )

    process_steps = [
        process_step_1,
        process_step_2,
        process_step_3,
        process_step_4,
        process_step_5,
    ]

    # demand

    M6225A_demand_1 = ProductDetail.Demand(
        quantity=484616, dst_time=TimeWithTimescale(2025, 5, TimeScale.MONTH)
    )
    M6225A_demand_2 = ProductDetail.Demand(
        quantity=3692307, dst_time=TimeWithTimescale(2025, 6, TimeScale.MONTH)
    )
    M6225A_demand_3 = ProductDetail.Demand(
        quantity=3807693, dst_time=TimeWithTimescale(2025, 7, TimeScale.MONTH)
    )
    M6225A_demand_4 = ProductDetail.Demand(
        quantity=3807692, dst_time=TimeWithTimescale(2025, 8, TimeScale.MONTH)
    )
    M6225A_demand_5 = ProductDetail.Demand(
        quantity=5792307, dst_time=TimeWithTimescale(2025, 9, TimeScale.MONTH)
    )
    M6225A_demand_6 = ProductDetail.Demand(
        quantity=5792308, dst_time=TimeWithTimescale(2025, 10, TimeScale.MONTH)
    )

    M6225A_demands = [
        M6225A_demand_1,
        M6225A_demand_2,
        M6225A_demand_3,
        M6225A_demand_4,
        M6225A_demand_5,
        M6225A_demand_6,
    ]

    M6225A = ProductDetail(
        demands=M6225A_demands,
        parallelity=1,
        t_base=674.3,
        basic_type="M6225A",
        salescode="BGSA300AC",
        chip_per_wafer=60927,
        process_steps=process_steps,
        reach_level=4,
        stock_buffer=0,
        ORT_level=0,
        rework_percentage=0,
        pr=85,
    )

    M6222A_demand_2 = ProductDetail.Demand(
        quantity=3438462, dst_time=TimeWithTimescale(2025, 6, TimeScale.MONTH)
    )
    M6222A_demand_3 = ProductDetail.Demand(
        quantity=3438462, dst_time=TimeWithTimescale(2025, 7, TimeScale.MONTH)
    )
    M6222A_demand_4 = ProductDetail.Demand(
        quantity=3392308, dst_time=TimeWithTimescale(2025, 8, TimeScale.MONTH)
    )
    M6222A_demand_5 = ProductDetail.Demand(
        quantity=5492308, dst_time=TimeWithTimescale(2025, 9, TimeScale.MONTH)
    )
    M6222A_demand_6 = ProductDetail.Demand(
        quantity=5492308, dst_time=TimeWithTimescale(2025, 10, TimeScale.MONTH)
    )

    M6222A_demands = [
        M6222A_demand_2,
        M6222A_demand_3,
        M6222A_demand_4,
        M6222A_demand_5,
        M6222A_demand_6,
    ]

    M6222A = ProductDetail(
        demands=M6222A_demands,
        parallelity=1,
        t_base=542.3,
        basic_type="M6222A",
        salescode="BGSA330AC",
        chip_per_wafer=45325,
        process_steps=process_steps,
        reach_level=4,
        stock_buffer=0,
        ORT_level=0,
        rework_percentage=0,
        pr=85,
    )

    # total_wk_of_demand = M6225A.plan_duration

    sheet_1 = ProductPlan(M6225A)
    sheet_2 = ProductPlan(M6222A)

    m_p = MergedProductPlan([sheet_1, sheet_2])
    print(
        [
            member
            for name, member in ProductDetail.ProcessStep.TypeOfProcessStep.__members__.items()
        ]
    )
