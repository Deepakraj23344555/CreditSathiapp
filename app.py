# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
from utils import inject_custom_css, get_lender_db, get_ca_clients, card_component, score_badge
from scoring import calculate_crs, generate_insights, generate_action_plan

# --- PAGE CONFIG ---
st.set_page_config(page_title="CreditSaathi | MSME Intelligence", page_icon="📈", layout="wide", initial_sidebar_state="expanded")
inject_custom_css()

# --- SESSION STATE MANAGEMENT ---
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'profile_assessed': False, 'score': 0, 'category': '', 'factors': {}, 
        'gaps': [], 'action_plan': [], 'turnover': 0, 'vintage': 0
    }
if 'form_step' not in st.session_state:
    st.session_state.form_step = 1
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'biz_name': '', 'industry': 'Manufacturing', 'turnover': 1500000, 
        'vintage': 2.0, 'bank_balance': 50000, 'gst_status': 'Regular (Monthly)', 
        'loan_history': 'No', 'emi_amount': 0
    }

# --- HEADER BANNER ---
st.markdown("""
<div style='background: linear-gradient(90deg, #0B1F3A 0%, #1E3A8A 100%); padding: 15px 30px; border-radius: 12px; margin-bottom: 30px; color: white; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(11, 31, 58, 0.2);'>
    <div style='font-size: 24px; font-weight: 800; letter-spacing: -0.5px;'>CreditSaathi <span style='font-size: 14px; font-weight: 400; color: #14B8A6; margin-left: 10px;'>Aapka Credit, Aapki Taakat</span></div>
    <div style='font-size: 14px; font-weight: 500; opacity: 0.9;'>MSME Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h2 style='color: #0B1F3A; text-align: center;'>Navigation</h2>", unsafe_allow_html=True)
st.sidebar.markdown("👤 **Logged in as:** KD")
st.sidebar.markdown("<br>", unsafe_allow_html=True)

menu = ["🏠 Home", "👤 Assess Profile", "📊 Dashboard", "🏦 Match Lenders", "🧑‍💼 CA/DSA Panel"]
choice = st.sidebar.radio("Go to:", menu, label_visibility="collapsed")

st.sidebar.markdown("---")
if st.sidebar.button("💬 Check via WhatsApp", use_container_width=True):
    st.sidebar.success("WhatsApp integration triggered!")

# --- HELPER VIZ COMPONENTS ---
def render_score_gauge(score):
    """Renders premium gradient gauge chart."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        number = {'font': {'color': '#0B1F3A', 'size': 56, 'weight': 'bold', 'family': 'Inter'}},
        gauge = {
            'axis': {'range': [0, 850], 'tickwidth': 1, 'tickcolor': "#CBD5E1"},
            'bar': {'color': "#14B8A6", 'thickness': 0.2},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 500], 'color': '#FEE2E2'},
                {'range': [500, 650], 'color': '#FEF3C7'},
                {'range': [650, 750], 'color': '#E0F2FE'},
                {'range': [750, 850], 'color': '#DCFCE7'}
            ],
            'threshold': {'line': {'color': "#1E3A8A", 'width': 4}, 'thickness': 0.75, 'value': score}
        }
    ))
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', font={'family': "Inter, sans-serif"})
    return fig

# --- ROUTING ---

if choice == "🏠 Home":
    col1, col2 = st.columns([1.2, 1], gap="large")
    with col1:
        st.markdown("<h1 style='font-size: 3.5rem; line-height: 1.1; margin-bottom: 20px;'>Unlock Capital for your MSME.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; color: #475569; line-height: 1.6;'>Stop guessing your loan eligibility. CreditSaathi evaluates your business data to generate a definitive Credit Readiness Score (CRS) and matches you with the right lenders instantly.</p><br>", unsafe_allow_html=True)
        if st.button("Start Assessment Flow →", type="primary"):
            st.info("👈 Select 'Assess Profile' from the sidebar to begin your journey.")
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="text-align: center; margin-top: 0;">Sample CRS Profile</h3>
            <div style="text-align: center; font-size: 72px; font-weight: 800; color: #14B8A6; margin: 10px 0; line-height: 1;">742</div>
            <div style="text-align: center; margin-bottom: 20px;">""" + score_badge("Good") + """</div>
            <div style="background: #F8FAFC; padding: 15px; border-radius: 8px; font-size: 14px; font-weight: 500;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>Cash Flow</span><span style="color:#166534;">✅ Stable</span></div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>GST Filing</span><span style="color:#166534;">✅ Regular</span></div>
                <div style="display: flex; justify-content: space-between;"><span>Vintage</span><span style="color:#92400E;">⚠️ Moderate</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif choice == "👤 Assess Profile":
    st.header("Business Profile Assessment")
    st.markdown("Follow the wizard to securely evaluate your credit footprint.")
    
    # Progress Bar UI
    progress_val = st.session_state.form_step / 3.0
    st.progress(progress_val)
    st.markdown(f"<p style='text-align:right; font-size:12px; color:#64748B; font-weight:600;'>Step {st.session_state.form_step} of 3</p>", unsafe_allow_html=True)

    # Multi-step Form Logic using session state
    if st.session_state.form_step == 1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("1. Business Identity")
        st.session_state.form_data['biz_name'] = st.text_input("Business Name", value=st.session_state.form_data['biz_name'])
        st.session_state.form_data['industry'] = st.selectbox("Industry", ["Manufacturing", "Retail/Trading", "Services", "IT/Tech", "Logistics", "Other"], index=["Manufacturing", "Retail/Trading", "Services", "IT/Tech", "Logistics", "Other"].index(st.session_state.form_data['industry']))
        st.session_state.form_data['vintage'] = st.number_input("Business Vintage (Years)", min_value=0.0, value=st.session_state.form_data['vintage'], step=0.5)
        if st.button("Next Step →", type="primary"):
            st.session_state.form_step = 2
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.form_step == 2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("2. Financial Footprint")
        st.session_state.form_data['turnover'] = st.number_input("Annual Turnover (₹)", min_value=0, value=st.session_state.form_data['turnover'], step=100000)
        st.session_state.form_data['bank_balance'] = st.number_input("Avg Monthly Bank Balance (₹)", min_value=0, value=st.session_state.form_data['bank_balance'], step=10000)
        st.session_state.form_data['gst_status'] = st.selectbox("GST Filing Status", ["Regular (Monthly)", "Quarterly (QRMP)", "Irregular", "Not Registered"], index=["Regular (Monthly)", "Quarterly (QRMP)", "Irregular", "Not Registered"].index(st.session_state.form_data['gst_status']))
        
        col1, col2 = st.columns(2)
        if col1.button("← Back"):
            st.session_state.form_step = 1
            st.rerun()
        if col2.button("Next Step →", type="primary"):
            st.session_state.form_step = 3
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.form_step == 3:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("3. Debt Obligations")
        st.session_state.form_data['loan_history'] = st.radio("Existing Loan History?", ["Yes", "No"], index=0 if st.session_state.form_data['loan_history'] == "Yes" else 1, horizontal=True)
        st.session_state.form_data['emi_amount'] = st.number_input("Total Monthly EMI (₹)", min_value=0, value=st.session_state.form_data['emi_amount'], step=5000) if st.session_state.form_data['loan_history'] == "Yes" else 0
        
        st.info("💡 Tip: Accurate debt reporting improves matching success.")
        
        col1, col2 = st.columns(2)
        if col1.button("← Back"):
            st.session_state.form_step = 2
            st.rerun()
        if col2.button("Generate Credit Report ✨", type="primary"):
            with st.spinner("Analyzing credit footprint using proprietary CRS model..."):
                time.sleep(1.5) # Simulate processing
                d = st.session_state.form_data
                score, category, factors = calculate_crs(d['turnover'], d['vintage'], d['bank_balance'], d['loan_history'], d['gst_status'], d['emi_amount'])
                
                monthly_income_est = d['turnover'] / 12 if d['turnover'] > 0 else 1
                foir_indicator = 'high' if (d['emi_amount'] / monthly_income_est) > 0.5 else 'low'
                
                gaps = generate_insights(factors, category, d['gst_status'], d['bank_balance'], d['vintage'], foir_indicator)
                action_plan = generate_action_plan(category, gaps)
                
                st.session_state.app_state.update({
                    'profile_assessed': True, 'score': score, 'category': category, 
                    'factors': factors, 'gaps': gaps, 'action_plan': action_plan,
                    'turnover': d['turnover'], 'vintage': d['vintage']
                })
                st.session_state.form_step = 1 # Reset form
            st.success("Analysis Complete! Redirecting to Dashboard...")
            time.sleep(1)
            st.switch_page("app.py") # Note: In a multi-page app this switches, here we rely on standard rerun or user navigation
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif choice == "📊 Dashboard":
    if not st.session_state.app_state['profile_assessed']:
        st.warning("Please complete the profile assessment to unlock the dashboard.")
    else:
        state = st.session_state.app_state
        
        # Top KPI Cards
        col1, col2, col3 = st.columns(3)
        c_colors = {"Excellent": "#DCFCE7", "Good": "#E0F2FE", "Moderate": "#FEF3C7", "High Risk": "#FEE2E2"}
        c_text = {"Excellent": "#166534", "Good": "#075985", "Moderate": "#92400E", "High Risk": "#991B1B"}
        
        with col1: st.markdown(card_component("Credit Readiness Score", state['score'], state['category'], c_colors.get(state['category']), c_text.get(state['category'])), unsafe_allow_html=True)
        with col2: st.markdown(card_component("Limit Eligibility", f"₹ {min(state['turnover'] * 0.2, 5000000):,.0f}", "Based on Turnover", "#F1F5F9", "#475569"), unsafe_allow_html=True)
        with col3: st.markdown(card_component("Profile Strength", f"{int((state['score']/850)*100)}%", "Complete", "#F0FDF4", "#166534"), unsafe_allow_html=True)
            
        # Charts Row
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        chart_col1, chart_col2 = st.columns([1, 1], gap="large")
        
        with chart_col1:
            st.markdown("<h4>Score Analysis</h4>", unsafe_allow_html=True)
            st.plotly_chart(render_score_gauge(state['score']), use_container_width=True, config={'displayModeBar': False})
            
        with chart_col2:
            st.markdown("<h4>Factor Breakdown</h4>", unsafe_allow_html=True)
            factors_df = pd.DataFrame(list(state['factors'].items()), columns=['Factor', 'Points'])
            fig = px.bar(factors_df, x='Points', y='Factor', orientation='h', color='Points', color_continuous_scale=['#E2E8F0', '#1E3A8A'])
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'family': 'Inter'})
            fig.update_traces(hovertemplate='<b>%{y}</b><br>Points: %{x}<extra></extra>')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
            
        # Action Plan & Gaps
        gap_col, act_col = st.columns(2, gap="large")
        with gap_col:
            st.markdown("<div class='glass-card'><h4>📋 Identified Gaps</h4>", unsafe_allow_html=True)
            for gap in state['gaps']:
                st.markdown(f"<div style='background: #FFF1F2; color: #9F1239; padding: 12px; border-radius: 8px; margin-bottom: 10px; font-size: 14px; border-left: 4px solid #E11D48;'>⚠️ {gap}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
                
        with act_col:
            st.markdown("<div class='glass-card'><h4>🚀 Action Plan</h4>", unsafe_allow_html=True)
            for item in state['action_plan']:
                b_color = "#EF4444" if item['priority'] == "Critical" else ("#F59E0B" if item['priority'] == "High" else "#10B981")
                bg_color = "#FEF2F2" if item['priority'] == "Critical" else ("#FFFBEB" if item['priority'] == "High" else "#F0FDF4")
                st.markdown(f"""
                <div style='background: {bg_color}; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid {b_color};'>
                    <div style='display: flex; justify-content: space-between; font-size: 13px; font-weight: 700; color: #0F172A; margin-bottom: 4px;'>
                        <span>⏱️ {item['time']}</span><span style='color: {b_color};'>{item['priority']}</span>
                    </div>
                    <div style='font-size: 14px; color: #334155;'>{item['action']}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif choice == "🏦 Match Lenders":
    st.header("Lender Matching Engine")
    
    if not st.session_state.app_state['profile_assessed']:
        st.info("Showing master database. Complete Assessment to see personalized matches.")
        st.dataframe(get_lender_db(), use_container_width=True)
    else:
        state = st.session_state.app_state
        st.markdown(f"<div style='background: #F8FAFC; padding: 16px; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 24px; font-weight: 500;'>Your CRS: <strong style='color:#1E3A8A; font-size: 18px;'>{state['score']}</strong> &nbsp;|&nbsp; Turnover: <strong>₹{state['turnover']:,.0f}</strong> &nbsp;|&nbsp; Vintage: <strong>{state['vintage']} Yrs</strong></div>", unsafe_allow_html=True)
        
        lenders = get_lender_db().copy()
        
        def evaluate_eligibility(row):
            if state['score'] >= row['Min Score Required'] and (state['turnover']/100000) >= row['Min Turnover (₹ Lakhs)'] and state['vintage'] >= row['Min Vintage (Years)']:
                return "✅ Eligible"
            elif state['score'] >= row['Min Score Required'] - 50:
                return "⚠️ Improve Score"
            return "❌ Not Eligible"
                
        lenders['Status'] = lenders.apply(evaluate_eligibility, axis=1)
        lenders['Sort_Key'] = lenders['Status'].map({"✅ Eligible": 0, "⚠️ Improve Score": 1, "❌ Not Eligible": 2})
        lenders = lenders.sort_values('Sort_Key').drop('Sort_Key', axis=1)
        
        st.dataframe(
            lenders.style.map(
                lambda v: 'color: #166534; background-color: #DCFCE7; font-weight: 600;' if v == '✅ Eligible' 
                else ('color: #92400E; background-color: #FEF3C7; font-weight: 600;' if v == '⚠️ Improve Score' 
                else 'color: #991B1B; background-color: #FEE2E2; font-weight: 600;'), 
                subset=['Status']
            ),
            use_container_width=True, hide_index=True
        )

elif choice == "🧑‍💼 CA/DSA Panel":
    st.header("Partner Dashboard")
    st.markdown("Pipeline Management.")
    
    clients = get_ca_clients()
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(card_component("Total Clients", len(clients)), unsafe_allow_html=True)
    with col2: st.markdown(card_component("Ready for Disbursal", len(clients[clients['Status'].isin(['Ready for Loan', 'Excellent', 'Good'])])), unsafe_allow_html=True)
    with col3: st.markdown(card_component("Avg Portfolio Score", int(clients['Current CRS'].mean()), "Up 12 pts", "#DCFCE7", "#166534"), unsafe_allow_html=True)
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.dataframe(
        clients.style.background_gradient(cmap="Blues", subset=['Current CRS']),
        use_container_width=True, hide_index=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div class='app-footer'>© CreditSaathi | Empowering MSMEs with Data Intelligence</div>", unsafe_allow_html=True)
