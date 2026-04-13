"""Pure calculation functions — no Streamlit dependency."""

import math
from config import MAX_COMBO_ITERATIONS


# ── Commission / Lifetime Value ──────────────────────────────────────────────

def calc_commission(premium, comm_pct, years, policies):
    """Return a dict of commission breakdowns for one product line."""
    commission_per_year = premium * (comm_pct / 100)
    total_per_policy = commission_per_year * years
    total_revenue = total_per_policy * policies
    return {
        'commission_per_year': commission_per_year,
        'total_commission_per_policy': total_per_policy,
        'total_revenue': total_revenue,
    }


# ── Break-Even ───────────────────────────────────────────────────────────────

def calc_break_even_single(budget, rev_per_close):
    """Policies of a single product needed to cover *budget*."""
    if rev_per_close <= 0:
        return 0
    return math.ceil(budget / rev_per_close)


def calc_all_combinations(budget, rev_per_close, max_counts):
    """Find all combos that meet *budget* using up to three product lines.

    Parameters
    ----------
    budget : float
    rev_per_close : list[float]   – revenue per close for each product (length 3)
    max_counts : list[int]        – max policies to try per product (length 3)

    Returns
    -------
    list[tuple[int, int, int, float, float]]
        (count_a, count_b, count_c, total_revenue, above_budget)
    """
    r0, r1, r2 = rev_per_close
    m0, m1, m2 = max_counts
    results = []
    iterations = 0

    for a in range(m0 + 1):
        a_rev = a * r0
        if a_rev >= budget:
            results.append((a, 0, 0, a_rev, a_rev - budget))
            break  # no point going higher on this axis alone
        for b in range(m1 + 1):
            ab_rev = a_rev + b * r1
            if ab_rev >= budget:
                results.append((a, b, 0, ab_rev, ab_rev - budget))
                break  # early exit on inner loop
            for c in range(m2 + 1):
                iterations += 1
                if iterations > MAX_COMBO_ITERATIONS:
                    return results  # safety cap
                total = ab_rev + c * r2
                if total >= budget:
                    results.append((a, b, c, total, total - budget))
                    break  # no need to try more c

    return results


def pareto_filter(combos):
    """Return only Pareto-efficient combos (not dominated on all three axes).

    Uses a sort-and-sweep approach that is O(n log n) rather than O(n²).
    """
    if not combos:
        return []

    # Sort by (a ASC, b ASC, c ASC) — lexicographic on policy counts
    sorted_combos = sorted(combos, key=lambda x: (x[0], x[1], x[2]))

    pareto = []
    for combo in sorted_combos:
        dominated = False
        # Only need to check against the current Pareto set (much smaller)
        for p in pareto:
            if p[0] <= combo[0] and p[1] <= combo[1] and p[2] <= combo[2] and (
                p[0] < combo[0] or p[1] < combo[1] or p[2] < combo[2]
            ):
                dominated = True
                break
        if not dominated:
            # Also remove any existing Pareto members dominated by this new combo
            pareto = [
                p for p in pareto
                if not (
                    combo[0] <= p[0] and combo[1] <= p[1] and combo[2] <= p[2]
                    and (combo[0] < p[0] or combo[1] < p[1] or combo[2] < p[2])
                )
            ]
            pareto.append(combo)

    return pareto


# ── Lead Channel ─────────────────────────────────────────────────────────────

def calc_lead_channel(cost_per_lead, closing_rate, hours_per_lead, hourly_wage):
    """Compute fully-loaded cost to close one household for a lead channel."""
    if closing_rate <= 0:
        return {
            'quotes_to_close': 0,
            'lead_cost_to_close': 0.0,
            'payroll_per_lead': 0.0,
            'payroll_to_close': 0.0,
            'total_cost_to_close': 0.0,
        }

    quotes = math.ceil(1.0 / (closing_rate / 100))
    lead_cost = quotes * cost_per_lead
    payroll_per_lead = hours_per_lead * hourly_wage
    payroll_to_close = quotes * payroll_per_lead
    total = lead_cost + payroll_to_close

    return {
        'quotes_to_close': quotes,
        'lead_cost_to_close': lead_cost,
        'payroll_per_lead': payroll_per_lead,
        'payroll_to_close': payroll_to_close,
        'total_cost_to_close': total,
    }


# ── Sensitivity (Tab 1 add-on) ──────────────────────────────────────────────

def sensitivity_retention(t1_data, delta_years_list):
    """Return grand totals for each retention delta in *delta_years_list*.

    Parameters
    ----------
    t1_data : dict  – keyed by product key, each value has 'premium', 'commission_pct', 'years', 'policies'
    delta_years_list : list[int]  – e.g. [-2, -1, 0, 1, 2]

    Returns
    -------
    dict  – {delta: grand_total}
    """
    results = {}
    for delta in delta_years_list:
        total = 0.0
        for d in t1_data.values():
            adjusted_years = max(0, d['years'] + delta)
            c = calc_commission(d['premium'], d['commission_pct'], adjusted_years, d['policies'])
            total += c['total_revenue']
        results[delta] = total
    return results
