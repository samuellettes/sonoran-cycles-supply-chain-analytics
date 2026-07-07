"""
order_generator.py

Generates sales order headers and sales order lines for the
Sonoran Cycles simulation.

Responsibilities:
- Generate dealer sales orders
- Generate direct-to-consumer sales orders
- Create order headers
- Create order lines
- Apply dealer discounts and DTC pricing
- Calculate booked revenue and gross profit
"""

import numpy as np
import pandas as pd

import simulation.simulation_config as config

from simulation.customer_engine import select_dealer, select_dtc_customer
from simulation.product_engine import choose_product
from simulation.demand_engine import calculate_daily_orders
from simulation.inventory_engine import allocate_inventory

def format_date(date):
    """
    Converts a date to a clean YYYY-MM-DD string.
    """

    return pd.Timestamp(date).strftime("%Y-%m-%d")


def weighted_choice(weight_dict):
    """
    Selects one value from a dictionary of weights.
    """

    values = list(weight_dict.keys())
    weights = np.array(list(weight_dict.values()), dtype=float)
    weights = weights / weights.sum()

    return np.random.choice(values, p=weights)


def get_payment_terms(customer, channel):
    """
    Returns payment terms based on customer type and dealer tier.
    """

    if channel == config.DTC:
        return "Credit Card"

    dealer_tier = customer["dealer_tier"]

    return config.DEALER_PAYMENT_TERMS_BY_TIER.get(
        dealer_tier,
        "Net 30",
    )


def get_discount_pct(customer, channel):
    """
    Returns discount percentage based on customer type and dealer tier.
    """

    if channel == config.DTC:
        return config.DTC_DISCOUNT_PCT

    dealer_tier = customer["dealer_tier"]

    return config.DEALER_DISCOUNT_BY_TIER.get(
        dealer_tier,
        0.35,
    )


def calculate_unit_cost(product):
    """
    Returns unit cost.

    If the products table already contains standard_cost, use it.
    Otherwise, estimate standard cost from MSRP and category.
    """

    if "standard_cost" in product.index and not pd.isna(product["standard_cost"]):
        return round(float(product["standard_cost"]), 2)

    category = product["category"]
    msrp = float(product["msrp"])

    cost_pct = config.STANDARD_COST_PCT_BY_CATEGORY.get(
        category,
        0.56,
    )

    return round(msrp * cost_pct, 2)


def choose_dealer_quantity():
    """
    Selects quantity for a dealer order line.
    """

    return int(weighted_choice(config.DEALER_LINE_QTY_WEIGHTS))


def choose_dtc_quantity():
    """
    Selects quantity for a DTC order line.
    """

    return int(weighted_choice(config.DTC_LINE_QTY_WEIGHTS))


def generate_order_header(order_id, date, customer, channel):
    """
    Creates one sales order header.
    """

    return {
        "sales_order_id": order_id,
        "order_date": format_date(date),
        "customer_id": customer["customer_id"],
        "customer_name": customer["customer_name"],
        "sales_channel": channel,
        "order_status": config.ORDER_STATUS_BOOKED,
        "payment_terms": get_payment_terms(customer, channel),
        "warehouse": config.DEFAULT_WAREHOUSE,
        "order_total": 0.00,
    }


def generate_order_line(
    sim,
    order_id,
    line_number,
    product,
    quantity,
    discount_pct,
):
    """
    Creates one sales order line and allocates available inventory.
    """

    inventory_result = allocate_inventory(
        sim=sim,
        product_id=product["product_id"],
        requested_qty=quantity,
    )

    requested_qty = quantity
    fulfilled_qty = inventory_result["fulfilled_qty"]
    backordered_qty = inventory_result["backordered_qty"]
    fill_rate = inventory_result["fill_rate"]

    msrp = float(product["msrp"])
    unit_price = round(msrp * (1 - discount_pct), 2)

    booked_revenue = round(unit_price * requested_qty, 2)
    fulfilled_revenue = round(unit_price * fulfilled_qty, 2)

    unit_cost = calculate_unit_cost(product)

    booked_cost = round(unit_cost * requested_qty, 2)
    fulfilled_cost = round(unit_cost * fulfilled_qty, 2)

    booked_gross_profit = round(booked_revenue - booked_cost, 2)
    fulfilled_gross_profit = round(fulfilled_revenue - fulfilled_cost, 2)

    return {
        "sales_order_id": order_id,
        "line_number": line_number,
        "product_id": product["product_id"],
        "sku": product.get("sku", None),
        "model_name": product["model_name"],
        "category": product["category"],
        "size": product["size"],
        "color": product["color"],

        "requested_qty": requested_qty,
        "fulfilled_qty": fulfilled_qty,
        "backordered_qty": backordered_qty,
        "fill_rate": fill_rate,

        "unit_msrp": msrp,
        "discount_pct": round(discount_pct, 3),
        "unit_price": unit_price,

        "extended_price": booked_revenue,
        "fulfilled_revenue": fulfilled_revenue,

        "unit_cost": unit_cost,
        "extended_cost": booked_cost,
        "fulfilled_cost": fulfilled_cost,

        "gross_profit": booked_gross_profit,
        "fulfilled_gross_profit": fulfilled_gross_profit,
    }


def save_order(sim, header, lines):
    """
    Saves order header and order lines to the simulation object.
    """

    header["order_total"] = round(
        sum(line["extended_price"] for line in lines),
        2,
    )

    sim.sales_orders.append(header)
    sim.sales_order_lines.extend(lines)

    return header, lines


def generate_dealer_order(sim, date):
    """
    Generates one dealer sales order.
    """

    customer = select_dealer(sim)
    order_id = sim.next_sales_order_number()

    header = generate_order_header(
        order_id=order_id,
        date=date,
        customer=customer,
        channel=config.DEALER,
    )

    discount_pct = get_discount_pct(customer, config.DEALER)

    line_count = np.random.randint(
        config.MIN_DEALER_LINES,
        config.MAX_DEALER_LINES + 1,
    )

    lines = []
    used_product_ids = set()

    for line_number in range(1, line_count + 1):
        product = choose_product(
            sim,
            customer["dealer_profile"],
        )

        attempts = 0

        while product["product_id"] in used_product_ids and attempts < 10:
            product = choose_product(
                sim,
                customer["dealer_profile"],
            )
            attempts += 1

        used_product_ids.add(product["product_id"])

        quantity = choose_dealer_quantity()

        line = generate_order_line(
            sim=sim,
            order_id=order_id,
            line_number=line_number,
            product=product,
            quantity=quantity,
            discount_pct=discount_pct,
        )

        lines.append(line)

    return save_order(sim, header, lines)


def generate_dtc_order(sim, date):
    """
    Generates one direct-to-consumer sales order.
    """

    customer = select_dtc_customer(sim)
    order_id = sim.next_sales_order_number()

    header = generate_order_header(
        order_id=order_id,
        date=date,
        customer=customer,
        channel=config.DTC,
    )

    discount_pct = get_discount_pct(customer, config.DTC)

    line_count = 1

    if np.random.random() < config.DTC_SECOND_LINE_PROBABILITY:
        line_count = 2

    lines = []
    used_product_ids = set()

    for line_number in range(1, line_count + 1):
        product = choose_product(
            sim,
            dealer_profile="Direct",
        )

        attempts = 0

        while product["product_id"] in used_product_ids and attempts < 10:
            product = choose_product(
                sim,
                dealer_profile="Direct",
            )
            attempts += 1

        used_product_ids.add(product["product_id"])

        quantity = choose_dtc_quantity()

        line = generate_order_line(
            sim=sim,
            order_id=order_id,
            line_number=line_number,
            product=product,
            quantity=quantity,
            discount_pct=discount_pct,
        )

        lines.append(line)

    return save_order(sim, header, lines)


def generate_daily_orders(sim, date, weather):
    """
    Generates all dealer and DTC sales orders for one day.
    """

    dealer_order_count = calculate_daily_orders(
        date=date,
        channel=config.DEALER,
        weather=weather,
    )

    dtc_order_count = calculate_daily_orders(
        date=date,
        channel=config.DTC,
        weather=weather,
    )

    for _ in range(dealer_order_count):
        generate_dealer_order(sim, date)

    for _ in range(dtc_order_count):
        generate_dtc_order(sim, date)

    return {
        "date": format_date(date),
        "weather": weather,
        "dealer_orders": dealer_order_count,
        "dtc_orders": dtc_order_count,
        "total_orders": dealer_order_count + dtc_order_count,
    }