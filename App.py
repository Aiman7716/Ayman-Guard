import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. الإعدادات والتصميم الفاخر ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    div.stButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 12px !important; font-weight: bold !important; height: 3.5em; transition: 0.3s; }
    .status-card { background: #1c2128; border: 1px solid #30363d; padding: 20px; border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك التقني والأمان ---
DB_NAME = "ayman_secure_v13.db"
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_to_telegram(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()

# إدارة الجلسة (Session)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None
if 'show_login' not in st.session_state: st.session_state.show_login = False

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الحماية والمصادقة v13.0</p></div>', unsafe_allow_html=True)
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 التحميل", "👥 حماية المجتمع", "📧 تواصل", "🔐 الإدارة"])

with tabs[1]: # الفحص الشامل (دمج الروابط والملفات)
    choice = st.radio("اختر هدف الفحص:", ["روابط ومواقع 🔗", "تحليل ملفات 📁"], horizontal=True)
    if choice == "روابط ومواقع 🔗":
        p_url = st.text_input("ألصق الرابط المراد فحصه:")
        if p_url:
            col1, col2 = st.columns(2)
            if col1.button("🛡️ فحص الأمان"):
                try:
                    res = requests.get(p_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                    st.success(f"✅ الرابط مستجيب (Status: {res.status_code})")
                    send_to_telegram(f"🔍 فحص رابط: {p_url}")
                except: st.error("❌ الرابط غير مستقر أو وهمي.")
            
            # حل مشكلة الصورة الحزينة بتوفير رابط مباشر
            st.markdown(f'<a href="{p_url}" target="_blank"><button style="width:100%; background-color:#238636; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer; font-weight:bold;">👁️ فتح الرابط للمعاينة في نافذة جديدة</button></a>', unsafe_allow_html=True)
            st.caption("ملاحظة: بعض المواقع تمنع المعاينة الداخلية لحمايتك، لذا يفضل فتحها في نافذة جديدة.")
    else:
        u_file = st.file_uploader("ارفع الملف للفحص البصري:")
        if u_file and st.button("🔍 بدء التحليل"):
            content = u_file.getvalue().decode("latin-1", errors="replace")
            st.code(content[:2000])
            st.success("تم تحليل هيكل الملف بنجاح.")

with tabs[2]: # التحميل الصامت
    v_url = st.text_input("رابط الفيديو:")
    if st.button("🚀 تحميل"):
        if v_url:
            with st.spinner(" "): 
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'v.mp4', 'quiet': True, 'user_agent': 'Mozilla/5.0'}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                    with open("v.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ", f, "ayman_video.mp4")
                    os.remove("v.mp4")
                except: st.error("❌ فشل التحميل. قد يكون الرابط خاصاً.")

with tabs[3]: # حماية المجتمع
    with st.form("comm"):
        n, d = st.text_input("الاسم:"), st.text_area("تفاصيل البلاغ:")
        if st.form_submit_button("🚨 إرسال بلاغ"):
            db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?,?,?)", (n, d, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("تم الإرسال"); send_to_telegram(f"🚨 بلاغ مجتمعي: {d}")

with tabs[5]: # تبويب الإدارة (النظام الذي طلبته)
    if not st.session_state.logged_in:
        pwd = st.text_input("كلمة السر السيادية:", type="password")
        if pwd == "ayman7716":
            st.success("✅ كلمة السر صحيحة")
            # زر تسجيل الدخول الذي طلبته
            if st.button("👤 تسجيل الدخول (طلب رمز تليجرام)"):
                st.session_state.auth_code = str(random.randint(1000, 9999))
                send_to_telegram(f"🔐 كود المصادقة الثنائية الخاص بك هو: <b>{st.session_state.auth_code}</b>")
                st.session_state.show_login = True
                st.info("تم إرسال الكود إلى حسابك في تليجرام.")

            if st.session_state.show_login:
                v_code = st.text_input("أدخل كود التحقق المستلم:")
                if st.button("🔓 تأكيد الدخول"):
                    if v_code == st.session_state.auth_code:
                        st.session_state.logged_in = True
                        st.rerun()
                    else: st.error("الكود غير صحيح!")
    else:
        st.subheader("⚙️ لوحة التحكم السيادية")
        if st.button("🔴 تسجيل الخروج"): st.session_state.logged_in = False; st.rerun()
        st.write("---")
        st.write("📩 الرسائل المستلمة:")
        for r in db.execute("SELECT * FROM messages ORDER BY id DESC").fetchall(): st.info(f"{r[1]}: {r[2]}")
        st.write("🚨 البلاغات:")
        for r in db.execute("SELECT * FROM reports ORDER BY id DESC").fetchall(): st.warning(f"{r[1]}: {r[2]}")
