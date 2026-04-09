import streamlit as st
import plotly.graph_objects as go

# --- DARK PREMIUM FINTECH PALETTE ---
COLORS = {
    "background": "#0B1F3A",      
    "card_bg": "rgba(17, 42, 76, 0.45)", 
    "primary": "#FFFFFF",         
    "secondary": "#CBD5F5",       
    "accent": "#14B8A6",          
    "border": "rgba(255, 255, 255, 0.08)",          
    "text_muted": "#94A3B8",      
    "success": "#059669",
    "warning": "#D97706",
    "danger": "#DC2626"
}

def inject_premium_dark_theme():
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Hide Clutter */
        #MainMenu {{visibility: hidden;}}
        header {{background: transparent !important; visibility: hidden;}}
        footer {{visibility: hidden;}}
        .stDeployButton {{display: none;}}

        /* Global Typography & Background */
        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, sans-serif !important;
            color: #FFFFFF !important;
        }}
        
        .stApp {{
            background: radial-gradient(circle at 15% 0%, #112A4C 0%, #0B1F3A 40%, #05101F 100%) !important;
            background-attachment: fixed !important;
        }}

        /* Headings */
        h1, h2, h3, h4, .st-emotion-cache-10trblm h1 {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }}

        /* --- CRITICAL FIX: SIDEBAR CONTRAST --- */
        /* Force all text inside the sidebar to be a readable light color */
        [data-testid="stSidebar"] {{
            background-color: rgba(5, 16, 31, 0.85) !important; /* Slightly darker for better base contrast */
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid {COLORS["border"]} !important;
        }}
        
        /* Brute-force white text for everything in the sidebar */
        [data-testid="stSidebar"] * {{
            color: #F8FAFC !important; 
        }}
        
        /* Specifically target Streamlit Radio Buttons to ensure text is white */
        div[role="radiogroup"] label p {{
            color: #FFFFFF !important;
            font-size: 15px !important;
            font-weight: 500 !important;
        }}
        /* -------------------------------------- */
        
        /* Premium Glass Cards */
        .premium-card {{
            background: {COLORS["card_bg"]};
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid {COLORS["border"]};
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
            margin-bottom: 24px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }}
        .premium-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(20, 184, 166, 0.3);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25), 0 0 20px rgba(20, 184, 166, 0.1);
        }}
        
        /* Glowing Buttons */
        .stButton>button {{
            background: linear-gradient(135deg, #1E3A8A 0%, #14B8A6 100%) !important;
            color: #FFFFFF !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            width: 100%;
            box-shadow: 0 4px 15px rgba(20, 184, 166, 0.2) !important;
        }}
        .stButton>button:hover {{
            box-shadow: 0 8px 25px rgba(20, 184, 166, 0.4) !important;
            transform: translateY(-2px) scale(1.01) !important;
        }}

        /* Inputs - Increased Brightness for Readability */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important; 
            color: #FFFFFF !important;
            border-radius: 10px !important;
        }}
        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {{
            border-color: #14B8A6 !important;
            box-shadow: 0 0 0 1px #14B8A6 !important;
        }}

        /* Typography */
        .text-muted {{ color: {COLORS["text_muted"]} !important; font-size: 14px; line-height: 1.6; font-weight: 400; }}
        .text-secondary {{ color: {COLORS["secondary"]} !important; line-height: 1.6; }}
        .score-huge {{ font-size: 64px; font-weight: 800; color: #FFFFFF; line-height: 1; margin: 10px 0; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def metric_kpi(title, value, icon, trend=None):
    trend_color = COLORS['accent'] if trend == 'up' else COLORS['danger']
    trend_html = f"<span style='color: {trend_color}; font-size: 13px; font-weight: 600; margin-left: 8px;'>{'↑' if trend == 'up' else '↓'}</span>" if trend else ""
    return f"""
    <div class="premium-card" style="padding: 20px;">
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

def status_badge(text, color_hex):
    return f"<span style='background: {color_hex}20; color: {color_hex}; border: 1px solid {color_hex}40; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; display: inline-block;'>{text}</span>"

def premium_lender_card(lender, type_name, status, rate, prob):
    color = COLORS["accent"] if "✅" in status else COLORS["warning"] if "⚠️" in status else COLORS["danger"]
    return f"""
    <div class="premium-card" style="padding: 24px; border-left: 4px solid {color};">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <h3 style="margin: 0; font-size: 20px;">{lender}</h3>
                <span style="background: rgba(255,255,255,0.05); padding: 4px 10px; border-radius: 6px; font-size: 12px; color: {COLORS['secondary']}; border: 1px solid {COLORS['border']};">{type_name}</span>
            </div>
            {status_badge(f"{prob}% Match", color)}
        </div>
        <div style="display: flex; justify-content: space-between; border-top: 1px solid {COLORS['border']}; padding-top: 16px;">
            <p style="margin: 0; color: {COLORS['text_muted']}; font-size: 14px;">Status: <span style="color: {color}; font-weight: 600;">{status}</span></p>
            <p style="margin: 0; color: {COLORS['text_muted']}; font-size: 14px;">Est. Rate: <span style="color: #FFFFFF; font-weight: 600;">{rate}</span></p>
        </div>
    </div>
    """

def apply_dark_theme(fig):
    fig.update_layout(
        font=dict(family="Inter, sans-serif", color=COLORS["secondary"]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
