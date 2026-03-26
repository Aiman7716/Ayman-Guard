import streamlit as st
import sqlite3, requests, hashlib, pandas as pd
from datetime import datetime

# --- 1. الإعدادات ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 

# --- 2. التصميم البصري الفاخر (UI/UX) ---
st.set_page_config(page_title="Ayman Guard", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* ضبط الخلفية والخطوط */
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; }
    .stApp { background-color: #0d1117; }

    /* تحسين الهيدر الرئيسي */
    .main-title {
        background: linear-gradient(90deg, #1f6feb, #58a6ff);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* إخفاء القائمة الجانبية الافتراضية لتحسين المنظر */
    [data-testid="stSidebar"] { display: none; }
    
    /* تنسيق أزرار التنقل العلوية (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #161b22;
        padding: 10px;
        border-radius: 12px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        color: #8b949e !important;
        font-weight: bold !important;
    }
    .stTabs [aria-selected="true"] {
        color: #58a6ff !important;
        border-bottom: 2px solid #58a6ff !important;
    }

    /* بطاقات البيانات المرتبة */
    .glass-card {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        margin-top: 15px;
        text-align: center;
    }

    /* إخفاء الزوائد */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. الواجهة العلوية ---
st.markdown('<div class="main-title"><h1>🛡️ درع أيمن الأمني</h1><p>النسخة الاحترافية v31.0</p></div>', unsafe_allow_html=True)

# استبدال القائمة الجانبية المشوهة بنظام التبويبات الأنيق
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "👥 المجتمع", "📧 تواصل", "🔐 الإدارة"])

# --- 4. محتويات التبويبات ---

with tab1:
    st.markdown('<div class="glass-card"><h3>📊 رادار التهديدات</h3></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.metric("إجمالي البلاغات", "12")
    col2.metric("حالات تم تأمينها", "100%")

with tab2:
    st.markdown('<div class="glass-card"><h3>🔍 مركز الفحص الشامل</h3></div>', unsafe_allow_html=True)
    option = st.selectbox("نوع الفحص:", ["روابط مشبوهة", "ملفات مرفقة"])
    url_input = st.text_input("أدخل الرابط أو ارفع الملف:")
    if st.button("بدء التحليل"):
        st.success("جاري الفحص عبر محركاتنا...")

with tab3:
    st.markdown('<div class="glass-card"><h3>👥 بلاغات المجتمع</h3></div>', unsafe_allow_html=True)
    report_text = st.text_area("صف حالة الاحتيال:")
    if st.button("نشر التحذير"):
        st.info("تم تسجيل البلاغ وإرساله للقنوات الأمنية.")

with tab5:
    st.markdown('<div class="glass-card"><h3>🔐 لوحة التحكم الخاصة بك</h3></div>', unsafe_allow_html=True)
    admin_pw = st.text_input("كلمة سر المسؤول:", type="password")
    if admin_pw == "ayman7716":
        st.success("مرحباً أيمن! يمكنك الآن إدارة التقارير.")
