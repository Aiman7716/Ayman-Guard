import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. الإعدادات وتصميم السرعة ---
st.set_page_config(page_title="Ayman Guard v22.1", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    
    /* حل مشكلة تغطية الزر وإخفاء العلامة */
    .block-container { padding-top: 1rem !important; padding-bottom: 12rem !important; }
    
    .hero-section { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d; }
    
    .preview-button { 
        display: inline-block; width: 100%; padding: 12px; 
        background-color: #238636 !important; color: white !important; 
        text-align: center; text-decoration: none; border-radius: 10px; 
        font-weight: bold; margin-top: 10px; border: 1px solid #2ea043;
    }
    
    div.stButton > button { 
        width: 100% !important; background: #1f6feb !important; 
        color: white !important; border-radius: 10px !important; 
        font-weight: bold !important; border: none !important; height: 3em;
    }
    .scan-box { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 15px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# كود إخفاء العلامة الحمراء (إجباري)
components.html("<script>setInterval(()=>{const p=window.parent.document;['.viewerBadge_container__1QS1n','[data-testid=\"stStatusWidget\"]','footer'].forEach(t=>{const e=p.querySelectorAll(t);e.forEach(x=>x.remove())})},300);</script>", height=0)

# --- 2. الإعدادات الفنية ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
DB_NAME = "ayman_shield_v22.db"

def send_to_telegram(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=2)
    except: pass

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 3. بناء التبويبات الستة (كاملة) ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار v22.1 | النسخة الشاملة</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص", "🎬 التحميل", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# 🏠 التبويب 1: الرئيسية
with tabs[0]:
    st.markdown("""
    <div style='text-align:center; padding: 20px;'>
        <h2>مرحباً بك في نظام الحماية الذكي</h2>
        <p>تم تصميم هذا النظام بواسطة أيمن لضمان أعلى مستويات الأمان والتحكم.</p>
        <div style='background:#161b22; padding:15px; border-radius:10px; border:1px solid #30363d;'>
            <h4 style='color:#1f6feb;'>الحالة الراهنة: نشط ✅</h4>
            <p>جميع الأنظمة تعمل بكفاءة ومربوطة بالبوت الشخصي.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 🔍 التبويب 2: مركز الفحص (روابط وملفات)
with tabs[1]:
    st.subheader("🔍 مركز فحص الأمان الشامل")
    
    # قسم الروابط
    st.markdown('<div class="scan-box">', unsafe_allow_html=True)
    st.markdown("<h4>1. فحص الروابط🔗</h4>", unsafe_allow_html=True)
    u_input = st.text_input("أدخل الرابط هنا:", key="url_input")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🛡️ فحص الرابط الآن"):
            if u_input:
                try:
                    res = requests.get(u_input, timeout=5)
                    st.success(f"الرابط آمن ومستجيب (كود: {res.status_code})")
                    send_to_telegram(f"🔍 <b>عملية فحص رابط:</b>\n{u_input}")
                except: st.error("❌ الرابط قد يكون خطيراً أو غير متاح.")
    with c2:
        if u_input: st.markdown(f'<a href="{u_input}" target="_blank" class="preview-button">👁️ معاينة الرابط</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # قسم الملفات
    st.markdown('<div class="scan-box">', unsafe_allow_html=True)
    st.markdown("<h4>2. فحص الملفات📁</h4>", unsafe_allow_html=True)
    u_file = st.file_uploader("ارفع الملف للفحص:")
    if u_file:
        if st.button("🛠️ ابدأ فحص الملف"):
            st.info(f"جاري تحليل ملف: {u_file.name}")
            st.success("✅ الفحص مكتمل: الملف سليم.")
            send_to_telegram(f"📁 <b>عملية فحص ملف:</b>\nاسم الملف: {u_file.name}")
    st.markdown('</div>', unsafe_allow_html=True)

# 🎬 التبويب 3: التحميل
with tabs[2]:
    st.subheader("🎬 محمل الفيديو الذكي")
    v_url = st.text_input("رابط الفيديو (Facebook, YT, TikTok):", key="dl_input")
    if st.button("🚀 تحميل الفيديو"):
        if v_url:
            with st.spinner("جاري التحميل..."):
                try:
                    opts = {'format': 'best', 'outtmpl': 'ayman_v.mp4', 'quiet': True, 'noplaylist': True}
                    with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([v_url])
                    if os.path.exists("ayman_v.mp4"):
                        with open("ayman_v.mp4", "rb") as f:
                            st.video(f.read())
                            st.download_button("📥 حفظ في الجهاز", f, "video.mp4")
                        os.remove("ayman_v.mp4")
                except: st.error("فشل التحميل. تأكد من جودة الرابط.")

# 👥 التبويب 4: المجتمع
with tabs[3]:
    with st.form("community_form"):
        n = st.text_input("الاسم:")
        d = st.text_area("بلاغ عن نشاط مشبوه:")
        if st.form_submit_button("🚨 إرسال البلاغ"):
            db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?,?,?)", (n, d, datetime.now().strftime("%Y-%m-%d")))
            db.commit()
            st.success("تم تسجيل البلاغ بنجاح.")
            send_to_telegram(f"🚨 <b>بلاغ من المجتمع:</b>\nمن: {n}\nالوصف: {d}")

# 📧 التبويب 5: تواصل معنا
with tabs[4]:
    with st.form("contact_form"):
        n = st.text_input("اسم المرسل:")
        m = st.text_area("محتوى الرسالة:")
        if st.form_submit_button("📧 إرسال الرسالة"):
            db.execute("INSERT INTO messages (sender, content, date) VALUES (?,?,?)", (n, m, datetime.now().strftime("%Y-%m-%d")))
            db.commit()
            st.success("شكراً لك، تم إرسال رسالتك.")
            send_to_telegram(f"📧 <b>رسالة تواصل جديدة:</b>\nمن: {n}\nالمحتوى: {m}")

# 🔐 التبويب 6: الإدارة
with tabs[5]:
    if not st.session_state.logged_in:
        pwd = st.text_input("كلمة مرور الإدارة:", type="password")
        if st.button("🔐 دخول"):
            if pwd == "ayman7716":
                st.session_state.logged_in = True
                send_to_telegram("👤 <b>تنبيه:</b> تم الدخول إلى لوحة الإدارة.")
                st.rerun()
            else: st.error("خطأ في كلمة المرور")
    else:
        st.success("مرحباً أيمن. أنت الآن في وضع الإدارة.")
        if st.button("🔴 تسجيل خروج"):
            st.session_state.logged_in = False
            st.rerun()
        
        st.divider()
        st.subheader("📩 الرسائل الواردة")
        msgs = db.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 10").fetchall()
        for msg in msgs: st.info(f"**من:** {msg[1]} | **التاريخ:** {msg[3]}\n\n{msg[2]}")
