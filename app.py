"""Commission Goldmine — Melon Local ROI Calculator.

Run with:  streamlit run app.py
"""

import os
import streamlit as st

from config import APP_TITLE, APP_VERSION, PRESETS, SIDEBAR_IMAGE, SHAREABLE_PARAMS, PRODUCTS
from styling import inject_css, inject_localstorage_sync
from exports import build_batch_zip
from utils import fmt, now_local
from tabs import (
    tab_lifetime_value,
    tab_break_even,
    tab_lead_channels,
    tab_talk_tracks,
    tab_how_to_use,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    layout='wide',
    initial_sidebar_state='expanded',
)

inject_css()
inject_localstorage_sync()

# ── URL query params → session state (shareable scenarios) ───────────────────
qp = st.query_params
for param in SHAREABLE_PARAMS:
    qp_val = qp.get(param)
    if qp_val is not None:
        try:
            st.session_state[f't1_{param}'] = float(qp_val)
        except (ValueError, TypeError):
            if param == 'agent_name':
                st.session_state['agent_name'] = str(qp_val)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Melon Local graphic (graceful fallback)
    img_path = os.path.join(os.path.dirname(__file__), SIDEBAR_IMAGE)
    if os.path.exists(img_path):
        st.image(img_path, width=200)
    st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

    st.title('⚙️ Settings')

    st.subheader('Quick Presets (Tab 1)')
    preset = st.selectbox(
        'Load Scenario',
        list(PRESETS.keys()),
        help='Pre-configured scenarios for Lifetime Value Tracker (Tab 1 only)',
    )

    if 'last_preset' not in st.session_state:
        st.session_state.last_preset = 'Average'

    if preset in PRESETS and preset != st.session_state.last_preset:
        for key, val in PRESETS[preset].items():
            st.session_state[f't1_{key}'] = val
        st.session_state.last_preset = preset
        st.success(f'✓ {preset} preset loaded')
        st.rerun()

    st.divider()

    # ── Share Scenario Link ──────────────────────────────────────────────────
    st.subheader('Share This Scenario')
    if st.button('Generate Share Link', key='gen_share_link'):
        params = {}
        for key in PRODUCTS:
            for field in ['prem', 'comm', 'yrs', 'policies']:
                sk = f't1_{key}_{field}'
                val = st.session_state.get(sk)
                if val is not None:
                    params[f'{key}_{field}'] = str(val)
        agent = st.session_state.get('agent_name', '')
        if agent:
            params['agent_name'] = agent

        query_str = '&'.join(f'{k}={v}' for k, v in params.items())
        st.code(f'?{query_str}', language=None)
        st.caption('Append this to your app URL to share the current scenario.')

    st.divider()

    st.subheader('App Info')
    st.markdown(f"""
    <div style="color:#1a1a1a;">

    <p><strong>Version:</strong> {APP_VERSION}<br>
    <strong>Internal Tool for Melon Local CSMs</strong></p>

    <p><strong>What's this?</strong><br>
    Your secret weapon for showing insurance agents what their policies are <em>really</em> worth.
    This isn't spreadsheets and guesswork—it's lifetime commission value, broken down and ready to share.</p>

    <p><strong>Three Tools Inside:</strong></p>
    <ul style="color:#1a1a1a;">
        <li>💰 <strong>Lifetime Value Tracker</strong> - Total commission sitting in their book</li>
        <li>🎯 <strong>Path to Profit</strong> - Every way to hit their budget goal</li>
        <li>🔍 <strong>Lead Cost Showdown</strong> - Which lead source costs less (for real)</li>
    </ul>

    <p><strong>Export as:</strong></p>
    <ul style="color:#1a1a1a;">
        <li>📧 HTML (email-friendly, charts work)</li>
        <li>📄 PDF (formal, ready to send)</li>
        <li>📊 Excel (edit offline, share with the team)</li>
        <li>📦 Batch ZIP (all tabs in one download)</li>
    </ul>

    <p><strong>Questions?</strong> Ping Mike Long</p>

    </div>
    """, unsafe_allow_html=True)

# ── Main title ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:1.5rem 0 1rem 0;">
    <h1 style="color:#114E38;font-size:2.8rem;font-weight:700;margin-bottom:0.5rem;
               font-family:'Playfair Display',Georgia,serif;">
        <span class="doodle-underline">Commission Goldmine</span>
    </h1>
    <p style="color:#47B74F;font-size:1.15rem;font-weight:500;margin:0.5rem 0 0 0;">
        Your internal calculators for showing agents what their policies are <em>really</em> worth
    </p>
    <p style="color:#666;font-size:0.9rem;margin:0.3rem 0 0 0;">
        A Melon Local tool for Client Success
    </p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    '💰 Lifetime Value Tracker',
    '🎯 Path to Profit',
    '🔍 Lead Cost Showdown',
    '💬 Talk Tracks',
    '📖 How to Use',
])

with tab1:
    t1_data = tab_lifetime_value.render()

with tab2:
    tab_break_even.render(t1_data=t1_data)

with tab3:
    tab_lead_channels.render(t1_data=t1_data)

with tab4:
    tab_talk_tracks.render()

with tab5:
    tab_how_to_use.render()

# ── Batch Export (bottom of page) ────────────────────────────────────────────
st.divider()
st.markdown(
    '<h3 style="color:#114E38;font-family:\'Playfair Display\',Georgia,serif;text-align:center;">'
    '📦 Batch Export — All Tabs</h3>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="color:#666;font-size:0.95rem;margin-bottom:1rem;text-align:center;">'
    'Download all tab reports in a single ZIP file.</p>',
    unsafe_allow_html=True,
)

if st.button('Generate Batch ZIP', key='batch_zip'):
    with st.spinner('Building reports...'):
        from exports import html_wrap, build_html_table, create_formatted_excel

        agent_name = st.session_state.get('agent_name', '') or None
        ts = now_local().strftime("%Y%m%d_%H%M")
        files = {}

        # Tab 1 HTML
        grand_total = sum(d['total_revenue'] for d in t1_data.values())
        headers = ['Product', 'Annual Premium', 'Commission %', 'Years', 'Policies',
                   'Commission/Year', 'Lifetime Comm/Policy', 'Total Commission']
        rows = []
        for d in t1_data.values():
            rows.append([d['product'], fmt(d['premium']), f"{d['commission_pct']:.1f}%",
                        f"{d['years']:.1f}", d['policies'], fmt(d['commission_per_year']),
                        fmt(d['total_commission_per_policy']), fmt(d['total_revenue'])])
        total_row = ['GRAND TOTAL', '', '', '', '', '', '', fmt(grand_total)]
        body = ('<h1>ROI Calculator Results</h1>'
                f'<div class="subtitle">Grand Total: {fmt(grand_total)}</div>'
                + build_html_table(headers, rows, total_row))
        files[f'roi_report_{ts}.html'] = html_wrap('ROI Report', body, agent_name=agent_name).encode('utf-8')

        # Tab 1 Excel
        import pandas as pd
        excel_df = pd.DataFrame([{
            'Product': d['product'], 'Annual Premium': d['premium'],
            'Commission %': d['commission_pct'], 'Years': d['years'],
            'Policies': d['policies'], 'Commission per Year': d['commission_per_year'],
            'Lifetime Commission': d['total_commission_per_policy'],
            'Total Commission': d['total_revenue'],
        } for d in t1_data.values()])
        files[f'roi_data_{ts}.xlsx'] = create_formatted_excel(excel_df, 'ROI Calculator')

        zip_data = build_batch_zip(files)
        if zip_data:
            st.download_button(
                label='📦 Download ZIP',
                data=zip_data,
                file_name=f'melon_reports_{ts}.zip',
                mime='application/zip',
            )
        else:
            st.warning('No reports could be generated.')
