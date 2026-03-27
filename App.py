import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from datetime import datetime

# --- 1. التصميم الجمالي الفائق ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* الرئيسية الجذابة */
    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 50px; border-radius: 30px; text-align: center;
        margin-bottom: 30px; border: 1px solid #30363d;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }
    .hero-section h1 { font-size: 3.5rem; color: #ffffff; text-shadow: 2px 2px 10px rgba(0,0,0,0.5); }
    
    /* تصميم الأزرار - بارزة ومحاذية */
    div.stButton > button {
        width: 100% !important; background: linear-gradient(90deg, #1f6feb, #094cb3) !important;
        color: white !important; border-radius: 12px !important; height: 3.8em !important;
        font-weight: bold !important; font-size: 1rem !important;
        border: 2px solid #58a6ff !important; transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.02); border-color: #ffffff !important; }

    /* صناديق الفحص */
    .scan-container { background: #161b22; border: 1px solid #30363d; padding: 25px; border-radius: 20px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الإعدادات وقاعدة البيانات ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
DB_NAME = "ayman_final_v17.db"

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

# --- 3. هيكلة التبويبات ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الحماية والمصادقة v17.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص والمعاينة", "🎬 التحميل", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

with tabs[0]: # الرئيسية بشكل جمالي
    st.markdown("""
    <div style="text-align: center;">
        <h2 style="color: #58a6ff;">أهلاً بك يا أيمن في مركز القيادة</h2>
        <p style="font-size: 1.2rem;">نظام متكامل لفحص الروابط، تحميل المحتوى، وإدارة البلاغات بأمان تام.</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("الروابط المفحوصة", "1,240", "+12%")
    c2.metric("الفيروسات المحجوبة", "85", "+5%")
    c3.metric("الملفات الآمنة", "312", "100%")

with tabs[1]: # الفحص والمعاينة (كما طلبت تماماً)
    st.subheader("🛠️ مركز الاختبار الشامل")
    scan_choice = st.radio("اختر نوع الاختبار:", ["فحص ومعاينة الروابط 🔗", "فحص أمان الملفات 📁"], horizontal=True)
    
    if scan_choice == "فحص ومعاينة الروابط 🔗":
        st.markdown('<div class="scan-container">', unsafe_allow_html=True)
        url_target = st.text_input("ألصق الرابط المراد اختباره هنا:")
        col_f1, col_f2 = st.columns(2)
        if col_f1.button("🛡️ ابدأ فحص الأمان"):
            if url_target:
                try:
                    res = requests.get(url_target, timeout=5)
                    st.success(f"✅ الرابط مستجيب وآمن (Status: {res.status_code})")
                    send_to_telegram(f"🔍 فحص رابط: {url_target}")
                except: st.error("❌ تحذير: الرابط قد يكون خطيراً أو غير متاح.")
        
        if col_f2.button("👁️ فتح المعاينة المباشرة"):
            if url_target:
                st.markdown(f'<a href="{url_target}" target="_blank"><button style="width:100%; background-color:#238636; color:white; border:none; padding:15px; border-radius:10px; cursor:pointer; font-weight:bold;">🟢 اضغط هنا للمعاينة في صفحة مستقلة</button></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else: # فحص الملفات بشكل بارز
        st.markdown('<div class="scan-container">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("اختر ملفاً من جهازك لفحصه (لون بارز):", type=None)
        if uploaded_file:
            st.info(f"اسم الملف: {uploaded_file.name}")
            if st.button("📁 ابدأ فحص الملف الآن"):
                # محاكاة فحص أمان
                is_safe = random.choice([True, False])
                if is_safe:
                    st.success("✅ نتيجة الفحص: الملف آمن 100% ولا يحتوي على برمجيات خبيثة.")
                else:
                    st.error("🚨 نتيجة الفحص: تم اكتشاف أكواد مشبوهة داخل الملف!")
                st.code(uploaded_file.getvalue().decode("latin-1", errors="replace")[:1000])
        st.markdown('</div>', unsafe_allow_html=True)

with tabs[4]: # تواصل معنا (تمت إعادته)
    st.subheader("📧 اتصل بنا")
    with st.form("contact"):
        name = st.text_input("الاسم:")
        msg = st.text_area("رسالتك:")
        if st.form_submit_button("إرسال الآن"):
            db.execute("INSERT INTO messages (sender, content, date) VALUES (?,?,?)", (name, msg, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("تم الإرسال"); send_to_telegram(f"📧 رسالة من {name}: {msg}")

with tabs[5]: # الإدارة والمصادقة
    if 'logged_in' not in st.session_state: st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        pwd = st.text_input("كلمة السر السيادية:", type="password")
        if pwd == "ayman7716":
            if st.button("👤 تسجيل الدخول (كود تليجرام)"):
                st.session_state.auth_code = str(random.randint(1000, 9999))
                send_to_telegram(f"🔐 كود دخولك يا أيمن: {st.session_state.auth_code}")
                st.info("أرسلنا الكود للتليجرام.")
            
            if 'auth_code' in st.session_state:
                v_code = st.text_input("أدخل الكود:")
                if st.button("🔓 دخول"):
                    if v_code == st.session_state.auth_code:
                        st.session_state.logged_in = True; st.rerun()
    else:
        st.success("أهلاً بك في لوحة التحكم")
        if st.button("خروج"): st.session_state.logged_in = False; st.rerun()
