# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
from utils import inject_custom_css, get_lender_db, get_ca_clients
from scoring import calculate_crs, generate_insights, generate_action_plan

# --- PAGE CONFIG ---
st.set_page_config(page_title="CreditSaathi | MSME Credit Intelligence", page_icon="📈", layout="wide")
inject_custom_css()

# --- SESSION STATE INITIALIZATION ---
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'profile_assessed': False,
        'score': 0,
        'category': '',
        'factors': {},
        'gaps': [],
        'action_plan': [],
        'turnover': 0,
        'vintage': 0
    }

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://img.icons8.com/color/96/000000/line-chart.png", width=60)
st.sidebar.title("CreditSaathi")
st.sidebar.caption("Aapka Credit, Aapki Taakat")
st.sidebar.markdown("---")

st.sidebar.markdown("👤 **Logged in as:** KD")

menu = ["🏠 Home", "👤 Assess Profile", "📊 Dashboard", "🏦 Match Lenders", "🧑‍💼 CA/DSA Panel"]
choice = st.sidebar.radio("Navigation", menu)

st.sidebar.markdown("---")
if st.sidebar.button("💬 Check via WhatsApp", use_container_width=True):
    st.sidebar.success("WhatsApp integration triggered!")

# --- HELPER COMPONENTS ---
def render_score_gauge(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Credit Readiness Score", 'font': {'size': 18, 'color': '#0F172A'}},
        number = {'font': {'color': '#1E3A8A', 'size': 48, 'weight': 'bold'}},
        gauge = {
            'axis': {'range': [0, 850], 'tickwidth': 1, 'tickcolor': "#CBD5E1"},
            'bar': {'color': "#14B8A6"},
            'bgcolor': "#F1F5F9",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 500], 'color': '#FEE2E2'},
                {'range': [500, 650], 'color': '#FEF3C7'},
                {'range': [650, 750], 'color': '#E0F2FE'},
                {'range': [750, 850], 'color': '#DCFCE7'}
            ],
            'threshold': {
                'line': {'color': "#0B1F3A", 'width': 3},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'family': "Inter, sans-serif"})
    return fig

# --- ROUTING ---

if choice == "🏠 Home":
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown("<h1 style='font-size: 3.5rem; color: #0B1F3A; font-weight: 800; line-height: 1.2;'>Unlock Capital for your MSME.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; color: #475569; margin-top: 1rem; line-height: 1.6;'>Stop guessing your loan eligibility. CreditSaathi evaluates your business data to generate a definitive Credit Readiness Score (CRS) and matches you with the right lenders instantly.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Check Your Credit Score →", type="primary"):
            st.info("👈 Please select 'Assess Profile' from the sidebar menu to begin.")
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #0F172A;'>How it works</h3>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)
        col_a.info("**1️⃣ Share Details**\n\nEnter basic business & financial info.")
        col_b.warning("**2️⃣ Get Score**\n\nReceive your CRS and Gap Analysis.")
        col_c.success("**3️⃣ Match Lenders**\n\nFind banks tailored to your profile.")

    with col2:
        st.markdown("""
        <div style="background: #FFFFFF; padding: 40px; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1); border: 1px solid #E2E8F0;">
            <h3 style="text-align: center; color: #0B1F3A; margin-top: 0; font-weight: 700;">Sample CRS Profile</h3>
            <div style="text-align: center; font-size: 72px; font-weight: 800; color: #14B8A6; margin: 10px 0; letter-spacing: -2px;">742</div>
            <div style="text-align: center; color: #475569; margin-bottom: 25px; font-weight: 500; font-size: 16px;">Category: <span style="color: #166534; font-weight: 700; background: #DCFCE7; padding: 4px 12px; border-radius: 20px; border: 1px solid #BBF7D0; margin-left: 8px;">Good</span></div>
            <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 25px 0;">
            <div style="color: #334155; font-size: 16px; line-height: 1.8;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div><span style="display: inline-block; width: 24px;">✅</span> <span style="font-weight: 600; color: #0F172A;">Cash Flow</span></div>
                    <div style="color: #166534; font-weight: 500; font-size: 14px; background: #F0FDF4; padding: 2px 10px; border-radius: 6px;">Stable</div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div><span style="display: inline-block; width: 24px;">✅</span> <span style="font-weight: 600; color: #0F172A;">GST Filing</span></div>
                    <div style="color: #166534; font-weight: 500; font-size: 14px; background: #F0FDF4; padding: 2px 10px; border-radius: 6px;">Regular</div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div><span style="display: inline-block; width: 24px;">⚠️</span> <span style="font-weight: 600; color: #0F172A;">Vintage</span></div>
                    <div style="color: #92400E; font-weight: 500; font-size: 14px; background: #FFFBEB; padding: 2px 10px; border-radius: 6px;">Moderate</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif choice == "👤 Assess Profile":
    st.header("Business Profile Assessment")
    st.markdown("Enter your MSME details securely to generate your CRS.")
    
    with st.form("assessment_form"):
        col1, col2 = st.columns(2, gap="large")
        with col1:
            biz_name = st.text_input("Business Name")
            industry = st.selectbox("Industry", ["Manufacturing", "Retail/Trading", "Services", "IT/Tech", "Logistics", "Other"])
            turnover = st.number_input("Annual Turnover (₹)", min_value=0, value=1500000, step=100000)
            vintage = st.number_input("Business Vintage (Years)", min_value=0.0, value=2.0, step=0.5)
            
        with col2:
            bank_balance = st.number_input("Avg Monthly Bank Balance (₹)", min_value=0, value=50000, step=10000)
            gst_status = st.selectbox("GST Filing Status", ["Regular (Monthly)", "Quarterly (QRMP)", "Irregular", "Not Registered"])
            loan_history = st.radio("Existing Loan History?", ["Yes", "No"], horizontal=True)
            emi_amount = st.number_input("Total Monthly EMI (₹)", min_value=0, value=0, step=5000) if loan_history == "Yes" else 0
            
        st.markdown("---")
        st.file_uploader("Upload 6 months Bank Statement (PDF - Optional)", type=["pdf"])
        
        submitted = st.form_submit_button("Generate Credit Intelligence Report", type="primary", use_container_width=True)
        
        if submitted:
            with st.spinner("Analyzing financial footprint..."):
                time.sleep(1.5)
                score, category, factors = calculate_crs(turnover, vintage, bank_balance, loan_history, gst_status, emi_amount)
                
                monthly_income_est = turnover / 12 if turnover > 0 else 1
                foir_indicator = 'high' if (emi_amount / monthly_income_est) > 0.5 else 'low'
                
                gaps = generate_insights(factors, category, gst_status, bank_balance, vintage, foir_indicator)
                action_plan = generate_action_plan(category, gaps)
                
                st.session_state.app_state.update({
                    'profile_assessed': True, 'score': score, 'category': category, 
                    'factors': factors, 'gaps': gaps, 'action_plan': action_plan,
                    'turnover': turnover, 'vintage': vintage
                })
                
            st.success("Profile Analyzed Successfully! Navigate to 'Dashboard' to view insights.")

elif choice == "📊 Dashboard":
    if not st.session_state.app_state['profile_assessed']:
        st.warning("Please assess a profile first to view the dashboard.")
        if st.button("Go to Assessment"):
            st.rerun()
    else:
        state = st.session_state.app_state
        st.header("Credit Intelligence Dashboard")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Top Metrics
        col1, col2, col3 = st.columns(3)
        badge_class = f"badge-{state['category'].lower().replace(' ', '-')}"
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Credit Readiness Score</div>
                <div class="metric-value">{state['score']}</div>
                <div class="badge {badge_class}">{state['category']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Est. Limit Eligibility</div>
                <div class="metric-value">₹ {min(state['turnover'] * 0.2, 5000000):,.0f}</div>
                <div class="badge badge-good">Based on Turnovers</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Profile Strength</div>
                <div class="metric-value">{int((state['score']/850)*100)}%</div>
                <div class="badge badge-good">Complete</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Charts Row
        st.markdown("<br>", unsafe_allow_html=True)
        chart_col1, chart_col2 = st.columns([1, 1], gap="large")
        
        with chart_col1:
            st.markdown("<h4 style='color: #0F172A;'>Score Breakdown</h4>", unsafe_allow_html=True)
            st.plotly_chart(render_score_gauge(state['score']), use_container_width=True)
            
        with chart_col2:
            st.markdown("<h4 style='color: #0F172A;'>Factor Contributions</h4>", unsafe_allow_html=True)
            factors_df = pd.DataFrame(list(state['factors'].items()), columns=['Factor', 'Points'])
            fig = px.bar(factors_df, x='Points', y='Factor', orientation='h',
                         color='Points', color_continuous_scale=['#DBEAFE', '#1E3A8A'])
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=10, b=20), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
        # Analysis Row
        st.markdown("---")
        gap_col, act_col = st.columns(2, gap="large")
        
        with gap_col:
            st.markdown("<h4 style='color: #0F172A;'>📋 Identified Gaps</h4>", unsafe_allow_html=True)
            for gap in state['gaps']:
                st.error(f"**Action Required:** {gap}")
                
        with act_col:
            st.markdown("<h4 style='color: #0F172A;'>🚀 Recommendation Timeline</h4>", unsafe_allow_html=True)
            for item in state['action_plan']:
                border_color = "#EF4444" if item['priority'] == "Critical" else ("#F59E0B" if item['priority'] == "High" else "#22C55E")
                bg_color = "#FEF2F2" if item['priority'] == "Critical" else ("#FFFBEB" if item['priority'] == "High" else "#F0FDF4")
                st.markdown(f"""
                <div style='padding: 16px; border-left: 5px solid {border_color}; background: {bg_color}; margin-bottom: 12px; border-radius: 0 8px 8px 0; border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                        <strong style='color: #0F172A; font-size: 15px;'>{item['time']}</strong>
                        <span style='font-size: 12px; font-weight: 600; color: {border_color};'>{item['priority']} Priority</span>
                    </div>
                    <div style='color: #334155; font-size: 14px;'>{item['action']}</div>
                </div>
                """, unsafe_allow_html=True)

elif choice == "🏦 Match Lenders":
    st.header("Lender Matching Engine")
    
    if not st.session_state.app_state['profile_assessed']:
        st.info("Showing master lender database. Assess your profile to see personalized matches.")
        lenders = get_lender_db()
        st.dataframe(lenders, use_container_width=True)
    else:
        state = st.session_state.app_state
        st.markdown(f"**Your CRS:** `{state['score']}` &nbsp;|&nbsp; **Turnover:** `₹{state['turnover']:,.0f}` &nbsp;|&nbsp; **Vintage:** `{state['vintage']} Yrs`")
        st.markdown("<br>", unsafe_allow_html=True)
        
        lenders = get_lender_db()
        
        def evaluate_eligibility(row):
            if state['score'] >= row['Min Score Required'] and \
               (state['turnover']/100000) >= row['Min Turnover (₹ Lakhs)'] and \
               state['vintage'] >= row['Min Vintage (Years)']:
                return "✅ Eligible"
            elif state['score'] >= row['Min Score Required'] - 50:
                return "⚠️ Improve Score"
            else:
                return "❌ Not Eligible"
                
        lenders['Status'] = lenders.apply(evaluate_eligibility, axis=1)
        lenders['Sort_Key'] = lenders['Status'].map({"✅ Eligible": 0, "⚠️ Improve Score": 1, "❌ Not Eligible": 2})
        lenders = lenders.sort_values('Sort_Key').drop('Sort_Key', axis=1)
        
        st.dataframe(
            lenders.style.applymap(
                lambda v: 'color: #166534; background-color: #DCFCE7; font-weight: 600;' if v == '✅ Eligible' 
                else ('color: #92400E; background-color: #FEF3C7; font-weight: 600;' if v == '⚠️ Improve Score' 
                else 'color: #991B1B; background-color: #FEE2E2; font-weight: 600;'), 
                subset=['Status']
            ),
            use_container_width=True,
            hide_index=True
        )

elif choice == "🧑‍💼 CA/DSA Panel":
    st.header("CA / DSA Partner Dashboard")
    st.markdown("Manage your client pipeline and track their credit readiness.")
    
    clients = get_ca_clients()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clients Managed", len(clients))
    col2.metric("Ready for Disbursement", len(clients[clients['Status'].isin(['Ready for Loan', 'Excellent', 'Good'])]))
    col3.metric("Avg Portfolio Score", int(clients['Current CRS'].mean()), delta="12 pts")
    
    st.markdown("### Client Roster")
    st.dataframe(
        clients.style.background_gradient(cmap="Blues", subset=['Current CRS']),
        use_container_width=True,
        hide_index=True
    )
