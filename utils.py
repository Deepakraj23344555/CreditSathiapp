import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# STRICT Color Palette
COLORS = {
    "primary": "#0B1F3A",
    "secondary": "#1E3A8A",
    "accent": "#14B8A6",
    "background": "#F8FAFC",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "text": "#1E293B",
    "surface": "rgba(255, 255, 255, 0.95)" # For glassmorphism
}

def hex_to_rgba(hex_code, alpha):
    """Converts a hex color string to an rgba string for Plotly compatibility."""
    hex_code = hex_code.lstrip('#')
    r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r},{g},{b},{alpha})'

def inject_custom_css():
    """Injects premium fintech CSS with glassmorphism, animations, and Inter font."""
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        /* Global Typography & Background */
        html, body, [class*="css"]  {{
            font-family: 'Inter', sans-serif;
        }}
        .stApp {{
            background-color: {COLORS["background"]};
            background-image: radial-gradient(circle at 50% 0%, {COLORS["secondary"]}10 0%, transparent 50%);
        }}
        h1, h2, h3 {{ color: {COLORS["primary"]} !important; font-weight: 700 !important; letter-spacing: -0.5px; }}
        
        /* Sidebar styling - Modern & Clean */
        [data-testid="stSidebar"] {{
            background-color: {COLORS["primary"]};
            color: white;
            box-shadow: 4px 0 15px rgba(0,0,0,0.05);
        }}
        [data-testid="stSidebar"] * {{ color: rgba(255,255,255,0.9) !important; }}
        
        /* Glassmorphism Cards */
        .fintech-card {{
            background: {COLORS["surface"]};
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
            margin-bottom: 20px;
            border: 1px solid rgba(0,0,0,0.05);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .fintech-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
        }}
        .card-top-accent {{ border-top: 4px solid {COLORS["secondary"]}; }}
        
        /* Score Display */
        .score-display {{
            font-size: 56px;
            font-weight: 800;
            color: {COLORS["primary"]};
            text-align: center;
            line-height: 1.1;
            margin: 10px 0;
            background: -webkit-linear-gradient(45deg, {COLORS["primary"]}, {COLORS["secondary"]});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        /* Buttons - Rounded & Animated */
        .stButton>button {{
            background-color: {COLORS["accent"]};
            color: white;
            border-radius: 50px; /* Pill shape */
            border: none;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 12px {COLORS["accent"]}40;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .stButton>button:hover {{
            background-color: {COLORS["primary"]};
            box-shadow: 0 6px 16px {COLORS["primary"]}40;
            transform: translateY(-1px);
        }}
        
        /* Step Wizard & Badges */
        .badge {{ padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 13px; display: inline-block; }}
        .badge-success {{ background-color: {COLORS["success"]}15; color: {COLORS["success"]}; }}
        .badge-warning {{ background-color: {COLORS["warning"]}15; color: {COLORS["warning"]}; }}
        .badge-danger {{ background-color: {COLORS["danger"]}15; color: {COLORS["danger"]}; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- REUSABLE UI COMPONENTS ---

def render_metric_card(title, value, icon="📊"):
    """Renders a standard KPI card."""
    st.markdown(f"""
    <div class="fintech-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <p style="margin: 0; color: #64748B; font-weight: 600; font-size: 14px;">{title}</p>
            <span style="font-size: 20px;">{icon}</span>
        </div>
        <h3 style="margin: 10px 0 0 0; font-size: 24px;">{value}</h3>
    </div>
    """, unsafe_allow_html=True)

def render_score_badge(score, category, badge_class):
    """Renders the main CRS score card."""
    st.markdown(f"""
    <div class="fintech-card card-top-accent" style="text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
        <p style="font-size: 16px; margin:0; color: #64748B; font-weight: 600;">Credit Readiness Score</p>
        <div class="score-display">{score}</div>
        <span class="badge {badge_class}">{category}</span>
    </div>
    """, unsafe_allow_html=True)

def render_lender_tile(lender, lender_type, status, rate, border_color):
    """Renders a lender matching result tile."""
    st.markdown(f"""
    <div class="fintech-card" style="border-left: 5px solid {border_color}; padding: 16px 24px;">
        <h4 style="margin: 0 0 8px 0;">{lender} <span style="font-size: 13px; color: #64748B; font-weight: 400; background: #F1F5F9; padding: 2px 8px; border-radius: 12px; margin-left: 8px;">{lender_type}</span></h4>
        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #E2E8F0; padding-top: 12px; margin-top: 8px;">
            <p style="margin: 0; font-weight: 600; color: {border_color};">{status}</p>
            <p style="margin: 0; color: #64748B; font-size: 14px;">Est. Max Rate: <strong style="color: {COLORS['text']};">{rate}</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- ENHANCED PLOTLY VISUALIZATIONS ---

def _base_layout(fig):
    """Applies common premium layout settings to all charts."""
    fig.update_layout(
        font=dict(family="Inter", color=COLORS["text"]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Inter", bordercolor="#E2E8F0")
    )
    return fig

def create_gauge_chart(score):
    if score < 500: color = COLORS["danger"]
    elif score < 650: color = COLORS["warning"]
    elif score < 750: color = COLORS["accent"]
    else: color = COLORS["success"]

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Credit Utilization / Health", 'font': {'color': '#64748B', 'size': 14}},
        gauge = {
            'axis': {'range': [0, 850], 'tickwidth': 1, 'tickcolor': "#CBD5E1"},
            'bar': {'color': color, 'thickness': 0.85},
            'bgcolor': "#F8FAFC",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 500], 'color': hex_to_rgba(COLORS["danger"], 0.1)},
                {'range': [500, 650], 'color': hex_to_rgba(COLORS["warning"], 0.1)},
                {'range': [650, 750], 'color': hex_to_rgba(COLORS["accent"], 0.1)},
                {'range': [750, 850], 'color': hex_to_rgba(COLORS["success"], 0.1)}],
            'threshold': {'line': {'color': COLORS["primary"], 'width': 4}, 'thickness': 0.85, 'value': score}}))
    
    fig.update_layout(height=300)
    return _base_layout(fig)

def create_breakdown_pie(components):
    labels = list(components.keys())
    values = list(components.values())
    fig = px.pie(names=labels, values=values, hole=0.55, 
                 color_discrete_sequence=[COLORS["primary"], COLORS["secondary"], COLORS["accent"], COLORS["warning"], COLORS["success"]])
    fig.update_traces(textposition='inside', textinfo='percent', hoverinfo='label+percent+value', marker=dict(line=dict(color='#FFFFFF', width=2)))
    fig.update_layout(height=320, showlegend=False, title=dict(text="Factor Breakdown", font=dict(size=14, color='#64748B')))
    return _base_layout(fig)

def create_factor_bar(components):
    labels = list(components.keys())
    values = list(components.values())
    max_values = [30, 15, 20, 20, 15]
    
    fig = go.Figure(data=[
        go.Bar(name='Achieved', x=labels, y=values, marker_color=COLORS["accent"], marker_line_color=COLORS["accent"], marker_line_width=1.5, opacity=0.9),
        go.Bar(name='Potential', x=labels, y=max_values, marker_color=hex_to_rgba(COLORS["primary"], 0.1), hoverinfo='skip')
    ])
    
    fig.update_layout(
        barmode='overlay', 
        height=320, 
        showlegend=False,
        title=dict(text="Performance vs Potential", font=dict(size=14, color='#64748B')),
        xaxis=dict(showgrid=False, tickangle=-45),
        yaxis=dict(showgrid=True, gridcolor='#F1F5F9', gridwidth=1)
    )
    return _base_layout(fig)
