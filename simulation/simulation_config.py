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

DEFAULT_WEATHER = "Sunny"

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

# =========================================================
# ORDER GENERATION SETTINGS
# =========================================================

DEFAULT_WAREHOUSE = "Phoenix Distribution Center"

ORDER_STATUS_BOOKED = "Booked"

DEALER_PAYMENT_TERMS_BY_TIER = {
    "Platinum": "Net 45",
    "Gold": "Net 30",
    "Silver": "Net 30",
    "Bronze": "Prepaid",
    "N/A": "Credit Card",
}

DEALER_DISCOUNT_BY_TIER = {
    "Platinum": 0.42,
    "Gold": 0.38,
    "Silver": 0.35,
    "Bronze": 0.32,
    "N/A": 0.00,
}

DTC_DISCOUNT_PCT = 0.00

MIN_DEALER_LINES = 2
MAX_DEALER_LINES = 6

DEALER_LINE_QTY_WEIGHTS = {
    1: 0.35,
    2: 0.30,
    3: 0.20,
    4: 0.10,
    5: 0.05,
}

DTC_LINE_QTY_WEIGHTS = {
    1: 0.95,
    2: 0.05,
}

DTC_SECOND_LINE_PROBABILITY = 0.08


# =========================================================
# STANDARD COST ASSUMPTIONS
# =========================================================

STANDARD_COST_PCT_BY_CATEGORY = {
    "Cross Country": 0.53,
    "Downcountry": 0.55,
    "Trail": 0.56,
    "Aggressive Trail": 0.58,
    "Enduro": 0.60,
    "eMTB": 0.64,
    "Gravel": 0.52,
}

# =========================================================
# PURCHASING / REPLENISHMENT SETTINGS
# =========================================================

PO_STATUS_OPEN = "Open"
PO_STATUS_RECEIVED = "Received"

DEFAULT_REORDER_POINT = 20
DEFAULT_TARGET_STOCK = 80