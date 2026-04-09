import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def calculate_crs(turnover, vintage, bank_balance, gst_status, emi_amount):
    monthly_revenue_est = turnover / 12
    cash_flow_ratio = bank_balance / monthly_revenue_est if monthly_revenue_est > 0 else 0
    cash_flow_score = min(255, int((cash_flow_ratio / 0.5) * 255))
    vintage_score = min(127, int((vintage / 5) * 127))
    gst_mapping = {"Regular (Up to date)": 170, "Delayed (< 3 months)": 100, "Irregular": 40, "Not Registered": 0}
    gst_score = gst_mapping.get(gst_status, 0)
    foir = emi_amount / monthly_revenue_est if monthly_revenue_est > 0 else 1
    if foir == 0: debt_score = 170
    elif foir <= 0.3: debt_score = 150
    elif foir <= 0.5: debt_score = 100
    elif foir <= 0.7: debt_score = 50
    else: debt_score = 0
    digital_score = np.random.randint(70, 110)
    total_score = max(0, min(850, cash_flow_score + vintage_score + gst_score + debt_score + digital_score))
    components = {
        "Cash Flow Stability": round((cash_flow_score/255)*30, 1), "Business Vintage": round((vintage_score/127)*15, 1),
        "GST Compliance": round((gst_score/170)*20, 1), "Debt Service": round((debt_score/170)*20, 1), "Digital Footprint": round((digital_score/127)*15, 1)
    }
    return int(total_score), components

@st.cache_data
def get_advanced_lenders(score, turnover, vintage):
    lenders = [
        {"Lender": "HDFC Bank", "Type": "Bank", "Min Score": 700, "Min Turnover": 5000000, "Base Rate": 10.5, "Multiplier": 0.2},
        {"Lender": "SBI", "Type": "Bank", "Min Score": 650, "Min Turnover": 2500000, "Base Rate": 9.8, "Multiplier": 0.15},
        {"Lender": "Bajaj Finserv", "Type": "NBFC", "Min Score": 600, "Min Turnover": 1000000, "Base Rate": 14.0, "Multiplier": 0.25},
        {"Lender": "FlexiLoans", "Type": "Fintech", "Min Score": 500, "Min Turnover": 200000, "Base Rate": 18.0, "Multiplier": 0.3},
    ]
    results = []
    for l in lenders:
        if score >= l["Min Score"] and turnover >= l["Min Turnover"]:
            prob = min(98, max(40, int(((score - l["Min Score"]) / 150) * 100) + 40))
            max_loan = min(turnover * l["Multiplier"], 50000000)
            status, color = "✅ Eligible", "#22C55E"
        elif score >= l["Min Score"] - 50:
            prob = np.random.randint(20, 39)
            max_loan = turnover * (l["Multiplier"]/2)
            status, color = "⚠️ Improve Score", "#F59E0B"
        else:
            prob = np.random.randint(1, 15)
            max_loan = 0
            status, color = "❌ Not Eligible", "#EF4444"
        
        results.append({
            "Lender": l["Lender"], "Type": l["Type"], "Status": status, "Color": color,
            "Approval %": prob, "Rate Range": f"{l['Base Rate']}% - {l['Base Rate']+3}%",
            "Loan Range": f"₹{int(max_loan*0.5):,} - ₹{int(max_loan):,}" if max_loan > 0 else "N/A"
        })
    return pd.DataFrame(results)

def get_esg_score(industry):
    """Simulates a Green/Sustainability score based on industry profiles."""
    base = {"Manufacturing": 45, "Retail": 60, "Services": 75, "IT/Tech": 85, "Other": 50}
    return base.get(industry, 50) + np.random.randint(-10, 10)
