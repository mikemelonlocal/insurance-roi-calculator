# Brand tokens
DARK_GREEN = '#114E38'
PRI_GREEN = '#47B74F'
YELLOW = '#F1CB20'
BEIGE = '#FEF8E9'
SAND = '#EDDFDB'
WHITE = '#FFFFFF'
BORDER = '#D9D9D9'

# App metadata
APP_TITLE = 'Commission Goldmine | Melon Local'
APP_VERSION = '4.0'
SIDEBAR_IMAGE = 'melon_graphic.svg'

# Default commission rate
DEFAULT_COMMISSION_PCT = 10.0

# Default hourly wage for lead channel calculations
DEFAULT_HOURLY_WAGE = 15.0

# Product definitions: key → (label, default_premium, default_years, default_policies)
PRODUCTS = {
    'auto':    {'label': '🚗 Auto',    'default_premium': 2250.0, 'default_years': 2, 'default_policies': 10},
    'home':    {'label': '🏠 Home',    'default_premium': 2775.0, 'default_years': 5, 'default_policies': 5},
    'renters': {'label': '🏢 Renters', 'default_premium': 180.0,  'default_years': 1, 'default_policies': 3},
}

# Preset configurations (Tab 1)
PRESETS = {
    'Average': {
        'auto_prem': 2250.0, 'auto_comm': 10.0, 'auto_yrs': 2.0, 'auto_policies': 10.0,
        'home_prem': 2775.0, 'home_comm': 10.0, 'home_yrs': 5.0, 'home_policies': 5.0,
        'renters_prem': 180.0, 'renters_comm': 10.0, 'renters_yrs': 1.0, 'renters_policies': 3.0,
    },
    'Conservative': {
        'auto_prem': 1800.0, 'auto_comm': 10.0, 'auto_yrs': 2.0, 'auto_policies': 5.0,
        'home_prem': 2200.0, 'home_comm': 10.0, 'home_yrs': 3.0, 'home_policies': 3.0,
        'renters_prem': 150.0, 'renters_comm': 10.0, 'renters_yrs': 1.0, 'renters_policies': 2.0,
    },
    'Moderate': {
        'auto_prem': 2250.0, 'auto_comm': 10.0, 'auto_yrs': 2.0, 'auto_policies': 10.0,
        'home_prem': 2775.0, 'home_comm': 10.0, 'home_yrs': 5.0, 'home_policies': 5.0,
        'renters_prem': 180.0, 'renters_comm': 10.0, 'renters_yrs': 1.0, 'renters_policies': 3.0,
    },
    'Aggressive': {
        'auto_prem': 2800.0, 'auto_comm': 12.0, 'auto_yrs': 3.0, 'auto_policies': 20.0,
        'home_prem': 3500.0, 'home_comm': 12.0, 'home_yrs': 7.0, 'home_policies': 10.0,
        'renters_prem': 220.0, 'renters_comm': 12.0, 'renters_yrs': 2.0, 'renters_policies': 5.0,
    },
    'High-Value Client': {
        'auto_prem': 3500.0, 'auto_comm': 15.0, 'auto_yrs': 5.0, 'auto_policies': 15.0,
        'home_prem': 4500.0, 'home_comm': 15.0, 'home_yrs': 10.0, 'home_policies': 8.0,
        'renters_prem': 0.0, 'renters_comm': 10.0, 'renters_yrs': 0.0, 'renters_policies': 0.0,
    },
}

# Default lead channel configurations
DEFAULT_LEAD_CHANNELS = [
    {
        'name': 'Internet Leads',
        'cost_per_lead': 4.0,
        'closing_rate': 3.0,
        'hours_per_lead': 2.0,
    },
    {
        'name': 'SF.com Leads',
        'cost_per_lead': 30.0,
        'closing_rate': 12.5,
        'hours_per_lead': 1.5,
    },
]

# Max iterations for break-even combo generation to prevent freezing
MAX_COMBO_ITERATIONS = 500_000
