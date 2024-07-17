import pandas as pd
import sys

sys.path.append("controllers")
sys.path.append("models")

from models.product_plan import ProductPlan
from models.merged_product_plan import MergedProductPlan


class MergedProductPlanGenerator:
    def __init__(self, list_of_product_plans: list[ProductPlan]):
        self.list_of_product_plans = list_of_product_plans

    def validate_product_plans(self):
        # Example validation: Ensure the list is not empty
        if not self.list_of_product_plans:
            raise ValueError("The list of product plans cannot be empty.")

    def generate_merged_product_plan(self) -> MergedProductPlan:
        self.validate_product_plans()
        merged_product_plan = MergedProductPlan(self.list_of_product_plans)
        return merged_product_plan


# Example usage
if __name__ == "__main__":
    # Assuming you have a list of ProductPlan objects
    list_of_product_plans = [
        ...
    ]  # This should be populated with actual ProductPlan objects

    generator = MergedProductPlanGenerator(list_of_product_plans)
    merged_product_plan = generator.generate_merged_product_plan()

    # Now you can use the merged_product_plan object as needed
