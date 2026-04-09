import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# --- LIGHT PREMIUM FINTECH PALETTE (WCAG Compliant) ---
COLORS = {
    "background": "#F8FAFC",      # Off-white background
    "card_bg": "#FFFFFF",         # Pure white cards
    "primary": "#0B1F3A",         # Dark Navy (High contrast text)
    "secondary": "#1E3A8A",       # Royal Blue
    "accent": "#14B8A6",          # Teal
    "border": "#E2E8F0",          # Light grey borders
    "text_muted": "#475569",      # Slate grey for secondary text
    "success": "#059669",
    "warning": "#D97706",
    "danger": "#DC2626"
}

def inject_premium_css():
    """Injects high-contrast, clutter-free CSS with Poppins & Inter fonts."""
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@600;700;800&display=swap');
        
        /* Hide Streamlit Clutter completely */
        #MainMenu {{visibility: hidden;}}
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .stDeployButton {{display: none;}}

        /* Global Typography & Background */
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
            color: {COLORS["primary"]} !important;
            background-color: {COLORS["background"]} !important;
        }}
        
        /* Headings - Premium Poppins Font */
        h1, h2, h3, .st-emotion-cache-10trblm h1 {{
            font-family: 'Poppins', sans-serif !important;
            color: {COLORS["primary"]} !important;
            letter-spacing: -0.5px;
        }}
        
        /* Clean White Cards */
        .clean-card {{
            background-color: {COLORS["card_bg"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            margin-bottom: 24px;
            transition: box-shadow 0.2s ease;
        }}
        .clean-card:hover {{
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }}
        
        /* Buttons - Rounded & Highly Visible */
        .stButton>button {{
            background-color: {COLORS["primary"]} !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 12px 24px !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }}
        .stButton>button:hover {{
            background-color: {COLORS["secondary"]} !important;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3) !important;
        }}

        /* Typography Utilities */
        .text-muted {{ color: {COLORS["text_muted"]}; font-size: 15px; line-height: 1.6; }}
        .score-huge {{ font-size: 64px; font-weight: 800; font-family: 'Poppins', sans-serif; color: {COLORS["primary"]}; line-height: 1; margin: 10px 0; }}
        
        /* Input Field Overrides for Readability */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
            background-color: #FFFFFF !important;
            border: 1px solid {COLORS["border"]} !important;
            color: {COLORS["primary"]} !important;
            border-radius: 8px !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- REUSABLE HTML COMPONENTS ---

def metric_kpi(title, value, icon, trend=None):
    trend_color = COLORS['success'] if trend == 'up' else COLORS['danger']
    trend_html = f"<span style='color: {trend_color}; font-size: 13px; font-weight: 600; margin-left: 8px;'>{'↑' if trend == 'up' else '↓'}</span>" if trend else ""
    return f"""
    <div class="clean-card" style="padding: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <p style="margin: 0; color: {COLORS['text_muted']}; font-weight: 600; font-size: 13px; text-transform: uppercase;">{title}</p>
            <span style="font-size: 20px;">{icon}</span>
        </div>
        <div style="display: flex; align-items: baseline;">
            <h3 style="margin: 0; font-size: 28px; font-weight: 700;">{value}</h3>
            {trend_html}
        </div>
    </div>
    """

def status_badge(text, status_type):
    color = COLORS.get(status_type, COLORS["primary"])
    return f"<span style='background: {color}15; color: {color}; border: 1px solid {color}30; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; display: inline-block;'>{text}</span>"

def premium_lender_card(lender, type_name, status, rate, prob):
    color = COLORS["success"] if "✅" in status else COLORS["warning"] if "⚠️" in status else COLORS["danger"]
    return f"""
    <div class="clean-card" style="padding: 24px; border-left: 4px solid {color};">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <h3 style="margin: 0; font-size: 20px;">{lender}</h3>
                <span style="background: {COLORS['background']}; padding: 4px 10px; border-radius: 6px; font-size: 12px; color: {COLORS['text_muted']}; border: 1px solid {COLORS['border']};">{type_name}</span>
            </div>
            {status_badge(f"{prob}% Match", "success" if prob > 60 else "warning")}
        </div>
        <div style="display: flex; justify-content: space-between; border-top: 1px solid {COLORS['border']}; padding-top: 16px;">
            <p style="margin: 0; color: {COLORS['text_muted']}; font-size: 14px;">Status: <span style="color: {color}; font-weight: 600;">{status}</span></p>
            <p style="margin: 0; color: {COLORS['text_muted']}; font-size: 14px;">Est. Rate: <span style="color: {COLORS['primary']}; font-weight: 600;">{rate}</span></p>
        </div>
    </div>
    """

def apply_light_theme(fig):
    """Formats Plotly charts to match the clean light UI."""
    fig.update_layout(
        font=dict(family="Inter, sans-serif", color=COLORS["primary"]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
