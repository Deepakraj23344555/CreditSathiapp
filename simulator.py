import streamlit as st
from scoring import calculate_crs

def render_simulator():
    st.title("🧪 What-If Simulator")
    st.markdown("Adjust parameters to see how financial decisions impact your Credit Readiness Score.")
    
    curr = st.session_state.user_inputs
    current_score = st.session_state.crs_score
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Simulate Changes")
        
        # 1. SAFE BANK BALANCE SLIDER
        min_bal = int(curr['bank_balance'])
        # Ensure max_value is always at least min_value + step to prevent crashes
        max_bal = max(min_bal + 10000, int(curr['turnover'] / 2))
        new_bal = st.slider("Increase Avg Monthly Balance", min_bal, max_bal, min_bal, step=10000)
        
        # 2. SAFE EMI SLIDER
        curr_emi = int(curr['emi_amount'])
        if curr_emi > 0:
            # Ensure the step isn't larger than the actual EMI amount
            step_val = min(5000, curr_emi) 
            new_emi = st.slider("Reduce Monthly EMIs", 0, curr_emi, curr_emi, step=step_val)
        else:
            new_emi = 0
            st.markdown("<p style='color: #64748B; font-size: 14px; margin-top: 20px; margin-bottom: 20px;'>✅ No existing EMIs to reduce.</p>", unsafe_allow_html=True)
            
        # 3. GST DROPDOWN
        new_gst = st.selectbox("Improve GST Status", ["Regular (Up to date)", "Delayed (< 3 months)"], index=0 if curr['gst_status'] == "Regular (Up to date)" else 1)
        
    with col2:
        new_score, _ = calculate_crs(curr['turnover'], curr['vintage'], new_bal, new_gst, new_emi)
        delta = new_score - current_score
        
        st.markdown("### Projected Outcome")
        color = "#22C55E" if delta > 0 else "#64748B"
        
        st.markdown(f"""
        <div class="fintech-card" style="text-align: center; border: 2px solid {color};">
            <h2 style="margin:0; color: #0B1F3A;">{new_score}</h2>
            <p style="color: {color}; font-weight: bold; font-size: 18px;">{'+' if delta > 0 else ''}{delta} Points</p>
            <p style="color: #64748B; font-size: 14px;">If you maintain these metrics for 90 days.</p>
        </div>
        """, unsafe_allow_html=True)
