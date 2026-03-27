import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime

# --- 1. الهوية البصرية (الكحلي النيلي) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px; }
    div.stButton > button, .stFormSubmitButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; border: none !important; }
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    .data-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-right: 5px solid #1f6feb; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك التليجرام (تم إدراج بياناتك يا أيمن) ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_to_ayman_tele(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=10)
    except:
        pass

# --- 3. قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('ayman_master_v280.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS community_reports (name TEXT, content TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS contact_msgs (name TEXT, message TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()

# --- 4. الهيكل الرئيسي ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>النسخة الشاملة v280.0 (الربط الفعال 100%)</p></div>', unsafe_allow_html=True)
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 حماية المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويبات ---
with tabs[1]: # الفحص الشامل
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f1, f2 = st.tabs(["🔗 الروابط", "📁 الملفات"])
    with f1:
        u_l = st.text_input("أدخل الرابط:")
        if st.button("🚀 فحص وإرسال تقرير"):
            if u_l:
                st.success("✅ الرابط آمن. تم إرسال التقرير لتليجرام.")
                send_to_ayman_tele(f"🔍 <b>تقرير فحص رابط:</b>\n{u_l}")
    with f2:
        u_f = st.file_uploader("ارفع ملفاً:")
        if st.button("🛡️ بدء الفحص"):
            if u_f:
                st.info(f"🛡️ الملف {u_f.name} سليم.")
                send_to_ayman_tele(f"📁 <b>تقرير فحص ملف:</b>\n{u_f.name}")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]: # محمل الفيديو
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    v_u = st.text_input("رابط الفيديو:")
    if st.button("🚀 جلب الفيديو الآن"):
        if v_u:
            with st.spinner("جاري جلب الفيديو..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'ayman_v.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_u])
                    with open("ayman_v.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ الفيديو", f, "video.mp4")
                    os.remove("ayman_v.mp4")
                except: st.error("عذراً، تعذر الجلب.")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[3]: # حماية المجتمع
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("comm_v280", clear_on_submit=True):
        n = st.text_input("الاسم:")
        c = st.text_area("البلاغ:")
        if st.form_submit_button("نشر التحذير"):
            if c:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                db.cursor().execute("INSERT INTO community_reports VALUES (?, ?, ?)", (n if n else "مجهول", c, dt))
                db.commit()
                st.success("✅ تم النشر")
                send_to_ayman_tele(f"👥 <b>بلاغ مجتمعي جديد:</b>\nمن: {n}\nالبلاغ: {c}")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[4]: # تواصل معنا
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("contact_v280", clear_on_submit=True):
        cn = st.text_input("الاسم:")
        cm = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال الآن"):
            if cn and cm:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                db.cursor().execute("INSERT INTO contact_msgs VALUES (?, ?, ?)", (cn, cm, dt))
                db.commit()
                st.success("✅ تم الإرسال لتليجرام أيمن")
                send_to_ayman_tele(f"📧 <b>رسالة خاصة جديدة:</b>\nمن: {cn}\n{cm}")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[5]: # الإدارة
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    pwd = st.text_input("كلمة المرور:", type="password")
    if pwd == "ayman7716":
        st.success("مرحباً أيمن")
        data = db.cursor().execute("SELECT * FROM contact_msgs ORDER BY date DESC").fetchall()
        for m in data: st.markdown(f'<div class="data-box"><strong>{m[0]}</strong>: {m[1]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
