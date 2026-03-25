import streamlit as st
import tldextract
import sqlite3
import time
from datetime import datetime

# --- 1. إعدادات الصفحة والتنسيق العربي ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# كود التنسيق لتجنب تداخل النصوص وظهور رموز غريبة
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
        .main { background-color: #0e1117; }
        .stButton>button { 
            width: 100%; border-radius: 20px; background: #00d4ff; 
            color: black; font-weight: bold; border: none; height: 3em;
        }
        .report-card { 
            background: rgba(255, 75, 75, 0.1); border: 1px dashed #ff4b4b; 
            border-radius: 12px; padding: 10px; margin: 10px 0; 
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك قاعدة البيانات المحمي ---
def get_db_connection():
    # استخدام اسم جديد كلياً لضمان عدم وجود أخطاء سابقة
    conn = sqlite3.connect('ayman_guard_pro.db', check_same_thread=False)
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS reports (url TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS stats (count INTEGER)')
    c.execute('INSERT OR IGNORE INTO stats (rowid, count) VALUES (1, 250)')
    conn.commit()
    conn.close()

init_db()

# --- 3. لوحة التحكم (القائمة الجانبية) ---
with st.sidebar:
    st.markdown("### 🔐 إدارة النظام")
    admin_key = st.text_input("كلمة المرور:", type="password")
    if admin_key == "ayman123":
        st.success("أهلاً بك يا أيمن")
        if st.button("🗑️ مسح البلاغات"):
            conn = get_db_connection()
            conn.execute("DELETE FROM reports")
            conn.commit()
            conn.close()
            st.rerun()

# --- 4. الواجهة الرئيسية ---
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🛡️ درع أيمن الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>خدمة فحص الروابط وحماية المجتمع من الاحتيال</p>", unsafe_allow_html=True)

# محرك فحص الروابط
url_input = st.text_input("🔍 الصق الرابط المراد فحصه هنا:", placeholder="https://example.com")
if st.button("🚀 اطلق الدرع"):
    if url_input:
        conn = get_db_connection()
        conn.execute("UPDATE stats SET count = count + 1 WHERE rowid = 1")
        conn.commit()
        conn.close()
        
        with st.spinner('جاري التحليل الرقمي...'):
            time.sleep(1)
            extract = tldextract.extract(url_input.lower())
            domain_name = f"{extract.domain}.{extract.suffix}"
            
            # قائمة المواقع الرسمية الموثوقة
