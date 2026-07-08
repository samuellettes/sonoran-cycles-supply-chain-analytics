"""
forecasting.py

Creates baseline demand forecasts for the Sonoran Cycles simulation.

Responsibilities:
- Aggregate requested demand by product and month
- Generate rolling baseline forecasts
- Apply simple seasonality adjustment
- Compare forecasted demand to actual demand
- Calculate forecast error, absolute error, WAPE, and forecast bias

Forecasts are based on requested quantity, not fulfilled quantity,
because demand planning should measure unconstrained customer demand.
"""

import numpy as np
import pandas as pd

import simulation.simulation_config as config


def build_monthly_actuals(sim):
    """
    Aggregates requested demand by product and month.
    """

    orders_df = pd.DataFrame(sim.sales_orders)
    lines_df = pd.DataFrame(sim.sales_order_lines)

    if orders_df.empty or lines_df.empty:
        raise ValueError("No sales data found. Run the sales simulation first.")

    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])

    lines_with_dates = lines_df.merge(
        orders_df[["sales_order_id", "order_date"]],
        on="sales_order_id",
        how="left",
    )

    lines_with_dates["month_start"] = (
        lines_with_dates["order_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly_actuals = (
        lines_with_dates
        .groupby(
            [
                "product_id",
                "model_name",
                "category",
                "month_start",
            ],
            as_index=False,
        )["requested_qty"]
        .sum()
        .rename(columns={"requested_qty": "actual_qty"})
    )

    product_master = sim.products[
        [
            "product_id",
            "model_name",
            "category",
        ]
    ].drop_duplicates()

    months = pd.date_range(
        start=monthly_actuals["month_start"].min(),
        end=monthly_actuals["month_start"].max(),
        freq="MS",
    )

    product_month_grid = (
        product_master.assign(key=1)
        .merge(
            pd.DataFrame({"month_start": months, "key": 1}),
            on="key",
        )
        .drop(columns="key")
    )

    monthly_actuals = product_month_grid.merge(
        monthly_actuals,
        on=[
            "product_id",
            "model_name",
            "category",
            "month_start",
        ],
        how="left",
    )

    monthly_actuals["actual_qty"] = (
        monthly_actuals["actual_qty"]
        .fillna(0)
        .astype(int)
    )

    return monthly_actuals


def calculate_seasonality_adjustment(target_month, history_months):
    """
    Adjusts the rolling average based on monthly seasonality.
    """

    target_factor = config.MONTHLY_MULTIPLIER[pd.Timestamp(target_month).month]

    history_factors = [
        config.MONTHLY_MULTIPLIER[pd.Timestamp(month).month]
        for month in history_months
    ]

    average_history_factor = np.mean(history_factors)

    if average_history_factor == 0:
        return 1.0

    return target_factor / average_history_factor


def generate_baseline_forecast(sim, lookback_months=3):
    """
    Generates a rolling baseline forecast by product and month.

    Method:
    - Use the previous N months of actual demand
    - Calculate a rolling average
    - Adjust for monthly seasonality
    - Compare forecast to actual demand
    """

    monthly_actuals = build_monthly_actuals(sim)

    forecast_rows = []

    for product_id, product_history in monthly_actuals.groupby("product_id"):
        product_history = (
            product_history
            .sort_values("month_start")
            .reset_index(drop=True)
        )

        for index in range(lookback_months, len(product_history)):
            target_row = product_history.iloc[index]
            history = product_history.iloc[index - lookback_months:index]

            base_forecast = history["actual_qty"].mean()

            seasonality_adjustment = calculate_seasonality_adjustment(
                target_month=target_row["month_start"],
                history_months=history["month_start"],
            )

            forecast_qty = int(
                round(
                    max(
                        0,
                        base_forecast * seasonality_adjustment,
                    )
                )
            )

            actual_qty = int(target_row["actual_qty"])

            forecast_error = actual_qty - forecast_qty
            absolute_error = abs(forecast_error)

            if actual_qty > 0:
                absolute_percentage_error = absolute_error / actual_qty
            else:
                absolute_percentage_error = None

            forecast_rows.append(
                {
                    "forecast_month": target_row["month_start"].strftime("%Y-%m-%d"),
                    "product_id": product_id,
                    "model_name": target_row["model_name"],
                    "category": target_row["category"],
                    "lookback_months": lookback_months,
                    "forecast_qty": forecast_qty,
                    "actual_qty": actual_qty,
                    "forecast_error": forecast_error,
                    "absolute_error": absolute_error,
                    "absolute_percentage_error": absolute_percentage_error,
                    "seasonality_adjustment": round(seasonality_adjustment, 3),
                }
            )

    forecast_df = pd.DataFrame(forecast_rows)

    sim.forecast_history = forecast_df.to_dict("records")

    return forecast_df


def calculate_forecast_metrics(forecast_df):
    """
    Calculates summary forecast accuracy metrics.
    """

    if forecast_df.empty:
        raise ValueError("Forecast table is empty.")

    total_actual_qty = forecast_df["actual_qty"].sum()
    total_forecast_qty = forecast_df["forecast_qty"].sum()
    total_absolute_error = forecast_df["absolute_error"].sum()
    total_forecast_error = forecast_df["forecast_error"].sum()

    if total_actual_qty > 0:
        wape = total_absolute_error / total_actual_qty
        bias_pct = total_forecast_error / total_actual_qty
    else:
        wape = None
        bias_pct = None

    mape_rows = forecast_df[
        forecast_df["absolute_percentage_error"].notna()
    ]

    mean_absolute_percentage_error = (
        mape_rows["absolute_percentage_error"].mean()
        if not mape_rows.empty
        else None
    )

    return {
        "forecast_rows": len(forecast_df),
        "total_actual_qty": int(total_actual_qty),
        "total_forecast_qty": int(total_forecast_qty),
        "total_absolute_error": int(total_absolute_error),
        "wape": round(wape, 4) if wape is not None else None,
        "bias_pct": round(bias_pct, 4) if bias_pct is not None else None,
        "mean_absolute_percentage_error": (
            round(mean_absolute_percentage_error, 4)
            if mean_absolute_percentage_error is not None
            else None
        ),
    }