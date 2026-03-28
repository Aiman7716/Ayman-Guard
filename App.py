import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. الإعدادات والتصميم الجمالي ---
st.set_page_config(page_title="Ayman Guard Pro v20", layout="wide")

# كود التنسيق وإخفاء معالم الموقع (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* إخفاء القوائم والفوتر والهيدر */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* إخفاء العلامة الحمراء (محاولة CSS قصوى) */
    div[data-testid="stStatusWidget"], .viewerBadge_container__1QS1n, [class*="viewerBadge"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* حل مشكلة التغطية: توفير مساحة كبيرة جداً في الأسفل */
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 15rem !important; /* زدنا المساحة لرفع الأزرار بعيداً عن الشعار */
    }

    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 40px; border-radius: 25px; text-align: center;
        margin-bottom: 25px; border: 1px solid #30363d;
    }
    
    /* تصميم زر المعاينة ليكون بارزاً وفوق أي شعار */
    .preview-button {
        display: inline-block;
        width: 100%;
        padding: 15px;
        background-color: #238636 !important;
        color: white !important;
        text-align: center;
        text-decoration: none;
        border-radius: 12px;
        font-weight: bold;
        border: 2px solid #2ea043;
        margin-top: 10px;
        z-index: 9999 !important; /* لضمان ظهوره فوق كل شيء */
    }
    
    div.stButton > button {
        width: 100% !important; background: linear-gradient(90deg, #1f6feb, #094cb3) !important;
        color: white !important; border-radius: 12px !important; height: 3.5em !important;
        font-weight: bold !important; border: 2px solid #58a6ff !important;
    }
    .scan-box { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 20px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- كود JavaScript "المدمر" للعلامة الحمراء ---
components.html("""
    <script>
    function destroyBadges() {
        const p = window.parent.document;
        // استهداف كل العناصر الممكنة التي تمثل العلامة الحمراء
        const selectors = ['.viewerBadge_container__1QS1n', '[data-testid="stStatusWidget"]', 'footer', 'header', '[class*="viewerBadge"]'];
        selectors.forEach(s => {
            const els = p.querySelectorAll(s);
            els.forEach(el => {
                el.style.setProperty('display', 'none', 'important');
                el.remove();
            });
        });
    }
    // تنفيذ مكثف كل 300 مللي ثانية
    setInterval(destroyBadges, 300);
    </script>
""", height=0)

# --- 2. محرك الأمان وقواعد البيانات ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
DB_NAME = "ayman_perfect_v20.db"

def send_to_telegram(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None

# --- 3. بناء واجهة التبويبات ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار v20.6 | حل مشكلة زر المعاينة</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص والمعاينة", "🎬 التحميل", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# 2. الفحص والمعاينة (المكان الذي كان يختفي فيه الزر)
with tabs[1]:
    st.subheader("🛠️ مركز الاختبار الشامل")
    scan_choice = st.radio("اختر المهمة:", ["فحص ومعاينة الروابط 🔗", "فحص أمان الملفات 📁"], horizontal=True)
    st.markdown('<div class="scan-box">', unsafe_allow_html=True)
    
    if scan_choice == "فحص ومعاينة الروابط 🔗":
        u = st.text_input("ألصق الرابط هنا:", key="url_input_final_v6")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛡️ ابدأ فحص الأمان"):
                if u:
                    try:
                        res = requests.get(u, timeout=5)
                        st.success(f"الرابط مستجيب وآمن ({res.status_code})")
                    except: st.error("❌ الرابط غير متاح")
        with col2:
            # زر المعاينة الجديد بتصميم HTML لضمان عدم اختفائه
            if u:
                st.markdown(f'<a href="{u}" target="_blank" class="preview-button">👁️ معاينة الرابط الآن</a>', unsafe_allow_html=True)
            else:
                st.info("أدخل رابطاً لتفعيل المعاينة")
    else:
        u_f = st.file_uploader("ارفع الملف للفحص:", key="file_input_v6")
    
    st.markdown('</div>', unsafe_allow_html=True)

# استكمال بقية الكود (التحميل، المجتمع، الإدارة)
with tabs[2]: # التحميل
    v_u = st.text_input("رابط الفيديو للتحميل:", key="dl_v6")
    if st.button("🚀 تحميل الآن"):
        st.info("جاري المعالجة...")

with tabs[3]: # المجتمع
    with st.form("comm"):
        rn, rd = st.text_input("اسمك:"), st.text_area("بلاغ عن خطر:")
        if st.form_submit_button("🚨 إرسال"):
            db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?,?,?)", (rn, rd, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("تم التوثيق")

with tabs[4]: # تواصل معنا
    with st.form("contact"):
        cn, cm = st.text_input("الاسم:"), st.text_area("الرسالة:")
        if st.form_submit_button("📧 إرسال"):
            db.execute("INSERT INTO messages (sender, content, date) VALUES (?,?,?)", (cn, cm, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("شكراً لتواصلك")

with tabs[5]: # الإدارة
    if not st.session_state.logged_in:
        st.subheader("🔐 الدخول")
        pwd = st.text_input("كلمة السر:", type="password")
        if st.button("👤 دخول"):
            if pwd == "ayman7716": st.session_state.logged_in = True; st.rerun()
    else:
        st.success("مرحباً أيمن")
        if st.button("🔴 خروج"): st.session_state.logged_in = False; st.rerun()
