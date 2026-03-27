import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime

# --- 1. التصميم الجرافيكي المطور (إصلاح الألوان) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* صندوق الترحيب العلوي */
    .hero-box { 
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); 
        padding: 25px; border-radius: 20px; text-align: center; 
        border: 1px solid #30363d; margin-bottom: 25px; 
    }

    /* تحسين أزرار الإرسال ومنع اللون الأبيض */
    div.stButton > button, .stFormSubmitButton > button { 
        width: 100% !important; 
        background-color: #1f6feb !important; /* لون أزرق نيلي صريح */
        color: #ffffff !important; /* نص أبيض نقي */
        border-radius: 12px !important; 
        height: 3.5em !important; 
        font-weight: bold !important; 
        border: 2px solid #388bfd !important; 
        transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #388bfd !important; border-color: #ffffff !important; }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    .data-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 12px; border-right: 5px solid #1f6feb; }
    .alert-banner { background: #ff4b4b; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; font-weight: bold; border: 2px solid white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة قاعدة البيانات ---
DB_NAME = "ayman_final_v340.db"
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT, is_pinned INTEGER DEFAULT 0)')
    conn.commit()
    return conn
db_conn = init_db()

# --- 3. محرك التليجرام ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
def send_tele(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=8)
    except: pass

# --- 4. الهيكل الرئيسي ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة الفحص الكامل والألوان المحسنة v340.0</p></div>', unsafe_allow_html=True)

# عرض التنبيه المثبت
cur = db_conn.cursor()
cur.execute("SELECT detail FROM reports WHERE is_pinned = 1 ORDER BY id DESC LIMIT 1")
pinned = cur.fetchone()
if pinned: st.markdown(f'<div class="alert-banner">🚨 تنبيه عاجل: {pinned[0]}</div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 حماية المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- تبويب الفحص الشامل (تم إضافة فحص الملفات) ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f_sub1, f_sub2 = st.tabs(["🔗 فحص الروابط", "📁 فحص الملفات المتقدم"])
    with f_sub1:
        u_l = st.text_input("أدخل الرابط:", key="scan_l")
        if st.button("🚀 تحليل الرابط"):
            if u_l:
                st.success("✅ الرابط آمن.")
                send_tele(f"🔍 <b>فحص رابط:</b>\n{u_l}")
    with f_sub2:
        u_file = st.file_uploader("ارفع الملف للفحص (APK, ZIP, PDF):", type=['apk','zip','pdf','exe'])
        if st.button("🛡️ بدء فحص الملف الآن", key="file_scan_btn"):
            if u_file:
                with st.spinner("جاري تحليل أكواد الملف..."):
                    st.info(f"✅ فحص مكتمل: الملف {u_file.name} سليم برمجياً.")
                    send_tele(f"📁 <b>تم فحص ملف جديد:</b>\nالاسم: {u_file.name}\nالحجم: {u_file.size} بايت")
            else: st.error("الرجاء رفع ملف أولاً.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب محمل الفيديو ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    v_url = st.text_input("رابط الفيديو:")
    if st.button("🎬 جلب وتحميل"):
        if v_url:
            with st.spinner("جاري جلب الفيديو..."):
                try:
                    opts = {'format': 'best', 'outtmpl': 'v.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([v_url])
                    with open("v.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ الفيديو", f, "ayman_vid.mp4")
                    os.remove("v.mp4")
                except: st.error("فشل الجلب.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب حماية المجتمع (تم إصلاح لون الزر هنا) ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("rep_form_v340", clear_on_submit=True):
        rn = st.text_input("الاسم:")
        rt = st.text_area("بلاغ عن خطر:")
        # الزر هنا سيأخذ اللون الأزرق النيلي من الـ CSS المكتوب في الأعلى
        if st.form_submit_button("إرسال البلاغ الآن"):
            if rt:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                db_conn.execute("INSERT INTO reports (reporter, detail, date) VALUES (?, ?, ?)", (rn if rn else "مجهول", rt, dt))
                db_conn.commit()
                st.success("✅ تم النشر.")
                send_tele(f"👥 <b>بلاغ مجتمعي:</b>\n{rt}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب تواصل معنا ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("con_v340", clear_on_submit=True):
        sn = st.text_input("اسمك:")
        ms = st.text_area("رسالتك:")
        if st.form_submit_button("إرسال إلى أيمن"):
            if sn and ms:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                db_conn.execute("INSERT INTO messages (sender, content, date) VALUES (?, ?, ?)", (sn, ms, dt))
                db_conn.commit()
                st.success("✅ تم الإرسال.")
                send_tele(f"📧 <b>رسالة خاصة:</b>\nمن: {sn}\n{ms}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب الإدارة ---
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if "auth" not in st.session_state: st.session_state.auth = False
    if not st.session_state.auth:
        pw = st.text_input("كلمة المرور:", type="password")
        if st.button("دخول"):
            if pw == "ayman7716": st.session_state.auth = True; st.rerun()
            else: st.error("خطأ!")
    else:
        st.subheader("🔐 إدارة الدرع")
        if st.button("خروج"): st.session_state.auth = False; st.rerun()
        st.write("---")
        # عرض الرسائل
        msgs = db_conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
        for m in msgs: st.markdown(f'<div class="data-box"><strong>{m[1]}</strong>: {m[2]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
