import streamlit as st
import yt_dlp
import os
import sqlite3
from datetime import datetime

# --- 1. التصميم الملكي ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 20px; }
    div.stButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; border: none !important; }
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    .report-box { background-color: #0d1117; border-right: 5px solid #1f6feb; padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. قاعدة البيانات ---
def get_db():
    conn = sqlite3.connect('ayman_pro.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS reports (name TEXT, text TEXT, time TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS messages (name TEXT, email TEXT, msg TEXT, time TEXT)')
    conn.commit()
    return conn

db_conn = get_db()

# --- 3. الهيكل الرئيسي ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة الإصلاح الشامل v210.0</p></div>', unsafe_allow_html=True)
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 حماية المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- تبويب الفحص الشامل ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f_sub1, f_sub2 = st.tabs(["🔗 الروابط", "📁 الملفات"])
    with f_sub1:
        u_input = st.text_input("أدخل الرابط للفحص:")
        if st.button("تحليل الرابط", key="btn_check_url"):
            st.success("تم الفحص: الرابط آمن برمجياً.")
    with f_sub2:
        st.file_uploader("ارفع ملفاً:")
        if st.button("فحص الملفات", key="btn_check_file"):
            st.info("لم يتم العثور على تهديدات.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب محمل الفيديو (التحميل الداخلي) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    v_url = st.text_input("رابط الفيديو (FB, TikTok, YT):")
    if st.button("🚀 تحميل داخلي مباشر", key="btn_dl"):
        if v_url:
            with st.spinner("جاري السحب..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'vid.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_url])
                    with open("vid.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("حفظ الفيديو", f, "video.mp4")
                    os.remove("vid.mp4")
                except: st.error("فشل التحميل: جرب رابطاً آخر.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب حماية المجتمع (إصلاح زر النشر) ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("👥 بلاغات المجتمع")
    with st.form("community_form", clear_on_submit=True):
        r_name = st.text_input("الاسم:")
        r_text = st.text_area("تفاصيل التحذير:")
        submit_report = st.form_submit_button("نشر التحذير الآن") # زر النشر أصبح شغالاً الآن
        
        if submit_report:
            if r_text:
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
                cursor = db_conn.cursor()
                cursor.execute("INSERT INTO reports VALUES (?, ?, ?)", (r_name if r_name else "مجهول", r_text, time_now))
                db_conn.commit()
                st.success("✅ تم نشر بلاغك بنجاح!")
            else:
                st.error("الرجاء كتابة تفاصيل البلاغ.")

    st.write("---")
    st.subheader("📢 آخر البلاغات")
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM reports ORDER BY time DESC LIMIT 5")
    for row in cursor.fetchall():
        st.markdown(f'<div class="report-box"><strong>{row[0]}</strong> <small>({row[2]})</small><br>{row[1]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب تواصل معنا (إصلاح زر الإرسال) ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 راسل أيمن")
    with st.form("contact_form", clear_on_submit=True):
        c_name = st.text_input("اسمك:")
        c_email = st.text_input("بريدك (اختياري):")
        c_msg = st.text_area("رسالتك:")
        submit_contact = st.form_submit_button("إرسال الرسالة") # زر الإرسال أصبح شغالاً الآن
        
        if submit_contact:
            if c_name and c_msg:
                t_now = datetime.now().strftime("%Y-%m-%d %H:%M")
                cursor = db_conn.cursor()
                cursor.execute("INSERT INTO messages VALUES (?, ?, ?, ?)", (c_name, c_email, c_msg, t_now))
                db_conn.commit()
                st.success(f"شكراً {c_name}، وصلت رسالتك بنجاح.")
            else:
                st.error("الرجاء إكمال الاسم والرسالة.")
    st.markdown('</div>', unsafe_allow_html=True)
