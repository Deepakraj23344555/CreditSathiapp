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
    """Injects the base premium dark UI with high-contrast text fixes."""
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Hide Clutter */
        #MainMenu {{visibility: hidden;}}
        header {{background: transparent !important; visibility: hidden;}}
        footer {{visibility: hidden;}}
        .stDeployButton {{display: none;}}

        /* Global Background */
        .stApp {{
            background: radial-gradient(circle at 15% 0%, #112A4C 0%, #0B1F3A 40%, #05101F 100%) !important;
            background-attachment: fixed !important;
        }}

        /* =========================================================
           CRITICAL FIXES: FORCING HIGH CONTRAST ON ALL SCREENS
           ========================================================= */
        
        /* 1. Main Screen Text & Markdown */
        html, body, [class*="css"], .stMarkdown p, .stText p, li {{
            font-family: 'Inter', -apple-system, sans-serif !important;
            color: #FFFFFF !important;
        }}

        /* 2. Headings */
        h1, h2, h3, h4, h5, h6, .st-emotion-cache-10trblm h1 {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }}

        /* 3. BULLETPROOF INPUT LABELS (Fixes form headers) */
        div[data-testid="stWidgetLabel"] p, 
        div[data-testid="stWidgetLabel"] span,
        label p, 
        label span,
        .stRadio label p, 
        .stCheckbox label p,
        .stSlider label p {{
            color: #CBD5F5 !important; 
            font-weight: 600 !important;
            font-size: 14px !important;
            letter-spacing: 0.3px !important;
            opacity: 1 !important;
            visibility: visible !important;
        }}

        /* 4. Streamlit TABS */
        button[data-baseweb="tab"] {{
            background-color: transparent !important;
        }}
        button[data-baseweb="tab"] p {{
            color: #94A3B8 !important; 
            font-weight: 500 !important;
            font-size: 16px !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] p {{
            color: #14B8A6 !important; 
            font-weight: 700 !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            border-bottom: 2px solid #14B8A6 !important;
        }}

        /* 5. Dataframes & Tables */
        .stDataFrame, .stTable {{
            color: #FFFFFF !important;
        }}
        [data-testid="stDataFrame"] div {{
            background-color: transparent !important;
            color: #FFFFFF !important;
        }}

        /* 6. Sidebar Full Contrast Override */
        [data-testid="stSidebar"] {{
            background-color: rgba(5, 16, 31, 0.85) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid {COLORS["border"]} !important;
        }}
        [data-testid="stSidebar"] * {{
            color: #F8FAFC !important; 
        }}
        div[role="radiogroup"] label p {{
            color: #FFFFFF !important;
            font-size: 15px !important;
            font-weight: 500 !important;
        }}
        
        /* 🌟 NEW CRITICAL FIX: SIDEBAR WHITE BOX TEXT FIX 🌟 */
        /* Forces text inside the white selectbox/inputs in the sidebar to be dark navy */
        [data-testid="stSidebar"] div[data-baseweb="select"] *,
        [data-testid="stSidebar"] .stTextInput input,
        [data-testid="stSidebar"] .stNumberInput input {{
            color: #0B1F3A !important;
        }}
        /* ========================================================= */
        
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

        /* CRITICAL FIX: TEXT INSIDE WHITE INPUT BOXES */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
            background-color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important; 
            color: #0B1F3A !important; 
            border-radius: 10px !important;
            font-weight: 500 !important;
        }}
        .stSelectbox div[data-baseweb="select"] span {{ color: #0B1F3A !important; }}
        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {{
            border-color: #14B8A6 !important;
            box-shadow: 0 0 0 1px #14B8A6 !important;
        }}
        li[role="option"], li[role="option"] span {{
            color: #0B1F3A !important; 
            background-color: #FFFFFF !important;
        }}
        ::placeholder {{ color: #94A3B8 !important; opacity: 1 !important; }}
        .stSlider div[data-testid="stThumbValue"] {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 14px !important;
        }}

        /* Custom Typography Classes */
        .text-muted {{ color: {COLORS["text_muted"]} !important; font-size: 14px; line-height: 1.6; font-weight: 400; }}
        .text-secondary {{ color: {COLORS["secondary"]} !important; line-height: 1.6; }}
        .score-huge {{ font-size: 64px; font-weight: 800; color: #FFFFFF; line-height: 1; margin: 10px 0; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def inject_global_language_css(lang):
    """Dynamically loads fonts and handles RTL layouts for global languages."""
    css = ""
    
    if lang == "ar":
        # Arabic RTL + Noto Sans Arabic Font
        css += """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;500;600;700&display=swap');
            html, body, [class*="css"], .stMarkdown p, .stText p, label, button, input {
                font-family: 'Noto Sans Arabic', sans-serif !important;
                direction: rtl !important;
                text-align: right !important;
            }
            /* Flip the sidebar for Arabic */
            [data-testid="stSidebar"] {
                direction: rtl !important;
            }
            /* Fix slider directions */
            .stSlider { direction: ltr !important; }
        </style>
        """
    elif lang == "hi":
        # Hindi + Noto Sans Devanagari Font
        css += """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');
            html, body, [class*="css"], .stMarkdown p, .stText p, label, button {
                font-family: 'Noto Sans Devanagari', 'Inter', sans-serif !important;
            }
        </style>
        """
    else:
        # Standard LTR (English, Spanish, French)
        css += """
        <style>
            html, body, [class*="css"] {
                direction: ltr !important;
                text-align: left !important;
            }
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

def hex_to_rgba(hex_code, alpha):
    """Converts hex color to rgba for Plotly transparency."""
    hex_code = hex_code.lstrip('#')
    r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r},{g},{b},{alpha})'

def create_gauge_chart(score):
    """Generates the premium dark-themed gauge chart."""
    if score < 500: color = COLORS["danger"]
    elif score < 650: color = COLORS["warning"]
    elif score < 750: color = COLORS["accent"]
    else: color = COLORS["success"]

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 850], 'tickwidth': 1, 'tickcolor': "rgba(255,255,255,0.2)"},
            'bar': {'color': color, 'thickness': 0.85},
            'bgcolor': "rgba(255,255,255,0.05)", 
            'borderwidth': 0,
            'steps': [
                {'range': [0, 500], 'color': hex_to_rgba(COLORS["danger"], 0.1)},
                {'range': [500, 650], 'color': hex_to_rgba(COLORS["warning"], 0.1)},
                {'range': [650, 750], 'color': hex_to_rgba(COLORS["accent"], 0.1)},
                {'range': [750, 850], 'color': hex_to_rgba(COLORS["success"], 0.1)}],
            'threshold': {'line': {'color': "#FFFFFF", 'width': 4}, 'thickness': 0.85, 'value': score}}))
    
    fig.update_layout(height=300)
    return fig
