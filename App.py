import streamlit as st
import tldextract
import time
import smtplib
from email.mime.text import MIMEText

# --- 1. إعدادات التنسيق الاحترافي (منع تداخل الكلمات) ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        /* إخفاء تام لأي أيقونة نظام تسبب تشوه keyboard_ar */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, 
        [data-testid="stIcon"], .stExpander svg { 
            display: none !important; visibility: hidden !important; 
        }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; margin-bottom: 20px; }
        .history-card {
            background-color: #f8f9fa; padding: 12px; border-radius: 8px;
            margin-bottom: 8px; border-right: 5px solid #00d4ff; color: #202124;
        }
        div.stButton > button {
            background: linear-gradient(90deg, #ff4b4b, #ff7676) !important;
            color: white !important; border-radius: 12px !important;
            width: 100% !important; height: 3.5em !important; font-weight: bold !important;
        }
        .success-badge {
            background-color: #e8f0fe; border-right: 6px solid #1a73e8;
            padding: 15px; border-radius: 10px; color: #174ea6; font-weight: bold; text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# تهيئة الذاكرة
if 'history' not in st.session_state: st.session_state.history = []
if 'blacklist' not in st.session_state: st.session_state.blacklist = {}

# --- 2. وظيفة التنبيه البريدي ---
def send_email_alert(link):
    # ملاحظة: استبدل بالبيانات الحقيقية في حساب جوجل الخاص بك
    sender = "ayman.shield@gmail.com"
    receiver = "ayman@example.com" 
    pw = "your_app_password"
    
    msg = MIMEText(f"قام مستخدم بالتبليغ عن رابط محتال: {link}")
    msg['Subject'] = '🚨 بلاغ اختراق جديد - درع أيمن'
    msg['From'] = sender
    msg['To'] = receiver
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, pw)
            server.sendmail(sender, receiver, msg.as_string())
        return True
    except: return False

# --- 3. محرك فحص الروابط ---
def security_scan(url):
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext
