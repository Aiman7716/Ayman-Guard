import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. الإعدادات والتصميم الملكي ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    div.stButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; }
    .file-box { background: #161b22; border: 1px solid #1f6feb; padding: 15px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك التقني والأمان ---
DB_NAME = "ayman_ultra_v11.db"
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
    conn.commit()
    return conn

db = init_db()

# إدارة الجلسة
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'temp_code' not in st.session_state: st.session_state.temp_code = None

# --- 3. واجهة المستخدم الرئيسية ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار المطور v11.0</p></div>', unsafe_allow_html=True)
tabs = st.tabs(["🏠 الرئيسية", "🔍 فحص الروابط", "📁 فحص الملفات", "🎬 التحميل", "📧 تواصل", "🔐 الإدارة"])

with tabs[0]:
    st.info("👋 أهلاً بك يا أيمن. تم تحديث ميزة فحص الملفات وتحويل محرك التحميل للوضع الصامت.")

with tabs[1]: # فحص الروابط
    p_url = st.text_input("ألصق الرابط للفحص:")
    if p_url:
        col1, col2 = st.columns(2)
        if col1.button("🛡️ فحص الأمان"):
            data = get_site_preview(p_url)
            if data: st.success(f"النتيجة: {data['status']} | {data['title']}")
            else: st.error("الرابط غير صالح.")
        if col2.button("👁️ معاينة الصفحة"):
            st.components.v1.iframe(p_url, height=450)

with tabs[2]: # فحص الملفات (الميزة المطلوبة)
    st.subheader("📁 نظام الفحص البصري للملفات")
    u_file = st.file_uploader("ارفع الملف المراد فحصه:", type=None)
    if u_file and st.button("🔍 بدء التحليل العميق"):
        with st.spinner("جاري قراءة محتوى الملف..."):
            raw_data = u_file.getvalue()
            try: content = raw_data.decode("utf-8")
            except: content = raw_data.decode("latin-1", errors="replace")
            
            st.markdown("<div class='file-box'>", unsafe_allow_html=True)
            st.code(content[:2500], language="text")
            st.markdown("</div>", unsafe_allow_html=True)
            st.success(f"✅ تم عرض أول 2500 حرف من ملف: {u_file.name}")
            send_to_telegram(f"📁 تم فحص ملف: {u_file.name}")

with tabs[3]: # التحميل (بدون رسائل مزعجة)
    v_url = st.text_input("رابط الفيديو:")
    if st.button("🚀 تحميل"):
        if v_url:
            with st.spinner(" "): # سبينر صامت بدون نص
                try:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': 'ayman_dl.mp4',
                        'quiet': True,
                        'no_warnings': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36'
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                    
                    with open("ayman_dl.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ الفيديو", f, "ayman_video.mp4")
                    os.remove("ayman_dl.mp4")
                except:
                    st.error("❌ تعذر التحميل. قد يكون الرابط خاصاً أو محمياً.")

with tabs[4]: # تواصل
    with st.form("contact"):
        name = st.text_input("الاسم:")
        msg = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            db.execute("INSERT INTO messages (sender, content, date) VALUES (?,?,?)", (name, msg, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("تم الإرسال"); send_to_telegram(f"📧 رسالة من {name}: {msg}")

with tabs[5]: # الإدارة
    if not st.session_state.logged_in:
        pwd = st.text_input("كلمة السر:", type="password")
        if pwd == "ayman7716":
            if st.button("🔐 طلب كود التليجرام"):
                st.session_state.temp_code = str(random.randint(1000, 9999))
                send_to_telegram(f"🔑 كود دخولك: <b>{st.session_state.temp_code}</b>")
            
            v_code = st.text_input("أدخل الكود:")
            if st.button("🔓 دخول"):
                if v_code == st.session_state.temp_code:
                    st.session_state.logged_in = True; st.rerun()
    else:
        st.subheader("لوحة التحكم")
        if st.button("خروج"): st.session_state.logged_in = False; st.rerun()
        for r in db.execute("SELECT * FROM messages ORDER BY id DESC").fetchall():
            st.info(f"📩 {r[1]}: {r[2]}")
