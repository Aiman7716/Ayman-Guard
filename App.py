import streamlit as st
import tldextract
import sqlite3
import time
from datetime import datetime

# --- إعدادات المظهر والخطوط السليمة ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
        .main { background-color: #0e1117; }
        .stButton>button { 
            width: 100%; border-radius: 25px; background: #00d4ff; 
            color: black; font-weight: bold; border: none; height: 3.5em;
        }
        .report-box { 
            background: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; 
            border-radius: 15px; padding: 15px; margin: 10px 0; 
        }
        /* حل مشكلة تداخل النصوص في القوائم */
        .stExpander { border-radius: 15px; background-color: #1a1c24; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# --- محرك قاعدة البيانات ---
def get_db():
    conn = sqlite3.connect('ayman_shield_final.db', check_same_thread=False)
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS reports (url TEXT, date TEXT)')
        conn.execute('CREATE TABLE IF NOT EXISTS stats (count INTEGER)')
        conn.execute('INSERT OR IGNORE INTO stats (rowid, count) VALUES (1, 250)')

init_db()

# --- القائمة الجانبية ---
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")
    pwd = st.text_input("كلمة المرور:", type="password")
    if pwd == "ayman123":
        if st.button("🗑️ مسح سجل البلاغات"):
            with get_db() as conn:
                conn.execute("DELETE FROM reports")
            st.success("تم المسح")

# --- الواجهة الرئيسية (تصحيح النصوص) ---
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🛡️ درع أيمن الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>حمايتك تبدأ من هنا.. افحص الروابط قبل فتحها</p>", unsafe_allow_html=True)

# محرك الفحص
url_in = st.text_input("🔍 الصق الرابط المراد فحصه:", placeholder="https://
