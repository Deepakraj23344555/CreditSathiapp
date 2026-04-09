import streamlit as st
import time

def render_ai_advisor():
    st.title("🤖 AI Credit Advisor")
    st.markdown("Ask anything about your score, loan eligibility, or business finance.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"Hi {st.session_state.user_inputs.get('name', '')}! I've analyzed your CRS of {st.session_state.crs_score}. How can I help you secure capital today?"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("E.g., How can I qualify for a 10 Lakh loan?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(1.5) # Fake API delay
                # Mock LLM Response for guaranteed runtime without API keys
                response = f"Based on your profile (Score: {st.session_state.crs_score}, Turnover: ₹{st.session_state.user_inputs.get('turnover',0):,}), to get a ₹10 Lakh loan you need to maintain a monthly balance of at least ₹80,000 and clear your pending GST returns. Lenders like HDFC and Bajaj will offer you ~14% interest if you achieve this in the next 60 days."
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
