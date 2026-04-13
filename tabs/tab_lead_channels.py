"""Tab 3 — Lead Cost Showdown (dynamic N-channel comparison)."""

import pandas as pd
import streamlit as st

from config import DEFAULT_HOURLY_WAGE, DEFAULT_LEAD_CHANNELS
from utils import fmt, validate_numeric, now_local
from calculations import calc_lead_channel
from charts import build_lead_comparison_chart, build_channel_roi_chart
from exports import (
    html_wrap, build_html_table, metric_card_html,
    build_pdf_report, create_formatted_excel, REPORTLAB_AVAILABLE,
)
from styling import copy_to_clipboard_button


def _init_channels():
    """Initialise session-state channel list once."""
    if 't3_channels' not in st.session_state:
        st.session_state['t3_channels'] = [dict(ch) for ch in DEFAULT_LEAD_CHANNELS]


def render(t1_data=None):
    _init_channels()
    channels = st.session_state['t3_channels']

    # Header with reset
    tcol1, tcol2 = st.columns([4, 1])
    with tcol1:
        st.markdown(
            '<h2 style="color:#114E38;font-family:\'Playfair Display\',Georgia,serif;">'
            '🔍 Lead Cost Showdown</h2>',
            unsafe_allow_html=True,
        )
    with tcol2:
        if st.button('🔄 Reset to Defaults', key='reset_t3'):
            st.session_state['t3_channels'] = [dict(ch) for ch in DEFAULT_LEAD_CHANNELS]
            if 't3_wage' in st.session_state:
                del st.session_state['t3_wage']
            st.rerun()

    st.markdown(
        '<p style="color:#1a1a1a;font-size:1.05rem;margin-bottom:1.5rem;">'
        'Agents love to argue about which lead source is "better." This settles it. Compare '
        'the <strong>fully-loaded cost</strong> to close one household—including the agent\'s '
        'time—across any lead channels.</p>',
        unsafe_allow_html=True,
    )

    st.subheader('Payroll Settings')
    hourly_wage = st.number_input(
        'Hourly Wage ($)', value=DEFAULT_HOURLY_WAGE, min_value=0.0, step=0.50,
        key='t3_wage', help='Agent or staff hourly rate',
    )
    hourly_wage = validate_numeric(hourly_wage)

    st.divider()
    st.subheader('Lead Channels')

    # Add / remove channel buttons
    btn_col1, btn_col2, _ = st.columns([1, 1, 4])
    with btn_col1:
        if st.button('➕ Add Channel', key='add_channel'):
            channels.append({
                'name': f'Channel {len(channels) + 1}',
                'cost_per_lead': 10.0,
                'closing_rate': 5.0,
                'hours_per_lead': 1.0,
            })
            st.rerun()
    with btn_col2:
        if len(channels) > 2 and st.button('➖ Remove Last', key='remove_channel'):
            channels.pop()
            st.rerun()

    # Channel inputs
    cols = st.columns(min(len(channels), 3))
    for i, ch in enumerate(channels):
        col = cols[i % len(cols)]
        with col:
            st.markdown(
                f'<div class="prod-card"><div class="prod-card-title">{ch["name"]}</div></div>',
                unsafe_allow_html=True,
            )
            ch['name'] = st.text_input('Channel Name', value=ch['name'], key=f't3_name_{i}')
            ch['cost_per_lead'] = st.number_input(
                'Cost per Lead ($)', value=ch['cost_per_lead'], min_value=0.0, step=0.50,
                key=f't3_cpl_{i}',
            )
            ch['closing_rate'] = st.number_input(
                'Closing Rate (%)', value=ch['closing_rate'], min_value=0.01, max_value=100.0,
                step=0.5, key=f't3_cr_{i}',
            )
            ch['hours_per_lead'] = st.number_input(
                'Hours to Work 1 Lead', value=ch['hours_per_lead'], min_value=0.0, step=0.25,
                key=f't3_hrs_{i}',
            )

    # ── Calculations ─────────────────────────────────────────────────────────
    results = []
    for ch in channels:
        cpl = validate_numeric(ch['cost_per_lead'])
        cr = validate_numeric(ch['closing_rate'], 0.01, 100)
        hrs = validate_numeric(ch['hours_per_lead'])
        r = calc_lead_channel(cpl, cr, hrs, hourly_wage)
        results.append({**r, 'name': ch['name'], 'cost_per_lead': cpl,
                        'closing_rate': cr, 'hours_per_lead': hrs})

    st.divider()
    st.subheader('Cost to Close Comparison')

    st.markdown(
        '<p style="font-size:0.85rem;color:#666;margin-bottom:0.5rem;">'
        '<strong>💡 The key insight:</strong> Cheaper per lead ≠ cheaper overall. '
        'This shows the <strong>total cost</strong> (leads + agent time) to close one household.</p>',
        unsafe_allow_html=True,
    )

    # Chart
    fig = build_lead_comparison_chart(results)
    st.plotly_chart(fig, use_container_width=True)

    # Winner callout
    if len(results) >= 2:
        winner = min(results, key=lambda r: r['total_cost_to_close'])
        others = [r for r in results if r['name'] != winner['name']]
        if all(winner['total_cost_to_close'] < o['total_cost_to_close'] for o in others):
            st.markdown(
                f'<div style="background:#FEF8E9;border-left:4px solid #47B74F;border-radius:0 8px 8px 0;'
                f'padding:12px 16px;color:#114E38;font-weight:600;margin-top:12px;">'
                f'🏆 <strong>{winner["name"]} wins.</strong> Cheapest to close one household '
                f'when you factor in time.</div>',
                unsafe_allow_html=True,
            )

    # ── ROI per Channel (combines with Tab 1 data) ────────────────────────────
    if t1_data:
        st.divider()
        st.subheader('ROI per Channel: Cost vs. Commission Earned')
        st.markdown(
            '<p style="font-size:0.9rem;color:#666;margin-bottom:0.5rem;">'
            'How does the cost to close compare against the average commission earned? '
            'Uses your Tab 1 commission data to calculate net ROI per closed household.</p>',
            unsafe_allow_html=True,
        )

        # Average commission across all products (1 policy each, weighted by product)
        avg_commission = sum(
            d['total_commission_per_policy'] for d in t1_data.values()
        ) / max(len(t1_data), 1)

        channels_with_roi = []
        for r in results:
            net = avg_commission - r['total_cost_to_close']
            channels_with_roi.append({
                **r,
                'avg_commission': avg_commission,
                'net_roi': net,
            })

        roi_fig = build_channel_roi_chart(channels_with_roi)
        st.plotly_chart(roi_fig, use_container_width=True)

        roi_cols = st.columns(len(channels_with_roi))
        for i, cr in enumerate(channels_with_roi):
            with roi_cols[i % len(roi_cols)]:
                color = '#2E7D32' if cr['net_roi'] > 0 else '#C62828'
                st.markdown(
                    f'<div style="text-align:center;padding:8px;">'
                    f'<div style="font-size:0.8rem;color:#666;font-weight:600;">{cr["name"]} Net ROI</div>'
                    f'<div style="font-size:1.4rem;font-weight:700;color:{color};">{fmt(cr["net_roi"])}</div>'
                    f'<div style="font-size:0.75rem;color:#999;">per closed household</div></div>',
                    unsafe_allow_html=True,
                )
                copy_to_clipboard_button(fmt(cr['net_roi']), label='Copy ROI', key=f'copy_roi_{i}')

    # ── Detail cards ─────────────────────────────────────────────────────────
    st.divider()
    detail_cols = st.columns(min(len(results), 3))
    card_colors = ['#114E38', '#47B74F', '#F1CB20', '#FF6B6B']

    for i, r in enumerate(results):
        col = detail_cols[i % len(detail_cols)]
        color = card_colors[i % len(card_colors)]
        with col:
            st.markdown(
                f'<div style="background:#FEF8E9;border-left:4px solid {color};border-radius:0 8px 8px 0;'
                f'padding:12px 18px;margin-bottom:10px;">'
                f'<span style="font-size:1rem;font-weight:700;color:#114E38;">{r["name"]} — Results</span>'
                '</div>',
                unsafe_allow_html=True,
            )
            st.metric('Quotes to Close 1 Household', f'{r["quotes_to_close"]}')
            st.metric('Lead Cost to Close', fmt(r['lead_cost_to_close']))
            st.metric('Payroll to Close 1 Household', fmt(r['payroll_to_close']))
            st.markdown(
                f'<div style="background:{color};border-radius:8px;padding:14px 18px;margin-top:8px;color:white;">'
                f'<div style="font-size:0.85rem;opacity:0.9;font-weight:600;">Total Cost to Close 1 Household</div>'
                f'<div style="font-size:1.6rem;font-weight:700;">{fmt(r["total_cost_to_close"])}</div>'
                f'<div style="font-size:0.78rem;opacity:0.8;">Lead cost {fmt(r["lead_cost_to_close"])} '
                f'+ Payroll {fmt(r["payroll_to_close"])}</div></div>',
                unsafe_allow_html=True,
            )

    # ── Exports ──────────────────────────────────────────────────────────────
    st.divider()
    st.markdown(
        '<h3 style="color:#114E38;font-family:\'Playfair Display\',Georgia,serif;">'
        '📤 Send the Proof</h3>',
        unsafe_allow_html=True,
    )

    def _build_t3_html():
        chart_html = fig.to_html(include_plotlyjs='cdn', config={'displayModeBar': False})

        winner = min(results, key=lambda r: r['total_cost_to_close'])
        winner_box = (
            f'<div style="background:#FEF8E9;border-left:4px solid #47B74F;border-radius:0 8px 8px 0;'
            f'padding:12px 16px;color:#114E38;font-weight:600;margin-top:12px;">'
            f'✓ {winner["name"]} is cheapest to close one household.</div>'
        )

        channel_cards = '<div class="two-col">'
        for r in results:
            channel_cards += (
                '<div><div class="prod-card">'
                f'<div class="prod-title">{r["name"]}</div>'
                '<div class="metric-grid">'
                + metric_card_html('Cost per Lead', fmt(r['cost_per_lead']))
                + metric_card_html('Closing Rate', f'{r["closing_rate"]}%')
                + metric_card_html('Payroll per Lead', fmt(r['payroll_per_lead']))
                + metric_card_html('Quotes to Close 1 HH', str(r['quotes_to_close']))
                + metric_card_html('Lead Cost to Close', fmt(r['lead_cost_to_close']))
                + metric_card_html('Payroll to Close 1 HH', fmt(r['payroll_to_close']))
                + '</div>'
                '<div class="total-box" style="background:#114E38;margin-top:14px;">'
                '<div class="label">Total Cost to Close 1 Household</div>'
                f'<div class="value">{fmt(r["total_cost_to_close"])}</div>'
                f'<div class="sub">Lead cost {fmt(r["lead_cost_to_close"])} '
                f'+ Payroll {fmt(r["payroll_to_close"])}</div>'
                '</div></div></div>'
            )
        channel_cards += '</div>'

        body = (
            '<h1>Lead Channel Cost-to-Close Report</h1>'
            f'<div class="subtitle">Hourly wage: {fmt(hourly_wage)}</div>'
            '<h2 style="margin-top:40px;">Cost Comparison</h2>'
            + chart_html + winner_box + channel_cards
        )
        return html_wrap('Lead Channel Report', body).encode('utf-8')

    exp_col1, exp_col2, exp_col3 = st.columns(3)

    with exp_col1:
        st.download_button(
            label='📧 Get HTML',
            data=_build_t3_html(),
            file_name=f'lead_channel_report_{now_local().strftime("%Y%m%d_%H%M")}.html',
            mime='text/html',
        )

    with exp_col2:
        if REPORTLAB_AVAILABLE:
            def _build_t3_pdf():
                from reportlab.lib.units import inch
                headers = ['Metric'] + [r['name'] for r in results]
                table_data = [headers]
                metrics = [
                    ('Cost per Lead', lambda r: fmt(r['cost_per_lead'])),
                    ('Closing Rate', lambda r: f'{r["closing_rate"]}%'),
                    ('Hours per Lead', lambda r: f'{r["hours_per_lead"]}'),
                    ('Quotes to Close 1 HH', lambda r: str(r['quotes_to_close'])),
                    ('Lead Cost to Close', lambda r: fmt(r['lead_cost_to_close'])),
                    ('Payroll to Close', lambda r: fmt(r['payroll_to_close'])),
                    ('TOTAL COST TO CLOSE', lambda r: fmt(r['total_cost_to_close'])),
                ]
                for label, fn in metrics:
                    table_data.append([label] + [fn(r) for r in results])
                n_cols = 1 + len(results)
                col_widths = [2.5 * inch] + [2 * inch] * len(results)
                return build_pdf_report(
                    'Lead Channel Comparison',
                    f'Hourly Wage: {fmt(hourly_wage)}',
                    table_data, col_widths, chart_fig=fig,
                )

            pdf_data = _build_t3_pdf()
            if pdf_data:
                st.download_button(
                    label='📄 Get PDF',
                    data=pdf_data,
                    file_name=f'lead_channel_report_{now_local().strftime("%Y%m%d_%H%M")}.pdf',
                    mime='application/pdf',
                )
        else:
            st.info('📥 PDF export requires reportlab')

    with exp_col3:
        comparison_df = pd.DataFrame([
            {
                'Channel': r['name'],
                'Cost per Lead': r['cost_per_lead'],
                'Closing Rate %': r['closing_rate'],
                'Hours per Lead': r['hours_per_lead'],
                'Payroll per Lead': r['payroll_per_lead'],
                'Quotes to Close 1 HH': r['quotes_to_close'],
                'Lead Cost to Close': r['lead_cost_to_close'],
                'Payroll to Close': r['payroll_to_close'],
                'Total Cost to Close': r['total_cost_to_close'],
            }
            for r in results
        ])
        excel_data = create_formatted_excel(comparison_df, sheet_name='Lead Channels')
        if excel_data:
            st.download_button(
                label='📊 Get Excel',
                data=excel_data,
                file_name=f'lead_channel_data_{now_local().strftime("%Y%m%d_%H%M")}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
        else:
            st.info('📥 Excel export requires openpyxl package')
