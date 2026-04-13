"""Commission Goldmine — Melon Local ROI Calculator.

Run with:  streamlit run app.py
"""

import os
import streamlit as st

from config import APP_TITLE, APP_VERSION, PRESETS, SIDEBAR_IMAGE
from styling import inject_css
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
    tab_lead_channels.render()

with tab4:
    tab_talk_tracks.render()

with tab5:
    tab_how_to_use.render()
