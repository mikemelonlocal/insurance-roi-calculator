"""Tests for calculations.py — pure computation functions."""

import math
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from calculations import (
    calc_commission,
    calc_break_even_single,
    calc_all_combinations,
    pareto_filter,
    calc_lead_channel,
    sensitivity_retention,
)


# ── calc_commission ──────────────────────────────────────────────────────────

class TestCalcCommission:
    def test_basic(self):
        r = calc_commission(premium=2250, comm_pct=10, years=2, policies=1)
        assert r['commission_per_year'] == 225.0
        assert r['total_commission_per_policy'] == 450.0
        assert r['total_revenue'] == 450.0

    def test_multiple_policies(self):
        r = calc_commission(premium=2775, comm_pct=10, years=5, policies=5)
        assert r['commission_per_year'] == 277.5
        assert r['total_commission_per_policy'] == 1387.5
        assert r['total_revenue'] == 6937.5

    def test_zero_premium(self):
        r = calc_commission(premium=0, comm_pct=10, years=5, policies=3)
        assert r['total_revenue'] == 0.0

    def test_zero_years(self):
        r = calc_commission(premium=2000, comm_pct=10, years=0, policies=5)
        assert r['total_revenue'] == 0.0


# ── calc_break_even_single ───────────────────────────────────────────────────

class TestBreakEvenSingle:
    def test_exact(self):
        # 1000 / 500 = exactly 2
        assert calc_break_even_single(1000, 500) == 2

    def test_rounds_up(self):
        # 1000 / 450 = 2.22 → 3
        assert calc_break_even_single(1000, 450) == 3

    def test_zero_revenue(self):
        assert calc_break_even_single(1000, 0) == 0


# ── calc_all_combinations ───────────────────────────────────────────────────

class TestAllCombinations:
    def test_simple(self):
        # budget=100, rev=[50, 100, 200], max=[2, 1, 1]
        combos = calc_all_combinations(100, [50, 100, 200], [2, 1, 1])
        # All should meet budget
        for a, b, c, total, above in combos:
            assert total >= 100

    def test_includes_single_product(self):
        combos = calc_all_combinations(100, [50, 100, 200], [2, 1, 1])
        # (2, 0, 0) should be there: 2*50 = 100
        assert any(c[0] == 2 and c[1] == 0 and c[2] == 0 for c in combos)

    def test_performance_does_not_hang(self):
        """Large budget should not hang due to iteration cap."""
        start = time.time()
        combos = calc_all_combinations(50000, [450, 1387.5, 18], [112, 37, 2778])
        elapsed = time.time() - start
        assert elapsed < 10, f"Took {elapsed:.1f}s — too slow"


# ── pareto_filter ────────────────────────────────────────────────────────────

class TestParetoFilter:
    def test_filters_dominated(self):
        combos = [
            (2, 0, 0, 100, 0),  # Pareto
            (3, 0, 0, 150, 50),  # Dominated by (2,0,0)
            (0, 1, 0, 100, 0),  # Pareto
            (1, 1, 0, 150, 50),  # Dominated by (0,1,0)
        ]
        result = pareto_filter(combos)
        assert (2, 0, 0, 100, 0) in result
        assert (0, 1, 0, 100, 0) in result
        assert (3, 0, 0, 150, 50) not in result
        assert (1, 1, 0, 150, 50) not in result

    def test_empty(self):
        assert pareto_filter([]) == []

    def test_single(self):
        combos = [(1, 2, 3, 100, 0)]
        assert pareto_filter(combos) == combos

    def test_incomparable_all_kept(self):
        """Two combos that don't dominate each other should both be kept."""
        combos = [
            (3, 0, 0, 150, 50),
            (0, 0, 5, 100, 0),
        ]
        result = pareto_filter(combos)
        assert len(result) == 2


# ── calc_lead_channel ────────────────────────────────────────────────────────

class TestCalcLeadChannel:
    def test_internet_leads_example(self):
        """Match the tutorial example: $4/lead, 3% close, 2 hrs, $15/hr."""
        r = calc_lead_channel(cost_per_lead=4, closing_rate=3, hours_per_lead=2, hourly_wage=15)
        assert r['quotes_to_close'] == 34  # ceil(100/3) = 34
        assert r['lead_cost_to_close'] == 136.0  # 34 * 4
        assert r['payroll_to_close'] == 1020.0  # 34 * 2 * 15
        assert r['total_cost_to_close'] == 1156.0

    def test_sf_leads_example(self):
        """Match the tutorial example: $30/lead, 12.5% close, 1.5 hrs, $15/hr."""
        r = calc_lead_channel(cost_per_lead=30, closing_rate=12.5, hours_per_lead=1.5, hourly_wage=15)
        assert r['quotes_to_close'] == 8  # ceil(100/12.5) = 8
        assert r['lead_cost_to_close'] == 240.0  # 8 * 30
        assert r['payroll_to_close'] == 180.0  # 8 * 1.5 * 15
        assert r['total_cost_to_close'] == 420.0

    def test_zero_closing_rate(self):
        r = calc_lead_channel(10, 0, 1, 15)
        assert r['total_cost_to_close'] == 0.0


# ── sensitivity_retention ────────────────────────────────────────────────────

class TestSensitivity:
    def test_basic(self):
        t1_data = {
            'auto': {'premium': 2250, 'commission_pct': 10, 'years': 2, 'policies': 1},
            'home': {'premium': 2775, 'commission_pct': 10, 'years': 5, 'policies': 1},
        }
        result = sensitivity_retention(t1_data, [-1, 0, 1])
        # At delta=0: auto=450, home=1387.5 → 1837.5
        assert result[0] == 450.0 + 1387.5
        # At delta=+1: auto=675, home=1665 → 2340
        assert result[1] == 675.0 + 1665.0
        # At delta=-1: auto=225, home=1110 → 1335
        assert result[-1] == 225.0 + 1110.0

    def test_negative_years_clamped_to_zero(self):
        t1_data = {
            'auto': {'premium': 2250, 'commission_pct': 10, 'years': 1, 'policies': 1},
        }
        result = sensitivity_retention(t1_data, [-2])
        # years=1-2 → max(0, -1) = 0 → revenue = 0
        assert result[-2] == 0.0
