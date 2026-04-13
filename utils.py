import math
from datetime import datetime

import pandas as pd
import streamlit as st

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None


def now_local():
    """Get current time in Pacific timezone."""
    try:
        if ZoneInfo is not None:
            return datetime.now(ZoneInfo('America/Los_Angeles'))
    except Exception:
        pass
    return datetime.now()


def get_tz_label():
    return "PT"


def fmt(v):
    """Format a number as currency."""
    if pd.isna(v) or v is None:
        return '$0.00'
    try:
        if math.isnan(v) or math.isinf(v):
            return '$0.00'
    except (TypeError, ValueError):
        return '$0.00'
    return f'${v:,.2f}'


def fmt_pct(v):
    """Format a number as a percentage."""
    if pd.isna(v) or v is None:
        return '0.0%'
    try:
        if math.isnan(v) or math.isinf(v):
            return '0.0%'
    except (TypeError, ValueError):
        return '0.0%'
    return f'{v:.1f}%'


def validate_numeric(value, min_val=0, max_val=None, default=0):
    """Validate and constrain a numeric input."""
    try:
        v = float(value)
        if math.isnan(v) or math.isinf(v):
            return default
        if v < min_val:
            return min_val
        if max_val is not None and v > max_val:
            return max_val
        return v
    except (ValueError, TypeError):
        return default


def safe_divide(numerator, denominator, default=0):
    """Safe division that returns *default* on zero/invalid denominator."""
    try:
        if denominator == 0:
            return default
        result = numerator / denominator
        if math.isnan(result) or math.isinf(result):
            return default
        return result
    except (ZeroDivisionError, TypeError):
        return default


def show_validation_warning(field_name, value, min_realistic=None, max_realistic=None):
    """Show a Streamlit warning for unrealistic values. Returns True if warning shown."""
    if value == 0:
        st.warning(f'⚠️ {field_name} is set to $0. Results may not be meaningful.')
        return True
    if min_realistic and value < min_realistic:
        st.warning(f'⚠️ {field_name} (${value:,.2f}) seems unusually low. Consider reviewing this value.')
        return True
    if max_realistic and value > max_realistic:
        st.warning(f'⚠️ {field_name} (${value:,.2f}) seems unusually high. Consider reviewing this value.')
        return True
    return False
