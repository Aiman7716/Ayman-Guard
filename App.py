import streamlit as st
import tldextract
import sqlite3
from datetime import datetime

# 1. إعدادات الصفحة والأيقونة (الشعار الجديد)
st.set_page_config(
    page_title="درع أيمن الذكي",
    page_icon="1774474792146.png",
    layout="centered"
)

# 2. إنشاء قاعدة البيانات
def init_db():
    conn = sqlite3.connect('aiman_guard.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports (url TEXT, email TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (name TEXT, email TEXT, msg TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 3. تصميم الواجهة (CSS) لتناسب ألوان الشعار
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #00d4ff;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #00d4ff;
        color: white;
    }
    .report-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #1e1e1e;
        border: 1px solid #333;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. عرض الشعار في المنتصف
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("1774474792146.png", use_container_width=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# 5. التبويبات (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["🔍 فحص الروابط", "📢 البلاغات", "📧 اتصل بنا", "🔐 الإدارة"])

# --- تبويب الفحص ---
with tab1:
    url_input = st.text_input("أدخل الرابط المراد فحصه هنا:")
    if st.button("بدء الفحص"):
        if url_input:
            ext = tldextract.extract(url_input)
            domain = f"{ext.domain}.{ext.suffix}"
            
            # قاعدة بيانات وهمية للفحص (يمكنك تطويرها)
            malicious_domains = ["test-hack.com", "spamsite.net"]
            
            if domain in malicious_domains:
                st.error(f"⚠️ تحذير: الرابط ({domain}) مشبوه!")
            else:
                st.success(f"✅ الرابط ({
