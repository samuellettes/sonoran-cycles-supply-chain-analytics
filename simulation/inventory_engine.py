"""
inventory_engine.py

Handles inventory allocation and inventory history for the
Sonoran Cycles simulation.

Responsibilities:
- Check available inventory by product
- Allocate inventory to sales order lines
- Calculate fulfilled and backordered quantities
- Maintain daily inventory snapshots
- Support future purchasing and replenishment logic
"""

import pandas as pd


def get_inventory_index(sim, product_id):
    """
    Returns the row index for a product in the inventory table.
    """

    matches = sim.inventory.index[
        sim.inventory["product_id"] == product_id
    ].tolist()

    if not matches:
        raise ValueError(f"Product ID {product_id} not found in inventory.")

    return matches[0]


def get_available_qty(sim, product_id):
    """
    Returns available inventory for a product.
    """

    index = get_inventory_index(sim, product_id)

    return int(sim.inventory.at[index, "available"])


def allocate_inventory(sim, product_id, requested_qty):
    """
    Allocates inventory to a sales order line.

    Returns fulfilled quantity, backordered quantity, and fill rate.
    """

    index = get_inventory_index(sim, product_id)

    available_qty = int(sim.inventory.at[index, "available"])

    fulfilled_qty = min(requested_qty, available_qty)
    backordered_qty = requested_qty - fulfilled_qty

    sim.inventory.at[index, "on_hand"] = (
        int(sim.inventory.at[index, "on_hand"]) - fulfilled_qty
    )

    sim.inventory.at[index, "available"] = (
        int(sim.inventory.at[index, "on_hand"])
        - int(sim.inventory.at[index, "allocated"])
    )

    fill_rate = fulfilled_qty / requested_qty if requested_qty > 0 else 0

    return {
        "fulfilled_qty": fulfilled_qty,
        "backordered_qty": backordered_qty,
        "fill_rate": round(fill_rate, 3),
    }


def record_inventory_snapshot(sim, date):
    """
    Records inventory position for every product on a given date.
    """

    snapshot = sim.inventory.copy()

    snapshot["snapshot_date"] = pd.Timestamp(date).strftime("%Y-%m-%d")

    snapshot = snapshot[
        [
            "snapshot_date",
            "product_id",
            "on_hand",
            "allocated",
            "available",
        ]
    ]

    sim.inventory_history.extend(
        snapshot.to_dict("records")
    )

    return snapshot


def calculate_inventory_summary(sim):
    """
    Returns summary-level inventory metrics.
    """

    total_on_hand = int(sim.inventory["on_hand"].sum())
    total_available = int(sim.inventory["available"].sum())

    out_of_stock_skus = int(
        (sim.inventory["available"] <= 0).sum()
    )

    return {
        "total_on_hand_units": total_on_hand,
        "total_available_units": total_available,
        "out_of_stock_skus": out_of_stock_skus,
    }