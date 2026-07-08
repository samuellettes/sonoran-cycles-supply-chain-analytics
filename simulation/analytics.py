"""
analytics.py

Builds KPI and analytical summary tables for the Sonoran Cycles
supply chain simulation.

Responsibilities:
- Summarize monthly sales performance
- Summarize model-level performance
- Summarize SKU-level inventory performance
- Summarize forecast accuracy by model
- Summarize supplier purchase order performance
- Export dashboard-ready analytics tables
"""

from pathlib import Path

import numpy as np
import pandas as pd


def safe_divide(numerator, denominator):
    """
    Safely divides two numbers.

    Returns 0 when the denominator is zero or missing.
    """

    if denominator == 0 or pd.isna(denominator):
        return 0

    return numerator / denominator


def get_orders_and_lines(sim):
    """
    Returns sales order headers and lines as DataFrames.
    """

    orders_df = pd.DataFrame(sim.sales_orders)
    lines_df = pd.DataFrame(sim.sales_order_lines)

    if orders_df.empty or lines_df.empty:
        raise ValueError("No sales order data found. Run the simulation first.")

    orders_df = orders_df.copy()
    lines_df = lines_df.copy()

    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])

    return orders_df, lines_df


def build_monthly_sales_summary(sim):
    """
    Builds monthly sales performance by sales channel.
    """

    orders_df, lines_df = get_orders_and_lines(sim)

    orders_df["month_start"] = (
        orders_df["order_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly_orders = (
        orders_df
        .groupby(["month_start", "sales_channel"], as_index=False)
        .agg(
            order_count=("sales_order_id", "nunique"),
            customer_count=("customer_id", "nunique"),
            booked_revenue=("order_total", "sum"),
        )
    )

    lines_with_dates = lines_df.merge(
        orders_df[
            [
                "sales_order_id",
                "order_date",
                "month_start",
                "sales_channel",
            ]
        ],
        on="sales_order_id",
        how="left",
    )

    monthly_lines = (
        lines_with_dates
        .groupby(["month_start", "sales_channel"], as_index=False)
        .agg(
            order_lines=("line_number", "count"),
            requested_units=("requested_qty", "sum"),
            fulfilled_units=("fulfilled_qty", "sum"),
            backordered_units=("backordered_qty", "sum"),
            fulfilled_revenue=("fulfilled_revenue", "sum"),
            booked_gross_profit=("gross_profit", "sum"),
            fulfilled_gross_profit=("fulfilled_gross_profit", "sum"),
        )
    )

    monthly_summary = monthly_orders.merge(
        monthly_lines,
        on=["month_start", "sales_channel"],
        how="left",
    )

    monthly_summary["service_level"] = monthly_summary.apply(
        lambda row: safe_divide(
            row["fulfilled_units"],
            row["requested_units"],
        ),
        axis=1,
    )

    monthly_summary["backorder_rate"] = monthly_summary.apply(
        lambda row: safe_divide(
            row["backordered_units"],
            row["requested_units"],
        ),
        axis=1,
    )

    monthly_summary["booked_gross_margin_pct"] = monthly_summary.apply(
        lambda row: safe_divide(
            row["booked_gross_profit"],
            row["booked_revenue"],
        ),
        axis=1,
    )

    monthly_summary["fulfilled_gross_margin_pct"] = monthly_summary.apply(
        lambda row: safe_divide(
            row["fulfilled_gross_profit"],
            row["fulfilled_revenue"],
        ),
        axis=1,
    )

    monthly_summary["month_start"] = monthly_summary["month_start"].dt.strftime(
        "%Y-%m-%d"
    )

    return monthly_summary.sort_values(
        ["month_start", "sales_channel"]
    ).reset_index(drop=True)


def build_model_performance_summary(sim):
    """
    Builds model-level sales, margin, and fulfillment performance.
    """

    _, lines_df = get_orders_and_lines(sim)

    model_summary = (
        lines_df
        .groupby(["model_name", "category"], as_index=False)
        .agg(
            sales_orders=("sales_order_id", "nunique"),
            order_lines=("line_number", "count"),
            unique_skus=("product_id", "nunique"),
            requested_units=("requested_qty", "sum"),
            fulfilled_units=("fulfilled_qty", "sum"),
            backordered_units=("backordered_qty", "sum"),
            booked_revenue=("extended_price", "sum"),
            fulfilled_revenue=("fulfilled_revenue", "sum"),
            booked_gross_profit=("gross_profit", "sum"),
            fulfilled_gross_profit=("fulfilled_gross_profit", "sum"),
        )
    )

    model_summary["service_level"] = model_summary.apply(
        lambda row: safe_divide(
            row["fulfilled_units"],
            row["requested_units"],
        ),
        axis=1,
    )

    model_summary["backorder_rate"] = model_summary.apply(
        lambda row: safe_divide(
            row["backordered_units"],
            row["requested_units"],
        ),
        axis=1,
    )

    model_summary["booked_gross_margin_pct"] = model_summary.apply(
        lambda row: safe_divide(
            row["booked_gross_profit"],
            row["booked_revenue"],
        ),
        axis=1,
    )

    model_summary["fulfilled_gross_margin_pct"] = model_summary.apply(
        lambda row: safe_divide(
            row["fulfilled_gross_profit"],
            row["fulfilled_revenue"],
        ),
        axis=1,
    )

    model_summary["average_selling_price"] = model_summary.apply(
        lambda row: safe_divide(
            row["booked_revenue"],
            row["requested_units"],
        ),
        axis=1,
    )

    return model_summary.sort_values(
        "booked_revenue",
        ascending=False,
    ).reset_index(drop=True)


def build_inventory_kpi_summary(sim):
    """
    Builds SKU-level inventory performance summary.

    This identifies SKUs with low average availability, frequent
    stockouts, and weak inventory positions.
    """

    inventory_df = pd.DataFrame(sim.inventory_history)

    if inventory_df.empty:
        raise ValueError("No inventory history found. Run the simulation first.")

    inventory_df = inventory_df.copy()
    inventory_df["snapshot_date"] = pd.to_datetime(inventory_df["snapshot_date"])

    product_columns = [
        "product_id",
        "model_name",
        "category",
        "size",
        "color",
    ]

    if "sku" in sim.products.columns:
        product_columns.insert(1, "sku")

    products_df = sim.products[product_columns].drop_duplicates()

    inventory_with_products = inventory_df.merge(
        products_df,
        on="product_id",
        how="left",
    )

    inventory_summary = (
        inventory_with_products
        .groupby(product_columns, as_index=False)
        .agg(
            average_on_hand=("on_hand", "mean"),
            average_available=("available", "mean"),
            minimum_available=("available", "min"),
            maximum_available=("available", "max"),
            ending_on_hand=("on_hand", "last"),
            ending_available=("available", "last"),
            snapshot_days=("snapshot_date", "nunique"),
            stockout_days=("available", lambda x: int((x <= 0).sum())),
        )
    )

    inventory_summary["stockout_rate"] = inventory_summary.apply(
        lambda row: safe_divide(
            row["stockout_days"],
            row["snapshot_days"],
        ),
        axis=1,
    )

    return inventory_summary.sort_values(
        ["stockout_days", "average_available"],
        ascending=[False, True],
    ).reset_index(drop=True)

def build_forecast_accuracy_by_model(sim):
    """
    Builds model-level forecast accuracy summary.
    """

    forecast_df = pd.DataFrame(sim.forecast_history)

    if forecast_df.empty:
        raise ValueError(
            "No forecast history found. Run generate_baseline_forecast() first."
        )

    forecast_summary = (
        forecast_df
        .groupby(["model_name", "category"], as_index=False)
        .agg(
            forecast_rows=("product_id", "count"),
            actual_qty=("actual_qty", "sum"),
            forecast_qty=("forecast_qty", "sum"),
            absolute_error=("absolute_error", "sum"),
            forecast_error=("forecast_error", "sum"),
        )
    )

    forecast_summary["wape"] = forecast_summary.apply(
        lambda row: safe_divide(
            row["absolute_error"],
            row["actual_qty"],
        ),
        axis=1,
    )

    forecast_summary["bias_pct"] = forecast_summary.apply(
        lambda row: safe_divide(
            row["forecast_error"],
            row["actual_qty"],
        ),
        axis=1,
    )

    forecast_summary["forecast_accuracy"] = 1 - forecast_summary["wape"]

    return forecast_summary.sort_values(
        "wape",
        ascending=False,
    ).reset_index(drop=True)


def build_supplier_performance_summary(sim):
    """
    Builds supplier-level purchase order performance summary.
    """

    po_df = pd.DataFrame(sim.purchase_orders)

    if po_df.empty:
        return pd.DataFrame(
            columns=[
                "supplier_id",
                "supplier_name",
                "purchase_orders",
                "open_purchase_orders",
                "received_purchase_orders",
                "ordered_units",
                "received_units",
                "open_units",
                "average_lead_time_days",
                "receipt_rate",
            ]
        )

    po_df = po_df.copy()

    po_df["open_units"] = np.where(
        po_df["po_status"] == "Open",
        po_df["ordered_qty"] - po_df["received_qty"],
        0,
    )

    po_df["is_open"] = po_df["po_status"] == "Open"
    po_df["is_received"] = po_df["po_status"] == "Received"

    supplier_summary = (
        po_df
        .groupby(["supplier_id", "supplier_name"], as_index=False)
        .agg(
            purchase_orders=("purchase_order_id", "nunique"),
            open_purchase_orders=("is_open", "sum"),
            received_purchase_orders=("is_received", "sum"),
            ordered_units=("ordered_qty", "sum"),
            received_units=("received_qty", "sum"),
            open_units=("open_units", "sum"),
            average_lead_time_days=("lead_time_days", "mean"),
        )
    )

    supplier_summary["receipt_rate"] = supplier_summary.apply(
        lambda row: safe_divide(
            row["received_units"],
            row["ordered_units"],
        ),
        axis=1,
    )

    return supplier_summary.sort_values(
        "ordered_units",
        ascending=False,
    ).reset_index(drop=True)


def build_daily_kpi_summary(sim):
    """
    Builds daily KPI summary combining sales, inventory, and purchasing.
    """

    orders_df, lines_df = get_orders_and_lines(sim)
    daily_summary_df = pd.DataFrame(sim.daily_order_summary)

    if daily_summary_df.empty:
        raise ValueError("No daily summary found. Run the simulation first.")

    daily_summary_df = daily_summary_df.copy()
    daily_summary_df["date"] = pd.to_datetime(daily_summary_df["date"])

    orders_df["date"] = orders_df["order_date"].dt.normalize()

    daily_orders = (
        orders_df
        .groupby("date", as_index=False)
        .agg(
            sales_orders=("sales_order_id", "nunique"),
            customer_count=("customer_id", "nunique"),
            booked_revenue=("order_total", "sum"),
        )
    )

    lines_with_dates = lines_df.merge(
        orders_df[["sales_order_id", "date"]],
        on="sales_order_id",
        how="left",
    )

    daily_lines = (
        lines_with_dates
        .groupby("date", as_index=False)
        .agg(
            requested_units=("requested_qty", "sum"),
            fulfilled_units=("fulfilled_qty", "sum"),
            backordered_units=("backordered_qty", "sum"),
            fulfilled_revenue=("fulfilled_revenue", "sum"),
        )
    )

    daily_kpi = daily_summary_df.merge(
        daily_orders,
        on="date",
        how="left",
    ).merge(
        daily_lines,
        on="date",
        how="left",
    )

    daily_kpi["service_level"] = daily_kpi.apply(
        lambda row: safe_divide(
            row["fulfilled_units"],
            row["requested_units"],
        ),
        axis=1,
    )

    daily_kpi["backorder_rate"] = daily_kpi.apply(
        lambda row: safe_divide(
            row["backordered_units"],
            row["requested_units"],
        ),
        axis=1,
    )

    daily_kpi["date"] = daily_kpi["date"].dt.strftime("%Y-%m-%d")

    return daily_kpi.sort_values("date").reset_index(drop=True)


def build_all_analytics_tables(sim):
    """
    Builds all dashboard-ready analytics tables.
    """

    tables = {
        "monthly_sales_summary": build_monthly_sales_summary(sim),
        "model_performance_summary": build_model_performance_summary(sim),
        "inventory_kpi_summary": build_inventory_kpi_summary(sim),
        "forecast_accuracy_by_model": build_forecast_accuracy_by_model(sim),
        "supplier_performance_summary": build_supplier_performance_summary(sim),
        "daily_kpi_summary": build_daily_kpi_summary(sim),
    }

    return tables


def export_analytics_tables(sim, output_folder=None):
    """
    Exports all analytics tables to CSV.
    """

    if output_folder is None:
        output_path = sim.output_path / "analytics"
    else:
        output_path = Path(output_folder)

    output_path.mkdir(parents=True, exist_ok=True)

    tables = build_all_analytics_tables(sim)

    for table_name, table_df in tables.items():
        table_df.to_csv(
            output_path / f"{table_name}.csv",
            index=False,
        )

    return tables