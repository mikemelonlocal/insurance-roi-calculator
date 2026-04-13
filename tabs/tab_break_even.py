"""Tab 2 — Path to Profit (Break-Even Simulator)."""

import math

import pandas as pd
import streamlit as st

from config import PRODUCTS, DEFAULT_COMMISSION_PCT
from utils import fmt, validate_numeric, safe_divide, now_local
from calculations import calc_break_even_single, calc_all_combinations, pareto_filter
from charts import build_pareto_scatter, build_goal_gauge, classify_efficiency
from exports import (
    html_wrap, build_html_table, metric_card_html,
    build_pdf_report, create_formatted_excel, REPORTLAB_AVAILABLE,
)
from styling import copy_to_clipboard_button


def render(t1_data=None):
    """Render Tab 2.  *t1_data* from Tab 1 is used when the user opts to sync values."""

    # Header with reset
    tcol1, tcol2 = st.columns([4, 1])
    with tcol1:
        st.markdown(
            '<h2 style="color:#114E38;font-family:\'Playfair Display\',Georgia,serif;">'
            '🎯 Path to Profit</h2>',
            unsafe_allow_html=True,
        )
    with tcol2:
        if st.button('🔄 Reset to Defaults', key='reset_t2'):
            for key in PRODUCTS:
                for field in ['prem', 'comm', 'yrs']:
                    sk = f't2_{key}_{field}'
                    if sk in st.session_state:
                        del st.session_state[sk]
            for sk in ['t2_budget', 't2_mgmt', 't2_include_mgmt', 't2_use_tab1']:
                if sk in st.session_state:
                    del st.session_state[sk]
            st.rerun()

    st.markdown(
        '<p style="color:#1a1a1a;font-size:1.05rem;margin-bottom:1.5rem;">'
        'When an agent asks "How many policies do I need to close?", this gives them the answer. '
        'Find every combination of Auto, Home, and Renters that covers their monthly marketing spend.</p>',
        unsafe_allow_html=True,
    )

    # ── Budget ───────────────────────────────────────────────────────────────
    st.subheader('Budget')
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        monthly_budget = st.number_input(
            'Monthly Budget ($)', value=1000.0, min_value=0.0, step=100.0,
            key='t2_budget', help="Agent's monthly marketing spend",
        )
    with col_b2:
        include_mgmt_fee = st.checkbox(
            'Include Management Fee', value=False, key='t2_include_mgmt',
            help='Add an optional management fee to the budget',
        )

    mgmt_fee = 0.0
    if include_mgmt_fee:
        mgmt_fee = st.number_input(
            'Management Fee ($)', value=0.0, min_value=0.0, step=50.0,
            key='t2_mgmt', help='Optional additional fee',
        )

    effective_budget = validate_numeric(monthly_budget) + validate_numeric(mgmt_fee)

    if effective_budget == 0:
        st.error('⚠️ Budget is $0. Please enter a budget amount to see break-even combinations.')
    elif effective_budget < 100:
        st.warning(f'⚠️ Budget (${effective_budget:,.2f}) is very low. Results may not be realistic.')

    st.metric('Effective Budget', fmt(effective_budget))

    st.divider()
    st.subheader('Product Assumptions')

    use_tab1_values = st.checkbox(
        '📋 Use values from ROI Calculator (Tab 1)',
        value=True,
        key='t2_use_tab1',
        help='Automatically pull premium, commission %, and years from Tab 1',
    )

    # ── Product inputs ───────────────────────────────────────────────────────
    t2_data = {}

    for key, cfg in PRODUCTS.items():
        label = cfg['label']
        def_prem = cfg['default_premium']
        def_yrs = float(cfg['default_years'])
        def_comm = DEFAULT_COMMISSION_PCT

        if use_tab1_values and t1_data and key in t1_data:
            def_prem = t1_data[key]['premium']
            def_comm = t1_data[key]['commission_pct']
            def_yrs = t1_data[key]['years']

        st.markdown(
            f'<div class="prod-card"><div class="prod-card-title">{label}</div></div>',
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            prem = st.number_input(
                'Annual Premium ($)', value=def_prem, min_value=0.0, step=10.0,
                key=f't2_{key}_prem', disabled=use_tab1_values,
            )
        with c2:
            comm = st.number_input(
                'Commission (%)', value=def_comm, min_value=0.0, max_value=100.0, step=0.5,
                key=f't2_{key}_comm', disabled=use_tab1_values,
            )
        with c3:
            yrs = st.number_input(
                'Years as Customer', value=def_yrs, min_value=0.0, step=0.5,
                key=f't2_{key}_yrs', disabled=use_tab1_values,
            )

        prem = validate_numeric(prem)
        comm = validate_numeric(comm, 0, 100)
        yrs = validate_numeric(yrs)

        rev_per_close = prem * (comm / 100) * yrs

        t2_data[key] = {
            'product': label,
            'premium': prem,
            'commission_pct': comm,
            'years': yrs,
            'rev_per_close': rev_per_close,
        }

        st.markdown(
            f'<div style="font-size:0.85rem;color:#555;margin-top:6px;padding-left:2px;">'
            f'<strong>Revenue per Closed-Won Lead:</strong> {fmt(rev_per_close)}</div>',
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Single-product break-evens ───────────────────────────────────────────
    st.subheader('Single-Product Break-Even')

    keys = list(PRODUCTS.keys())
    be = {k: calc_break_even_single(effective_budget, t2_data[k]['rev_per_close']) for k in keys}

    cols = st.columns(len(keys))
    for col, k in zip(cols, keys):
        n = be[k]
        with col:
            st.metric(
                f'{t2_data[k]["product"]} Break-Even',
                f'{n} closed-won {"app" if n == 1 else "apps"}',
                help=f'Close {n} to cover {fmt(effective_budget)}',
            )

    # ── Goal Tracker ────────────────────────────────────────────────────────
    st.divider()
    st.subheader('Goal Tracker: How Close Are You?')
    st.markdown(
        '<p style="font-size:0.9rem;color:#666;margin-bottom:0.5rem;">'
        'Enter how many policies the agent has closed this month across all products.</p>',
        unsafe_allow_html=True,
    )

    goal_cols = st.columns(len(keys))
    for i, (col, k) in enumerate(zip(goal_cols, keys)):
        with col:
            st.number_input(
                f'{t2_data[k]["product"]} Closed This Month',
                value=0, min_value=0, step=1,
                key=f'goal_{k}',
            )

    # Calculate combined revenue from all closed policies
    closed_counts = {k: st.session_state.get(f'goal_{k}', 0) for k in keys}
    total_closed_rev = sum(closed_counts[k] * t2_data[k]['rev_per_close'] for k in keys)
    remaining = max(0, effective_budget - total_closed_rev)
    pct = min(total_closed_rev / effective_budget * 100, 100) if effective_budget > 0 else 0

    # Revenue breakdown per product
    rev_parts = []
    for k in keys:
        cnt = closed_counts[k]
        if cnt > 0:
            rev = cnt * t2_data[k]['rev_per_close']
            name = t2_data[k]['product'].replace('🚗 ', '').replace('🏠 ', '').replace('🏢 ', '')
            rev_parts.append(f'{cnt} {name} = {fmt(rev)}')

    # Progress bar
    bar_color = '#47B74F' if pct >= 100 else '#F1CB20' if pct >= 50 else '#FF6B6B'
    st.markdown(
        f'<div style="margin:12px 0 6px 0;">'
        f'<div style="background:#e0e0e0;border-radius:8px;height:28px;overflow:hidden;">'
        f'<div style="background:{bar_color};height:100%;width:{pct:.1f}%;border-radius:8px;'
        f'transition:width 0.3s;display:flex;align-items:center;justify-content:center;'
        f'color:white;font-weight:700;font-size:0.8rem;">'
        f'{pct:.0f}%</div></div></div>',
        unsafe_allow_html=True,
    )

    # Summary metrics
    tcr1, tcr2, tcr3 = st.columns(3)
    with tcr1:
        st.metric('Revenue from Closed Policies', fmt(total_closed_rev))
        if rev_parts:
            st.markdown(
                '<div style="font-size:0.8rem;color:#666;">' + ' | '.join(rev_parts) + '</div>',
                unsafe_allow_html=True,
            )
        copy_to_clipboard_button(fmt(total_closed_rev), label='Copy', key='copy_closed_rev')
    with tcr2:
        st.metric('Budget Target', fmt(effective_budget))
    with tcr3:
        if remaining > 0:
            st.metric('Still Needed', fmt(remaining))
        else:
            surplus = total_closed_rev - effective_budget
            st.metric('Above Break-Even', fmt(surplus), delta=f'+{surplus / effective_budget * 100:.0f}%' if effective_budget else '')

    st.divider()
    st.subheader('All Combinations')

    # Revenue per close & max counts
    rev_list = [t2_data[k]['rev_per_close'] for k in keys]
    max_list = [be[k] for k in keys]

    # Generate combos with performance guard
    estimated = 1
    for m in max_list:
        estimated *= (m + 1)

    if estimated > 1_000_000:
        st.warning(
            f'⚠️ Estimated {estimated:,} iterations — capping search to prevent freezing. '
            'Consider reducing the budget or increasing product premiums.',
        )

    all_valid = calc_all_combinations(effective_budget, rev_list, max_list)
    pareto_combos = pareto_filter(all_valid)

    # ── Filter dropdowns ─────────────────────────────────────────────────────
    auto_options = ['Any'] + [str(v) for v in range(max_list[0] + 1)]
    home_options = ['Any'] + [str(v) for v in range(max_list[1] + 1)]
    renters_options = ['Any'] + [str(v) for v in range(max_list[2] + 1)]

    fcol_header1, fcol_header2 = st.columns([3, 1])
    with fcol_header1:
        st.markdown("**Filter by specific policy counts (select 'Any' to show all):**")
    with fcol_header2:
        if st.button('🔄 Clear Filters', key='clear_filters_t2'):
            st.session_state['filter_auto'] = 'Any'
            st.session_state['filter_home'] = 'Any'
            st.session_state['filter_renters'] = 'Any'
            st.rerun()

    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        sel_auto = st.selectbox('Auto Policies', auto_options, key='filter_auto')
        f_auto = None if sel_auto == 'Any' else int(sel_auto)
    with fcol2:
        sel_home = st.selectbox('Home Policies', home_options, key='filter_home')
        f_home = None if sel_home == 'Any' else int(sel_home)
    with fcol3:
        sel_rent = st.selectbox('Renters Policies', renters_options, key='filter_renters')
        f_rent = None if sel_rent == 'Any' else int(sel_rent)

    filter_active = f_auto is not None or f_home is not None or f_rent is not None

    if filter_active:
        filtered = all_valid
        if f_auto is not None:
            filtered = [c for c in filtered if c[0] == f_auto]
        if f_home is not None:
            filtered = [c for c in filtered if c[1] == f_home]
        if f_rent is not None:
            filtered = [c for c in filtered if c[2] == f_rent]
        valid_combos = pareto_filter(filtered)
    else:
        valid_combos = pareto_combos

    valid_combos.sort(key=lambda x: (x[0] + x[1] + x[2], x[4]))

    if filter_active:
        st.info(f'Showing {len(valid_combos)} most efficient combination(s) matching the selected counts')
    else:
        col_info1, col_info2 = st.columns([4, 1])
        with col_info1:
            st.info(f'Showing all {len(valid_combos)} Pareto-efficient combinations')
        with col_info2:
            with st.expander('ℹ️ What is Pareto-efficient?'):
                st.markdown('''
                **Pareto-efficient** = No wasted effort

                These combinations cover your budget using the **minimum number of policies**.
                Any other combination with the same or lower policy counts wouldn't meet the budget.

                Example: If "5 autos" works, we won't show "6 autos" (that's wasteful).
                ''')

    # ── Display table ────────────────────────────────────────────────────────
    if valid_combos:
        df_combos = []
        for a, h, r, total_rev, above in valid_combos:
            df_combos.append({
                'Auto': a,
                'Home': h,
                'Renters': r,
                'Total Closed-Won Leads': a + h + r,
                'Total Revenue': fmt(total_rev),
                'Above Budget': fmt(above),
                'Efficiency': classify_efficiency(above, effective_budget),
            })

        df_display = pd.DataFrame(df_combos)

        st.markdown(
            '<p style="font-size:0.85rem;color:#666;margin-bottom:0.5rem;">'
            '<strong>💡 Efficiency colors:</strong> '
            '<span style="color:#2E7D32;">🟢 Break-even (0-10% over budget)</span> | '
            '<span style="color:#F57F17;">🟡 Profitable (10-30% over)</span> | '
            '<span style="color:#C62828;">🔴 High-performing (30%+ over)</span>. '
            '"Break-even" is most efficient, "High-performing" is highest value.</p>',
            unsafe_allow_html=True,
        )

        def _color_eff(val):
            if val == 'Break-even':
                return 'background-color: #E8F5E9; color: #2E7D32; font-weight: bold'
            elif val == 'Profitable':
                return 'background-color: #FFF9C4; color: #F57F17; font-weight: bold'
            elif val == 'High-performing':
                return 'background-color: #FFEBEE; color: #C62828; font-weight: bold'
            return ''

        styled = df_display.style.map(_color_eff, subset=['Efficiency'])
        st.dataframe(styled, use_container_width=True, hide_index=True)

        # Scatter chart
        st.subheader('Efficiency Visualization')
        pareto_fig = build_pareto_scatter(df_combos, effective_budget)
        st.plotly_chart(pareto_fig, use_container_width=True)

        # ── Exports ──────────────────────────────────────────────────────────
        st.divider()
        st.markdown(
            '<h3 style="color:#114E38;font-family:\'Playfair Display\',Georgia,serif;">'
            '📤 Share These Combos</h3>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="color:#666;font-size:0.95rem;margin-bottom:1rem;">'
            "Give agents all their options. Let them pick what feels doable.</p>",
            unsafe_allow_html=True,
        )

        exp_col1, exp_col2, exp_col3 = st.columns(3)

        with exp_col1:
            def _build_t2_html():
                chart_html = pareto_fig.to_html(include_plotlyjs='cdn', config={'displayModeBar': False})
                headers = ['Auto', 'Home', 'Renters', 'Total Closed-Won Leads',
                           'Total Revenue', 'Above Budget', 'Efficiency']
                rows = []
                for row in df_combos:
                    eff = row['Efficiency']
                    tag_map = {
                        'Break-even': '<span class="tag-tight">Break-even</span>',
                        'Profitable': '<span class="tag-mod">Profitable</span>',
                        'High-performing': '<span class="tag-over">High-performing</span>',
                    }
                    rows.append([
                        row['Auto'], row['Home'], row['Renters'],
                        row['Total Closed-Won Leads'], row['Total Revenue'],
                        row['Above Budget'], tag_map.get(eff, eff),
                    ])
                rev_keys = list(PRODUCTS.keys())
                body = (
                    '<h1>Break-Even Simulator Results</h1>'
                    f'<div class="subtitle">Effective Budget: {fmt(effective_budget)} '
                    f'| Found {len(valid_combos)} combinations</div>'
                    '<h2>Revenue per Closed-Won Lead</h2>'
                    '<div class="metric-grid">'
                    + metric_card_html('Auto', fmt(t2_data[rev_keys[0]]['rev_per_close']))
                    + metric_card_html('Home', fmt(t2_data[rev_keys[1]]['rev_per_close']))
                    + metric_card_html('Renters', fmt(t2_data[rev_keys[2]]['rev_per_close']))
                    + '</div>'
                    '<h2 style="margin-top:40px;">Efficiency Visualization</h2>'
                    + chart_html
                    + '<h2 style="margin-top:40px;">Combinations</h2>'
                    + build_html_table(headers, rows)
                )
                return html_wrap('Break-Even Report', body).encode('utf-8')

            st.download_button(
                label='📧 Get HTML',
                data=_build_t2_html(),
                file_name=f'breakeven_report_{now_local().strftime("%Y%m%d_%H%M")}.html',
                mime='text/html',
            )

        with exp_col2:
            if REPORTLAB_AVAILABLE:
                def _build_t2_pdf():
                    from reportlab.lib.units import inch
                    table_data = [['Auto', 'Home', 'Renters', 'Total', 'Revenue', 'Above Budget', 'Efficiency']]
                    for row in df_combos:
                        table_data.append([
                            str(row['Auto']), str(row['Home']), str(row['Renters']),
                            str(row['Total Closed-Won Leads']), row['Total Revenue'],
                            row['Above Budget'], row['Efficiency'],
                        ])
                    return build_pdf_report(
                        'Break-Even Simulator',
                        f'Effective Budget: {fmt(effective_budget)}',
                        table_data, [0.8 * inch] * 7,
                    )
                pdf_data = _build_t2_pdf()
                if pdf_data:
                    st.download_button(
                        label='📄 Get PDF',
                        data=pdf_data,
                        file_name=f'breakeven_report_{now_local().strftime("%Y%m%d_%H%M")}.pdf',
                        mime='application/pdf',
                    )
            else:
                st.info('📥 PDF export requires reportlab')

        with exp_col3:
            excel_data = create_formatted_excel(df_display, sheet_name='Break-Even Combos')
            if excel_data:
                st.download_button(
                    label='📊 Get Excel',
                    data=excel_data,
                    file_name=f'breakeven_data_{now_local().strftime("%Y%m%d_%H%M")}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                )
            else:
                st.info('📥 Excel export requires openpyxl package')
    else:
        st.warning('No valid combinations found with current parameters.')
