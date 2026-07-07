"""
customer_engine.py

Handles customer selection logic for the Sonoran Cycles simulation.

Responsibilities:
- Separate dealer and DTC customers
- Weight dealer selection by dealer tier
- Select realistic customers for generated orders
"""

import simulation.simulation_config as config


def add_customer_order_weights(customers_df):
    """
    Adds an order_weight column based on dealer tier.
    """

    customers_df = customers_df.copy()

    customers_df["order_weight"] = (
        customers_df["dealer_tier"]
        .map(config.CUSTOMER_WEIGHTS)
        .fillna(1)
    )

    return customers_df


def get_dealers(sim):
    """
    Returns dealer customers only.
    """

    return sim.customers[
        sim.customers["customer_type"] == config.DEALER
    ]


def get_dtc_customer(sim):
    """
    Returns the DTC customer account.
    """

    dtc = sim.customers[
        sim.customers["customer_type"] == config.DTC
    ]

    if dtc.empty:
        raise ValueError("No DTC customer found.")

    return dtc.iloc[0]


def select_dealer(sim):
    """
    Selects a dealer using tier-based order weights.
    """

    dealers = get_dealers(sim)

    if "order_weight" not in dealers.columns:
        raise ValueError(
            "Customers must have order_weight. "
            "Run add_customer_order_weights() first."
        )

    return dealers.sample(
        n=1,
        weights="order_weight"
    ).iloc[0]


def select_dtc_customer(sim):
    """
    Selects the DTC customer.
    """

    return get_dtc_customer(sim)