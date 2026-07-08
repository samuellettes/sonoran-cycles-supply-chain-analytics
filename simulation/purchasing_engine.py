"""
purchasing_engine.py

Handles purchase order creation and replenishment for the
Sonoran Cycles simulation.

Responsibilities:
- Check inventory against reorder points
- Create purchase orders for low-stock SKUs
- Assign supplier lead times
- Receive purchase orders when expected receipt dates arrive
- Update inventory when inbound stock is received
"""

import pandas as pd

import simulation.simulation_config as config

from simulation.inventory_engine import get_inventory_index


def format_date(date):
    """
    Converts a date to YYYY-MM-DD format.
    """

    return pd.Timestamp(date).strftime("%Y-%m-%d")


def get_product_supplier(sim, product_id):
    """
    Returns supplier information for a product.
    """

    product = sim.products[
        sim.products["product_id"] == product_id
    ]

    if product.empty:
        raise ValueError(f"Product ID {product_id} not found in products.")

    supplier_id = product.iloc[0]["supplier_id"]

    supplier = sim.suppliers[
        sim.suppliers["supplier_id"] == supplier_id
    ]

    if supplier.empty:
        raise ValueError(f"Supplier ID {supplier_id} not found in suppliers.")

    return supplier.iloc[0]


def get_open_po_qty(sim, product_id):
    """
    Returns open purchase order quantity for a product.
    """

    open_qty = 0

    for po in sim.purchase_orders:
        if (
            po["product_id"] == product_id
            and po["po_status"] == config.PO_STATUS_OPEN
        ):
            open_qty += int(po["ordered_qty"]) - int(po["received_qty"])

    return open_qty


def has_open_purchase_order(sim, product_id):
    """
    Checks whether a product already has an open purchase order.
    """

    return get_open_po_qty(sim, product_id) > 0


def calculate_purchase_order_qty(sim, product_id):
    """
    Calculates purchase order quantity needed to reach target stock.
    """

    index = get_inventory_index(sim, product_id)

    available = int(sim.inventory.at[index, "available"])
    target_stock = int(sim.inventory.at[index, "target_stock"])
    open_po_qty = get_open_po_qty(sim, product_id)

    order_qty = target_stock - available - open_po_qty

    return max(0, int(order_qty))


def create_purchase_order(sim, product_id, order_date):
    """
    Creates one purchase order for a product.
    """

    if has_open_purchase_order(sim, product_id):
        return None

    order_qty = calculate_purchase_order_qty(sim, product_id)

    if order_qty <= 0:
        return None

    supplier = get_product_supplier(sim, product_id)

    lead_time_days = int(supplier["lead_time_days"])
    expected_receipt_date = pd.Timestamp(order_date) + pd.Timedelta(days=lead_time_days)

    purchase_order = {
        "purchase_order_id": sim.next_purchase_order_number(),
        "product_id": product_id,
        "supplier_id": supplier["supplier_id"],
        "supplier_name": supplier["supplier_name"],
        "order_date": format_date(order_date),
        "expected_receipt_date": format_date(expected_receipt_date),
        "actual_receipt_date": None,
        "lead_time_days": lead_time_days,
        "ordered_qty": order_qty,
        "received_qty": 0,
        "po_status": config.PO_STATUS_OPEN,
    }

    sim.purchase_orders.append(purchase_order)

    return purchase_order


def receive_purchase_orders(sim, date):
    """
    Receives purchase orders whose expected receipt date has arrived.
    """

    received_count = 0
    received_units = 0

    current_date = pd.Timestamp(date)

    for po in sim.purchase_orders:
        if po["po_status"] != config.PO_STATUS_OPEN:
            continue

        expected_receipt_date = pd.Timestamp(po["expected_receipt_date"])

        if expected_receipt_date <= current_date:
            product_id = po["product_id"]
            received_qty = int(po["ordered_qty"])

            index = get_inventory_index(sim, product_id)

            sim.inventory.at[index, "on_hand"] = (
                int(sim.inventory.at[index, "on_hand"]) + received_qty
            )

            sim.inventory.at[index, "available"] = (
                int(sim.inventory.at[index, "on_hand"])
                - int(sim.inventory.at[index, "allocated"])
            )

            po["received_qty"] = received_qty
            po["actual_receipt_date"] = format_date(date)
            po["po_status"] = config.PO_STATUS_RECEIVED

            received_count += 1
            received_units += received_qty

    return {
        "purchase_orders_received": received_count,
        "purchase_units_received": received_units,
    }


def review_inventory_and_create_purchase_orders(sim, date):
    """
    Reviews all inventory positions and creates purchase orders
    for SKUs at or below their reorder point.
    """

    created_count = 0
    ordered_units = 0

    for _, row in sim.inventory.iterrows():
        product_id = row["product_id"]
        available = int(row["available"])
        reorder_point = int(row["reorder_point"])

        if available <= reorder_point:
            purchase_order = create_purchase_order(
                sim=sim,
                product_id=product_id,
                order_date=date,
            )

            if purchase_order is not None:
                created_count += 1
                ordered_units += int(purchase_order["ordered_qty"])

    return {
        "purchase_orders_created": created_count,
        "purchase_units_ordered": ordered_units,
    }