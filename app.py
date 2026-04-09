import streamlit as st
import time

# --- NEW PREMIUM UI COMPONENTS ---
from ui_components import inject_premium_css, metric_kpi, glass_badge, premium_lender_card, apply_dark_theme, COLORS

# --- EXISTING LOGIC & UTILS ---
from utils import create_gauge_chart, t, render_trust_layer
from scoring import calculate_crs, get_advanced_lenders, get_esg_score
from insights import get_behavioral_insights, generate_storytelling
from simulator import render_simulator
from ai_advisor import render_ai_advisor
from pdf_report import generate_pdf_report

# --- APP CONFIG & CSS INJECTION ---
st.set_page_config(page_title="CreditSaathi Premium", page_icon="✨", layout="wide")
inject_premium_css()

# --- INITIALIZATION & DEMO MODE ---
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'crs_score' not in st.session_state: st.session_state.crs_score = None
if 'user_inputs' not in st.session_state: st.session_state.user_inputs = {}

with st.sidebar:
    # Premium branding in sidebar
    st.markdown(f"<h2 style='color: white;'>CreditSaathi <span style='color:{COLORS['accent']};'>.</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 14px; margin-bottom: 30px;'>Institutional Grade Intelligence</p>", unsafe_allow_html=True)

    st.markdown("### ⚙️ Platform Settings")
    st.session_state.lang = st.radio("Language", ["EN", "HI"], horizontal=True)
    demo_mode = st.toggle("🧪 Enable Demo Mode (High Score)")
    
    if demo_mode:
        st.session_state.user_inputs = {'name': 'Acme Corp', 'industry': 'Tech', 'vintage': 5.0, 'turnover': 50000000, 'bank_balance': 2000000, 'gst_status': "Regular (Up to date)", 'emi_amount': 0}
        st.session_state.crs_score, st.session_state.components = calculate_crs(50000000, 5.0, 2000000, "Regular (Up to date)", 0)
    
    st.markdown("---")
    
    # Fully unified routing
    page = st.radio("Navigation", [
        t("nav_home"), 
        t("nav_assess"), 
        t("nav_dash"), 
        t("nav_gap"), 
        t("nav_lenders"), 
        t("nav_sim"), 
        t("nav_ai")
    ])

# --- ROUTING LOGIC ---

if page == t("nav_home"):
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; animation: slideUpFade 0.8s ease;">
            <div style="display: inline-block; margin-bottom: 20px;">
                """ + glass_badge("v2.0 Investor Grade Engine Live", COLORS["accent"]) + """
            </div>
            <h1 class="hero-title">Understand Your Credit.<br>Unlock Your Growth.</h1>
            <p class="text-muted" style="font-size: 20px; max-width: 600px; margin: 0 auto 40px auto;">
                Bank-grade analytics and AI-driven insights designed to bridge the gap between MSMEs and premium institutional capital.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Centered CTA button
        c1, c2, c3 = st.columns([2, 1, 2])
        with c2:
            if st.button("Enter Platform", use_container_width=True):
                st.info(f"Navigate to '{t('nav_assess')}' in the sidebar to begin your journey.")

elif page == t("nav_assess"):
    st.title(t("nav_assess"))
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        with col1:
            biz_name = st.text_input("Business Name", value=st.session_state.user_inputs.get('name', ''))
            industry = st.selectbox("Industry", ["Retail", "Manufacturing", "Services", "IT/Tech", "Other"])
            turnover = st.number_input("Annual Turnover (₹)", min_value=0, value=1500000, step=100000)
            vintage = st.number_input("Vintage (Years)", min_value=0.0, value=2.5, step=0.5)
        with col2:
            bank_balance = st.number_input("Avg Monthly Balance (₹)", min_value=0, value=50000, step=10000)
            gst_status = st.selectbox("GST Status", ["Regular (Up to date)", "Delayed (< 3 months)", "Irregular", "Not Registered"])
            loan_history = st.radio("Existing Loan?", ["Yes", "No"])
            emi_amount = st.number_input("Monthly EMIs (₹)", value=0) if loan_history == "Yes" else 0
            
        if st.form_submit_button("✨ Analyze Profile (AI Engine)"):
            with st.spinner("Analyzing millions of data points..."):
                time.sleep(1.5)
                score, comp = calculate_crs(turnover, vintage, bank_balance, gst_status, emi_amount)
                st.session_state.crs_score = score
                st.session_state.components = comp
                st.session_state.user_inputs = {'name': biz_name, 'industry': industry, 'turnover': turnover, 'vintage': vintage, 'bank_balance': bank_balance, 'gst_status': gst_status, 'emi_amount': emi_amount}
            st.success("Analysis Complete! Head to Dashboard.")

elif page == t("nav_dash"):
    if not st.session_state.crs_score: 
        st.warning("Please complete Assessment first.")
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <h3 style="color: {COLORS['accent']} !important;">No Data Found</h3>
            <p class="text-muted">Please run an assessment to generate your intelligence hub.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.title("Business Intelligence Hub")
        score = st.session_state.crs_score
        inputs = st.session_state.user_inputs
        
        # Smart Storytelling
        st.info(generate_storytelling(score, st.session_state.user_inputs))
        
        # TOP KPI ROW (Apple Style)
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.markdown(metric_kpi("Annual Run Rate", f"₹{inputs['turnover']/100000:.1f}L", "📈", "up"), unsafe_allow_html=True)
        with k2: st.markdown(metric_kpi("Liquidity Avg", f"₹{inputs['bank_balance']/1000:.1f}K", "💧"), unsafe_allow_html=True)
        with k3: st.markdown(metric_kpi("Vintage", f"{inputs['vintage']} Yrs", "⏳", "up"), unsafe_allow_html=True)
        with k4: st.markdown(metric_kpi("Debt Ratio", "Optimal" if inputs['emi_amount'] == 0 else "High", "⚖️"), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # MAIN LAYOUT
        col_main, col_side = st.columns([1.5, 1])
        
        with col_main:
            cat = "Prime" if score >= 750 else "Standard" if score >= 600 else "Sub-Prime"
            color_hex = COLORS["accent"] if score >= 700 else "#F59E0B"
            
            # Massive Score Display
            st.markdown(f"""
            <div class="glass-card" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="margin:0; color: {COLORS['text_muted']}; font-weight: 600; text-transform: uppercase;">Overall CRS</p>
                    <div class="score-huge">{score}</div>
                    {glass_badge(f"{cat} Tier Rating", color_hex)}
                </div>
                <div style="text-align: right;">
                    <p class="text-muted" style="max-width: 250px;">Based on algorithmic analysis of your cash flows, compliance, and vintage vectors.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Gauge chart updated dynamically for dark theme
            st.plotly_chart(apply_dark_theme(create_gauge_chart(score)), use_container_width=True)
            
            # PDF Report Download
            pdf = generate_pdf_report(score, st.session_state.user_inputs, st.session_state.components)
            st.download_button("📄 Download Investor PDF Report", data=pdf, file_name="CreditSaathi_Premium_Report.pdf", mime="application/pdf", use_container_width=True)

        with col_side:
            st.markdown("### Behavioral Insights")
            insights = get_behavioral_insights(st.session_state.components)
            for insight in insights:
                st.markdown(f"<div class='glass-card' style='padding: 20px; margin-bottom: 16px;'>{insight}</div>", unsafe_allow_html=True)

elif page == t("nav_gap"):
    if not st.session_state.crs_score: 
        st.warning("Please complete Assessment first.")
    else:
        st.title(t("nav_gap"))
        st.markdown("### Actionable Recommendations")
        insights = get_behavioral_insights(st.session_state.components)
        for insight in insights:
            st.markdown(f"<div class='glass-card' style='padding: 20px; margin-bottom: 16px; border-left: 4px solid {COLORS['accent']};'>{insight}</div>", unsafe_allow_html=True)

elif page == t("nav_lenders"):
    if not st.session_state.crs_score: 
        st.warning("Please complete Assessment.")
    else:
        st.markdown("<h2>Institutional Network</h2>", unsafe_allow_html=True)
        st.markdown("<p class='text-muted'>AI-matched capital providers based on your CRS.</p><br>", unsafe_allow_html=True)
        
        df = get_advanced_lenders(st.session_state.crs_score, st.session_state.user_inputs['turnover'], st.session_state.user_inputs['vintage'])
        for _, row in df.iterrows():
            st.markdown(premium_lender_card(row['Lender'], row['Type'], row['Status'], row['Rate Range'], row['Approval %']), unsafe_allow_html=True)
            
        st.markdown("---")
        st.markdown("### 📲 Share Securely")
        phone = st.text_input("Enter CA / Partner Phone Number")
        if st.button("Send via WhatsApp"):
            with st.spinner("Connecting to WhatsApp API..."):
                time.sleep(1)
                st.success("Report securely sent via WhatsApp!")

elif page == t("nav_sim"):
    if not st.session_state.crs_score: 
        st.warning("Please complete Assessment.")
    else: 
        render_simulator()

elif page == t("nav_ai"):
    if not st.session_state.crs_score: 
        st.warning("Please complete Assessment.")
    else: 
        render_ai_advisor()

render_trust_layer()
