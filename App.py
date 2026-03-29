import streamlit as st
import yt_dlp
import requests
import time
import random

# --- 1. الإعدادات والذاكرة السيادية ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي v37.0",
        'admin_password': "Ayman2026"  # كلمة المرور الافتراضية
    }

if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None
if 'v_ready' not in st.session_state: st.session_state.v_ready = False
if 'v_data' not in st.session_state: st.session_state.v_data = None
if 'v_url' not in st.session_state: st.session_state.v_url = ""

# --- 2. التنسيق البصري (CSS) ---
st.set_page_config(page_title=st.session_state.settings['site_title'], layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; border: 1px solid #30363d;
    }
    .contact-btn {
        background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; border: 1px solid #ffffff !important;
        font-weight: bold !important; text-decoration: none !important;
        display: block; padding: 15px; text-align: center; margin-bottom: 10px;
    }
    .bot-btn {
        background: linear-gradient(90deg, #0088cc, #00aaff) !important;
        color: white !important; border-radius: 15px !important;
        padding: 20px; font-size: 20px !important; text-decoration: none !important;
        display: block; text-align: center; font-weight: bold; border: 2px solid #ffffff;
    }
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; font-weight: bold; height: 3.5em; border: none; }
    button[kind="secondary"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. محرك الربط مع تليجرام (2FA) ---
def send_telegram_code(code):
    TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
    MY_ID = "906233240" 
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": MY_ID, "text": f"🔐 مرحباً أيمن، كود الدخول الخاص بك هو: {code}"})
        st.success("✅ تم إرسال الكود السري لحسابك الشخصي في تليجرام.")
    except:
        st.error("⚠️ فشل الاتصال بالبوت.")

# --- 4. واجهة الموقع الرئيسية ---
st.markdown(f'<div class="hero-section"><h1>{st.session_state.settings["site_title"]}</h1><p>{st.session_state.settings["site_sub"]}</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🎬 مركز التحميل", "🔍 مركز الفحص", "🛡️ الحماية والدعم", "⚙️ الإدارة"])

# (التبويبات الأخرى تبقى كما هي في الكود السابق لضمان العمل)
with tabs[0]: st.info("مرحباً بك يا أيمن. النظام محمي بالكامل.")
with tabs[1]:
    u_in = st.text_input("رابط الفيديو:")
    if st.button("🚀 بدء المعالجة"):
        if u_in: st.success("جاري الجلب...")
with tabs[2]:
    st.text_input("رابط للفحص:")
    st.button("🛡️ ابدأ فحص الرابط")
    st.markdown("---")
    st.file_uploader("فحص ملف:", type=['apk', 'pdf', 'png', 'jpg', 'zip'])
    st.button("🔍 ابدأ فحص الملف المرفوع")
with tabs[3]:
    st.markdown('<a href="https://t.me/Aiman_Guard_2026_bot" target="_blank" class="bot-btn">🤖 بوت الدرع</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://wa.me/966556868717" target="_blank" class="contact-btn">📱 واتساب</a>', unsafe_allow_html=True)

# --- التبويب 5: لوحة الإدارة (مع ميزة تغيير كلمة المرور) ---
with tabs[4]:
    if not st.session_state.is_admin:
        st.subheader("🔐 بوابة المسؤول")
        pwd_input = st.text_input("كلمة مرور الإدارة الحالية:", type="password")
        if st.button("🔑 طلب كود التحقق (2FA)"):
            if pwd_input == st.session_state.settings['admin_password']:
                st.session_state.auth_code = str(random.randint(111111, 999999))
                send_telegram_code(st.session_state.auth_code)
            else: st.error("❌ كلمة المرور غير صحيحة!")
        
        if st.session_state.auth_code:
            v_code = st.text_input("أدخل الكود من تليجرام:")
            if st.button("✅ تأكيد الدخول"):
                if v_code == st.session_state.auth_code:
                    st.session_state.is_admin = True
                    st.rerun()
    else:
        st.success("🔓 أهلاً أيمن في غرفة التحكم.")
        if st.button("🚪 خروج آمن"):
            st.session_state.is_admin = False
            st.rerun()
        
        st.markdown("---")
        # --- الميزة الجديدة: تغيير كلمة المرور ---
        st.subheader("🔑 تأمين الحساب")
        with st.expander("تغيير كلمة مرور الإدارة"):
            new_pwd = st.text_input("كلمة المرور الجديدة:", type="password")
            confirm_pwd = st.text_input("تأكيد كلمة المرور الجديدة:", type="password")
            if st.button("💾 حفظ كلمة المرور الجديدة"):
                if new_pwd and new_pwd == confirm_pwd:
                    st.session_state.settings['admin_password'] = new_pwd
                    st.success("✅ تم تغيير كلمة المرور بنجاح! سيتم استخدامها في المرة القادمة.")
                else:
                    st.error("⚠️ كلمتا المرور غير متطابقتين أو الحقل فارغ.")

        st.markdown("---")
        st.subheader("⚙️ تعديل مسميات الموقع")
        st.session_state.settings['site_title'] = st.text_input("عنوان الموقع:", st.session_state.settings['site_title'])
        if st.button("💾 حفظ وتطبيق"):
            st.success("✅ تم تحديث النظام!")
            st.rerun()
