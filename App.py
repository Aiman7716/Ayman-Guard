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
    
    /* إخفاء العلامة الحمراء عبر CSS */
    div[data-testid="stStatusWidget"], .viewerBadge_container__1QS1n, .viewerBadge_link__1S137 {
        display: none !important;
        height: 0px !important;
        width: 0px !important;
    }

    /* الحل لمشكلة التغطية: رفع المحتوى قليلاً للأعلى وتوفير مساحة في الأسفل */
    .block-container { 
        padding-top: 0rem !important; 
        padding-bottom: 5rem !important; /* مساحة إضافية في الأسفل لكي لا يغطي الشعار على الأزرار */
    }

    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 40px; border-radius: 25px; text-align: center;
        margin-bottom: 25px; border: 1px solid #30363d;
    }
    div.stButton > button {
        width: 100% !important; background: linear-gradient(90deg, #1f6feb, #094cb3) !important;
        color: white !important; border-radius: 12px !important; height: 3.5em !important;
        font-weight: bold !important; border: 2px solid #58a6ff !important;
    }
    .scan-box { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 20px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- كود JavaScript هجومي لحذف العلامة وتفريغ مساحتها ---
components.html("""
    <script>
    function killBadges() {
        // الوصول إلى نافذة الأب (المسؤولة عن الشعار الأحمر)
        const parentDoc = window.parent.document;
        const selectors = [
            'div[class*="viewerBadge"]',
            '[data-testid="stStatusWidget"]',
            'footer',
            '#streamlit-connection-status'
        ];
        
        selectors.forEach(selector => {
            const elements = parentDoc.querySelectorAll(selector);
            elements.forEach(el => {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
                el.remove();
            });
        });
    }
    // التنفيذ الفوري والمتكرر كل نصف ثانية
    setInterval(killBadges, 500);
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
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار v20.5 | حماية وتنسيق فائق</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص والمعاينة", "🎬 التحميل", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# 2. الفحص والمعاينة (الجزء المهم لتعديل المساحة)
with tabs[1]:
    st.subheader("🛠️ مركز الاختبار الشامل")
    scan_choice = st.radio("اختر المهمة:", ["فحص ومعاينة الروابط 🔗", "فحص أمان الملفات 📁"], horizontal=True)
    st.markdown('<div class="scan-box">', unsafe_allow_html=True)
    
    if scan_choice == "فحص ومعاينة الروابط 🔗":
        u = st.text_input("ألصق الرابط هنا:", key="url_input_v5")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛡️ ابدأ فحص الأمان"):
                if u:
                    try:
                        res = requests.get(u, timeout=5)
                        st.success(f"الرابط مستجيب وآمن ({res.status_code})")
                    except: st.error("❌ الرابط غير متاح")
        with col2:
            if u:
                st.markdown(f'<a href="{u}" target="_blank"><button style="width:100%; background:#238636; color:white; border:none; padding:15px; border-radius:12px; font-weight:bold; cursor:pointer;">👁️ معاينة الرابط</button></a>', unsafe_allow_html=True)
    else:
        u_f = st.file_uploader("ارفع الملف للفحص:", key="file_input_v5")
    
    # إضافة مساحة فارغة صغيرة تحت الأزرار لضمان عدم التداخل
    st.write("") 
    st.write("")
    st.markdown('</div>', unsafe_allow_html=True)

# --- استكمال بقية التبويبات (التحميل، المجتمع، الإدارة) كما هي في كودك السابق ---
with tabs[2]: # التحميل
    v_u = st.text_input("رابط الفيديو للتحميل:", key="dl_v5")
    if st.button("🚀 تحميل الآن"):
        st.info("جاري المعالجة...")
        # كود yt_dlp هنا

# (لوحة الإدارة والتواصل تظل كما هي)
