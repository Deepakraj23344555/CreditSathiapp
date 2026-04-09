# scoring.py
import numpy as np
import streamlit as st

@st.cache_data(show_spinner=False)
def calculate_crs(turnover, vintage, bank_balance, loan_history, gst_status, emi_amount):
    """
    Core scoring engine for Credit Readiness Score (0-850).
    Cached to optimize performance during re-runs.
    """
    score = 300 
    factors = {"Cash Flow": 0, "Vintage": 0, "GST Compliance": 0, "Debt Service": 0, "Digital Footprint": 0}
    
    if bank_balance > 500000: factors["Cash Flow"] = 165
    elif bank_balance > 100000: factors["Cash Flow"] = 120
    elif bank_balance > 25000: factors["Cash Flow"] = 70
    else: factors["Cash Flow"] = 20

    if vintage >= 5: factors["Vintage"] = 82
    elif vintage >= 2: factors["Vintage"] = 50
    elif vintage >= 1: factors["Vintage"] = 30
    else: factors["Vintage"] = 10

    if gst_status == "Regular (Monthly)": factors["GST Compliance"] = 110
    elif gst_status == "Quarterly (QRMP)": factors["GST Compliance"] = 80
    elif gst_status == "Irregular": factors["GST Compliance"] = 30
    else: factors["GST Compliance"] = 0

    monthly_income_est = turnover / 12 if turnover > 0 else 1
    foir = emi_amount / monthly_income_est

    if loan_history == "No": factors["Debt Service"] = 60 
    else:
        if foir < 0.3: factors["Debt Service"] = 110
        elif foir < 0.5: factors["Debt Service"] = 70
        elif foir < 0.7: factors["Debt Service"] = 30
        else: factors["Debt Service"] = 0

    if turnover > 5000000 and gst_status == "Regular (Monthly)": factors["Digital Footprint"] = 82
    elif turnover > 1000000: factors["Digital Footprint"] = 50
    else: factors["Digital Footprint"] = 20

    total_score = min(int(score + sum(factors.values())), 850)
    
    if total_score >= 750: category = "Excellent"
    elif total_score >= 650: category = "Good"
    elif total_score >= 500: category = "Moderate"
    else: category = "High Risk"

    return total_score, category, factors

@st.cache_data(show_spinner=False)
def generate_insights(factors, category, gst_status, bank_balance, vintage, foir_indicator):
    """Generates plain language gap analysis, cached for performance."""
    gaps = []
    if bank_balance < 50000: gaps.append("Your cash flow is inconsistent — maintain ₹50,000 minimum monthly average balance.")
    if vintage < 2: gaps.append(f"Low business vintage ({vintage} years) — many prime lenders require at least 24 months.")
    if gst_status in ["Not Registered", "Irregular"]: gaps.append("GST filings are missing/irregular — regularize filings for business continuity.")
    if foir_indicator == 'high': gaps.append("High existing EMI burden compared to turnover — reduce debt before applying for credit.")
    if not gaps: gaps.append("Strong financial profile. Ensure continuous timely payments to maintain this score.")
    return gaps

@st.cache_data(show_spinner=False)
def generate_action_plan(category, gaps):
    """Generates structured timeline-based recommendations."""
    if category == "Excellent":
        return [
            {"time": "30 Days", "action": "Negotiate lower interest rates with existing lenders.", "priority": "Low"},
            {"time": "60 Days", "action": "Explore non-collateralized limit enhancements.", "priority": "Medium"}
        ]
    elif category == "Good":
        return [
            {"time": "30 Days", "action": "Clear minor outstanding dues to push score above 750.", "priority": "High"},
            {"time": "90 Days", "action": "Formalize digital payments to improve statement volume.", "priority": "Medium"}
        ]
    else:
        return [
            {"time": "Immediate", "action": "File pending GST returns (last 3 months).", "priority": "Critical"},
            {"time": "30 Days", "action": "Consolidate high-interest loans to lower EMI burden.", "priority": "High"},
            {"time": "90 Days", "action": "Route all transactions through the primary current account.", "priority": "Medium"}
        ]
