# scoring.py
import pandas as pd
import numpy as np

def calculate_crs(turnover, vintage, bank_balance, gst_status, emi_amount):
    """
    Calculates the Credit Readiness Score (0-850) based on inputs.
    Weights: Cash Flow (30%), Vintage (15%), GST Compliance (20%), Debt Service (20%), Digital Footprint (15%).
    """
    # 1. Cash Flow Stability (Max 30% -> 255 points)
    # Assessed by Monthly Bank Balance relative to turnover
    monthly_revenue_est = turnover / 12
    cash_flow_ratio = bank_balance / monthly_revenue_est if monthly_revenue_est > 0 else 0
    cash_flow_score = min(255, int((cash_flow_ratio / 0.5) * 255)) # Ideal is maintaining 50% of monthly rev
    
    # 2. Business Vintage (Max 15% -> 127.5 points)
    vintage_score = min(127, int((vintage / 5) * 127)) # Max score at 5+ years
    
    # 3. GST Compliance (Max 20% -> 170 points)
    gst_mapping = {"Regular (Up to date)": 170, "Delayed (< 3 months)": 100, "Irregular": 40, "Not Registered": 0}
    gst_score = gst_mapping.get(gst_status, 0)
    
    # 4. Debt Service (Max 20% -> 170 points)
    # Fixed Obligation to Income Ratio (FOIR)
    foir = emi_amount / monthly_revenue_est if monthly_revenue_est > 0 else 1
    if foir == 0: debt_score = 170
    elif foir <= 0.3: debt_score = 150
    elif foir <= 0.5: debt_score = 100
    elif foir <= 0.7: debt_score = 50
    else: debt_score = 0
        
    # 5. Digital Footprint (Max 15% -> 127.5 points) - Simulated base score for MSMEs
    digital_score = np.random.randint(70, 110) # Mocked since API not available
    
    total_score = cash_flow_score + vintage_score + gst_score + debt_score + digital_score
    total_score = max(0, min(850, total_score)) # Clamp between 0 and 850
    
    components = {
        "Cash Flow Stability": round((cash_flow_score/255)*30, 1),
        "Business Vintage": round((vintage_score/127)*15, 1),
        "GST Compliance": round((gst_score/170)*20, 1),
        "Debt Service": round((debt_score/170)*20, 1),
        "Digital Footprint": round((digital_score/127)*15, 1)
    }
    
    return int(total_score), components

def get_gap_analysis(components, inputs):
    """Generates plain-language insights based on score components."""
    insights = []
    
    if components["Cash Flow Stability"] < 15:
        insights.append(f"⚠️ Your cash flow buffering is low. Maintain at least ₹{int(inputs['turnover']/24):,} in monthly balance to improve stability.")
    if components["Business Vintage"] < 7.5:
        insights.append(f"⏱️ Low business vintage. Lenders prefer 3+ years. Maintain clean records for the next {max(0, 3 - inputs['vintage'])} years.")
    if components["GST Compliance"] < 15:
        insights.append("📄 GST filings are flagged as irregular or delayed. Filing the last 3 returns consistently will boost your score by up to 15%.")
    if components["Debt Service"] < 10:
        insights.append("📉 Your EMI burden relative to revenue is high. Avoid taking new debt until existing EMIs are reduced.")
        
    if not insights:
        insights.append("✅ Excellent profile! Maintain current cash flows and GST compliance.")
        
    return insights

def get_action_plan(components):
    """Generates a 30/60/90 day action plan."""
    plan = []
    if components["GST Compliance"] < 20:
        plan.append({"priority": "High", "timeline": "30 Days", "action": "Reconcile and file all pending GSTR-1 and GSTR-3B."})
    if components["Cash Flow Stability"] < 25:
        plan.append({"priority": "Medium", "timeline": "60 Days", "action": "Route all business transactions through the primary current account to build volume."})
    if components["Debt Service"] < 15:
        plan.append({"priority": "High", "timeline": "90 Days", "action": "Pre-pay high-interest short-term loans to reduce monthly EMI outgo."})
    
    if not plan:
         plan.append({"priority": "Low", "timeline": "Ongoing", "action": "Explore premium credit limits or term loans at negotiated lower interest rates."})
         
    return pd.DataFrame(plan)

def get_eligible_lenders(score, turnover, vintage):
    """Matches MSMEs with mock lenders based on criteria."""
    lenders = [
        {"Lender": "HDFC Bank", "Type": "Bank", "Min Score": 700, "Min Turnover": 5000000, "Min Vintage": 3, "Max Rate": "10.5%"},
        {"Lender": "SBI", "Type": "Bank", "Min Score": 650, "Min Turnover": 2500000, "Min Vintage": 2, "Max Rate": "9.8%"},
        {"Lender": "Bajaj Finserv", "Type": "NBFC", "Min Score": 600, "Min Turnover": 1000000, "Min Vintage": 1, "Max Rate": "14.0%"},
        {"Lender": "Lendingkart", "Type": "Fintech", "Min Score": 550, "Min Turnover": 500000, "Min Vintage": 0.5, "Max Rate": "18.0%"},
        {"Lender": "FlexiLoans", "Type": "Fintech", "Min Score": 500, "Min Turnover": 200000, "Min Vintage": 0.5, "Max Rate": "21.0%"},
    ]
    
    df = pd.DataFrame(lenders)
    
    def check_eligibility(row):
        if score >= row["Min Score"] and turnover >= row["Min Turnover"] and vintage >= row["Min Vintage"]:
            return "✅ Eligible"
        elif score >= row["Min Score"] - 50 and turnover >= row["Min Turnover"] * 0.8:
            return "⚠️ Improve Score"
        else:
            return "❌ Not Eligible"
            
    df["Status"] = df.apply(check_eligibility, axis=1)
    return df
