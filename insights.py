def get_behavioral_insights(components):
    insights = []
    if components["Cash Flow Stability"] < 15:
        insights.append("📉 **Irregular Inflows:** Lenders view your cash flow as inconsistent, raising default risk flags.")
    if components["Debt Service"] < 10:
        insights.append("⚠️ **High Debt Burden:** Your EMI-to-Revenue ratio is critical. Lenders will hesitate to add more debt.")
    if components["GST Compliance"] < 15:
        insights.append("📄 **Compliance Gaps:** Missing GST filings signals poor governance to institutional banks.")
    if not insights:
        insights.append("🌟 **Stellar Profile:** You demonstrate high financial discipline. Prime lenders will compete for your business.")
    return insights

def generate_storytelling(score, inputs):
    if score >= 700:
        return f"**{inputs.get('name', 'Your business')}** is operating with high financial discipline. With an annual turnover of ₹{inputs.get('turnover',0):,} and a solid vintage of {inputs.get('vintage',0)} years, you have established strong trust. Lenders see you as a low-risk, prime borrower."
    elif score >= 600:
        return f"**{inputs.get('name', 'Your business')}** is growing steadily. While your turnover is healthy, optimizing your bank balances and managing existing EMIs will push you into the premium borrower tier."
    else:
        return f"**{inputs.get('name', 'Your business')}** is currently in a high-risk category. Consolidating existing EMIs and ensuring 100% GST compliance over the next 3-6 months is essential to unlock institutional credit."
