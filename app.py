import streamlit as st
import time
from utils import inject_custom_css, render_metric_card, render_lender_tile, create_gauge_chart, t, render_trust_layer
from scoring import calculate_crs, get_advanced_lenders, get_esg_score
from insights import get_behavioral_insights, generate_storytelling
from simulator import render_simulator
from ai_advisor import render_ai_advisor
from pdf_report import generate_pdf_report

# --- APP CONFIG ---
st.set_page_config(page_title="CreditSaathi Premium", page_icon="📈", layout="wide")
inject_custom_css()

# --- INITIALIZATION & DEMO MODE ---
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'crs_score' not in st.session_state: st.session_state.crs_score = None
if 'user_inputs' not in st.session_state: st.session_state.user_inputs = {}

with st.sidebar:
    st.markdown("### ⚙️ Platform Settings")
    st.session_state.lang = st.radio("Language", ["EN", "HI"], horizontal=True)
    demo_mode = st.toggle("🧪 Enable Demo Mode (High Score)")
    if demo_mode:
        st.session_state.user_inputs = {'name': 'Acme Corp', 'industry': 'Tech', 'vintage': 5.0, 'turnover': 50000000, 'bank_balance': 2000000, 'gst_status': "Regular (Up to date)", 'emi_amount': 0}
        st.session_state.crs_score, st.session_state.components = calculate_crs(50000000, 5.0, 2000000, "Regular (Up to date)", 0)
    
    st.markdown("---")
    page = st.radio("Navigation", [t("nav_home"), t("nav_assess"), t("nav_dash"), t("nav_gap"), t("nav_lenders"), t("nav_sim"), t("nav_ai")])

# --- ROUTING ---
if page == t("nav_home"):
    st.markdown(f"<h1 style='text-align: center; font-size: 48px;'>Investor-Grade Credit Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>Unlock institutional credit with AI-driven gap analysis.</p>", unsafe_allow_html=True)
    if st.button("Generate My Report →", use_container_width=True):
        st.info("Navigate to Assessment to begin.")

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
    if not st.session_state.crs_score: st.warning("Please complete Assessment first.")
    else:
        st.title("Business Intelligence Hub")
        score = st.session_state.crs_score
        
        # Smart Storytelling
        st.info(generate_storytelling(score, st.session_state.user_inputs))
        
        # KPIs
        c1, c2, c3, c4 = st.columns(4)
        benchmark_pct = min(99, int((score/850)*100))
        with c1: render_metric_card("Benchmark", f"Top {100-benchmark_pct}%", "🏆", trend="up" if score>600 else "down")
        with c2: render_metric_card("ESG / Green Score", f"{get_esg_score(st.session_state.user_inputs['industry'])}/100", "🌱")
        with c3: render_metric_card("Default Risk", "Low" if score>700 else "High", "🛡️")
        with c4: render_metric_card("Profile Strength", f"{benchmark_pct}%", "⚡")

        # Gamification Progress
        st.markdown(f"**Unlock Milestones:** {'✅ Premium Rates Unlocked!' if score >= 700 else '🔒 Reach 700 to unlock Premium Rates'}")
        st.progress(score/850)

        # Charts
        col1, col2 = st.columns([1.5, 2])
        with col1:
            st.plotly_chart(create_gauge_chart(score), use_container_width=True)
            # PDF Download
            pdf = generate_pdf_report(score, st.session_state.user_inputs, st.session_state.components)
            st.download_button("📄 Download PDF Report", data=pdf, file_name="CreditSaathi_Report.pdf", mime="application/pdf", use_container_width=True)
        with col2:
            st.markdown("### Behavioral Insights Engine")
            for insight in get_behavioral_insights(st.session_state.components):
                st.markdown(f"<div class='fintech-card' style='padding: 12px; margin-bottom: 8px;'>{insight}</div>", unsafe_allow_html=True)

elif page == t("nav_lenders"):
    if not st.session_state.crs_score: st.warning("Please complete Assessment.")
    else:
        st.title("Lender Matching Engine")
        df = get_advanced_lenders(st.session_state.crs_score, st.session_state.user_inputs['turnover'], st.session_state.user_inputs['vintage'])
        for _, row in df.iterrows():
            render_lender_tile(row['Lender'], row['Type'], row['Status'], row['Rate Range'], row['Color'], row['Approval %'], row['Loan Range'])
            
        st.markdown("---")
        st.markdown("### 📲 Share Securely")
        phone = st.text_input("Enter CA / Partner Phone Number")
        if st.button("Send via WhatsApp"):
            with st.spinner("Connecting to WhatsApp API..."):
                time.sleep(1)
                st.success("Report securely sent via WhatsApp!")

elif page == t("nav_sim"):
    if not st.session_state.crs_score: st.warning("Please complete Assessment.")
    else: render_simulator()

elif page == t("nav_ai"):
    if not st.session_state.crs_score: st.warning("Please complete Assessment.")
    else: render_ai_advisor()

render_trust_layer()
