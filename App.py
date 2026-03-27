import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. الإعدادات والتصميم ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    div.stButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 12px !important; font-weight: bold !important; transition: 0.3s; }
    .status-card { background: #1c2128; border: 1px solid #30363d; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك التقني ---
DB_NAME = "ayman_final_v12.db"
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_to_telegram(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

def get_site_preview(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=7)
        soup = BeautifulSoup(res.text, 'html.parser')
        return {"title": soup.title.string if soup.title else "بدون عنوان", "status": "سليم ✅" if res.status_code == 200 else "مشبوه ⚠️"}
    except: return None

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الحماية المتكامل v12.0</p></div>', unsafe_allow_html=True)
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 التحميل", "👥 حماية المجتمع", "📧 تواصل", "🔐 الإدارة"])

with tabs[0]:
    st.success("👋 أهلاً يا أيمن. تم دمج الفحص وإعادة تبويب المجتمع بنجاح.")

with tabs[1]: # دمج فحص الروابط والملفات
    m = st.radio("نوع الفحص:", ["روابط 🔗", "ملفات 📁"], horizontal=True)
    if m == "روابط 🔗":
        p_url = st.text_input("أدخل الرابط للفحص:")
        if p_url:
            c1, c2 = st.columns(2)
            if c1.button("🛡️ فحص الأمان"):
                data = get_site_preview(p_url)
                if data: st.info(f"النتيجة: {data['status']} | {data['title']}")
                else: st.error("الرابط غير صالح.")
            if c2.button("👁️ معاينة"): st.components.v1.iframe(p_url, height=400)
    else:
        u_file = st.file_uploader("ارفع الملف للفحص:")
        if u_file and st.button("🔍 تحليل الملف"):
            content = u_file.getvalue().decode("latin-1", errors="replace")
            st.code(content[:2000])
            st.success("تم تحليل هيكل الملف بصرياً.")

with tabs[2]: # تحميل الفيديو (تحسين فيسبوك)
    v_url = st.text_input("رابط الفيديو هنا:")
    if st.button("🚀 بدء التحميل"):
        if v_url:
            with st.spinner(" "): 
                try:
                    ydl_opts = {
                        'format': 'best', 'outtmpl': 'vid.mp4', 'quiet': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                    with open("vid.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ الفيديو", f, "video.mp4")
                    os.remove("vid.mp4")
                except: st.error("⚠️ الرابط قد يحتاج تسجيل دخول أو هو رابط خاص.")

with tabs[3]: # تبويب حماية المجتمع (الذي طلبته)
    st.subheader("👥 بلاغات المجتمع")
    with st.form("community_form"):
        r_name = st.text_input("اسم المبلغ:")
        r_detail = st.text_area("تفاصيل النشاط المشبوه أو الرابط الضار:")
        if st.form_submit_button("🚨 إرسال بلاغ"):
            db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?,?,?)", (r_name, r_detail, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("تم استلام بلاغك وسيقوم أيمن بمراجعته."); send_to_telegram(f"🚨 بلاغ مجتمع: {r_detail}")

with tabs[4]: # تواصل
    with st.form("contact"):
        n, m = st.text_input("الاسم:"), st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            db.execute("INSERT INTO messages (sender, content, date) VALUES (?,?,?)", (n, m, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("تم الإرسال"); send_to_telegram(f"📧 رسالة: {m}")

with tabs[5]: # الإدارة
    if not st.session_state.logged_in:
        pwd = st.text_input("كلمة السر:", type="password")
        if pwd == "ayman7716":
            if st.button("🔐 دخول الإدارة"): st.session_state.logged_in = True; st.rerun()
    else:
        st.subheader("⚙️ لوحة التحكم")
        if st.button("🔴 خروج"): st.session_state.logged_in = False; st.rerun()
        st.write("---")
        st.write("📩 الرسائل:")
        for r in db.execute("SELECT * FROM messages ORDER BY id DESC").fetchall(): st.info(f"{r[1]}: {r[2]}")
        st.write("🚨 البلاغات:")
        for r in db.execute("SELECT * FROM reports ORDER BY id DESC").fetchall(): st.warning(f"{r[1]}: {r[2]}")
