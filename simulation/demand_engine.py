"""
demand_engine.py

Calculates daily demand for the Sonoran Cycles simulation.

Responsibilities:
- Apply monthly seasonality
- Apply weekday effects
- Apply promotions
- Apply weather impacts
- Add random market variation
- Calculate demand indices for Dealer and DTC channels
"""

import numpy as np
import simulation.simulation_config as config


def get_monthly_multiplier(date):
    return config.MONTHLY_MULTIPLIER[date.month]


def get_weekday_multiplier(date, channel):
    weekday = date.weekday()

    if channel == config.DEALER:
        return config.DEALER_WEEKDAY[weekday]

    if channel == config.DTC:
        return config.DTC_WEEKDAY[weekday]

    raise ValueError("Channel must be 'Dealer' or 'DTC'.")


def get_promotion_multiplier(date):
    date_string = date.strftime("%Y-%m-%d")
    return config.PROMOTIONS.get(date_string, 1.0)


def get_weather_multiplier(weather):
    return config.WEATHER_MULTIPLIER.get(weather, 1.0)


def get_random_noise():
    return np.random.normal(
        loc=config.NOISE_MEAN,
        scale=config.NOISE_STD_DEV,
    )


def calculate_demand_index(date, channel, weather):
    demand_index = (
        get_monthly_multiplier(date)
        * get_weekday_multiplier(date, channel)
        * get_promotion_multiplier(date)
        * get_weather_multiplier(weather)
        * get_random_noise()
    )

    return round(demand_index, 3)


def calculate_daily_orders(date, channel, weather):
    demand_index = calculate_demand_index(date, channel, weather)

    if channel == config.DEALER:
        base_orders = config.BASE_DEALER_ORDERS
    elif channel == config.DTC:
        base_orders = config.BASE_DTC_ORDERS
    else:
        raise ValueError("Invalid channel.")

    return max(0, round(base_orders * demand_index))


def preview_day(date, weather):
    dealer_orders = calculate_daily_orders(date, config.DEALER, weather)
    dtc_orders = calculate_daily_orders(date, config.DTC, weather)

    print(f"Date: {date.date()}")
    print(f"Weather: {weather}")
    print(f"Dealer Orders: {dealer_orders}")
    print(f"DTC Orders: {dtc_orders}")