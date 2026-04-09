import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# --- WORLD-CLASS FINTECH COLOR PALETTE ---
COLORS = {
    "bg_dark": "#050B14",       # Deepest background
    "primary": "#0B1F3A",       # Navy
    "secondary": "#1E3A8A",     # Royal Blue
    "accent": "#14B8A6",        # Electric Teal
    "accent_glow": "rgba(20, 184, 166, 0.4)",
    "white_glass": "rgba(255, 255, 255, 0.03)",
    "white_border": "rgba(255, 255, 255, 0.08)",
    "text_main": "#F8FAFC",
    "text_muted": "#94A3B8"
}

def inject_premium_css():
    """Injects Apple/CRED level CSS with Glassmorphism, Animations, and Blobs."""
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
        
        /* Global Reset & Typography */
        html, body, [class*="css"] {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: {COLORS["text_main"]} !important;
            -webkit-font-smoothing: antialiased;
        }}
        
        /* The Gradient Background */
        .stApp {{
            background: radial-gradient(circle at 15% 0%, {COLORS["secondary"]}40 0%, {COLORS["bg_dark"]} 40%, {COLORS["bg_dark"]} 100%) !important;
            background-attachment: fixed;
        }}
        
        /* Hide Streamlit Clutter */
        header {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        
        /* Sidebar Styling (Glass) */
        [data-testid="stSidebar"] {{
            background: rgba(11, 31, 58, 0.4) !important;
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-right: 1px solid {COLORS["white_border"]};
        }}
        [data-testid="stSidebarNav"] span {{ color: {COLORS["text_main"]} !important; font-weight: 500; }}
        
        /* Smooth Fade-In Animation */
        @keyframes slideUpFade {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Glassmorphism Cards */
        .glass-card {{
            background: linear-gradient(145deg, {COLORS["white_glass"]} 0%, rgba(255,255,255,0.01) 100%);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid {COLORS["white_border"]};
            border-radius: 24px;
            padding: 32px;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            position: relative;
            overflow: hidden;
        }}
        
        /* Card Hover Glow Effect */
        .glass-card:hover {{
            transform: translateY(-4px) scale(1.01);
            border-color: rgba(20, 184, 166, 0.3);
            box-shadow: 0 40px 80px rgba(0, 0, 0, 0.5), 0 0 40px {COLORS["accent_glow"]};
        }}
        
        /* Card Inner Blob Accent */
        .glass-card::before {{
            content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
            background: radial-gradient(circle at 50% 0%, {COLORS["accent"]}15 0%, transparent 50%);
            opacity: 0; transition: opacity 0.5s ease; pointer-events: none;
        }}
        .glass-card:hover::before {{ opacity: 1; }}

        /* Premium Headers */
        h1, h2, h3 {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }}
        .hero-title {{
            font-size: 56px; font-weight: 800;
            background: linear-gradient(to right, #FFFFFF, {COLORS["accent"]});
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            line-height: 1.1; margin-bottom: 16px;
        }}
        
        /* Glowing Gradient Buttons */
        .btn-premium {{
            background: linear-gradient(135deg, {COLORS["accent"]} 0%, {COLORS["secondary"]} 100%);
            color: white !important; font-weight: 600; font-size: 16px;
            padding: 14px 32px; border-radius: 50px; border: none;
            cursor: pointer; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 10px 20px {COLORS["accent_glow"]};
            text-decoration: none; display: inline-block;
        }}
        .btn-premium:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 15px 30px rgba(20, 184, 166, 0.6);
        }}
        
        /* Streamlit Native Button Override */
        .stButton>button {{
            background: linear-gradient(135deg, {COLORS["accent"]} 0%, {COLORS["secondary"]} 100%) !important;
            color: white !important; border-radius: 50px !important; border: none !important;
            padding: 10px 24px !important; font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }}
        .stButton>button:hover {{
            box-shadow: 0 0 20px {COLORS["accent_glow"]} !important;
            transform: scale(1.02) !important;
        }}

        /* Typography Utilities */
        .text-muted {{ color: {COLORS["text_muted"]}; font-size: 15px; line-height: 1.6; }}
        .score-huge {{ font-size: 72px; font-weight: 800; color: white; line-height: 1; margin: 10px 0; }}
        
        /* Input Overrides for Dark Theme */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: white !important; border-radius: 12px !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- REUSABLE HTML COMPONENTS ---

def metric_kpi(title, value, icon, trend=None):
    """Renders an Apple-style KPI card."""
    trend_html = f"<span style='color: {COLORS['accent']}; font-size: 13px; font-weight: 600; background: rgba(20, 184, 166, 0.1); padding: 4px 8px; border-radius: 12px; margin-left: 10px;'>{'↑' if trend == 'up' else '↓'} Trend</span>" if trend else ""
    return f"""
    <div class="glass-card" style="padding: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <p style="margin: 0; color: {COLORS['text_muted']}; font-weight: 500; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">{title}</p>
            <span style="font-size: 24px; opacity: 0.8;">{icon}</span>
        </div>
        <div style="display: flex; align-items: baseline;">
            <h3 style="margin: 0; font-size: 32px; font-weight: 700;">{value}</h3>
            {trend_html}
        </div>
    </div>
    """

def glass_badge(text, color_hex):
    """Generates a glowing pill badge."""
    return f"<span style='background: {color_hex}20; color: {color_hex}; border: 1px solid {color_hex}40; padding: 6px 16px; border-radius: 30px; font-size: 13px; font-weight: 600; display: inline-block; box-shadow: 0 0 10px {color_hex}20;'>{text}</span>"

def premium_lender_card(lender, type_name, status, rate, prob):
    """Renders a high-end lender tile."""
    color = COLORS["accent"] if "✅" in status else "#F59E0B" if "⚠️" in status else "#EF4444"
    return f"""
    <div class="glass-card" style="padding: 24px; margin-bottom: 16px; border-left: 4px solid {color};">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <h3 style="margin: 0; font-size: 22px;">{lender}</h3>
                <span style="background: rgba(255,255,255,0.1); padding: 4px 10px; border-radius: 8px; font-size: 12px; color: {COLORS['text_muted']};">{type_name}</span>
            </div>
            {glass_badge(f"{prob}% Match", color)}
        </div>
        <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 16px;">
            <p style="margin: 0; color: {COLORS['text_muted']};">Status: <span style="color: {color}; font-weight: 600;">{status}</span></p>
            <p style="margin: 0; color: {COLORS['text_muted']};">Est. Rate: <span style="color: white; font-weight: 600;">{rate}</span></p>
        </div>
    </div>
    """

# --- PLOTLY DARK MODE OVERRIDES ---

def apply_dark_theme(fig):
    """Modifies existing Plotly charts to fit the glassmorphism dark theme."""
    fig.update_layout(
        font=dict(family="SF Pro Display, Inter, sans-serif", color=COLORS["text_muted"]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        hoverlabel=dict(bgcolor=COLORS["primary"], font_size=14, font_family="SF Pro Display", bordercolor=COLORS["accent"])
    )
    return fig
