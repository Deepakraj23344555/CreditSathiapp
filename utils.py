import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

COLORS = {
    "primary": "#0B1F3A", "secondary": "#1E3A8A", "accent": "#14B8A6",
    "background": "#F8FAFC", "success": "#22C55E", "warning": "#F59E0B",
    "danger": "#EF4444", "text": "#1E293B", "surface": "rgba(255, 255, 255, 0.95)"
}

# --- Translations ---
TRANSLATIONS = {
    "EN": {
        "nav_home": "🏠 Home", "nav_assess": "👤 Start Assessment", "nav_dash": "📊 Dashboard",
        "nav_gap": "📋 Gap Analysis & Plan", "nav_lenders": "🏦 Lenders", "nav_sim": "🧪 What-If Simulator",
        "nav_ai": "🤖 AI Advisor", "trust_msg": "🔒 Bank-grade 256-bit encryption. RBI Compliant Data Security."
    },
    "HI": {
        "nav_home": "🏠 होम", "nav_assess": "👤 मूल्यांकन शुरू करें", "nav_dash": "📊 डैशबोर्ड",
        "nav_gap": "📋 गैप विश्लेषण", "nav_lenders": "🏦 ऋणदाता (Lenders)", "nav_sim": "🧪 सिमुलेटर",
        "nav_ai": "🤖 एआई सलाहकार", "trust_msg": "🔒 बैंक-ग्रेड 256-बिट एन्क्रिप्शन। RBI अनुपालन डेटा सुरक्षा।"
    }
}

def t(key):
    lang = st.session_state.get('lang', 'EN')
    return TRANSLATIONS[lang].get(key, key)

def hex_to_rgba(hex_code, alpha):
    hex_code = hex_code.lstrip('#')
    r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r},{g},{b},{alpha})'

def inject_custom_css():
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        html, body, [class*="css"]  {{ font-family: 'Inter', sans-serif; }}
        .stApp {{ background-color: {COLORS["background"]}; }}
        .fintech-card {{ background: {COLORS["surface"]}; backdrop-filter: blur(10px); border-radius: 16px; padding: 24px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.05); transition: transform 0.2s ease; }}
        .fintech-card:hover {{ transform: translateY(-2px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.08); }}
        .card-top-accent {{ border-top: 4px solid {COLORS["secondary"]}; }}
        .score-display {{ font-size: 56px; font-weight: 800; color: {COLORS["primary"]}; text-align: center; line-height: 1.1; margin: 10px 0; }}
        .stButton>button {{ background-color: {COLORS["accent"]}; color: white; border-radius: 50px; font-weight: 600; box-shadow: 0 4px 12px {COLORS["accent"]}40; }}
        .badge {{ padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 13px; display: inline-block; }}
        .badge-success {{ background-color: {COLORS["success"]}15; color: {COLORS["success"]}; }}
        .badge-warning {{ background-color: {COLORS["warning"]}15; color: {COLORS["warning"]}; }}
        .badge-danger {{ background-color: {COLORS["danger"]}15; color: {COLORS["danger"]}; }}
        .trust-layer {{ text-align: center; font-size: 12px; color: #64748B; padding: 20px; border-top: 1px solid #E2E8F0; margin-top: 40px; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_metric_card(title, value, icon="📊", trend=None):
    trend_html = f"<span style='color: {'#22C55E' if trend == 'up' else '#EF4444'}; font-size: 12px;'>{'↑' if trend == 'up' else '↓'}</span>" if trend else ""
    st.markdown(f"""
    <div class="fintech-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <p style="margin: 0; color: #64748B; font-weight: 600; font-size: 14px;">{title}</p>
            <span style="font-size: 20px;">{icon}</span>
        </div>
        <h3 style="margin: 10px 0 0 0; font-size: 24px;">{value} {trend_html}</h3>
    </div>
    """, unsafe_allow_html=True)

def render_lender_tile(lender, lender_type, status, rate, border_color, prob, loan_range):
    st.markdown(f"""
    <div class="fintech-card" style="border-left: 5px solid {border_color}; padding: 16px 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h4 style="margin: 0 0 8px 0;">{lender} <span style="font-size: 13px; color: #64748B; font-weight: 400; background: #F1F5F9; padding: 2px 8px; border-radius: 12px;">{lender_type}</span></h4>
            <span class="badge" style="background: {border_color}15; color: {border_color};">Approval: {prob}%</span>
        </div>
        <div style="display: flex; justify-content: space-between; border-top: 1px solid #E2E8F0; padding-top: 12px; margin-top: 8px;">
            <p style="margin: 0; font-size: 14px; color: #64748B;">Eligibility: <strong>{loan_range}</strong></p>
            <p style="margin: 0; color: #64748B; font-size: 14px;">Est. Rate: <strong>{rate}</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_trust_layer():
    st.markdown(f"<div class='trust-layer'>{t('trust_msg')}</div>", unsafe_allow_html=True)
    
# Plotly Charts (Reused from previous, ensuring Base Layout logic applies)
def _base_layout(fig):
    fig.update_layout(font=dict(family="Inter", color=COLORS["text"]), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_gauge_chart(score):
    if score < 500: color = COLORS["danger"]
    elif score < 650: color = COLORS["warning"]
    elif score < 750: color = COLORS["accent"]
    else: color = COLORS["success"]
    fig = go.Figure(go.Indicator(mode = "gauge+number", value = score, domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [0, 850], 'tickwidth': 1, 'tickcolor': "#CBD5E1"}, 'bar': {'color': color, 'thickness': 0.85},
                 'steps': [{'range': [0, 500], 'color': hex_to_rgba(COLORS["danger"], 0.1)}, {'range': [750, 850], 'color': hex_to_rgba(COLORS["success"], 0.1)}],
                 'threshold': {'line': {'color': COLORS["primary"], 'width': 4}, 'thickness': 0.85, 'value': score}}))
    fig.update_layout(height=300)
    return _base_layout(fig)
