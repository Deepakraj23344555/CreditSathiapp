import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from ui_components import COLORS, apply_dark_theme

def render_predictive_cashflow(current_balance):
    """Simulates a Prophet/LSTM time-series cashflow prediction."""
    st.markdown("### 🔮 Predictive Cashflow Radar")
    st.markdown("<p class='text-muted'>AI forecasting based on your historical transaction velocity.</p>", unsafe_allow_html=True)
    
    # Generate mock future data
    days = ["Today", "Day 5", "Day 10", "Day 15 (Payroll)", "Day 20", "Day 25", "Day 30"]
    balances = [current_balance, current_balance*0.9, current_balance*0.7, -50000, 20000, 80000, 110000]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=balances, mode='lines+markers', name='Projected Balance', line=dict(color=COLORS['accent'], width=3)))
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS['danger'], annotation_text="Cash Shortfall Risk")
    
    fig = apply_dark_theme(fig)
    fig.update_layout(height=250, margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    if any(b < 0 for b in balances):
        st.error("⚠️ AI detects a potential ₹50,000 cash shortfall in 15 days. Tap 'Get Loans' to secure an overdraft facility now.")

def render_virtual_card(business_name):
    """Renders an Embedded Finance Virtual Credit Card."""
    st.markdown("### 💳 CreditSaathi Capital Card")
    st.markdown("<p class='text-muted'>Pre-approved embedded finance limit unlocked.</p>", unsafe_allow_html=True)
    
    card_html = f"""
    <div style="background: linear-gradient(135deg, #1E3A8A 0%, #14B8A6 100%); border-radius: 16px; padding: 24px; color: white; box-shadow: 0 10px 30px rgba(20,184,166,0.3); max-width: 400px; position: relative; overflow: hidden;">
        <div style="position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
        <h3 style="margin: 0; font-size: 20px; font-weight: 700;">CreditSaathi <span style="font-weight: 300;">CORPORATE</span></h3>
        <p style="font-family: monospace; font-size: 18px; letter-spacing: 2px; margin: 30px 0 10px 0;">**** **** **** 4920</p>
        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <p style="margin: 0; font-size: 10px; opacity: 0.8; text-transform: uppercase;">Cardholder</p>
                <p style="margin: 0; font-size: 16px; font-weight: 600; text-transform: uppercase;">{business_name}</p>
            </div>
            <div style="text-align: right;">
                <p style="margin: 0; font-size: 10px; opacity: 0.8; text-transform: uppercase;">Available Limit</p>
                <p style="margin: 0; font-size: 20px; font-weight: 700;">₹5,00,000</p>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Activate Virtual Card Now", use_container_width=True)

def render_invoice_discounting():
    """Simulates B2B Invoice Discounting / Supply Chain Finance."""
    st.markdown("### 📄 Invoice Discounting (Get Paid Early)")
    st.markdown("<p class='text-muted'>Don't wait 90 days for corporate clients to pay. Upload your invoice and get cash instantly.</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Corporate Buyer (e.g., Reliance, Tata)")
            inv_amt = st.number_input("Invoice Amount (₹)", min_value=0, step=10000, value=500000)
        with col2:
            st.file_uploader("Upload GST Invoice (PDF)")
            
        if st.button("Check Discounting Offer", use_container_width=True):
            st.success(f"✅ Offer Unlocked! We can advance **₹{int(inv_amt * 0.96):,}** to your bank account today (4% discount fee). Buyer will pay us in 90 days.")
        st.markdown("</div>", unsafe_allow_html=True)
