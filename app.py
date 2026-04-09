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

# Using KD as the authenticated user/CA name contextually
st.sidebar.markdown("👤 **Logged in as:** KD")

menu = ["🏠 Home", "👤 Assess Profile", "📊 Dashboard", "🏦 Match Lenders", "🧑‍💼 CA/DSA Panel"]
choice = st.sidebar.radio("Navigation", menu)

st.sidebar.markdown("---")
if st.sidebar.button("💬 Check via WhatsApp"):
    st.sidebar.success("WhatsApp integration triggered! (Mock)")

# --- HELPER COMPONENTS ---
def render_score_gauge(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Credit Readiness Score (CRS)", 'font': {'size': 20, 'color': '#0B1F3A'}},
        gauge = {
            'axis': {'range': [0, 850], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#14B8A6"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 500], 'color': '#FEE2E2'},
                {'range': [500, 650], 'color': '#FEF3C7'},
                {'range': [650, 750], 'color': '#E0F2FE'},
                {'range': [750, 850], 'color': '#DCFCE7'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# --- ROUTING ---

if choice == "🏠 Home":
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("<h1 style='font-size: 3rem;'>Unlock Capital for your MSME.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; color: #64748B;'>Stop guessing your loan eligibility. CreditSaathi evaluates your business data to generate a definitive Credit Readiness Score (CRS) and matches you with the right lenders.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Check Your Credit Score →", key="home_cta"):
            st.info("👈 Navigate to 'Assess Profile' in the sidebar to begin.")
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### How it works")
        col_a, col_b, col_c = st.columns(3)
        col_a.info("1️⃣ Share Business Details")
        col_b.warning("2️⃣ Get CRS & Gap Analysis")
        col_c.success("3️⃣ Match with Lenders")

    with col2:
        # Abstract UI representation
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #E2E8F0;">
            <h3 style="text-align: center; color: #1E3A8A;">Sample CRS Profile</h3>
            <div style="text-align: center; font-size: 60px; font-weight: bold; color: #14B8A6; margin: 20px 0;">742</div>
            <div style="text-align: center; color: #64748B; margin-bottom: 20px;">Category: <span style="color: #22C55E; font-weight: bold;">Good</span></div>
            <hr style="border: 0; border-top: 1px solid #E2E8F0;">
            <p>✅ Cash Flow: Stable</p>
            <p>✅ GST: Regular</p>
            <p>⚠️ Vintage: Moderate</p>
        </div>
        """, unsafe_allow_html=True)

elif choice == "👤 Assess Profile":
    st.header("Business Profile Assessment")
    st.markdown("Enter your MSME details securely to generate your CRS.")
    
    with st.form("assessment_form"):
        col1, col2 = st.columns(2)
        with col1:
            biz_name = st.text_input("Business Name")
            industry = st.selectbox("Industry", ["Manufacturing", "Retail/Trading", "Services", "IT/Tech", "Logistics", "Other"])
            turnover = st.number_input("Annual Turnover (₹)", min_value=0, value=1500000, step=100000)
            vintage = st.number_input("Business Vintage (Years)", min_value=0.0, value=2.0, step=0.5)
            
        with col2:
            bank_balance = st.number_input("Average Monthly Bank Balance (₹)", min_value=0, value=50000, step=10000)
            gst_status = st.selectbox("GST Filing Status", ["Regular (Monthly)", "Quarterly (QRMP)", "Irregular", "Not Registered"])
            loan_history = st.radio("Existing Loan History?", ["Yes", "No"], horizontal=True)
            emi_amount = st.number_input("Total Monthly EMI (₹)", min_value=0, value=0, step=5000) if loan_history == "Yes" else 0
            
        st.markdown("---")
        st.caption("Optional: Upload Bank Statement (PDF) for automated parsing (Mock feature)")
        st.file_uploader("Upload 6 months Bank Statement", type=["pdf"])
        
        submitted = st.form_submit_button("Generate Credit Intelligence Report")
        
        if submitted:
            with st.spinner("Analyzing financial footprint..."):
                time.sleep(1.5) # Simulate processing
                score, category, factors = calculate_crs(turnover, vintage, bank_balance, loan_history, gst_status, emi_amount)
                
                monthly_income_est = turnover / 12 if turnover > 0 else 1
                foir_indicator = 'high' if (emi_amount / monthly_income_est) > 0.5 else 'low'
                
                gaps = generate_insights(factors, category, gst_status, bank_balance, vintage, foir_indicator)
                action_plan = generate_action_plan(category, gaps)
                
                # Save to session state
                st.session_state.app_state.update({
                    'profile_assessed': True, 'score': score, 'category': category, 
                    'factors': factors, 'gaps': gaps, 'action_plan': action_plan,
                    'turnover': turnover, 'vintage': vintage
                })
                
            st.success("Profile Analyzed Successfully! Navigate to 'Dashboard' to view insights.")

elif choice == "📊 Dashboard":
    if not st.session_state.app_state['profile_assessed']:
        st.warning("Please assess a profile first to view the dashboard.")
        st.info("👈 Go to 'Assess Profile' in the sidebar.")
    else:
        state = st.session_state.app_state
        st.header("Credit Intelligence Dashboard")
        
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
                <div class="badge badge-good">Based on 20% Turnover</div>
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
        st.markdown("### Score Breakdown")
        chart_col1, chart_col2 = st.columns([1, 1])
        
        with chart_col1:
            st.plotly_chart(render_score_gauge(state['score']), use_container_width=True)
            
        with chart_col2:
            # Bar chart of factors
            factors_df = pd.DataFrame(list(state['factors'].items()), columns=['Factor', 'Points Contribution'])
            fig = px.bar(factors_df, x='Points Contribution', y='Factor', orientation='h',
                         color='Points Contribution', color_continuous_scale=['#1E3A8A', '#14B8A6'])
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
        # Analysis Row
        st.markdown("---")
        st.markdown("### 📋 Gap Analysis & Action Plan")
        gap_col, act_col = st.columns(2)
        
        with gap_col:
            st.markdown("#### Identified Gaps")
            for gap in state['gaps']:
                st.error(f"⚠️ {gap}")
                
        with act_col:
            st.markdown("#### Recommendation Timeline")
            for item in state['action_plan']:
                color = "red" if item['priority'] == "Critical" else ("orange" if item['priority'] == "High" else "green")
                st.markdown(f"""
                <div style='padding: 10px; border-left: 4px solid {color}; background: white; margin-bottom: 10px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
                    <strong>{item['time']}</strong>: {item['action']} <br>
                    <span style='font-size: 12px; color: gray;'>Priority: {item['priority']}</span>
                </div>
                """, unsafe_allow_html=True)

        # Score Tracking Simulation
        with st.expander("📈 View Score Projection"):
            st.markdown("Simulated trajectory if Action Plan is followed:")
            dates = pd.date_range(start=pd.Timestamp.today(), periods=6, freq='ME')
            scores = [state['score']]
            for i in range(1, 6):
                # Simulate growth converging towards 800
                new_score = scores[-1] + (800 - scores[-1]) * 0.15
                scores.append(int(new_score))
            
            proj_df = pd.DataFrame({"Date": dates, "Projected Score": scores})
            fig_proj = px.line(proj_df, x="Date", y="Projected Score", markers=True)
            fig_proj.update_traces(line_color="#14B8A6", line_width=3, marker_size=8)
            fig_proj.update_layout(height=300, yaxis_range=[300, 850])
            st.plotly_chart(fig_proj, use_container_width=True)


elif choice == "🏦 Match Lenders":
    st.header("Lender Matching Engine")
    
    if not st.session_state.app_state['profile_assessed']:
        st.warning("Assess your profile first to see personalized lender matches.")
        lenders = get_lender_db()
        st.dataframe(lenders, use_container_width=True)
    else:
        state = st.session_state.app_state
        st.markdown(f"**Your CRS:** {state['score']} | **Turnover:** ₹{state['turnover']:,.0f} | **Vintage:** {state['vintage']} Yrs")
        
        lenders = get_lender_db()
        
        # Evaluation Logic
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
        
        # Sort so Eligible is at top
        lenders['Sort_Key'] = lenders['Status'].map({"✅ Eligible": 0, "⚠️ Improve Score": 1, "❌ Not Eligible": 2})
        lenders = lenders.sort_values('Sort_Key').drop('Sort_Key', axis=1)
        
        st.dataframe(
            lenders.style.applymap(
                lambda v: 'color: green; font-weight: bold;' if v == '✅ Eligible' 
                else ('color: orange; font-weight: bold;' if v == '⚠️ Improve Score' else 'color: red;'), 
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
    col1.metric("Total Clients", len(clients))
    col2.metric("Ready for Disbursement", len(clients[clients['Status'].isin(['Ready for Loan', 'Excellent', 'Good'])]))
    col3.metric("Avg Portfolio Score", int(clients['Current CRS'].mean()))
    
    st.markdown("### Client Roster")
    st.dataframe(
        clients.style.background_gradient(cmap="Blues", subset=['Current CRS']),
        use_container_width=True,
        hide_index=True
    )
