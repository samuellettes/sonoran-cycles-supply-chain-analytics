"""
simulation.py

Central simulation object for the Sonoran Cycles demand planning project.
"""

from pathlib import Path
import pandas as pd


class Simulation:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.data_path = self.project_root / "data"
        self.output_path = self.project_root / "outputs"

        self.products = None
        self.customers = None
        self.suppliers = None
        self.calendar = None

        self.sales_orders = []
        self.sales_order_lines = []
        self.purchase_orders = []
        self.inventory_history = []
        self.forecast_history = []

        self.inventory = None

        self.next_sales_order = 100000
        self.next_purchase_order = 50000

    def load_master_data(self):
        self.products = pd.read_csv(self.data_path / "products.csv")
        self.customers = pd.read_csv(self.data_path / "customers.csv")
        self.suppliers = pd.read_csv(self.data_path / "suppliers.csv")
        self.calendar = pd.read_csv(self.data_path / "calendar.csv")

    def initialize_inventory(self):
        self.inventory = self.products[["product_id"]].copy()
        self.inventory["on_hand"] = 40
        self.inventory["allocated"] = 0
        self.inventory["available"] = 40

    def next_sales_order_number(self):
        order = f"SO{self.next_sales_order}"
        self.next_sales_order += 1
        return order

    def next_purchase_order_number(self):
        po = f"PO{self.next_purchase_order}"
        self.next_purchase_order += 1
        return po

    def export_tables(self):
        self.output_path.mkdir(exist_ok=True)

        pd.DataFrame(self.sales_orders).to_csv(
            self.output_path / "sales_orders.csv",
            index=False,
        )

        pd.DataFrame(self.sales_order_lines).to_csv(
            self.output_path / "sales_order_lines.csv",
            index=False,
        )

        pd.DataFrame(self.purchase_orders).to_csv(
            self.output_path / "purchase_orders.csv",
            index=False,
        )

        pd.DataFrame(self.inventory_history).to_csv(
            self.output_path / "inventory_history.csv",
            index=False,
        )