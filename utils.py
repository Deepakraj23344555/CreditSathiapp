# utils.py
import streamlit as st
import pandas as pd

def inject_custom_css():
    """Injects premium fintech CSS styling, optimized for Streamlit's light theme."""
    st.markdown("""
    <style>
        /* Global typography and link adjustments */
        a {
            color: #1E3A8A !important;
            text-decoration: none;
        }
        
        /* Premium Card Styling */
        .metric-card {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #E2E8F0;
            text-align: center;
            margin-bottom: 20px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
        }
        
        .metric-value {
            font-size: 38px;
            font-weight: 800;
            color: #0B1F3A;
            margin: 12px 0;
            font-family: 'Inter', sans-serif;
        }
        
        .metric-label {
            font-size: 13px;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
        }

        /* Status Badges */
        .badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }
        .badge-excellent { background: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }
        .badge-good { background: #E0F2FE; color: #075985; border: 1px solid #BAE6FD; }
        .badge-moderate { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
        .badge-high-risk { background: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }

        /* Custom Button Override */
        .stButton>button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-1px);
        }
        
        /* Ensure DataFrame headers look premium */
        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def get_lender_db():
    return pd.DataFrame({
        "Lender Name": ["HDFC Bank", "SBI", "Bajaj Finserv", "LendingKart", "KreditBee MSME", "ICICI Bank"],
        "Type": ["Bank", "PSU Bank", "NBFC", "Digital NBFC", "Digital NBFC", "Bank"],
        "Min Score Required": [720, 700, 650, 550, 500, 710],
        "Min Turnover (₹ Lakhs)": [50, 40, 20, 10, 5, 50],
        "Min Vintage (Years)": [3, 3, 2, 1, 0.5, 3],
        "Interest Rate (%)": ["10.5 - 14", "9.5 - 12", "14 - 18", "18 - 24", "20 - 28", "10 - 13"]
    })

def get_ca_clients():
    return pd.DataFrame({
        "Client Name": ["Sharma Traders", "Verma Electronics", "Gupta Textiles", "Rao Manufacturing", "Singh Logistics"],
        "Industry": ["Retail", "Electronics", "Textiles", "Manufacturing", "Logistics"],
        "Current CRS": [740, 610, 480, 810, 690],
        "Status": ["Ready for Loan", "Needs Improvement", "High Risk", "Excellent", "Good"],
        "Last Updated": ["2023-10-25", "2023-10-24", "2023-10-20", "2023-10-26", "2023-10-21"]
    })
