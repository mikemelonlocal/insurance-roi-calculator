"""Inject branded CSS into the Streamlit app."""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&display=swap');

html, body, [class*='css'] { font-family: 'Poppins', sans-serif; }

h1, h2, h3, .stTabs [data-baseweb='tab'] {
    font-family: 'Playfair Display', 'Georgia', serif !important;
}
p, label, input, select, textarea, button, .stMetric {
    font-family: 'Poppins', sans-serif !important;
}

.stApp { background: #FFFFFF; }

.doodle-underline {
    position: relative;
    display: inline-block;
}
.doodle-underline::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: -8px;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #F1CB20 0%, #F1CB20 60%, transparent 60%);
    background-size: 12px 4px;
    background-repeat: repeat-x;
}

.melon-shape {
    border-radius: 50% / 60%;
    background: linear-gradient(135deg, #47B74F 0%, #40A74C 100%);
}
.stripe-texture {
    background-image: repeating-linear-gradient(
        45deg, transparent, transparent 10px,
        rgba(71, 183, 79, 0.1) 10px, rgba(71, 183, 79, 0.1) 20px
    );
}

/* Top header bar */
header[data-testid='stHeader'] { background: #114E38; color: #FFFFFF; }
header[data-testid='stHeader'] * { color: #FFFFFF !important; }

/* Sidebar */
section[data-testid='stSidebar'] { background: #FEF8E9; }
section[data-testid='stSidebar'] > div { padding-top: 2rem; }

/* Tabs */
div[data-baseweb='tab-list'] { border-bottom: 2px solid #114E38; gap: 4px; }
button[data-baseweb='tab'] {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    color: #114E38;
    border-radius: 6px 6px 0 0;
    padding: 8px 20px;
}
button[data-baseweb='tab'][aria-selected='true'] {
    background: #114E38 !important;
    color: #FFFFFF !important;
}
button[data-baseweb='tab'][aria-selected='true'] * {
    color: #FFFFFF !important;
}

/* Metric cards */
div[data-testid='metric-container'] {
    background: #FFFFFF;
    border: 1px solid #D9D9D9;
    border-radius: 8px;
    padding: 12px 16px;
}
div[data-testid='metric-container'] label {
    color: #114E38; font-weight: 600; font-size: 0.78rem;
}
div[data-testid='metric-container'] div[data-testid='stMetricValue'] {
    font-size: 1.4rem; font-weight: 700; color: #1a1a1a;
}

/* Buttons */
div.stDownloadButton > button,
div.stButton > button {
    background: #47B74F; color: #FFFFFF; border: none;
    border-radius: 6px; font-family: 'Poppins', sans-serif;
    font-weight: 600; padding: 8px 20px;
}
div.stDownloadButton > button:hover,
div.stButton > button:hover { background: #114E38; }

/* Dataframe */
div[data-testid='stDataFrame'] {
    border: 1px solid #D9D9D9; border-radius: 8px; overflow: hidden;
}
div[data-testid='stDataFrame'] table,
div[data-testid='stDataFrame'] thead,
div[data-testid='stDataFrame'] tbody,
div[data-testid='stDataFrame'] tr,
div[data-testid='stDataFrame'] th,
div[data-testid='stDataFrame'] td {
    background-color: #FFFFFF !important; color: #1a1a1a !important;
}
div[data-testid='stDataFrame'] th {
    background-color: #114E38 !important; color: #FFFFFF !important; font-weight: 600 !important;
}
div[data-testid='stDataFrame'] tbody tr:nth-child(even) { background-color: #FAFAFA !important; }
div[data-testid='stDataFrame'] tbody tr:nth-child(odd)  { background-color: #FFFFFF !important; }
div[data-testid='stDataFrame'] * { color: #1a1a1a !important; }
div[data-testid='stDataFrame'] th * { color: #FFFFFF !important; }

hr { border-color: #D9D9D9; }

/* Input fields */
div[data-baseweb='select'] > div,
div[data-baseweb='select'] > div > div,
div[data-baseweb='base-input'] > div,
input[type='number'], input[type='text'], textarea,
div[data-baseweb='popover'] {
    background-color: #FFFFFF !important; color: #1a1a1a !important;
    border: 1px solid #D9D9D9 !important;
}
div[data-baseweb='base-input'] button,
div[data-baseweb='base-input'] svg {
    background-color: #FFFFFF !important; color: #1a1a1a !important;
}
div[role='listbox'], div[role='option'], li[role='option'] {
    background-color: #FFFFFF !important; color: #1a1a1a !important;
}
div[role='option']:hover, li[role='option']:hover {
    background-color: #F5F5F5 !important;
}

label[data-testid='stWidgetLabel'],
.stNumberInput label, .stSelectbox label, .stCheckbox label {
    color: #114E38 !important; font-weight: 600 !important;
}
input[type='checkbox'] { accent-color: #47B74F !important; }

p, .stMarkdown p, div[data-testid='stMarkdownContainer'] p {
    color: #1a1a1a !important;
}

/* Remove extra padding from dataframes */
div[data-testid='stDataFrame'] { margin-bottom: 0 !important; padding-bottom: 0 !important; }
div[data-testid='stDataFrame'] > div { padding-bottom: 0 !important; margin-bottom: 0 !important; }
div[data-testid='stDataFrame'] > div > div { padding-bottom: 0 !important; margin-bottom: 0 !important; }
div[data-testid='stDataFrame'] table { margin-bottom: 0 !important; border-bottom: none !important; }
div[data-testid='stDataFrame'] tbody tr:last-child td { border-bottom: none !important; }
.dataframe-container { padding-bottom: 0 !important; margin-bottom: 0 !important; }

/* Product callout cards */
.prod-card {
    background-color: #FEF8E9; border-left: 4px solid #114E38;
    border-radius: 0 8px 8px 0; padding: 12px 18px; margin-bottom: 6px;
}
.prod-card-title { font-size: 1rem; font-weight: 700; color: #114E38; margin-bottom: 2px; }

/* Section headers */
h1 { color: #114E38 !important; font-size: 1.8rem !important; font-weight: 700 !important; }
h2 { color: #114E38 !important; font-weight: 600 !important; }
h3 { color: #114E38 !important; font-weight: 600 !important; }

div[data-testid='stAlert'] { border-radius: 8px; }

@media (max-width: 768px) {
    div[data-testid='column'] { width: 100% !important; flex: 100% !important; }
    .prod-card { margin-bottom: 12px; }
}
</style>
"""


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)
