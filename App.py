import streamlit as st
import os
import sqlite3
import requests
from datetime import datetime

# --- 1. إعدادات الواجهة السيادية ---
st.set_page_config(page_title="Ayman Guard Root v23", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .main-card { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px; }
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; border: none; }
    .download-btn { display: block; width: 100%; padding: 15px; background-color: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 12px; font-weight: bold; margin-top: 10px; border: 1px solid #fff; }
    </style>
""", unsafe_allow_html=True)

# --- 2. المحرك والمصادقة ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def log_to_bot(txt):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": txt}, timeout=2)
    except: pass

# --- 3. بناء الهيكل (تجنب NameError و IndentError) ---
st.markdown('<div class="main-card"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار الجذري المستقر v23.0</p></div>', unsafe_allow_html=True)

# استخدام قائمة صريحة للتبويبات لمنع NameError
tab_names = ["🏠 الرئيسية", "🎬 التحميل", "🔍 الفحص", "🔐 الإدارة"]
t = st.tabs(tab_names)

with t[0]:
    st.success("✅ تم ضبط المسافات البرمجية وتثبيت المحرك بنجاح.")
    st.info("يا أيمن، هذا الكود يعالج الفيديو مباشرة في المتصفح لتجنب أخطاء السيرفر.")

with t[1]:
    st.subheader("🎬 محمل الفيديو المتطور")
    url_input = st.text_input("أدخل رابط الفيديو:")
    if st.button("🚀 استخراج رابط التحميل"):
        if url_input:
            with st.spinner("جاري المعالجة..."):
                try:
                    import yt_dlp
                    ydl_opts = {'format': 'best', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url_input, download=False)
                        direct_link = info.get('url', None)
                    if direct_link:
                        st.video(url_input)
                        st.markdown(f'<a href="{direct_link}" target="_blank" class="download-btn">📥 اضغط هنا للتحميل المباشر</a>', unsafe_allow_html=True)
                        log_to_bot("🎬 نجاح استخراج رابط فيديو")
                    else:
                        st.error("تعذر العثور على رابط مباشر.")
                except Exception as e:
                    st.error(f"حدث خطأ في المحرك: {e}")

with t[2]:
    st.subheader("🔍 فحص الروابط")
    test_url = st.text_input("رابط الفحص:")
    if st.button("🛡️ ابدأ الفحص"):
        try:
            res = requests.head(test_url, timeout=5)
            st.success(f"الرابط نشط ({res.status_code})")
        except:
            st.error("الرابط غير متاح")

with t[3]:
    if 'auth' not in st.session_state: st.session_state.auth = False
    if not st.session_state.auth:
        pwd = st.text_input("كلمة السر:", type="password")
        if st.button("دخول"):
            if pwd == "ayman7716":
                st.session_state.auth = True
                st.rerun()
    else:
        st.write("🔓 لوحة التحكم مفتوحة")
        if st.button("تسجيل خروج"):
            st.session_state.auth = False
            st.rerun()
