# utils.py
import streamlit as st
import pandas as pd

def inject_custom_css():
    """Injects premium fintech CSS styling (Glassmorphism, Soft Shadows, Modern Typography)."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Global App Styling */
        .stApp {
            background-color: #F8FAFC;
            font-family: 'Inter', sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #0B1F3A !important;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
        }

        /* Glassmorphism & Card UI */
        .glass-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
            border: 1px solid rgba(226, 232, 240, 0.8);
            margin-bottom: 24px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }

        /* KPI / Metric Cards */
        .metric-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        
        .metric-value {
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(135deg, #0B1F3A 0%, #1E3A8A 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 8px 0;
            line-height: 1.2;
        }
        
        .metric-label {
            font-size: 13px;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }

        /* Reusable Badges */
        .score-badge {
            display: inline-flex;
            align-items: center;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.3px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        /* Custom Button Override - Rounded & Hover Effects */
        .stButton>button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.5rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: none !important;
        }
        
        .stButton>button[kind="primary"] {
            background: linear-gradient(135deg, #0B1F3A 0%, #1E3A8A 100%) !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3) !important;
        }

        .stButton>button[kind="primary"]:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 20px rgba(30, 58, 138, 0.4) !important;
            background: linear-gradient(135deg, #1E3A8A 0%, #0B1F3A 100%) !important;
        }

        .stButton>button[kind="secondary"]:hover {
            background-color: #F1F5F9 !important;
            border-color: #CBD5E1 !important;
            transform: translateY(-1px);
        }

        /* Progress Bar Enhancements */
        .stProgress > div > div > div > div {
            background-color: #14B8A6;
            border-radius: 10px;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
            box-shadow: 4px 0 15px rgba(0,0,0,0.02);
        }
        
        /* Footer */
        .app-footer {
            text-align: center;
            padding: 24px;
            color: #94A3B8;
            font-size: 13px;
            font-weight: 500;
            border-top: 1px solid #E2E8F0;
            margin-top: 40px;
        }
    </style>
    """, unsafe_allow_html=True)

# --- REUSABLE UI COMPONENTS ---

def card_component(label, value, badge_text=None, badge_color="#F1F5F9", text_color="#475569"):
    """Generates a reusable, styled KPI card."""
    badge_html = f'<div class="score-badge" style="background: {badge_color}; color: {text_color}; border: 1px solid rgba(0,0,0,0.05); margin-top: 8px;">{badge_text}</div>' if badge_text else ''
    return f"""
    <div class="glass-card metric-container">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {badge_html}
    </div>
    """

def score_badge(category):
    """Returns CSS colored badge based on category."""
    colors = {
        "Excellent": ("#DCFCE7", "#166534", "✅"),
        "Good": ("#E0F2FE", "#075985", "📈"),
        "Moderate": ("#FEF3C7", "#92400E", "⚠️"),
        "High Risk": ("#FEE2E2", "#991B1B", "🛑")
    }
    bg, fg, icon = colors.get(category, ("#F1F5F9", "#475569", "▪️"))
    return f'<span class="score-badge" style="background: {bg}; color: {fg}; border: 1px solid rgba(0,0,0,0.05);">{icon} {category}</span>'

# --- DATA LOADING (CACHED FOR PERFORMANCE) ---

@st.cache_data(ttl=3600)
def get_lender_db():
    """Returns mock lender dataset, cached for faster reloads."""
    return pd.DataFrame({
        "Lender Name": ["HDFC Bank", "SBI", "Bajaj Finserv", "LendingKart", "KreditBee MSME", "ICICI Bank"],
        "Type": ["Bank", "PSU Bank", "NBFC", "Digital NBFC", "Digital NBFC", "Bank"],
        "Min Score Required": [720, 700, 650, 550, 500, 710],
        "Min Turnover (₹ Lakhs)": [50, 40, 20, 10, 5, 50],
        "Min Vintage (Years)": [3, 3, 2, 1, 0.5, 3],
        "Interest Rate (%)": ["10.5 - 14", "9.5 - 12", "14 - 18", "18 - 24", "20 - 28", "10 - 13"]
    })

@st.cache_data(ttl=3600)
def get_ca_clients():
    """Returns mock CA client dataset, cached."""
    return pd.DataFrame({
        "Client Name": ["Sharma Traders", "Verma Electronics", "Gupta Textiles", "Rao Manufacturing", "Singh Logistics"],
        "Industry": ["Retail", "Electronics", "Textiles", "Manufacturing", "Logistics"],
        "Current CRS": [740, 610, 480, 810, 690],
        "Status": ["Ready for Loan", "Needs Improvement", "High Risk", "Excellent", "Good"],
        "Last Updated": ["2023-10-25", "2023-10-24", "2023-10-20", "2023-10-26", "2023-10-21"]
    })
