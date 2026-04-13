"""Tests for utils.py — formatting and validation helpers."""

import math
import sys
import os

# Allow imports from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import fmt, fmt_pct, validate_numeric, safe_divide


# ── fmt ──────────────────────────────────────────────────────────────────────

class TestFmt:
    def test_normal(self):
        assert fmt(1234.5) == '$1,234.50'

    def test_zero(self):
        assert fmt(0) == '$0.00'

    def test_none(self):
        assert fmt(None) == '$0.00'

    def test_nan(self):
        assert fmt(float('nan')) == '$0.00'

    def test_inf(self):
        assert fmt(float('inf')) == '$0.00'

    def test_negative(self):
        assert fmt(-100) == '$-100.00'

    def test_large(self):
        assert fmt(1_000_000) == '$1,000,000.00'


# ── fmt_pct ──────────────────────────────────────────────────────────────────

class TestFmtPct:
    def test_normal(self):
        assert fmt_pct(12.5) == '12.5%'

    def test_zero(self):
        assert fmt_pct(0) == '0.0%'

    def test_none(self):
        assert fmt_pct(None) == '0.0%'

    def test_nan(self):
        assert fmt_pct(float('nan')) == '0.0%'

    def test_inf(self):
        assert fmt_pct(float('inf')) == '0.0%'


# ── validate_numeric ────────────────────────────────────────────────────────

class TestValidateNumeric:
    def test_normal(self):
        assert validate_numeric(42) == 42.0

    def test_clamp_min(self):
        assert validate_numeric(-5, min_val=0) == 0

    def test_clamp_max(self):
        assert validate_numeric(200, max_val=100) == 100

    def test_nan(self):
        assert validate_numeric(float('nan'), default=7) == 7

    def test_inf(self):
        assert validate_numeric(float('inf'), default=7) == 7

    def test_none(self):
        assert validate_numeric(None, default=3) == 3

    def test_string(self):
        assert validate_numeric('abc', default=0) == 0

    def test_string_number(self):
        assert validate_numeric('42.5') == 42.5


# ── safe_divide ──────────────────────────────────────────────────────────────

class TestSafeDivide:
    def test_normal(self):
        assert safe_divide(10, 2) == 5.0

    def test_zero_denominator(self):
        assert safe_divide(10, 0) == 0

    def test_zero_denominator_custom_default(self):
        assert safe_divide(10, 0, default=-1) == -1

    def test_none_input(self):
        assert safe_divide(10, None, default=0) == 0

    def test_zero_numerator(self):
        assert safe_divide(0, 5) == 0.0
