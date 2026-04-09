import streamlit as st
import time

# --- PREMIUM DARK UI ENGINE ---
from ui_components import inject_premium_dark_theme, metric_kpi, status_badge, premium_lender_card, apply_dark_theme, COLORS

# --- BACKEND LOGIC (Untouched) ---
from utils import create_gauge_chart, t, render_trust_layer
from scoring import calculate_crs, get_advanced_lenders, get_esg_score
from insights import get_behavioral_insights, generate_storytelling
from simulator import render_simulator
from ai_advisor import render_ai_advisor
from pdf_report import generate_pdf_report

# 1. Config First
st.set_page_config(page_title="CreditSaathi Premium", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# 2. Inject Global Theme
inject_premium_dark_theme()

# --- STATE INIT ---
if 'crs_score' not in st.session_state: st.session_state.crs_score = None
if 'user_inputs' not in st.session_state: st.session_state.user_inputs = {}

# --- CLEAN SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown(f"<h2 style='color: #FFFFFF;'>CreditSaathi <span style='color: {COLORS['accent']};'>.</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 14px; margin-bottom: 20px;'>Institutional Grade Engine</p>", unsafe_allow_html=True)
    
    # Simplified Guided Navigation
    page = st.radio("Main Menu", [
        "🏠 Home", 
        "📝 Step 1: Enter Details", 
        "📊 Step 2: View Score", 
        "🏦 Step 3: Get Loans",
        "💡 AI Advisor"
    ])
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    render_trust_layer()

# --- ROUTING LOGIC ---

if page == "🏠 Home":
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 40px;">
            <h1 style="font-size: 52px; line-height: 1.2;">Understand Your Business Credit.<br><span style="color: {COLORS['accent']};">Unlock New Opportunities.</span></h1>
            <p class="text-secondary" style="font-size: 18px; max-width: 600px; margin: 20px auto;">
                See your creditworthiness the way lenders do — and take control of your financial future in less than 2 minutes.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([2, 2, 2])
        with c2:
            if st.button("Check My Score Now"):
                st.info("👈 Please click 'Step 1: Enter Details' in the sidebar to begin.")

elif page == "📝 Step 1: Enter Details":
    st.title("Tell Us About Your Business")
    st.markdown("<p class='text-muted'>This information is 256-bit encrypted and only used to calculate your health score.</p>", unsafe_allow_html=True)
    
    with st.form("input_form"):
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            biz_name = st.text_input("Business Name", placeholder="e.g., Sharma Traders")
            industry = st.selectbox("What is your business type?", ["Retail", "Manufacturing", "Services", "IT/Tech", "Other"])
            turnover = st.number_input("Approximate Annual Turnover (₹)", min_value=0, value=1500000, step=100000)
            vintage = st.slider("How old is your business? (Years)", min_value=0.0, max_value=20.0, value=2.5, step=0.5)
            
        with col2:
            bank_balance = st.number_input("Average Monthly Bank Balance (₹)", min_value=0, value=50000, step=10000)
            gst_status = st.selectbox("GST Filing Status", ["Regular (Up to date)", "Delayed (< 3 months)", "Irregular", "Not Registered"])
            loan_history = st.radio("Do you currently have any active business loans?", ["No", "Yes"])
            emi_amount = st.number_input("Total Monthly EMIs you pay (₹)", value=0) if loan_history == "Yes" else 0
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("Generate My Report"):
            with st.spinner("Analyzing your profile..."):
                time.sleep(1)
                score, comp = calculate_crs(turnover, vintage, bank_balance, gst_status, emi_amount)
                st.session_state.crs_score = score
                st.session_state.components = comp
                st.session_state.user_inputs = {'name': biz_name, 'industry': industry, 'turnover': turnover, 'vintage': vintage, 'bank_balance': bank_balance, 'gst_status': gst_status, 'emi_amount': emi_amount}
            st.success("Success! Head over to Step 2 to view your score.")
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "📊 Step 2: View Score":
    if not st.session_state.crs_score: 
        st.warning("Please complete Step 1 first.")
    else:
        score = st.session_state.crs_score
        inputs = st.session_state.user_inputs
        
        st.title("Your Credit Health Score")
        st.info(generate_storytelling(score, inputs))
        
        # MAIN LAYOUT
        col_main, col_side = st.columns([1.5, 1])
        
        with col_main:
            cat = "Excellent" if score >= 750 else "Good" if score >= 600 else "Needs Work"
            color_key = COLORS['accent'] if score >= 700 else COLORS['warning']
            
            st.markdown(f"""
            <div class="premium-card" style="display: flex; justify-content: space-between; align-items: center; border-left: 4px solid {color_key};">
                <div>
                    <p style="margin:0; color: {COLORS['text_muted']}; font-weight: 600; text-transform: uppercase;">Overall Score</p>
                    <div class="score-huge">{score}</div>
                    {status_badge(f"{cat} Category", color_key)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Gauge chart updated for Dark theme
            st.plotly_chart(apply_dark_theme(create_gauge_chart(score)), use_container_width=True)
            
            pdf = generate_pdf_report(score, inputs, st.session_state.components)
            st.download_button("📄 Download My Full Report", data=pdf, file_name="CreditSaathi_Report.pdf", mime="application/pdf")

        with col_side:
            st.markdown("### What’s Holding You Back")
            insights = get_behavioral_insights(st.session_state.components)
            for insight in insights:
                st.markdown(f"<div class='premium-card' style='padding: 16px; margin-bottom: 12px; border-left: 2px solid {COLORS['accent']};'><p style='margin:0; font-size: 14px; color: {COLORS['secondary']};'>{insight}</p></div>", unsafe_allow_html=True)
                
        st.markdown("---")
        st.markdown("### Your 90-Day Growth Plan")
        render_simulator()

elif page == "🏦 Step 3: Get Loans":
    if not st.session_state.crs_score: 
        st.warning("Please complete Step 1 first.")
    else:
        st.title("Loans You’re Eligible For Today")
        st.markdown("<p class='text-muted'>Based on your health score, we matched you with these institutional partners.</p>", unsafe_allow_html=True)
        
        df = get_advanced_lenders(st.session_state.crs_score, st.session_state.user_inputs['turnover'], st.session_state.user_inputs['vintage'])
        for _, row in df.iterrows():
            st.markdown(premium_lender_card(row['Lender'], row['Type'], row['Status'], row['Rate Range'], row['Approval %']), unsafe_allow_html=True)

elif page == "💡 AI Advisor":
    if not st.session_state.crs_score: 
        st.warning("Please complete Step 1 first.")
    else: 
        render_ai_advisor()
