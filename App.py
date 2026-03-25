import streamlit as st
import tldextract
import time

# --- 1. إعدادات الأمان والتنسيق (حل مشكلة التشوه البصري) ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        
        /* 🚨 منع ظهور keyboard_ar نهائياً عبر حظر أيقونات النظام 🚨 */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, 
        [data-testid="stIcon"], .stExpander svg, .st-emotion-cache-6q9sum { 
            display: none !important; 
            visibility: hidden !important; 
        }

        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        
        .history-item {
            background-color: #f9f9f9; padding: 10px; border-radius: 8px;
            margin-bottom: 5px; border-right: 4px solid #00d4ff; color: #333;
        }

        div.stButton > button {
            background-color: #ff4b4b !important; color: white !important;
            border-radius: 12px !important; width: 100% !important; height: 3.5em !important;
            border: none !important;
        }
        
        .trusted-badge {
            background-color: #e3f2fd; border-right: 5px solid #2196f3;
            padding: 15px; border-radius: 10px; color: #0d47a1; font-weight: bold; text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []
if 'blacklist' not in st.session_state: st.session_state.blacklist = {}

# --- 2. محرك الفحص ---
def security_scan(url):
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    partner = "alhossam7710140-001-site1.mtempurl.com"
    official = u.endswith('.gov.sa') or u.endswith('.edu.sa')
    trusted = ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa']

    if partner in u: return "PARTNER", domain_full
    elif official or domain_full in trusted: return "
