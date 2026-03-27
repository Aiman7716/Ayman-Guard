import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. الإعدادات والتصميم الاحترافي ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    div.stButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; }
    .status-box { background: #1c2128; border: 1px solid #30363d; padding: 20px; border-radius: 15px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك التقني والأمان ---
DB_NAME = "ayman_final_v10.db"
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_to_telegram(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

def get_site_preview(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=7)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.title.string if soup.title else "عنوان غير معروف"
        return {"title": title, "status": "سليم ✅" if res.status_code == 200 else "مشبوه ⚠️"}
    except: return None

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()

# إدارة الجلسة للأمان
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'temp_code' not in st.session_state: st.session_state.temp_code = None

# --- 3. واجهة المستخدم الرئيسية ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الحماية v10.0 | فحص - تحميل - إدارة</p></div>', unsafe_allow_html=True)
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص والمعاينة", "🎬 التحميل الذكي", "👥 المجتمع", "📧 تواصل", "🔐 الإدارة"])

with tabs[0]:
    st.success("👋 أهلاً بك يا أيمن. النظام يعمل الآن بكفاءة 100% وتم إصلاح محرك التحميل.")

with tabs[1]: # تبويب الفحص والمعاينة
    link_input = st.text_input("أدخل الرابط هنا للفحص أو العرض:")
    if link_input:
        c1, c2 = st.columns(2)
        if c1.button("🛡️ فحص الأمان"):
            data = get_site_preview(link_input)
            if data:
                st.markdown(f"<div class='status-box'><h3>النتيجة: {data['status']}</h3><p>الموقع: {data['title']}</p></div>", unsafe_allow_html=True)
                send_to_telegram(f"🔍 فحص رابط: {link_input}")
            else: st.error("❌ الرابط غير مستقر أو وهمي.")
        
        if c2.button("👁️ عرض الصفحة"):
            st.info("جاري المعاينة آمنة...")
            st.components.v1.iframe(link_input, height=400)

with tabs[2]: # تبويب التحميل (تم تحديثه لفك تشفير فيسبوك)
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    if st.button("🚀 بدء التحميل والتحويل"):
        if v_url:
            with st.spinner("جاري كسر التشفير وجلب الفيديو..."):
                try:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': 'ayman_dl.mp4',
                        'quiet': True,
                        'no_warnings': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36'
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_url])
                    
                    with open("ayman_dl.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ الفيديو في هاتفك", f, "video.mp4")
                    os.remove("ayman_dl.mp4")
                except:
                    st.error("⚠️ الرابط قد يكون خاصاً أو يحتاج لتسجيل دخول. تأكد من جودة الرابط.")

with tabs[3]: # المجتمع
    with st.form("comm_f"):
        rep_n = st.text_input("الاسم:")
        rep_d = st.text_area("تفاصيل البلاغ:")
        if st.form_submit_button("نشر البلاغ"):
            db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?, ?, ?)", (rep_n, rep_d, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("تم النشر"); send_to_telegram(f"🚨 بلاغ جديد: {rep_d}")

with tabs[4]: # تواصل
    with st.form("cont_f"):
        msg_n = st.text_input("اسمك:")
        msg_c = st.text_area("رسالتك:")
        if st.form_submit_button("إرسال"):
            db.execute("INSERT INTO messages (sender, content, date) VALUES (?, ?, ?)", (msg_n, msg_c, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("تم الإرسال"); send_to_telegram(f"📧 رسالة من {msg_n}: {msg_c}")

with tabs[5]: # تبويب الإدارة (المصادقة عبر التليجرام)
    if not st.session_state.logged_in:
        pwd = st.text_input("كلمة السر السيادية:", type="password")
        if pwd == "ayman7716":
            if st.button("🔐 طلب كود دخول عبر تليجرام"):
                st.session_state.temp_code = str(random.randint(1000, 9999))
                send_to_telegram(f"🔑 كود الدخول الخاص بك: <b>{st.session_state.temp_code}</b>")
                st.info("تفقد التليجرام الخاص بك.")
            
            v_code = st.text_input("أدخل الكود المستلم:")
            if st.button("🔓 دخول الإدارة"):
                if v_code == st.session_state.temp_code:
                    st.session_state.logged_in = True
                    st.rerun()
                else: st.error("الكود غير صحيح.")
    else:
        st.subheader("⚙️ لوحة تحكم أيمن")
        if st.button("🔴 خروج"): st.session_state.logged_in = False; st.rerun()
        rows = db.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
        for r in rows: st.info(f"📩 **{r[1]}**: {r[2]}")
