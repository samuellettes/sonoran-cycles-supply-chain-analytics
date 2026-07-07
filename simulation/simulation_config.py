START_DATE = "2021-01-01"
END_DATE = "2025-12-31"

BASE_DEALER_ORDERS = 18
BASE_DTC_ORDERS = 10

DEALER = "Dealer"
DTC = "DTC"

MONTHLY_MULTIPLIER = {
    1: 0.55,
    2: 0.65,
    3: 0.90,
    4: 1.20,
    5: 1.35,
    6: 1.30,
    7: 1.15,
    8: 1.00,
    9: 0.90,
    10: 0.75,
    11: 0.80,
    12: 0.60,
}

DEALER_WEEKDAY = {
    0: 1.10,
    1: 1.20,
    2: 1.15,
    3: 1.05,
    4: 0.95,
    5: 0.30,
    6: 0.10,
}

DTC_WEEKDAY = {
    0: 0.90,
    1: 0.90,
    2: 0.95,
    3: 1.00,
    4: 1.15,
    5: 1.40,
    6: 1.30,
}

WEATHER_MULTIPLIER = {
    "Sunny": 1.05,
    "Cloudy": 1.00,
    "Rain": 0.80,
    "Snow": 0.60,
}

PROMOTIONS = {}

NOISE_MEAN = 1.00
NOISE_STD_DEV = 0.08

# =========================================================
# CUSTOMER ORDER WEIGHTS
# =========================================================

CUSTOMER_WEIGHTS = {
    "Platinum": 12,
    "Gold": 8,
    "Silver": 4,
    "Bronze": 2,
    "N/A": 1,
}


# =========================================================
# SIZE DEMAND WEIGHTS
# =========================================================

SIZE_WEIGHTS = {
    "XS": 0.05,
    "S": 0.15,
    "M": 0.35,
    "L": 0.30,
    "XL": 0.15,
}


# =========================================================
# DEALER PROFILE MODEL PREFERENCES
# =========================================================

DEALER_PROFILE_MODEL_WEIGHTS = {
    "Trail Shop": {
        "Sabino": 0.45,
        "Romero": 0.30,
        "Oracle": 0.15,
        "Catalina": 0.05,
        "Rincon": 0.03,
        "Sky Island": 0.01,
        "Sonoita": 0.01,
    },

    "XC Specialist": {
        "Catalina": 0.45,
        "Rincon": 0.35,
        "Sabino": 0.10,
        "Romero": 0.05,
        "Oracle": 0.03,
        "Sky Island": 0.01,
        "Sonoita": 0.01,
    },

    "Aggressive MTB": {
        "Romero": 0.45,
        "Oracle": 0.35,
        "Sabino": 0.15,
        "Catalina": 0.02,
        "Rincon": 0.01,
        "Sky Island": 0.01,
        "Sonoita": 0.01,
    },

    "Premium Dealer": {
        "Sky Island": 0.45,
        "Oracle": 0.20,
        "Romero": 0.15,
        "Sabino": 0.10,
        "Catalina": 0.05,
        "Rincon": 0.03,
        "Sonoita": 0.02,
    },

    "Gravel Shop": {
        "Sonoita": 0.70,
        "Catalina": 0.10,
        "Sabino": 0.08,
        "Rincon": 0.05,
        "Romero": 0.04,
        "Oracle": 0.02,
        "Sky Island": 0.01,
    },

    "Generalist": {
        "Sabino": 0.28,
        "Romero": 0.20,
        "Catalina": 0.18,
        "Oracle": 0.15,
        "Sky Island": 0.07,
        "Sonoita": 0.07,
        "Rincon": 0.05,
    },

    "Direct": {
        "Sabino": 0.30,
        "Catalina": 0.20,
        "Romero": 0.18,
        "Oracle": 0.12,
        "Sky Island": 0.08,
        "Sonoita": 0.07,
        "Rincon": 0.05,
    },
}