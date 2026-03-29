import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from datetime import datetime

# --- 1. التصميم الجمالي السيادي (UI/UX) ---
st.set_page_config(page_title="Ayman Guard Pro v19", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px; border-radius: 20px; text-align: center;
        margin-bottom: 20px; border: 1px solid #30363d;
    }
    
    div.stButton > button {
        width: 100% !important; background: #1f6feb !important;
        color: white !important; border-radius: 12px !important; height: 3.5em !important;
        font-weight: bold !important; border: none !important;
    }
    
    /* زر التنزيل الأخضر الواضح */
    .stDownloadButton>button {
        background-color: #238636 !important;
        height: 4.5em !important;
        font-size: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك التقني وقاعدة البيانات ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
DB_NAME = "ayman_guard_v19.db"

def send_to_telegram(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text}, timeout=5)
    except: pass

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

conn = init_db()

# إدارة الجلسة
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 3. بناء الواجهة السيادية ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>النسخة المصلحة v19.0</p></div>', unsafe_allow_html=True)

# تعريف التبويبات بشكل صريح لمنع خطأ الصورة الأخيرة
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 التحميل", "📧 تواصل", "🔐 الإدارة"])

with tabs[0]:
    st.markdown("<div style='text-align:center;'><h2>مرحباً بك يا أيمن</h2><p>تم إصلاح جميع أخطاء المحرك بنجاح ✅</p></div>", unsafe_allow_html=True)

with tabs[1]:
    st.subheader("🔍 مركز الفحص")
    u_link = st.text_input("رابط للفحص:")
    if st.button("🛡️ ابدأ الفحص"):
        try:
            r = requests.get(u_link, timeout=5)
            st.success(f"الرابط مستجيب ({r.status_code})")
            send_to_telegram(f"🔍 فحص رابط: {u_link}")
        except: st.error("فشل الوصول للرابط")

with tabs[2]:
    st.subheader("🎬 محمل الفيديو (المحرك الأصلي المستقر)")
    v_url = st.text_input("ألصق الرابط هنا:")
    if st.button("🚀 معالجة وتحميل"):
        if v_url:
            with st.spinner("جاري التحميل..."):
                try:
                    # العودة للمحرك القديم الذي لا يسبب "No such file"
                    out = "video_final.mp4"
                    ydl_opts = {'format': 'best', 'outtmpl': out, 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_url])
                    
                    if os.path.exists(out):
                        with open(out, "rb") as f:
                            st.video(v_url)
                            st.download_button(label="📥 حفظ الفيديو فوراً", data=f, file_name="ayman_shield.mp4", mime="video/mp4")
                        os.remove(out)
                        send_to_telegram(f"🎬 نجاح تحميل: {v_url}")
                except Exception as e:
                    st.error(f"خطأ: تأكد من الرابط أو جرب فتحه في متصفح خارجي. ({e})")

with tabs[3]:
    with st.form("contact"):
        n, m = st.text_input("الاسم:"), st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            conn.execute("INSERT INTO messages (sender, content, date) VALUES (?,?,?)", (n, m, str(datetime.now())))
            conn.commit()
            st.success("تم الإرسال ✅")
            send_to_telegram(f"📩 رسالة من {n}: {m}")

with tabs[4]:
    if not st.session_state.logged_in:
        pwd = st.text_input("كلمة السر:", type="password")
        if st.button("دخول"):
            if pwd == "ayman7716":
                st.session_state.logged_in = True
                st.rerun()
    else:
        if st.button("تسجيل خروج"): st.session_state.logged_in = False; st.rerun()
        st.write("📩 آخر الرسائل:")
        msgs = conn.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 5").fetchall()
        for msg in msgs: st.info(f"{msg[1]}: {msg[2]}")
