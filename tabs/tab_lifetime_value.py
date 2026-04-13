"""Tab 1 — Lifetime Value Tracker."""

import pandas as pd
import streamlit as st

from config import PRODUCTS, DEFAULT_COMMISSION_PCT
from utils import fmt, validate_numeric
from calculations import calc_commission, sensitivity_retention
from charts import build_revenue_bar_chart, build_sensitivity_chart
from exports import (
    html_wrap, build_html_table, metric_card_html,
    build_pdf_report, create_formatted_excel, REPORTLAB_AVAILABLE,
)
from utils import now_local


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

        st.markdown(
            f'<div style="font-size:0.82rem;color:#555;margin-top:6px;padding-left:2px;">'
            f'Revenue preview: {fmt(result["commission_per_year"])}/year × {yrs:.1f} years '
            f'× {policies} policies = <strong>{fmt(result["total_revenue"])}</strong></div>',
            unsafe_allow_html=True,
        )

    # Grand total
    grand_total = sum(d['total_revenue'] for d in t1_data.values())

    st.divider()
    st.subheader('Summary')

    sum_col1, sum_col2 = st.columns([2, 1])

    with sum_col1:
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
            - **Annual Premium**: What the customer forks over each year for this policy
            - **Commission %**: Agent's cut of that premium
            - **Years**: How long they stick around (customer retention)
            - **Policies**: How many of these the agent has closed
            - **Commission/Year**: What this product pays the agent annually
            - **Lifetime Comm/Policy**: The magic number—what ONE policy is worth over its lifetime
            - **Total Commission**: All policies of this type, added up, over time

            💡 **The big idea:** That "Lifetime Comm/Policy" number? That's what the agent is
            *really* selling when they close a policy. Not just this year's check—the whole relationship.
            """)

    with sum_col2:
        st.markdown(
            '<div style="background-color:#114E38;border-radius:8px;padding:14px 20px 16px 20px;'
            'color:white;text-align:center;">'
            '<div style="font-size:0.8rem;opacity:0.9;font-weight:600;margin-bottom:6px;">'
            'Grand Total Commission</div>'
            '<div class="doodle-underline" style="font-size:2rem;font-weight:700;display:inline-block;'
            'position:relative;line-height:1.1;">' + fmt(grand_total) + '</div>'
            '<div style="font-size:0.72rem;opacity:0.85;margin-top:6px;">'
            '💰 The value sitting in this book</div></div>',
            unsafe_allow_html=True,
        )

    # Revenue Breakdown chart
    st.subheader('Revenue Breakdown')

    products_list = [
        d['product'].replace('🚗 ', '').replace('🏠 ', '').replace('🏢 ', '')
        for d in t1_data.values()
    ]
    revenue_values = [d['total_revenue'] for d in t1_data.values()]
    fig = build_revenue_bar_chart(products_list, revenue_values)
    st.plotly_chart(fig, use_container_width=True)

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
    st.markdown(
        '<p style="color:#666;font-size:0.95rem;margin-bottom:1rem;">'
        "Email it to the agent, attach it to a proposal, or print it out. Your call.</p>",
        unsafe_allow_html=True,
    )

    col_exp1, col_exp2, col_exp3 = st.columns(3)

    with col_exp1:
        @st.cache_data
        def _build_t1_html(_data_hash, _grand, _chart_html):
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
            body = (
                '<h1>ROI Calculator Results</h1>'
                f'<div class="subtitle">Grand Total Commission: {fmt(grand_total)}</div>'
                + build_html_table(headers, rows, total_row)
                + '<h2 style="margin-top:40px;">Revenue Breakdown</h2>'
                + _chart_html
            )
            return html_wrap('ROI Calculator Report', body).encode('utf-8')

        chart_html = fig.to_html(include_plotlyjs='cdn', config={'displayModeBar': False})
        data_hash = str([(d['premium'], d['commission_pct'], d['years'], d['policies']) for d in t1_data.values()])
        st.download_button(
            label='📧 Get HTML (for email)',
            data=_build_t1_html(data_hash, grand_total, chart_html),
            file_name=f'roi_report_{now_local().strftime("%Y%m%d_%H%M")}.html',
            mime='text/html',
            help='Interactive charts work in email clients',
        )

    with col_exp2:
        if REPORTLAB_AVAILABLE:
            @st.cache_data
            def _build_t1_pdf(_data_hash, _grand):
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
                )

            pdf_data = _build_t1_pdf(data_hash, grand_total)
            if pdf_data:
                st.download_button(
                    label='📄 Get PDF (formal)',
                    data=pdf_data,
                    file_name=f'roi_report_{now_local().strftime("%Y%m%d_%H%M")}.pdf',
                    mime='application/pdf',
                    help='Clean print-ready format',
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
                help='Editable spreadsheet format',
            )
        else:
            st.info('📥 Excel export requires openpyxl package')

    return t1_data
