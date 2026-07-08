"""
simulation_runner.py

Runs the Sonoran Cycles sales simulation across a calendar date range.

Responsibilities:
- Prepare the simulation object
- Loop through calendar dates
- Receive inbound purchase orders
- Generate daily dealer and DTC orders
- Review inventory and create new purchase orders
- Record daily inventory snapshots
- Store daily order summaries
"""

import pandas as pd

import simulation.simulation_config as config

from simulation.customer_engine import add_customer_order_weights
from simulation.order_generator import generate_daily_orders

from simulation.inventory_engine import (
    record_inventory_snapshot,
    calculate_inventory_summary,
)

from simulation.purchasing_engine import (
    receive_purchase_orders,
    review_inventory_and_create_purchase_orders,
)


def prepare_simulation(sim):
    """
    Prepares the simulation object before running.
    """

    sim.customers = add_customer_order_weights(sim.customers)

    return sim


def get_weather_for_day(calendar_row):
    """
    Returns weather for a calendar row.

    If the calendar table does not contain weather, use the default
    weather setting from simulation_config.py.
    """

    if "weather" in calendar_row and pd.notna(calendar_row["weather"]):
        return calendar_row["weather"]

    if "weather_condition" in calendar_row and pd.notna(calendar_row["weather_condition"]):
        return calendar_row["weather_condition"]

    return config.DEFAULT_WEATHER


def filter_calendar(calendar_df, start_date=None, end_date=None):
    """
    Filters calendar to an optional date range.
    """

    calendar_df = calendar_df.copy()
    calendar_df["date"] = pd.to_datetime(calendar_df["date"])

    if start_date is not None:
        calendar_df = calendar_df[
            calendar_df["date"] >= pd.Timestamp(start_date)
        ]

    if end_date is not None:
        calendar_df = calendar_df[
            calendar_df["date"] <= pd.Timestamp(end_date)
        ]

    return calendar_df


def run_sales_simulation(sim, start_date=None, end_date=None):
    """
    Runs sales order generation, inventory allocation, and replenishment
    over the selected calendar range.
    """

    if sim.calendar is None:
        raise ValueError(
            "Calendar has not been loaded. Run sim.load_master_data() first."
        )

    prepare_simulation(sim)

    calendar = filter_calendar(
        sim.calendar,
        start_date=start_date,
        end_date=end_date,
    )

    daily_summaries = []

    for _, calendar_row in calendar.iterrows():
        date = calendar_row["date"]
        weather = get_weather_for_day(calendar_row)

        # 1. Receive inbound purchase orders due today
        receipt_summary = receive_purchase_orders(
            sim=sim,
            date=date,
        )

        # 2. Generate customer orders and allocate available inventory
        daily_summary = generate_daily_orders(
            sim=sim,
            date=date,
            weather=weather,
        )

        # 3. Review ending inventory and create new purchase orders
        po_summary = review_inventory_and_create_purchase_orders(
            sim=sim,
            date=date,
        )

        # 4. Record ending inventory snapshot
        record_inventory_snapshot(
            sim=sim,
            date=date,
        )

        # 5. Calculate inventory summary metrics
        inventory_summary = calculate_inventory_summary(sim)

        # 6. Add purchasing and inventory metrics to the daily summary
        daily_summary.update(receipt_summary)
        daily_summary.update(po_summary)
        daily_summary.update(inventory_summary)

        daily_summaries.append(daily_summary)

    sim.daily_order_summary = daily_summaries

    return daily_summaries