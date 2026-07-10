"""
reporting.py

Generates executive-style written summaries from the Sonoran Cycles
simulation outputs and analytics tables.

Responsibilities:
- Summarize key business KPIs
- Identify top-performing models
- Identify fulfillment and inventory risks
- Summarize forecast accuracy
- Summarize supplier exposure
- Export a Markdown executive insights report
"""

from pathlib import Path

import pandas as pd


def safe_divide(numerator, denominator):
    if denominator == 0 or pd.isna(denominator):
        return 0

    return numerator / denominator


def format_currency(value):
    return f"${value:,.0f}"


def format_number(value):
    return f"{value:,.0f}"


def format_percent(value):
    return f"{value:.1%}"


def build_summary_metrics(sim, analytics_tables):
    """
    Builds high-level summary metrics from simulation results.
    """

    orders_df = pd.DataFrame(sim.sales_orders)
    lines_df = pd.DataFrame(sim.sales_order_lines)
    po_df = pd.DataFrame(sim.purchase_orders)
    forecast_df = pd.DataFrame(sim.forecast_history)

    requested_units = lines_df["requested_qty"].sum()
    fulfilled_units = lines_df["fulfilled_qty"].sum()
    backordered_units = lines_df["backordered_qty"].sum()

    booked_revenue = lines_df["extended_price"].sum()
    fulfilled_revenue = lines_df["fulfilled_revenue"].sum()

    service_level = safe_divide(fulfilled_units, requested_units)
    backorder_rate = safe_divide(backordered_units, requested_units)

    open_po_units = 0

    if not po_df.empty:
        open_po_units = po_df.loc[
            po_df["po_status"] == "Open",
            "ordered_qty",
        ].sum()

    forecast_wape = safe_divide(
        forecast_df["absolute_error"].sum(),
        forecast_df["actual_qty"].sum(),
    )

    forecast_bias = safe_divide(
        forecast_df["forecast_error"].sum(),
        forecast_df["actual_qty"].sum(),
    )

    metrics = {
        "sales_orders": orders_df["sales_order_id"].nunique(),
        "sales_order_lines": len(lines_df),
        "purchase_orders": len(po_df),
        "booked_revenue": booked_revenue,
        "fulfilled_revenue": fulfilled_revenue,
        "requested_units": requested_units,
        "fulfilled_units": fulfilled_units,
        "backordered_units": backordered_units,
        "service_level": service_level,
        "backorder_rate": backorder_rate,
        "open_po_units": open_po_units,
        "forecast_wape": forecast_wape,
        "forecast_bias": forecast_bias,
    }

    return metrics


def get_top_model(analytics_tables):
    """
    Returns the top model by booked revenue.
    """

    model_summary = analytics_tables["model_performance_summary"]

    return (
        model_summary
        .sort_values("booked_revenue", ascending=False)
        .iloc[0]
    )


def get_weakest_service_model(analytics_tables):
    """
    Returns the model with weakest service level among models with demand.
    """

    model_summary = analytics_tables["model_performance_summary"]

    filtered = model_summary[
        model_summary["requested_units"] > 0
    ]

    return (
        filtered
        .sort_values("service_level", ascending=True)
        .iloc[0]
    )


def get_worst_stockout_sku(analytics_tables):
    """
    Returns the SKU with the most stockout days.
    """

    inventory_summary = analytics_tables["inventory_kpi_summary"]

    return (
        inventory_summary
        .sort_values(
            ["stockout_days", "stockout_rate"],
            ascending=[False, False],
        )
        .iloc[0]
    )


def get_worst_forecast_model(analytics_tables):
    """
    Returns the model with the highest WAPE.
    """

    forecast_summary = analytics_tables["forecast_accuracy_by_model"]

    return (
        forecast_summary
        .sort_values("wape", ascending=False)
        .iloc[0]
    )


def get_top_supplier_exposure(analytics_tables):
    """
    Returns the supplier with the most open PO exposure.
    """

    supplier_summary = analytics_tables["supplier_performance_summary"]

    if supplier_summary.empty:
        return None

    return (
        supplier_summary
        .sort_values(
            ["open_units", "ordered_units"],
            ascending=[False, False],
        )
        .iloc[0]
    )


def build_executive_summary_markdown(sim, analytics_tables):
    """
    Builds a Markdown executive insights report.
    """

    metrics = build_summary_metrics(sim, analytics_tables)

    top_model = get_top_model(analytics_tables)
    weakest_service_model = get_weakest_service_model(analytics_tables)
    worst_stockout_sku = get_worst_stockout_sku(analytics_tables)
    worst_forecast_model = get_worst_forecast_model(analytics_tables)
    top_supplier = get_top_supplier_exposure(analytics_tables)

    supplier_text = ""

    if top_supplier is not None:
        supplier_text = (
            f"- The supplier with the highest open PO exposure was "
            f"**{top_supplier['supplier_name']}**, with "
            f"**{format_number(top_supplier['open_units'])} open units**.\n"
        )

    markdown = f"""# Sonoran Cycles Executive Insights

## KPI Snapshot

| Metric | Value |
|---|---:|
| Sales Orders | {format_number(metrics["sales_orders"])} |
| Sales Order Lines | {format_number(metrics["sales_order_lines"])} |
| Purchase Orders | {format_number(metrics["purchase_orders"])} |
| Booked Revenue | {format_currency(metrics["booked_revenue"])} |
| Fulfilled Revenue | {format_currency(metrics["fulfilled_revenue"])} |
| Requested Units | {format_number(metrics["requested_units"])} |
| Fulfilled Units | {format_number(metrics["fulfilled_units"])} |
| Backordered Units | {format_number(metrics["backordered_units"])} |
| Service Level | {format_percent(metrics["service_level"])} |
| Backorder Rate | {format_percent(metrics["backorder_rate"])} |
| Open PO Units | {format_number(metrics["open_po_units"])} |
| Forecast WAPE | {format_percent(metrics["forecast_wape"])} |
| Forecast Bias | {format_percent(metrics["forecast_bias"])} |

---

## Key Findings

- The highest-revenue model was **{top_model["model_name"]}**, generating **{format_currency(top_model["booked_revenue"])}** in booked revenue.
- The weakest model-level service level was **{weakest_service_model["model_name"]}**, with a service level of **{format_percent(weakest_service_model["service_level"])}**.
- The SKU with the highest stockout exposure was **{worst_stockout_sku.get("sku", "N/A")}**, with **{format_number(worst_stockout_sku["stockout_days"])} stockout days**.
- The hardest model to forecast was **{worst_forecast_model["model_name"]}**, with WAPE of **{format_percent(worst_forecast_model["wape"])}**.
{supplier_text}
---

## Planning Implications

The simulation suggests that demand planning should focus on three areas:

1. **High-revenue models with fulfillment risk**  
   Products that drive meaningful revenue but have weak service levels should receive priority in inventory planning.

2. **SKU-level stockout concentration**  
   Stockout days and backordered units help identify where reorder points or target stock levels may be too low.

3. **Forecast accuracy by model and season**  
   Models with high WAPE or consistent bias may need more refined forecasting logic, especially around seasonal demand shifts.

---

## Recommended Actions

- Review reorder points and target stock levels for SKUs with high stockout days.
- Prioritize inventory availability for high-revenue models with below-average service levels.
- Investigate whether forecast bias is concentrated in specific models or months.
- Monitor supplier open PO exposure to understand replenishment timing risk.
- Use the Power BI dashboard to track service level, backorders, supplier exposure, and forecast accuracy over time.

---

## Portfolio Summary

This report was generated from a Python-based supply chain simulation that creates ERP-style sales orders, inventory history, purchase orders, replenishment activity, and forecast history.

The analysis demonstrates how simulated operational data can be transformed into SQL analysis, KPI summaries, and dashboard-ready business insights.
"""

    return markdown


def export_executive_summary(sim, analytics_tables, output_file=None):
    """
    Exports the executive insights report to Markdown.
    """

    if output_file is None:
        output_path = sim.project_root / "reports" / "executive_insights.md"
    else:
        output_path = Path(output_file)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    markdown = build_executive_summary_markdown(
        sim,
        analytics_tables,
    )

    output_path.write_text(markdown)

    metrics = build_summary_metrics(
        sim,
        analytics_tables,
    )

    return output_path, metrics