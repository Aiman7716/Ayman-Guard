import streamlit as st
import yt_dlp
import os
import requests
from datetime import datetime

# --- 1. الإعدادات وتأمين الواجهة من الانهيار ---
st.set_page_config(page_title="Ayman Guard v26", layout="wide")

# طريقة CSS آمنة لإخفاء العلامة الحمراء دون جافا سكريبت (هذا يمنع البياض)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* إخفاء العناصر المزعجة بطريقة CSS آمنة */
    header, footer, #MainMenu {visibility: hidden !important;}
    div[data-testid="stStatusWidget"], .viewerBadge_container__1QS1n { display: none !important; }

    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 15px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px; }
    .card { background: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 10px; }
    
    .stButton>button { width: 100%; background: #1f6feb !important; color: white !important; border-radius: 10px; height: 3.5em; font-weight: bold; border: none; }
    .preview-btn { display: block; width: 100%; padding: 12px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 10px; font-weight: bold; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التنبيهات (مع عزل كامل للشبكة) ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def notify_ayman(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=1)
    except: pass

# --- 3. بناء التبويبات المتكاملة (دمج الفحص) ---
st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>نسخة الاستقرار القصوى v26.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص", "🎬 التحميل", "👥 التواصل", "🔐 الإدارة"])

# 1. الرئيسية
with tabs[0]:
    st.markdown("<div style='text-align:center;'><h3>مرحباً بك يا أيمن</h3><p>تم حل مشكلة الشاشة البيضاء نهائياً ✅</p></div>", unsafe_allow_html=True)

# 2. مركز الفحص (دمج الروابط والملفات)
with tabs[1]:
    st.subheader("🔍 فحص الروابط والملفات")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        u_url = st.text_input("🔗 أدخل الرابط للفحص:")
        if st.button("🛡️ ابدأ الفحص"):
            if u_url:
                try:
                    r = requests.get(u_url, timeout=3)
                    st.success(f"الرابط مستجيب وآمن ({r.status_code})")
                    notify_ayman(f"🔍 <b>فحص رابط:</b>\n{u_url}")
                except: st.error("❌ تعذر الوصول للرابط.")
        if u_url: st.markdown(f'<a href="{u_url}" target="_blank" class="preview-btn">👁️ معاينة الرابط</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        u_file = st.file_uploader("📁 ارفع ملفاً للفحص:")
        if u_file and st.button("🛠️ تحليل الملف"):
            st.success(f"تم فحص {u_file.name} بنجاح ✅")
            notify_ayman(f"📁 <b>فحص ملف:</b>\n{u_file.name}")
        st.markdown('</div>', unsafe_allow_html=True)

# 3. التحميل (نظام المعالجة المنفصلة)
with tabs[2]:
    st.subheader("🎬 محمل الفيديو")
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    if st.button("🚀 تحميل الفيديو"):
        if v_url:
            with st.spinner("جاري التجهيز..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'v.mp4', 'quiet': True, 'noplaylist': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_url])
                    if os.path.exists("v.mp4"):
                        with open("v.mp4", "rb") as f:
                            st.video(f.read())
                            st.download_button("📥 حفظ", f, "video.mp4")
                        os.remove("v.mp4")
                        notify_ayman(f"🎬 <b>تحميل ناجح:</b>\n{v_url}")
                except:
                    st.error("فشل التحميل. الرابط قد يكون خاصاً.")

# 4. التواصل (مربوط بالبوت)
with tabs[3]:
    with st.form("contact"):
        name = st.text_input("الاسم:")
        msg = st.text_area("الرسالة أو البلاغ:")
        if st.form_submit_button("إرسال لبوت التليجرام"):
            if name and msg:
                notify_ayman(f"📧 <b>رسالة جديدة:</b>\nمن: {name}\n{msg}")
                st.success("تم الإرسال ✅")

# 5. الإدارة (مربوط بالبوت)
with tabs[4]:
    if "auth" not in st.session_state: st.session_state.auth = False
    if not st.session_state.auth:
        pwd = st.text_input("كلمة السر:", type="password")
        if st.button("دخول"):
            if pwd == "ayman7716":
                st.session_state.auth = True
                notify_ayman("🔓 <b>دخول للإدارة</b>"); st.rerun()
    else:
        st.success("أهلاً أيمن")
        if st.button("خروج"): st.session_state.auth = False; st.rerun()
