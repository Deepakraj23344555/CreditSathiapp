import streamlit as st
import pandas as pd

def inject_custom_css():
    """Injects premium fintech CSS styling."""
    st.markdown("""
    <style>
        /* Color Palette */
        :root {
            --primary: #0B1F3A;
            --secondary: #1E3A8A;
            --accent: #14B8A6;
            --bg: #F8FAFC;
            --success: #22C55E;
            --warning: #F59E0B;
            --danger: #EF4444;
            --text-dark: #1E293B;
            --text-muted: #64748B;
        }

        /* Global App Styling */
        .stApp {
            background-color: var(--bg);
        }
        
        h1, h2, h3 {
            color: var(--primary) !important;
            font-family: 'Inter', sans-serif;
        }

        /* Card Styling */
        .metric-card {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid rgba(0,0,0,0.05);
            text-align: center;
            margin-bottom: 20px;
        }
        
        .metric-value {
            font-size: 36px;
            font-weight: 700;
            color: var(--secondary);
            margin: 10px 0;
        }
        
        .metric-label {
            font-size: 14px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Status Badges */
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 14px;
            font-weight: 600;
        }
        .badge-excellent { background: #DCFCE7; color: var(--success); }
        .badge-good { background: #E0F2FE; color: var(--secondary); }
        .badge-moderate { background: #FEF3C7; color: var(--warning); }
        .badge-high-risk { background: #FEE2E2; color: var(--danger); }

        /* Custom Button */
        .stButton>button {
            background-color: var(--primary);
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: var(--accent);
            box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3);
            color: white;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: white;
            border-right: 1px solid rgba(0,0,0,0.05);
        }
    </style>
    """, unsafe_allow_html=True)

def get_lender_db():
    """Returns mock lender dataset."""
    return pd.DataFrame({
        "Lender Name": ["HDFC Bank", "SBI", "Bajaj Finserv", "LendingKart", "KreditBee MSME", "ICICI Bank"],
        "Type": ["Bank", "PSU Bank", "NBFC", "Digital NBFC", "Digital NBFC", "Bank"],
        "Min Score Required": [720, 700, 650, 550, 500, 710],
        "Min Turnover (₹ Lakhs)": [50, 40, 20, 10, 5, 50],
        "Min Vintage (Years)": [3, 3, 2, 1, 0.5, 3],
        "Interest Rate (%)": ["10.5 - 14", "9.5 - 12", "14 - 18", "18 - 24", "20 - 28", "10 - 13"]
    })

def get_ca_clients():
    """Returns mock CA client dataset."""
    return pd.DataFrame({
        "Client Name": ["Sharma Traders", "Verma Electronics", "Gupta Textiles", "Rao Manufacturing", "Singh Logistics"],
        "Industry": ["Retail", "Electronics", "Textiles", "Manufacturing", "Logistics"],
        "Current CRS": [740, 610, 480, 810, 690],
        "Status": ["Ready for Loan", "Needs Improvement", "High Risk", "Excellent", "Good"],
        "Last Updated": ["2023-10-25", "2023-10-24", "2023-10-20", "2023-10-26", "2023-10-21"]
    })
