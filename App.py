import streamlit as st
import tldextract, sqlite3, os, requests, hashlib
from datetime import datetime

# --- الإعدادات ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

def send_telegram_msg(message):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except: pass

def check_virustotal(file_content):
    file_hash = hashlib.sha256(file_content).hexdigest()
    headers = {"x-apikey": VT_API_KEY}
    try:
        response = requests.get(f"https://www.virustotal.com/api/v3/files/{file_hash}", headers=headers)
        if response.status_code == 200: return response.json()['data']['attributes']['last_analysis_stats']
    except: return None
    return None

# --- التصميم السيبراني ---
st.set_page_config(page_title="درع أيمن الاحترافي", page_icon="🛡️", layout="centered")
st.markdown("""<style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .main-title { text-align: center; background: linear-gradient(90deg, #00d4ff, #0055ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.8rem; font-weight: bold; text-shadow: 2px 2px 15px rgba(0, 212, 255, 0.4); margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #1a1c23; padding: 10px; border-radius: 15px; direction: RTL; }
    .stButton>button { background: linear-gradient(45deg, #00d4ff, #0055ff); color: white; border-radius: 12px; width: 100%; height: 3.5em; border: none; }
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
    input, textarea { background-color: #161b22 !important; color: white !important; direction: RTL !important; }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي</div>', unsafe_allow_html=True)

tabs = st.tabs(["🔍 فحص ذكي المطور", "🔗 فحص الروابط", "📧 اتصل بنا", "🔐 الإدارة"])

with tabs[0]:
    st.subheader("📁 فحص الملفات (عالمي + محلي)")
    up_file = st.file_uploader("ارفع الملف للفحص الشامل:", type=None)
    if up_file:
        with st.spinner('جاري التحليل...'):
            content = up_file.read()
            # 1. الفحص المحلي (ذكاء الدرع الخاص)
            is_eicar = b"EICAR-STANDARD-ANTIVIRUS-TEST-FILE" in content
            
            # 2. الفحص العالمي
            res = check_virustotal(content)
            
            if is_eicar:
                st.error("🚨 إنذار: تم اكتشاف كود اختبار الفيروسات (EICAR) عبر الفحص المحلي!")
                send_telegram_msg(f"🚨 تنبيه أمني من درع أيمن:\nتم اكتشاف ملف اختبار فيروسات محلياً!\nالملف: {up_file.name}")
            elif res and res.get('malicious', 0) > 0:
                st.error(f"🚨 تحذير: تم اكتشاف {res['malicious']} تهديد عالمي!")
                send_telegram_msg(f"🚨 تهديد عالمي!\nالملف: {up_file.name}\nالعدد: {res['malicious']}")
            elif res:
                st.success("✅ الملف آمن ومفحوص عالمياً.")
            else:
                st.warning("ℹ️ الملف جديد على قاعدة البيانات العالمية، لكنه يبدو آمناً محلياً.")

# (بقية التبويبات تظل كما هي في كودك السابق)
