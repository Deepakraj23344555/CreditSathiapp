# app.py
import streamlit as st
import time
import pandas as pd
from utils import inject_custom_css, create_gauge_chart, create_breakdown_pie, create_factor_bar
from scoring import calculate_crs, get_gap_analysis, get_action_plan, get_eligible_lenders

# App Config
st.set_page_config(page_title="CreditSaathi | MSME Credit Intelligence", page_icon="📈", layout="wide")
inject_custom_css()

# Session State Initialization
if 'crs_score' not in st.session_state:
    st.session_state.crs_score = None
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = {}

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=60) # Placeholder minimalist icon
st.sidebar.title("CreditSaathi")
st.sidebar.markdown("*Aapka Credit, Aapki Taakat*")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["🏠 Home", "👤 User Input", "📊 Dashboard", "📋 Gap Analysis", "🚀 Action Plan", "🏦 Lenders", "🧑‍💼 CA/DSA Panel"])

st.sidebar.markdown("---")
if st.sidebar.button("💬 Check via WhatsApp"):
    st.sidebar.success("WhatsApp integration triggered! (Mock)")

# --- PAGES ---

if page == "🏠 Home":
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>Unlock Your Business Potential</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: gray;'>Calculate your Credit Readiness Score (CRS) and get matched with India's top lenders instantly.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div class="fintech-card" style="text-align: center;">
            <h3>What is CRS?</h3>
            <p>The Credit Readiness Score is an AI-driven, 0-850 metric that evaluates your MSME's health based on GST compliance, cash flow stability, and business vintage.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Check Your Credit Score Now", use_container_width=True):
            st.info("Please navigate to '👤 User Input' in the sidebar to begin.")

elif page == "👤 User Input":
    st.title("Business Profile")
    st.markdown("Fill in your details to generate your dynamic Credit Readiness Score.")
    
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        with col1:
            biz_name = st.text_input("Business Name")
            industry = st.selectbox("Industry", ["Retail", "Manufacturing", "Services", "IT/Tech", "Logistics", "Other"])
            turnover = st.number_input("Annual Turnover (₹)", min_value=0, value=1500000, step=100000)
            vintage = st.number_input("Business Vintage (Years)", min_value=0.0, value=2.5, step=0.5)
        with col2:
            bank_balance = st.number_input("Average Monthly Bank Balance (₹)", min_value=0, value=50000, step=10000)
            gst_status = st.selectbox("GST Filing Status", ["Regular (Up to date)", "Delayed (< 3 months)", "Irregular", "Not Registered"])
            loan_history = st.radio("Existing Loan History?", ["Yes", "No"])
            emi_amount = st.number_input("Total Existing Monthly EMIs (₹)", min_value=0, value=0, step=5000) if loan_history == "Yes" else 0
            
        uploaded_file = st.file_uploader("Upload Bank Statement (Optional PDF/CSV)", type=["pdf", "csv"])
        
        submitted = st.form_submit_button("Generate Score")
        
        if submitted:
            with st.spinner("Analyzing GST footprint and cash flows..."):
                time.sleep(1.5) # Simulate processing
                score, components = calculate_crs(turnover, vintage, bank_balance, gst_status, emi_amount)
                
                st.session_state.crs_score = score
                st.session_state.components = components
                st.session_state.user_inputs = {
                    "name": biz_name, "turnover": turnover, "vintage": vintage
                }
                
                st.success("Score generated successfully! Go to the Dashboard.")

elif page == "📊 Dashboard":
    if st.session_state.crs_score is None:
        st.warning("Please submit your details in the 'User Input' page first.")
    else:
        st.title("Credit Intelligence Dashboard")
        score = st.session_state.crs_score
        
        # Determine category and badge
        if score < 500: cat, badge_class = "High Risk", "badge-danger"
        elif score < 650: cat, badge_class = "Moderate", "badge-warning"
        elif score < 750: cat, badge_class = "Good", "badge-success"
        else: cat, badge_class = "Excellent", "badge-success"

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div class="fintech-card" style="text-align: center;">
                <p style="font-size: 18px; margin:0;">Credit Readiness Score</p>
                <div class="score-display">{score}</div>
                <span class="{badge_class}">{cat}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.plotly_chart(create_breakdown_pie(st.session_state.components), use_container_width=True)
            
        with col2:
            st.plotly_chart(create_gauge_chart(score), use_container_width=True)
            st.plotly_chart(create_factor_bar(st.session_state.components), use_container_width=True)

elif page == "📋 Gap Analysis":
    if st.session_state.crs_score is None:
        st.warning("Please submit your details in the 'User Input' page first.")
    else:
        st.title("Gap Analysis")
        st.markdown("Actionable insights based on your financial footprint.")
        
        insights = get_gap_analysis(st.session_state.components, st.session_state.user_inputs)
        
        for insight in insights:
            st.markdown(f"""
            <div class="fintech-card" style="padding: 16px; border-left: 4px solid #1E3A8A;">
                <p style="margin: 0; font-size: 16px;">{insight}</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "🚀 Action Plan":
    if st.session_state.crs_score is None:
        st.warning("Please submit your details in the 'User Input' page first.")
    else:
        st.title("Strategic Action Plan")
        st.markdown("Your custom roadmap to achieving an Excellent (750+) rating.")
        
        plan_df = get_action_plan(st.session_state.components)
        
        def color_priority(val):
            color = '#EF4444' if val == 'High' else '#F59E0B' if val == 'Medium' else '#22C55E'
            return f'color: {color}; font-weight: bold;'

        st.dataframe(plan_df.style.map(color_priority, subset=['priority']), use_container_width=True, hide_index=True)

        # Simulated Score Tracking
        st.markdown("### Simulated Trajectory")
        chart_data = pd.DataFrame({
            "Month": ["Now", "Month 1", "Month 2", "Month 3"],
            "Projected Score": [st.session_state.crs_score, min(850, st.session_state.crs_score + 15), min(850, st.session_state.crs_score + 35), min(850, st.session_state.crs_score + 60)]
        })
        fig = px.line(chart_data, x="Month", y="Projected Score", markers=True, title="Score Projection upon Plan Completion")
        fig.update_traces(line_color="#14B8A6", marker=dict(size=10, color="#0B1F3A"))
        st.plotly_chart(fig, use_container_width=True)

elif page == "🏦 Lenders":
    if st.session_state.crs_score is None:
        st.warning("Please submit your details in the 'User Input' page first.")
    else:
        st.title("Lender Matching Engine")
        st.markdown("Lenders matching your current profile.")
        
        df_lenders = get_eligible_lenders(st.session_state.crs_score, st.session_state.user_inputs['turnover'], st.session_state.user_inputs['vintage'])
        
        for _, row in df_lenders.iterrows():
            if "✅" in row['Status']: border_color = "#22C55E"
            elif "⚠️" in row['Status']: border_color = "#F59E0B"
            else: border_color = "#EF4444"
                
            st.markdown(f"""
            <div class="fintech-card" style="border-left: 6px solid {border_color};">
                <h4>{row['Lender']} <span style="font-size: 14px; color: gray; font-weight: normal;">({row['Type']})</span></h4>
                <div style="display: flex; justify-content: space-between;">
                    <p><strong>Status:</strong> {row['Status']}</p>
                    <p><strong>Est. Max Rate:</strong> {row['Max Rate']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif page == "🧑‍💼 CA/DSA Panel":
    st.title("Partner Dashboard")
    st.markdown("Overview of client portfolios (Mock Data)")
    
    mock_clients = pd.DataFrame({
        "Client Name": ["Sharma Traders", "Verma Logistics", "Gupta Enterprises", "TechFix Solutions"],
        "CRS Score": [720, 610, 480, 790],
        "GST Status": ["Regular", "Delayed", "Irregular", "Regular"],
        "Eligibility": ["High", "Medium", "Low", "Excellent"]
    })
    
    st.dataframe(mock_clients, use_container_width=True, hide_index=True)
    st.button("Invite New Client via Link")
