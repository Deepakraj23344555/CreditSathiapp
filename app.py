import streamlit as st
import time
import pandas as pd

# --- I18N TRANSLATIONS ---
from translations import t

# --- PREMIUM UI COMPONENTS ---
from ui_components import inject_premium_dark_theme, inject_global_language_css, metric_kpi, status_badge, premium_lender_card, apply_dark_theme, COLORS

# --- BACKEND LOGIC ---
from utils import create_gauge_chart
from scoring import calculate_crs, get_advanced_lenders, get_esg_score
from insights import get_behavioral_insights, generate_storytelling
from simulator import render_simulator
from ai_advisor import render_ai_advisor
from pdf_report import generate_pdf_report

# 1. Config First
st.set_page_config(page_title="CreditSaathi Global", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# 2. Init State
if 'lang' not in st.session_state: 
    st.session_state.lang = 'en'
if 'crs_score' not in st.session_state: 
    st.session_state.crs_score = None
if 'user_inputs' not in st.session_state: 
    st.session_state.user_inputs = {}

# 3. Inject CSS
inject_premium_dark_theme()
inject_global_language_css(st.session_state.lang) # Handles custom fonts & Arabic RTL

# --- LANGUAGE SELECTOR MAPPING ---
LANG_OPTIONS = {
    "en": "English 🇺🇸",
    "hi": "हिंदी 🇮🇳",
    "es": "Español 🇪🇸",
    "ar": "العربية 🇦🇪"
}
DISPLAY_TO_CODE = {v: k for k, v in LANG_OPTIONS.items()}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"<h2 style='color: #FFFFFF;'>CreditSaathi <span style='color: {COLORS['accent']};'>.</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 14px; margin-bottom: 20px;'>Institutional Grade Engine</p>", unsafe_allow_html=True)
    
    st.markdown("### 🌐 Global Settings")
    current_display = LANG_OPTIONS[st.session_state.lang]
    selected_display = st.selectbox("Select Language", options=list(DISPLAY_TO_CODE.keys()), index=list(DISPLAY_TO_CODE.keys()).index(current_display), label_visibility="collapsed")
    
    if DISPLAY_TO_CODE[selected_display] != st.session_state.lang:
        st.session_state.lang = DISPLAY_TO_CODE[selected_display]
        st.rerun()
        
    demo_mode = st.toggle("🧪 Enable Demo Mode")
    if demo_mode:
        st.session_state.user_inputs = {'name': 'Acme Corp', 'industry': 'Tech', 'vintage': 5.0, 'turnover': 50000000, 'bank_balance': 2000000, 'gst_status': "Regular (Up to date)", 'emi_amount': 0}
        st.session_state.crs_score, st.session_state.components = calculate_crs(50000000, 5.0, 2000000, "Regular (Up to date)", 0)
        
    st.markdown("---")
    
    # Dynamic Navigation
    page = st.radio("Main Menu", [
        t("nav_home"), 
        t("nav_assess"), 
        t("nav_dash"), 
        t("nav_lenders"),
        t("nav_ca"),
        t("nav_sim"),
        t("nav_ai")
    ])
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 12px; color: #64748B; padding: 20px; border-top: 1px solid rgba(255,255,255,0.1);'>{t('trust_msg')}</div>", unsafe_allow_html=True)

# --- ROUTING LOGIC ---

if page == t("nav_home"):
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 40px;">
            <h1 style="font-size: 52px; line-height: 1.2;">{t('hero_t1')}<br><span style="color: {COLORS['accent']};">{t('hero_t2')}</span></h1>
            <p class="text-secondary" style="font-size: 18px; max-width: 600px; margin: 20px auto;">
                {t('hero_sub')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([2, 2, 2])
        with c2:
            if st.button(t("hero_btn")):
                st.info(f"👈 Please click '{t('nav_assess')}' in the sidebar to begin.")

elif page == t("nav_assess"):
    st.title(t("nav_assess"))
    st.markdown("<p class='text-muted'>Onboard via RBI's Account Aggregator framework.</p>", unsafe_allow_html=True)
    
    with st.form("input_form"):
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        
        # Identity & Compliance Layer
        st.markdown("#### 1. Identity & Compliance")
        col_kyc1, col_kyc2, col_kyc3 = st.columns(3)
        with col_kyc1:
            biz_name = st.text_input(t("biz_name"), placeholder="e.g., Sharma Traders")
        with col_kyc2:
            pan_num = st.text_input(t("pan_num"), placeholder="ABCDE1234F")
        with col_kyc3:
            aadhaar_kyc = st.text_input(t("aadhaar_kyc"), placeholder="[Aadhaar Redacted]", type="password") 
            
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        # Account Aggregator Integration Simulation
        st.markdown("#### 2. Financial Footprint")
        aa_button = st.form_submit_button(t("aa_fetch"))
        if aa_button:
            st.toast("✅ Bank statements & GST data fetched successfully via Sahamati AA!")
            
        col1, col2 = st.columns(2)
        with col1:
            industry = st.selectbox("Industry", ["Retail", "Manufacturing", "Services", "IT/Tech", "Other"])
            turnover = st.number_input(t("turnover"), min_value=0, value=1500000, step=100000)
            vintage = st.slider(t("vintage"), min_value=0.0, max_value=20.0, value=2.5, step=0.5)
        with col2:
            bank_balance = st.number_input(t("bank_bal"), min_value=0, value=50000, step=10000)
            gst_status = st.selectbox(t("gst"), ["Regular (Up to date)", "Delayed (< 3 months)", "Irregular", "Not Registered"])
            loan_history = st.radio("Active business loans?", ["No", "Yes"])
            emi_amount = st.number_input("Monthly EMIs (₹)", value=0) if loan_history == "Yes" else 0
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button(t("btn_generate")):
            with st.spinner("Processing underwriting algorithms..."):
                time.sleep(1.5)
                score, comp = calculate_crs(turnover, vintage, bank_balance, gst_status, emi_amount)
                st.session_state.crs_score = score
                st.session_state.components = comp
                st.session_state.user_inputs = {'name': biz_name, 'industry': industry, 'turnover': turnover, 'vintage': vintage, 'bank_balance': bank_balance, 'gst_status': gst_status, 'emi_amount': emi_amount}
            st.success("Analysis Complete! Head to Step 2.")
        st.markdown("</div>", unsafe_allow_html=True)

elif page == t("nav_dash"):
    if not st.session_state.crs_score: 
        st.warning(f"Please complete {t('nav_assess')} first.")
    else:
        score = st.session_state.crs_score
        inputs = st.session_state.user_inputs
        
        st.title(t("score_title"))
        st.info(generate_storytelling(score, inputs))
        
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
            
            st.plotly_chart(apply_dark_theme(create_gauge_chart(score)), use_container_width=True)
            
            pdf = generate_pdf_report(score, inputs, st.session_state.components)
            st.download_button("📄 Download My Full Report", data=pdf, file_name="CreditSaathi_Report.pdf", mime="application/pdf")

        with col_side:
            st.markdown(f"### {t('insights_title')}")
            insights = get_behavioral_insights(st.session_state.components)
            for insight in insights:
                st.markdown(f"<div class='premium-card' style='padding: 16px; margin-bottom: 12px; border-left: 2px solid {COLORS['accent']};'><p style='margin:0; font-size: 14px; color: {COLORS['secondary']};'>{insight}</p></div>", unsafe_allow_html=True)

elif page == t("nav_lenders"):
    if not st.session_state.crs_score: 
        st.warning(f"Please complete {t('nav_assess')} first.")
    else:
        st.title(t("lenders_title"))
        st.markdown("<p class='text-muted'>Based on your health score, we matched you with these institutional partners.</p>", unsafe_allow_html=True)
        
        df = get_advanced_lenders(st.session_state.crs_score, st.session_state.user_inputs['turnover'], st.session_state.user_inputs['vintage'])
        for _, row in df.iterrows():
            st.markdown(premium_lender_card(row['Lender'], row['Type'], row['Status'], row['Rate Range'], row['Approval %']), unsafe_allow_html=True)

elif page == t("nav_ca"):
    st.title("🧑‍💼 Partner Dashboard (CA/DSA)")
    st.markdown("<p class='text-muted'>Manage your MSME clients and track their credit readiness.</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="premium-card" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h3 style="margin:0;">Invite New Client</h3>
            <p class="text-muted" style="margin:0;">Send a secure WhatsApp link to initiate Account Aggregator fetch.</p>
        </div>
        <button class="stButton" style="padding: 10px 20px; background: #14B8A6; border-radius: 8px; color: white; border: none; font-weight: bold;">Generate WhatsApp Invite</button>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Client Portfolio")
    
    mock_clients = pd.DataFrame({
        "Client Name": ["Gupta Textiles", "Verma Electronics", "Singh Logistics", "Rao Manufacturing"],
        "CRS Score": [740, 610, 480, 810],
        "Turnover (₹)": ["2.5 Cr", "80 Lakh", "40 Lakh", "5.0 Cr"],
        "Eligible Lenders": [12, 4, 0, 15],
        "Status": ["Prime", "Standard", "High Risk", "Super Prime"]
    })
    
    st.dataframe(mock_clients, use_container_width=True, hide_index=True)

elif page == t("nav_sim"):
    if not st.session_state.crs_score: 
        st.warning(f"Please complete {t('nav_assess')} first.")
    else: 
        render_simulator()

elif page == t("nav_ai"):
    if not st.session_state.crs_score: 
        st.warning(f"Please complete {t('nav_assess')} first.")
    else: 
        render_ai_advisor()
