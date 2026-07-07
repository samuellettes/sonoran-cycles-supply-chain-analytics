"""
product_engine.py

Handles product selection logic for the Sonoran Cycles simulation.

Responsibilities:
- Select models based on dealer profile
- Apply size demand distribution
- Select valid SKUs from the product master
- Support separate dealer and DTC buying behavior
"""

import numpy as np
import simulation.simulation_config as config


def choose_weighted_value(weight_dict):
    """
    Selects one value from a dictionary of weights.
    """

    values = list(weight_dict.keys())
    weights = list(weight_dict.values())

    return np.random.choice(
        values,
        p=weights
    )


def choose_model(dealer_profile):
    """
    Chooses a bike model based on dealer profile.
    """

    if dealer_profile not in config.DEALER_PROFILE_MODEL_WEIGHTS:
        raise ValueError(
            f"Unknown dealer profile: {dealer_profile}"
        )

    return choose_weighted_value(
        config.DEALER_PROFILE_MODEL_WEIGHTS[dealer_profile]
    )


def choose_size():
    """
    Chooses bike size based on realistic size distribution.
    """

    return choose_weighted_value(config.SIZE_WEIGHTS)


def choose_product(sim, dealer_profile):
    """
    Chooses a specific SKU from the product master.

    Selection process:
    1. Choose model based on dealer profile
    2. Choose size based on demand distribution
    3. Randomly select one available color for that model/size
    """

    model = choose_model(dealer_profile)
    size = choose_size()

    matching_products = sim.products[
        (sim.products["model_name"] == model)
        & (sim.products["size"] == size)
        & (sim.products["active_flag"] == True)
    ]

    if matching_products.empty:
        raise ValueError(
            f"No matching product found for model={model}, size={size}"
        )

    return matching_products.sample(n=1).iloc[0]