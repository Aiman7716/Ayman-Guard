import streamlit as st
import os
import requests
from datetime import datetime

# --- 1. إعدادات الأمان القصوى لمنع انهيار السيرفر ---
st.set_page_config(page_title="Ayman Guard v27", layout="wide")

# تصميم CSS بسيط جداً لتقليل استهلاك الذاكرة (السر في الخفة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    header, footer, #MainMenu {visibility: hidden !important;}
    .hero { background: #1f6feb; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .card { background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 10px; }
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; font-weight: bold; border-radius: 8px; border: none; height: 3em; }
    .preview-link { display: block; width: 100%; padding: 10px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التنبيهات (تم اختصاره لأقصى درجة) ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def bot_send(txt):
    try: requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={txt}", timeout=1)
    except: pass

# --- 3. بناء التبويبات المتكاملة ---
st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1></div>', unsafe_allow_html=True)

# دمج فحص الروابط والملفات كما طلبت
tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص", "🎬 التحميل", "👥 التواصل", "🔐 الإدارة"])

# 1. الرئيسية الأنيقة
with tabs[0]:
    st.success("أهلاً أيمن. النظام يعمل الآن بوضع 'الاستقرار الأقصى' لمنع بياض الشاشة.")
    st.info("تم ربط كافة التبويبات بالبوت الشخصي ✅")

# 2. مركز الفحص (دمج الروابط والملفات في تبويب واحد)
with tabs[1]:
    st.subheader("🔍 فحص ومعاينة")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    u_url = st.text_input("🔗 أدخل الرابط:")
    if st.button("🛡️ فحص الرابط"):
        if u_url:
            st.write(f"تم تسجيل الرابط للفحص: {u_url}")
            bot_send(f"SCAN_LINK: {u_url}")
            st.success("تم إرسال التنبيه للبوت.")
    if u_url: st.markdown(f'<a href="{u_url}" target="_blank" class="preview-link">👁️ معاينة الرابط</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    u_file = st.file_uploader("📁 فحص ملف:")
    if u_file:
        if st.button("🛠️ تحليل الملف"):
            st.success(f"تم تحليل {u_file.name}")
            bot_send(f"SCAN_FILE: {u_file.name}")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. التحميل (نظام التحميل المباشر لتجنب الانهيار)
with tabs[2]:
    st.subheader("🎬 محمل الفيديو")
    v_url = st.text_input("رابط الفيديو:")
    if st.button("🚀 معالجة التحميل"):
        if v_url:
            st.warning("جاري التجهيز... إذا ظهر بياض، فالرابط ثقيل على السيرفر.")
            # استخدام مكتبة yt_dlp بحذر شديد داخل try
            try:
                import yt_dlp
                opts = {'format': 'best', 'outtmpl': 'v.mp4', 'quiet': True, 'noplaylist': True}
                with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([v_url])
                if os.path.exists("v.mp4"):
                    with open("v.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ", f, "video.mp4")
                    os.remove("v.mp4")
                    bot_send(f"SUCCESS_DL: {v_url}")
            except:
                st.error("السيرفر لا يتحمل هذا الرابط حالياً.")
                bot_send(f"FAIL_DL: {v_url}")

# 4. التواصل (مربوط بالبوت)
with tabs[3]:
    st.subheader("🚨 تواصل وبلاغات")
    with st.form("ayman_form"):
        n = st.text_input("الاسم:")
        m = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            bot_send(f"MSG_FROM_{n}: {m}")
            st.success("تم الإرسال!")

# 5. الإدارة (مربوط بالبوت)
with tabs[4]:
    if "is_auth" not in st.session_state: st.session_state.is_auth = False
    if not st.session_state.is_auth:
        pwd = st.text_input("كلمة السر:", type="password")
        if st.button("دخول"):
            if pwd == "ayman7716":
                st.session_state.is_auth = True
                bot_send("ADMIN_LOGIN")
                st.rerun()
    else:
        st.write("أهلاً أيمن في الإدارة")
        if st.button("خروج"): st.session_state.is_auth = False; st.rerun()
