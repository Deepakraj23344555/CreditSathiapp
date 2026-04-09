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
    "text": "#1E293B"
}

def inject_custom_css():
    """Injects custom CSS to match the premium fintech UI requirements."""
    css = f"""
    <style>
        /* Base styling */
        .stApp {{
            background-color: {COLORS["background"]};
        }}
        h1, h2, h3 {{
            color: {COLORS["primary"]} !important;
            font-family: 'Inter', sans-serif;
        }}
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {COLORS["primary"]};
            color: white;
        }}
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        /* Cards */
        .fintech-card {{
            background-color: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 20px;
            border-top: 4px solid {COLORS["secondary"]};
        }}
        .score-display {{
            font-size: 48px;
            font-weight: bold;
            color: {COLORS["primary"]};
            text-align: center;
        }}
        /* Buttons */
        .stButton>button {{
            background-color: {COLORS["accent"]};
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: {COLORS["secondary"]};
            color: white;
        }}
        /* Status Badges */
        .badge-success {{ background-color: {COLORS["success"]}20; color: {COLORS["success"]}; padding: 4px 12px; border-radius: 16px; font-weight: bold; font-size: 14px;}}
        .badge-warning {{ background-color: {COLORS["warning"]}20; color: {COLORS["warning"]}; padding: 4px 12px; border-radius: 16px; font-weight: bold; font-size: 14px;}}
        .badge-danger {{ background-color: {COLORS["danger"]}20; color: {COLORS["danger"]}; padding: 4px 12px; border-radius: 16px; font-weight: bold; font-size: 14px;}}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def hex_to_rgba(hex_code, alpha):
    """Converts a hex color string to an rgba string for Plotly compatibility."""
    hex_code = hex_code.lstrip('#')
    r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r},{g},{b},{alpha})'

def create_gauge_chart(score):
    """Creates a Plotly gauge chart for the CRS score."""
    if score < 500:
        color = COLORS["danger"]
    elif score < 650:
        color = COLORS["warning"]
    elif score < 750:
        color = COLORS["accent"]
    else:
        color = COLORS["success"]

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Credit Readiness Score", 'font': {'color': COLORS["primary"], 'size': 24}},
        gauge = {
            'axis': {'range': [0, 850], 'tickwidth': 1, 'tickcolor': COLORS["primary"]},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 500], 'color': hex_to_rgba(COLORS["danger"], 0.2)},
                {'range': [500, 650], 'color': hex_to_rgba(COLORS["warning"], 0.2)},
                {'range': [650, 750], 'color': hex_to_rgba(COLORS["accent"], 0.2)},
                {'range': [750, 850], 'color': hex_to_rgba(COLORS["success"], 0.2)}],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score}}))
    
    fig.update_layout(
        height=350, 
        margin=dict(l=20, r=20, t=50, b=20), 
        paper_bgcolor="rgba(0,0,0,0)", 
        font={'color': COLORS["text"]}
    )
    return fig

def create_breakdown_pie(components):
    """Creates a pie chart showing score breakdown."""
    labels = list(components.keys())
    values = list(components.values())
    fig = px.pie(names=labels, values=values, hole=0.4, title="Score Component Contribution",
                 color_discrete_sequence=[COLORS["primary"], COLORS["secondary"], COLORS["accent"], COLORS["warning"], COLORS["success"]])
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)")
    return fig

def create_factor_bar(components):
    """Creates a bar chart for factor performance."""
    labels = list(components.keys())
    values = list(components.values())
    max_values = [30, 15, 20, 20, 15] # Max weights
    
    fig = go.Figure(data=[
        go.Bar(name='Achieved', x=labels, y=values, marker_color=COLORS["accent"]),
        # Fixed: Using the hex_to_rgba helper instead of string concatenation
        go.Bar(name='Max Potential', x=labels, y=max_values, marker_color=hex_to_rgba(COLORS["primary"], 0.25))
    ])
    
    fig.update_layout(
        barmode='overlay', 
        title="Factor Performance vs Potential", 
        height=350, 
        margin=dict(l=20, r=20, t=50, b=20), 
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': COLORS["text"]}
    )
    return fig
