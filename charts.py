"""Plotly chart builders and matplotlib conversion for PDF export."""

import io
import re

import plotly.graph_objects as go

from config import DARK_GREEN, PRI_GREEN, BORDER
from utils import fmt, safe_divide

# Optional matplotlib for PDF charts
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# ── Shared layout defaults ───────────────────────────────────────────────────

_FONT = dict(family='Poppins, sans-serif', color='#1a1a1a')
_AXIS_TICK = dict(color='#1a1a1a')


def _base_layout(**overrides):
    defaults = dict(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=_FONT,
        margin=dict(t=30, b=60, l=60, r=30),
    )
    defaults.update(overrides)
    return defaults


# ── Tab 1: Revenue bar chart ────────────────────────────────────────────────

def build_revenue_bar_chart(product_names, revenue_values):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=product_names,
        y=revenue_values,
        marker_color=PRI_GREEN,
        text=[fmt(v) for v in revenue_values],
        textposition='outside',
    ))
    fig.update_layout(
        **_base_layout(height=400),
        yaxis=dict(showgrid=True, gridcolor=BORDER, tickprefix='$',
                   title=dict(text='Total Revenue', font=dict(color='#1a1a1a')),
                   tickfont=_AXIS_TICK),
        xaxis=dict(title=dict(text='Product', font=dict(color='#1a1a1a')),
                   tickfont=_AXIS_TICK),
    )
    return fig


# ── Tab 1: Sensitivity bar chart ────────────────────────────────────────────

def build_sensitivity_chart(sensitivity_data, current_delta=0):
    """Bar chart showing grand total at each retention delta."""
    labels = []
    values = []
    colors = []
    for delta, total in sorted(sensitivity_data.items()):
        labels.append(f'{delta:+d} yr' if delta != 0 else 'Current')
        values.append(total)
        colors.append(DARK_GREEN if delta == current_delta else PRI_GREEN)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        text=[fmt(v) for v in values],
        textposition='outside',
    ))
    fig.update_layout(
        **_base_layout(height=350),
        yaxis=dict(showgrid=True, gridcolor=BORDER, tickprefix='$', tickfont=_AXIS_TICK),
        xaxis=dict(title=dict(text='Retention Change', font=dict(color='#1a1a1a')),
                   tickfont=_AXIS_TICK),
    )
    return fig


# ── Tab 2: Pareto scatter ───────────────────────────────────────────────────

EFFICIENCY_COLORS = {
    'Break-even': PRI_GREEN,
    'Profitable': '#F1CB20',
    'High-performing': '#FF6B6B',
}


def classify_efficiency(above_budget, budget):
    pct = safe_divide(above_budget, budget, 0) * 100
    if pct <= 10:
        return 'Break-even'
    elif pct <= 30:
        return 'Profitable'
    return 'High-performing'


def build_pareto_scatter(combo_rows, effective_budget):
    """combo_rows: list of dicts with keys Auto, Home, Renters, Total Closed-Won Leads,
       Total Revenue (str), Above Budget (str), Efficiency."""
    fig = go.Figure()

    for eff, label_suffix in [
        ('Break-even', '(0-10% over)'),
        ('Profitable', '(10-30% over)'),
        ('High-performing', '(30%+ over)'),
    ]:
        rows = [c for c in combo_rows if c['Efficiency'] == eff]
        if not rows:
            continue
        fig.add_trace(go.Scatter(
            x=[c['Total Closed-Won Leads'] for c in rows],
            y=[float(c['Total Revenue'].replace('$', '').replace(',', '')) for c in rows],
            mode='markers',
            name=f'{eff} {label_suffix}',
            marker=dict(size=12, color=EFFICIENCY_COLORS[eff],
                        line=dict(width=1, color='white')),
            text=[
                f"{c['Auto']} Auto + {c['Home']} Home + {c['Renters']} Renters"
                f"<br>Revenue: {c['Total Revenue']}<br>Above Budget: {c['Above Budget']}"
                for c in rows
            ],
            hovertemplate='<b>%{text}</b><extra></extra>',
        ))

    if combo_rows:
        max_policies = max(c['Total Closed-Won Leads'] for c in combo_rows)
        fig.add_trace(go.Scatter(
            x=[0, max_policies + 2],
            y=[effective_budget, effective_budget],
            mode='lines',
            name='Budget Target',
            line=dict(color=DARK_GREEN, width=2, dash='dash'),
            hovertemplate=f'Budget: {fmt(effective_budget)}<extra></extra>',
        ))

    fig.update_layout(
        **_base_layout(height=450),
        xaxis=dict(title=dict(text='Total Closed-Won Leads (Policies)', font=dict(color='#1a1a1a')),
                   showgrid=True, gridcolor=BORDER, tickfont=_AXIS_TICK),
        yaxis=dict(title=dict(text='Total Revenue', font=dict(color='#1a1a1a')),
                   showgrid=True, gridcolor=BORDER, tickprefix='$', tickfont=_AXIS_TICK),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                    font=dict(color='#1a1a1a')),
        margin=dict(t=60, b=80, l=60, r=30),
    )
    return fig


# ── Tab 3: Lead comparison grouped bar ──────────────────────────────────────

def build_lead_comparison_chart(channels):
    """channels: list of dicts with 'name', 'lead_cost_to_close', 'payroll_to_close', 'total_cost_to_close'."""
    categories = ['Lead Cost to Close', 'Payroll to Close', 'Total Cost to Close']
    bar_colors = [DARK_GREEN, PRI_GREEN, '#F1CB20', '#FF6B6B', '#9C27B0', '#FF9800']

    fig = go.Figure()
    for i, ch in enumerate(channels):
        y_vals = [ch['lead_cost_to_close'], ch['payroll_to_close'], ch['total_cost_to_close']]
        fig.add_trace(go.Bar(
            name=ch['name'],
            x=categories,
            y=y_vals,
            marker_color=bar_colors[i % len(bar_colors)],
            text=[fmt(v) for v in y_vals],
            textposition='outside',
        ))

    fig.update_layout(
        **_base_layout(height=400),
        barmode='group',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                    font=dict(color='#1a1a1a')),
        yaxis=dict(showgrid=True, gridcolor=BORDER, tickprefix='$', tickfont=_AXIS_TICK),
        xaxis=dict(tickfont=_AXIS_TICK),
    )
    return fig


# ── Matplotlib conversion for PDF ───────────────────────────────────────────

def plotly_to_matplotlib_image(fig_plotly, width_inches=7, height_inches=4):
    """Convert a Plotly figure to a PNG BytesIO buffer via matplotlib."""
    if not MATPLOTLIB_AVAILABLE:
        return None

    try:
        fig, ax = plt.subplots(figsize=(width_inches, height_inches))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        if len(fig_plotly.data) > 1 and all(t.type == 'bar' for t in fig_plotly.data):
            # Grouped bar chart
            x_labels = [str(x) for x in fig_plotly.data[0].x]
            num_groups = len(x_labels)
            num_bars = len(fig_plotly.data)
            bar_width = 0.35
            x = np.arange(num_groups)
            mpl_colors = [DARK_GREEN, PRI_GREEN, '#F1CB20', '#FF6B6B']

            for i, trace in enumerate(fig_plotly.data):
                offset = (i - num_bars / 2 + 0.5) * bar_width
                bars = ax.bar(x + offset, trace.y, bar_width,
                              label=trace.name, color=mpl_colors[i % len(mpl_colors)])
                for bar, val in zip(bars, trace.y):
                    ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height(),
                            f'${val:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

            ax.set_xticks(x)
            ax.set_xticklabels(x_labels)
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=num_bars, frameon=False, fontsize=10)
            ylabel = (fig_plotly.layout.yaxis.title.text or '') if fig_plotly.layout.yaxis.title else ''
            ax.set_ylabel(ylabel, fontsize=11, color='#1a1a1a')
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        elif fig_plotly.data[0].type == 'bar':
            data = fig_plotly.data[0]
            x_labels = [re.sub(r'[^\w\s-]', '', str(x)).strip() for x in data.x]
            bars = ax.bar(x_labels, data.y, color=PRI_GREEN, width=0.6)
            for bar, val in zip(bars, data.y):
                ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height(),
                        f'${val:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
            xlabel = (fig_plotly.layout.xaxis.title.text or '') if fig_plotly.layout.xaxis.title else ''
            ylabel = (fig_plotly.layout.yaxis.title.text or '') if fig_plotly.layout.yaxis.title else ''
            ax.set_xlabel(xlabel, fontsize=11, color='#1a1a1a')
            ax.set_ylabel(ylabel, fontsize=11, color='#1a1a1a')
            max_val = max(data.y) if data.y else 1
            ax.set_ylim(0, max_val * 1.15)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        elif fig_plotly.data[0].type == 'scatter':
            data = fig_plotly.data[0]
            ax.scatter(data.x, data.y, c=PRI_GREEN, s=100, alpha=0.7,
                       edgecolors=DARK_GREEN, linewidth=1.5)
            xlabel = (fig_plotly.layout.xaxis.title.text or '') if fig_plotly.layout.xaxis.title else ''
            ylabel = (fig_plotly.layout.yaxis.title.text or '') if fig_plotly.layout.yaxis.title else ''
            ax.set_xlabel(xlabel, fontsize=11, color='#1a1a1a')
            ax.set_ylabel(ylabel, fontsize=11, color='#1a1a1a')
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            ax.grid(True, alpha=0.3)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors='#1a1a1a')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        plt.close(fig)
        return buf
    except Exception:
        return None
