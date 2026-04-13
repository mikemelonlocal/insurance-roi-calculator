"""Tab 1 — Lifetime Value Tracker.

New in v4.1: monthly toggle, cross-sell analysis, scenario comparison,
copy-to-clipboard, agent name personalization.
"""

import pandas as pd
import streamlit as st

from config import PRODUCTS, DEFAULT_COMMISSION_PCT
from utils import fmt, validate_numeric, now_local
from calculations import calc_commission, sensitivity_retention, calc_cross_sell
from charts import build_revenue_bar_chart, build_sensitivity_chart, build_cross_sell_chart
from exports import (
    html_wrap, build_html_table, metric_card_html,
    build_pdf_report, create_formatted_excel, REPORTLAB_AVAILABLE,
)
from styling import copy_to_clipboard_button


def render():
    """Render Tab 1 and return *t1_data* dict for downstream tabs."""

    # Header with reset
    tcol1, tcol2 = st.columns([4, 1])
    with tcol1:
        st.markdown(
            '<h2 style="color:#114E38;font-family:\'Playfair Display\',Georgia,serif;">'
            '💰 Lifetime Value Tracker</h2>',
            unsafe_allow_html=True,
        )
    with tcol2:
        if st.button('🔄 Reset to Defaults', key='reset_t1'):
            for key in PRODUCTS:
                for field in ['prem', 'comm', 'yrs', 'policies']:
                    sk = f't1_{key}_{field}'
                    if sk in st.session_state:
                        del st.session_state[sk]
            st.session_state['t1_preset'] = 'Average'
            st.rerun()

    st.markdown(
        '<p style="color:#1a1a1a;font-size:1.05rem;margin-bottom:1.5rem;">'
        'Show agents the <strong>total lifetime commission</strong> value sitting in their '
        "book of business. This isn't just this year's income—it's the compounding value of "
        'every policy they close.</p>',
        unsafe_allow_html=True,
    )

    # ── Monthly / Lifetime toggle ────────────────────────────────────────────
    view_mode = st.radio(
        'View', ['Lifetime', 'Monthly'],
        horizontal=True, key='t1_view_mode',
        help='Show totals as lifetime or broken down per month',
    )
    show_monthly = view_mode == 'Monthly'

    t1_data = {}

    for key, cfg in PRODUCTS.items():
        label = cfg['label']
        def_prem = cfg['default_premium']
        def_yrs = cfg['default_years']
        def_policies = cfg['default_policies']

        st.markdown(
            f'<div class="prod-card"><div class="prod-card-title">{label}</div></div>',
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            prem = st.number_input(
                'Annual Premium ($)',
                value=float(st.session_state.get(f't1_{key}_prem', def_prem)),
                min_value=0.0, step=10.0,
                key=f't1_{key}_prem',
                help='What the customer pays per year for the policy',
            )
        with c2:
            comm = st.number_input(
                'Commission (%)',
                value=float(st.session_state.get(f't1_{key}_comm', DEFAULT_COMMISSION_PCT)),
                min_value=0.0, max_value=100.0, step=0.5,
                key=f't1_{key}_comm',
                help="Agent's cut of the annual premium",
            )
        with c3:
            yrs = st.number_input(
                'Years as Customer',
                value=float(st.session_state.get(f't1_{key}_yrs', def_yrs)),
                min_value=0.0, step=0.5,
                key=f't1_{key}_yrs',
                help='How long the average customer stays',
            )
        with c4:
            policies = st.number_input(
                'Number of Policies',
                value=int(st.session_state.get(f't1_{key}_policies', def_policies)),
                min_value=0, step=1,
                key=f't1_{key}_policies',
                help='How many of these the agent has closed',
            )

        prem = validate_numeric(prem)
        comm = validate_numeric(comm, 0, 100)
        yrs = validate_numeric(yrs)
        policies = int(validate_numeric(policies))

        result = calc_commission(prem, comm, yrs, policies)

        t1_data[key] = {
            'product': label,
            'premium': prem,
            'commission_pct': comm,
            'years': yrs,
            'policies': policies,
            **result,
        }

        if show_monthly:
            monthly = result['total_revenue'] / 12 if result['total_revenue'] else 0
            st.markdown(
                f'<div style="font-size:0.82rem;color:#555;margin-top:6px;padding-left:2px;">'
                f'Monthly: <strong>{fmt(monthly)}</strong>/mo '
                f'({fmt(result["commission_per_year"])}/yr × {yrs:.1f} yrs × {policies} policies / 12)</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="font-size:0.82rem;color:#555;margin-top:6px;padding-left:2px;">'
                f'Revenue: {fmt(result["commission_per_year"])}/yr × {yrs:.1f} yrs '
                f'× {policies} policies = <strong>{fmt(result["total_revenue"])}</strong></div>',
                unsafe_allow_html=True,
            )

    # Grand total
    grand_total = sum(d['total_revenue'] for d in t1_data.values())
    grand_monthly = grand_total / 12 if grand_total else 0

    st.divider()
    st.subheader('Summary')

    sum_col1, sum_col2 = st.columns([2, 1])

    with sum_col1:
        if show_monthly:
            summary_df = pd.DataFrame([
                {
                    'Product': d['product'],
                    'Commission/Month': fmt(d['total_revenue'] / 12 if d['total_revenue'] else 0),
                    'Commission/Year': fmt(d['commission_per_year']),
                    'Total (Lifetime)': fmt(d['total_revenue']),
                }
                for d in t1_data.values()
            ])
        else:
            summary_df = pd.DataFrame([
                {
                    'Product': d['product'],
                    'Annual Premium': fmt(d['premium']),
                    'Commission %': f"{d['commission_pct']:.1f}%",
                    'Years': f"{d['years']:.1f}",
                    'Policies': d['policies'],
                    'Commission/Year': fmt(d['commission_per_year']),
                    'Lifetime Comm/Policy': fmt(d['total_commission_per_policy']),
                    'Total Commission': fmt(d['total_revenue']),
                }
                for d in t1_data.values()
            ])
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

        with st.expander("ℹ️ What These Numbers Mean", expanded=False):
            st.markdown("""
            - **Annual Premium**: What the customer pays per year
            - **Commission %**: Agent's cut of that premium
            - **Years**: Customer retention period
            - **Policies**: How many the agent has closed
            - **Lifetime Comm/Policy**: What ONE policy is worth over its lifetime
            - **Total Commission**: All policies of this type, over time
            """)

    with sum_col2:
        display_val = fmt(grand_monthly) + '/mo' if show_monthly else fmt(grand_total)
        display_label = 'Grand Total (Monthly)' if show_monthly else 'Grand Total Commission'
        st.markdown(
            f'<div style="background-color:#114E38;border-radius:8px;padding:14px 20px 16px 20px;'
            f'color:white;text-align:center;">'
            f'<div style="font-size:0.8rem;opacity:0.9;font-weight:600;margin-bottom:6px;">'
            f'{display_label}</div>'
            f'<div class="doodle-underline" style="font-size:2rem;font-weight:700;display:inline-block;'
            f'position:relative;line-height:1.1;">{display_val}</div>'
            f'<div style="font-size:0.72rem;opacity:0.85;margin-top:6px;">'
            f'💰 The value sitting in this book</div></div>',
            unsafe_allow_html=True,
        )
        copy_to_clipboard_button(
            fmt(grand_total) if not show_monthly else fmt(grand_monthly),
            label='Copy Total',
            key='copy_grand',
        )

    # Revenue Breakdown chart
    st.subheader('Revenue Breakdown')

    products_list = [
        d['product'].replace('🚗 ', '').replace('🏠 ', '').replace('🏢 ', '')
        for d in t1_data.values()
    ]
    if show_monthly:
        chart_values = [d['total_revenue'] / 12 for d in t1_data.values()]
    else:
        chart_values = [d['total_revenue'] for d in t1_data.values()]
    fig = build_revenue_bar_chart(products_list, chart_values)
    st.plotly_chart(fig, use_container_width=True)

    # ── Cross-Sell Analysis ──────────────────────────────────────────────────
    st.subheader('Cross-Sell: Household Value by Bundle')
    st.markdown(
        '<p style="font-size:0.9rem;color:#666;margin-bottom:0.5rem;">'
        'Show agents how much a household is worth when they cross-sell. '
        'Each bar = 1 policy of each type in the bundle.</p>',
        unsafe_allow_html=True,
    )
    bundles = calc_cross_sell(t1_data)
    cs_fig = build_cross_sell_chart(bundles)
    st.plotly_chart(cs_fig, use_container_width=True)

    best_bundle = max(bundles, key=lambda b: b['value'])
    st.markdown(
        f'<p style="font-size:0.88rem;color:#555;">💡 Best cross-sell opportunity: '
        f'<strong>{best_bundle["bundle"]}</strong> is worth '
        f'<strong>{fmt(best_bundle["value"])}</strong> per household in lifetime commission. '
        f'(Home + Renters excluded — both are fire products.)</p>',
        unsafe_allow_html=True,
    )

    # ── Scenario Comparison ──────────────────────────────────────────────────
    st.subheader('Scenario Comparison: Current vs. Growth')

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        extra_auto = st.number_input('Additional Auto Policies', value=0, min_value=0, step=1, key='sc_auto')
    with sc2:
        extra_home = st.number_input('Additional Home Policies', value=5, min_value=0, step=1, key='sc_home')
    with sc3:
        extra_renters = st.number_input('Additional Renters Policies', value=0, min_value=0, step=1, key='sc_renters')

    # Build dynamic description
    parts = []
    if extra_auto:
        parts.append(f'{extra_auto} more Auto')
    if extra_home:
        parts.append(f'{extra_home} more Home')
    if extra_renters:
        parts.append(f'{extra_renters} more Renters')
    scenario_desc = ' + '.join(parts) if parts else 'no additional policies'
    st.markdown(
        f'<p style="font-size:0.9rem;color:#666;margin-bottom:0.5rem;">'
        f'"What if they close <strong>{scenario_desc}</strong>?" Compare current book to a growth scenario.</p>',
        unsafe_allow_html=True,
    )

    extras = {'auto': extra_auto, 'home': extra_home, 'renters': extra_renters}
    scenario_total = 0.0
    for key, d in t1_data.items():
        extra = extras.get(key, 0)
        c = calc_commission(d['premium'], d['commission_pct'], d['years'], d['policies'] + extra)
        scenario_total += c['total_revenue']

    growth = scenario_total - grand_total
    sc_col1, sc_col2, sc_col3 = st.columns(3)
    with sc_col1:
        st.metric('Current Book', fmt(grand_total))
    with sc_col2:
        st.metric('Growth Scenario', fmt(scenario_total))
    with sc_col3:
        st.metric('Additional Revenue', fmt(growth), delta=f'{growth / grand_total * 100:+.1f}%' if grand_total else '+0%')

    # ── Sensitivity Analysis ─────────────────────────────────────────────────
    st.subheader('Sensitivity: What If Retention Changes?')
    st.markdown(
        '<p style="font-size:0.9rem;color:#666;margin-bottom:0.5rem;">'
        'See how the grand total shifts when average customer retention goes up or down.</p>',
        unsafe_allow_html=True,
    )

    sens_data = sensitivity_retention(t1_data, [-2, -1, 0, 1, 2])
    sens_fig = build_sensitivity_chart(sens_data, current_delta=0)
    st.plotly_chart(sens_fig, use_container_width=True)

    current = sens_data[0]
    plus_one = sens_data.get(1, current)
    delta_pct = ((plus_one - current) / current * 100) if current else 0
    st.markdown(
        f'<p style="font-size:0.88rem;color:#555;">💡 <strong>+1 year</strong> of retention adds '
        f'<strong>{fmt(plus_one - current)}</strong> ({delta_pct:+.1f}%) to the total book value.</p>',
        unsafe_allow_html=True,
    )

    # ── Exports ──────────────────────────────────────────────────────────────
    st.divider()
    st.markdown(
        '<h3 style="color:#114E38;font-family:\'Playfair Display\',Georgia,serif;">'
        '📤 Grab Your Report</h3>',
        unsafe_allow_html=True,
    )

    # Agent name field
    agent_name = st.text_input(
        'Agent Name (optional — personalizes exports)',
        value=st.session_state.get('agent_name', ''),
        key='agent_name',
        placeholder='e.g. John Smith',
    )

    col_exp1, col_exp2, col_exp3 = st.columns(3)

    with col_exp1:
        def _build_t1_html():
            headers = [
                'Product', 'Annual Premium', 'Commission %', 'Years',
                'Policies', 'Commission/Year', 'Lifetime Comm/Policy', 'Total Commission',
            ]
            rows = []
            for d in t1_data.values():
                rows.append([
                    d['product'], fmt(d['premium']), f"{d['commission_pct']:.1f}%",
                    f"{d['years']:.1f}", d['policies'], fmt(d['commission_per_year']),
                    fmt(d['total_commission_per_policy']), fmt(d['total_revenue']),
                ])
            total_row = ['GRAND TOTAL', '', '', '', '', '', '', fmt(grand_total)]
            chart_html = fig.to_html(include_plotlyjs='cdn', config={'displayModeBar': False})
            body = (
                '<h1>ROI Calculator Results</h1>'
                f'<div class="subtitle">Grand Total Commission: {fmt(grand_total)}</div>'
                + build_html_table(headers, rows, total_row)
                + '<h2 style="margin-top:40px;">Revenue Breakdown</h2>'
                + chart_html
            )
            return html_wrap('ROI Calculator Report', body, agent_name=agent_name or None).encode('utf-8')

        st.download_button(
            label='📧 Get HTML (for email)',
            data=_build_t1_html(),
            file_name=f'roi_report_{now_local().strftime("%Y%m%d_%H%M")}.html',
            mime='text/html',
        )

    with col_exp2:
        if REPORTLAB_AVAILABLE:
            def _build_t1_pdf():
                from reportlab.lib.units import inch
                table_data = [['Product', 'Annual\nPremium', 'Comm\n%', 'Years', 'Policies',
                               'Comm/\nYear', 'Lifetime\nComm/Policy', 'Total\nCommission']]
                for d in t1_data.values():
                    name = d['product'].replace('🚗 ', '').replace('🏠 ', '').replace('🏢 ', '')
                    table_data.append([
                        name, fmt(d['premium']), f"{d['commission_pct']:.1f}%",
                        f"{d['years']:.1f}", str(d['policies']),
                        fmt(d['commission_per_year']), fmt(d['total_commission_per_policy']),
                        fmt(d['total_revenue']),
                    ])
                table_data.append(['GRAND TOTAL', '', '', '', '', '', '', fmt(grand_total)])
                col_widths = [1.1*inch, 0.85*inch, 0.45*inch, 0.45*inch,
                              0.6*inch, 0.75*inch, 1.05*inch, 1.05*inch]
                return build_pdf_report(
                    'Insurance ROI Calculator',
                    f'Grand Total Commission: {fmt(grand_total)}',
                    table_data, col_widths, chart_fig=fig,
                    agent_name=agent_name or None,
                )

            pdf_data = _build_t1_pdf()
            if pdf_data:
                st.download_button(
                    label='📄 Get PDF (formal)',
                    data=pdf_data,
                    file_name=f'roi_report_{now_local().strftime("%Y%m%d_%H%M")}.pdf',
                    mime='application/pdf',
                )
        else:
            st.info('📥 PDF export requires reportlab package')

    with col_exp3:
        excel_df = pd.DataFrame([
            {
                'Product': d['product'].replace('🚗 ', '').replace('🏠 ', '').replace('🏢 ', ''),
                'Annual Premium': d['premium'],
                'Commission %': d['commission_pct'],
                'Years': d['years'],
                'Policies': d['policies'],
                'Commission per Year': d['commission_per_year'],
                'Lifetime Commission per Policy': d['total_commission_per_policy'],
                'Total Commission': d['total_revenue'],
            }
            for d in t1_data.values()
        ])
        excel_data = create_formatted_excel(excel_df, sheet_name='ROI Calculator')
        if excel_data:
            st.download_button(
                label='📊 Get Excel (editable)',
                data=excel_data,
                file_name=f'roi_data_{now_local().strftime("%Y%m%d_%H%M")}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
        else:
            st.info('📥 Excel export requires openpyxl package')

    return t1_data
