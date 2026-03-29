import streamlit as st
import requests

# --- 1. الإعدادات وتصميم الواجهة ---
st.set_page_config(page_title="Ayman Shield", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    header, footer, #MainMenu {visibility: hidden !important;}
    
    /* تصميم البطاقة الرئيسية */
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التنبيهات (البوت) ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def notify_ayman(msg):
    try: requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}", timeout=1)
    except: pass

# --- 3. إنشاء التبويبات الخمسة المتفق عليها ---
st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الحماية المتكامل v29</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص", "🎬 محمل الفيديو", "👥 التواصل والمجتمع", "🔐 الإدارة"])

# سنبدأ بالعمل على "الرئيسية" الآن
with tabs[0]:
    st.markdown("### ⚡ اختصارات الوصول السريع")
    st.info("مرحباً أيمن! اختر المهمة التي تريد القيام بها من التبويبات أعلاه، أو استخدم الأزرار السريعة (التي سنبرمجها في الخطوة القادمة).")
