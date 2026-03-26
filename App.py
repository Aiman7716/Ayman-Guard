import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random
from datetime import datetime

# --- 1. الإعدادات ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 

# --- 2. التصميم البصري المتقدم (CSS Custom Design) ---
st.set_page_config(page_title="Ayman Guard PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* ضبط الخط العام والاتجاه */
    * { font-family: 'Cairo', sans-serif; direction: RTL; }
    .stApp { background-color: #0d1117; }

    /* تحسين شكل القائمة الجانبية بالكامل */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-left: 1px solid #30363d;
        padding-top: 20px;
    }
    [data-testid="stSidebarNav"] { padding-top: 0px; }
    
    /* تحسين العناوين في القائمة الجانبية */
    .sidebar-title {
        color: #58a6ff;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        padding: 10px;
        border-bottom: 1px solid #30363d;
    }

    /* إصلاح تداخل نصوص الواجهة الرئيسية */
    .hero-section {
        background: linear-gradient(180deg, #1f6feb 0%, #0d1117 100%);
        padding: 40px 20px;
        border-radius: 0 0 25px 25px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .hero-section h1 {
        color: white;
        font-size: 2.2rem;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        margin: 0;
        line-height: 1.4;
    }

    /* بطاقات البيانات المرتبة */
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
        margin-bottom: 15px;
    }
    .metric-card:hover { border-color: #58a6ff; transform: translateY(-5px); }
    
    /* تحسين الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        background: linear-gradient(90deg, #1f6feb, #58a6ff) !important;
        color: white !important;
        font-weight: bold;
        border: none;
    }

    /* إخفاء الزوائد المزعجة */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. محتويات القائمة الجانبية المنظمة ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">🛡️ لوحة التحكم</div>', unsafe_allow_html=True)
    # استخدام نظام الراديو مع أيقونات نصية لجمالية أكثر
    menu = st.radio("اختر القسم:", 
                    ["🏠 الرادار الرئيسي", "🔍 فحص الملفات", "🔗 فحص الروابط", "👥 المجتمع الآمن", "📧 مراسلة الإدارة", "🔐 الإدارة والتقارير"],
                    index=0)
    st.markdown("---")
    st.markdown("<p style='text-align:center; color:#8b949e;'>أيمن جارد PRO v30.0</p>", unsafe_allow_html=True)

# --- 4. الواجهة الرئيسية (Hero Section) لمنع التداخل ---
st.markdown("""
    <div class="hero-section">
        <h1>درع أيمن الأمني</h1>
        <p style="color:#c9d1d9; font-size:1.1rem;">المنصة العالمية لتأمين المجتمع الرقمي</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. منطق الأقسام (نفس المنطق التقني السابق مع تحسين العرض) ---
if menu == "🏠 الرادار الرئيسي":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-card"><h3>📊 البلاغات</h3><h2 style="color:#58a6ff;">0</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>📩 الرسائل</h3><h2 style="color:#58a6ff;">0</h2></div>', unsafe_allow_html=True)
    st.info("💡 النظام يعمل بنجاح ويقوم بتحديث البيانات لحظياً.")

elif menu == "🔐 الإدارة والتقارير":
    st.markdown("### 🔐 منطقة الإدارة")
    pw = st.text_input("كلمة المرور:", type="password")
    if pw == "ayman7716":
        st.success("✅ تم تسجيل الدخول")
        # عرض البيانات ببطاقات مرتبة بدلاً من الجداول
        st.markdown('<div class="metric-card"><small>2026-03-26</small><br><b>بلاغ جديد: محاولة احتيال مالي</b></div>', unsafe_allow_html=True)
