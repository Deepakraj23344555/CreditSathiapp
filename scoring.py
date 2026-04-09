import numpy as np

def calculate_crs(turnover, vintage, bank_balance, loan_history, gst_status, emi_amount):
    """
    Core scoring engine for Credit Readiness Score (0-850).
    Factors: Cash Flow (30%), Vintage (15%), GST (20%), Debt (20%), Digital (15%)
    """
    score = 300 # Base minimum score
    factors = {"Cash Flow": 0, "Vintage": 0, "GST Compliance": 0, "Debt Service": 0, "Digital Footprint": 0}
    
    # 1. Cash Flow Stability (30% -> max 165 points)
    if bank_balance > 500000:
        factors["Cash Flow"] = 165
    elif bank_balance > 100000:
        factors["Cash Flow"] = 120
    elif bank_balance > 25000:
        factors["Cash Flow"] = 70
    else:
        factors["Cash Flow"] = 20

    # 2. Business Vintage (15% -> max 82.5 points)
    if vintage >= 5:
        factors["Vintage"] = 82
    elif vintage >= 2:
        factors["Vintage"] = 50
    elif vintage >= 1:
        factors["Vintage"] = 30
    else:
        factors["Vintage"] = 10

    # 3. GST Compliance (20% -> max 110 points)
    if gst_status == "Regular (Monthly)":
        factors["GST Compliance"] = 110
    elif gst_status == "Quarterly (QRMP)":
        factors["GST Compliance"] = 80
    elif gst_status == "Irregular":
        factors["GST Compliance"] = 30
    else:
        factors["GST Compliance"] = 0

    # 4. Debt Service (20% -> max 110 points)
    monthly_income_est = turnover / 12
    if monthly_income_est > 0:
        foir = emi_amount / monthly_income_est
    else:
        foir = 1.0

    if loan_history == "No":
        factors["Debt Service"] = 60 # No history is neutral
    else:
        if foir < 0.3:
            factors["Debt Service"] = 110
        elif foir < 0.5:
            factors["Debt Service"] = 70
        elif foir < 0.7:
            factors["Debt Service"] = 30
        else:
            factors["Debt Service"] = 0

    # 5. Digital Footprint / Proxy (15% -> max 82.5 points)
    # Simulated based on turnover scale and GST regularity
    if turnover > 5000000 and gst_status == "Regular (Monthly)":
        factors["Digital Footprint"] = 82
    elif turnover > 1000000:
        factors["Digital Footprint"] = 50
    else:
        factors["Digital Footprint"] = 20

    total_score = score + sum(factors.values())
    total_score = min(int(total_score), 850) # Cap at 850
    
    # Categorize
    if total_score >= 750:
        category = "Excellent"
    elif total_score >= 650:
        category = "Good"
    elif total_score >= 500:
        category = "Moderate"
    else:
        category = "High Risk"

    return total_score, category, factors

def generate_insights(factors, category, gst_status, bank_balance, vintage, foir_indicator):
    """Generates plain language gap analysis based on user inputs."""
    gaps = []
    
    if bank_balance < 50000:
        gaps.append("Your cash flow is inconsistent — maintain ₹50,000 minimum monthly average balance to show liquidity.")
    if vintage < 2:
        gaps.append(f"Low business vintage ({vintage} years) — many prime lenders require at least 24 months of operation.")
    if gst_status in ["Not Registered", "Irregular"]:
        gaps.append("GST filings are missing or irregular — regularize filings to prove business continuity and scale.")
    if foir_indicator == 'high':
        gaps.append("High existing EMI burden compared to estimated monthly turnover — reduce debt before applying for new credit.")
    
    if not gaps:
        gaps.append("Strong financial profile. Ensure continuous timely payments to maintain this score.")
        
    return gaps

def generate_action_plan(category, gaps):
    """Generates structured timeline-based recommendations."""
    plan = []
    
    if category == "Excellent":
        plan = [
            {"time": "30 Days", "action": "Negotiate lower interest rates with existing lenders.", "priority": "Low"},
            {"time": "60 Days", "action": "Explore non-collateralized limit enhancements.", "priority": "Medium"}
        ]
    elif category == "Good":
        plan = [
            {"time": "30 Days", "action": "Clear any minor outstanding dues to push score above 750.", "priority": "High"},
            {"time": "90 Days", "action": "Formalize digital payments to improve bank statement volume.", "priority": "Medium"}
        ]
    else:
        plan = [
            {"time": "Immediate", "action": "File pending GST returns (last 3 months).", "priority": "Critical"},
            {"time": "30 Days", "action": "Consolidate small high-interest loans to lower monthly EMI burden.", "priority": "High"},
            {"time": "90 Days", "action": "Route all business transactions through the primary current account.", "priority": "Medium"}
        ]
        
    return plan
