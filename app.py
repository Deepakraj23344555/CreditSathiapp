import streamlit as st
import time
import pandas as pd
import plotly.express as px
from utils import inject_custom_css, create_gauge_chart, create_breakdown_pie, create_factor_bar
from utils import render_metric_card, render_score_badge, render_lender_tile
from scoring import calculate_crs, get_gap_analysis, get_action_plan, get_eligible_lenders

# --- APP CONFIG & INIT ---
st.set_page_config(page_title="CreditSaathi | Premium MSME Intelligence", page_icon="📈", layout="wide", initial_sidebar_state="expanded")
inject_custom_css()

# Session State for Wizard & Data
if 'crs_score' not in st.session_state: st.session_state.crs_score = None
if 'user_inputs' not in st.session_state: st.session_state.user_inputs = {}
if 'form_step' not in st.session_state: st.session_state.form_step = 1

# --- HEADER / BRANDING ---
st.markdown("""
<div style="padding: 1rem 0; margin-bottom: 2rem; border-bottom: 1px solid #E2E8F0; display: flex; align-items: center; gap: 10px;">
    <div style="background: #14B8A6; padding: 10px; border-radius: 12px; color: white;">⚡</div>
    <div>
        <h2 style="margin: 0; font-size: 24px; color: #0B1F3A;">CreditSaathi</h2>
        <p style="margin: 0; font-size: 13px; color: #64748B;">Aapka Credit, Aapki Taakat</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR NAV ---
page = st.sidebar.radio("Navigation", ["🏠 Home", "👤 Start Assessment", "📊 Dashboard", "📋 Gap Analysis & Plan", "🏦 Lenders"])
st.sidebar.markdown("---")
if st.sidebar.button("💬 Chat Support"):
    st.sidebar.success("Support widget triggered!")

# --- ROUTING ---
if page == "🏠 Home":
    st.markdown("<h1 style='text-align: center; font-size: 48px; margin-top: 2rem;'>Unlock Your Business Potential</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: #64748B; max-width: 600px; margin: 0 auto 3rem auto;'>Calculate your Credit Readiness Score (CRS) and get matched with India's top lenders instantly.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div class="fintech-card card-top-accent" style="text-align: center;">
            <div style="font-size: 40px; margin-bottom: 15px;">📊</div>
            <h3>What is CRS?</h3>
            <p style="color: #475569; line-height: 1.6;">The Credit Readiness Score is an AI-driven, 0-850 metric that evaluates your MSME's health based on GST compliance, cash flow stability, and business vintage.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Assessment →", use_container_width=True):
            st.session_state.form_step = 1
            st.rerun() # Navigate seamlessly

elif page == "👤 Start Assessment":
    st.title("Business Profile")
    st.markdown("Complete the wizard to generate your dynamic score.")
    
    # Progress Bar
    progress = st.session_state.form_step / 3
    st.progress(progress)
    
    # --- MULTI-STEP WIZARD ---
    with st.container():
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        
        if st.session_state.form_step == 1:
            st.subheader("Step 1: Company Details")
            st.session_state.user_inputs['name'] = st.text_input("Business Name", value=st.session_state.user_inputs.get('name', ''))
            st.session_state.user_inputs['industry'] = st.selectbox("Industry", ["Retail", "Manufacturing", "Services", "IT/Tech", "Other"])
            st.session_state.user_inputs['vintage'] = st.number_input("Business Vintage (Years)", min_value=0.0, value=st.session_state.user_inputs.get('vintage', 2.5), step=0.5)
            
            if st.button("Next: Financials →"):
                if st.session_state.user_inputs['name']:
                    st.session_state.form_step = 2
                    st.rerun()
                else:
                    st.error("Please enter a Business Name.")

        elif st.session_state.form_step == 2:
            st.subheader("Step 2: Financial Health")
            st.session_state.user_inputs['turnover'] = st.number_input("Annual Turnover (₹)", min_value=0, value=st.session_state.user_inputs.get('turnover', 1500000), step=100000)
            st.session_state.user_inputs['bank_balance'] = st.number_input("Average Monthly Bank Balance (₹)", min_value=0, value=st.session_state.user_inputs.get('bank_balance', 50000), step=10000)
            st.session_state.user_inputs['gst_status'] = st.selectbox("GST Filing Status", ["Regular (Up to date)", "Delayed (< 3 months)", "Irregular", "Not Registered"])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back"):
                    st.session_state.form_step = 1
                    st.rerun()
            with col2:
                if st.button("Next: Liabilities →"):
                    st.session_state.form_step = 3
                    st.rerun()

        elif st.session_state.form_step == 3:
            st.subheader("Step 3: Liabilities")
            loan_history = st.radio("Existing Loan History?", ["Yes", "No"])
            st.session_state.user_inputs['emi_amount'] = st.number_input("Total Existing Monthly EMIs (₹)", min_value=0, value=0, step=5000) if loan_history == "Yes" else 0
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back"):
                    st.session_state.form_step = 2
                    st.rerun()
            with col2:
                if st.button("✨ Analyze & Generate Score"):
                    with st.spinner("Analyzing data vectors & credit footprint..."):
                        time.sleep(1.5) # UX: Let the user feel the "AI" working
                        
                        score, components = calculate_crs(
                            st.session_state.user_inputs['turnover'], 
                            st.session_state.user_inputs['vintage'], 
                            st.session_state.user_inputs['bank_balance'], 
                            st.session_state.user_inputs['gst_status'], 
                            st.session_state.user_inputs['emi_amount']
                        )
                        st.session_state.crs_score = score
                        st.session_state.components = components
                        
                    st.success("Analysis Complete! Generating Dashboard...")
                    time.sleep(0.5)
                    st.session_state.form_step = 1 # Reset for future
                    st.rerun() # Navigate automatically to Dashboard (logic handled by user needing to click nav, or you can force change 'page' if using a single state variable for routing)
                    
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "📊 Dashboard":
    if st.session_state.crs_score is None:
        st.warning("Please complete the Assessment first.")
    else:
        score = st.session_state.crs_score
        
        # Micro-interaction: Celebration if score is good
        if score >= 750: st.balloons()
        
        if score < 500: cat, badge_class = "High Risk", "badge-danger"
        elif score < 650: cat, badge_class = "Moderate", "badge-warning"
        elif score < 750: cat, badge_class = "Good", "badge-success"
        else: cat, badge_class = "Excellent", "badge-success"

        st.title(f"Welcome back, {st.session_state.user_inputs.get('name', 'Business')}!")
        
        # KPI Row
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1: render_metric_card("Annual Revenue", f"₹{st.session_state.user_inputs['turnover']:,.0f}", "💰")
        with kpi2: render_metric_card("Avg Monthly Balance", f"₹{st.session_state.user_inputs['bank_balance']:,.0f}", "🏦")
        with kpi3: render_metric_card("Business Vintage", f"{st.session_state.user_inputs['vintage']} Yrs", "⏳")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Main Visuals Row
        col1, col2, col3 = st.columns([1.2, 1.5, 1.5])
        with col1:
            render_score_badge(score, cat, badge_class)
        with col2:
            st.plotly_chart(create_gauge_chart(score), use_container_width=True, config={'displayModeBar': False})
        with col3:
            st.plotly_chart(create_breakdown_pie(st.session_state.components), use_container_width=True, config={'displayModeBar': False})
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(create_factor_bar(st.session_state.components), use_container_width=True, config={'displayModeBar': False})

elif page == "📋 Gap Analysis & Plan":
    if st.session_state.crs_score is None:
        st.warning("Please complete the Assessment first.")
    else:
        tab1, tab2 = st.tabs(["🔍 Gap Analysis", "🚀 Action Plan"])
        
        with tab1:
            st.subheader("Key Findings")
            insights = get_gap_analysis(st.session_state.components, st.session_state.user_inputs)
            for insight in insights:
                st.markdown(f"""
                <div class="fintech-card" style="border-left: 4px solid #14B8A6; padding: 16px 24px; margin-bottom: 12px;">
                    <p style="margin: 0; font-size: 15px; color: #334155;">{insight}</p>
                </div>
                """, unsafe_allow_html=True)
                
        with tab2:
            st.subheader("Strategic Roadmap")
            plan_df = get_action_plan(st.session_state.components)
            
            # Custom styled dataframe
            def color_priority(val):
                color = '#EF4444' if val == 'High' else '#F59E0B' if val == 'Medium' else '#22C55E'
                return f'color: {color}; font-weight: 600;'
            st.dataframe(plan_df.style.map(color_priority, subset=['priority']), use_container_width=True, hide_index=True)

            st.markdown("### Simulated Trajectory")
            chart_data = pd.DataFrame({
                "Timeline": ["Current", "30 Days", "60 Days", "90 Days"],
                "Projected Score": [st.session_state.crs_score, min(850, st.session_state.crs_score + 15), min(850, st.session_state.crs_score + 35), min(850, st.session_state.crs_score + 60)]
            })
            fig = px.line(chart_data, x="Timeline", y="Projected Score", markers=True)
            fig.update_traces(line_color="#14B8A6", line_width=3, marker=dict(size=12, color="#0B1F3A"))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter"), yaxis=dict(showgrid=True, gridcolor="#E2E8F0"))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

elif page == "🏦 Lenders":
    if st.session_state.crs_score is None:
        st.warning("Please complete the Assessment first.")
    else:
        st.title("Lender Matching Engine")
        st.markdown("Based on your CRS of **{}**, here are your matches:".format(st.session_state.crs_score))
        
        df_lenders = get_eligible_lenders(st.session_state.crs_score, st.session_state.user_inputs['turnover'], st.session_state.user_inputs['vintage'])
        
        for _, row in df_lenders.iterrows():
            if "✅" in row['Status']: color = "#22C55E"
            elif "⚠️" in row['Status']: color = "#F59E0B"
            else: color = "#EF4444"
                
            render_lender_tile(row['Lender'], row['Type'], row['Status'], row['Max Rate'], color)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 12px; padding-bottom: 20px;">
    © 2024 CreditSaathi | Empowering Indian MSMEs | Powered by Advanced Analytics
</div>
""", unsafe_allow_html=True)
