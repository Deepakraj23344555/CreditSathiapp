import streamlit as st

def inject_premium_dark_theme():
    """Injects the global Dark Navy premium fintech theme across the entire app."""
    css = """
    <style>
        /* Import Premium Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* ----------------------------------------------------
           1. GLOBAL BACKGROUND & TYPOGRAPHY
           ---------------------------------------------------- */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, sans-serif !important;
            color: #FFFFFF !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* The Ultimate Radial Gradient Background (Locks to viewport) */
        .stApp {
            background: radial-gradient(circle at 15% 0%, #112A4C 0%, #0B1F3A 40%, #05101F 100%) !important;
            background-attachment: fixed !important;
        }

        /* Hide Streamlit Clutter */
        header {background: transparent !important; visibility: hidden;}
        footer {visibility: hidden;}

        /* Typography Contrast & Readability Classes */
        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }
        .text-primary { color: #FFFFFF !important; }
        .text-secondary { color: #CBD5F5 !important; line-height: 1.6; }
        .text-muted { 
            color: #94A3B8 !important; 
            font-size: 14px; 
            line-height: 1.6; 
            letter-spacing: 0.2px; /* Improves small text readability */
            font-weight: 400;
        }
        .accent-text { color: #14B8A6 !important; font-weight: 600; }

        /* ----------------------------------------------------
           2. SIDEBAR & NAVIGATION
           ---------------------------------------------------- */
        [data-testid="stSidebar"] {
            background-color: rgba(5, 16, 31, 0.8) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        [data-testid="stSidebarNav"] span {
            color: #CBD5F5 !important;
            font-weight: 500;
            font-size: 15px;
        }
        /* Active Sidebar Item */
        [data-testid="stSidebarNav"] div[data-testid="stSidebarNavItems"] > div:hover {
            background-color: rgba(20, 184, 166, 0.1) !important;
        }

        /* ----------------------------------------------------
           3. PREMIUM CONTENT CARDS (GLASSMORPHISM)
           ---------------------------------------------------- */
        .premium-card {
            background: rgba(17, 42, 76, 0.45); /* Soft lighter dark #112A4C */
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
            margin-bottom: 24px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        .premium-card:hover {
            transform: translateY(-2px);
            border-color: rgba(20, 184, 166, 0.3); /* Teal border glow */
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25), 0 0 20px rgba(20, 184, 166, 0.1);
        }

        /* ----------------------------------------------------
           4. GLOWING GRADIENT BUTTONS
           ---------------------------------------------------- */
        .stButton > button {
            background: linear-gradient(135deg, #1E3A8A 0%, #14B8A6 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(20, 184, 166, 0.2) !important;
            width: 100%;
        }
        .stButton > button:hover {
            box-shadow: 0 8px 25px rgba(20, 184, 166, 0.4) !important;
            transform: translateY(-2px) scale(1.01) !important;
            color: #FFFFFF !important;
        }

        /* ----------------------------------------------------
           5. FORM INPUTS (High Contrast Dark Mode)
           ---------------------------------------------------- */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #FFFFFF !important;
            border-radius: 10px !important;
            font-size: 15px !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
            border-color: #14B8A6 !important;
            box-shadow: 0 0 0 1px #14B8A6 !important;
            background-color: rgba(255, 255, 255, 0.06) !important;
        }
        /* Placeholder text contrast */
        ::placeholder { color: #64748B !important; opacity: 1 !important; }

        /* ----------------------------------------------------
           6. TABS RE-STYLING
           ---------------------------------------------------- */
        .stTabs [data-baseweb="tab-list"] {
            background-color: transparent !important;
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            color: #CBD5F5 !important;
            background-color: transparent !important;
            border-bottom: 2px solid transparent !important;
            padding-bottom: 12px !important;
        }
        .stTabs [aria-selected="true"] {
            color: #14B8A6 !important;
            border-bottom: 2px solid #14B8A6 !important;
            font-weight: 600 !important;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
