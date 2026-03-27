import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime

# --- 1. إصلاح ألوان منطقة الرفع (وداعاً للون الأبيض) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* جعل منطقة الرفع كحلية داكنة */
    section[data-testid="stFileUploadDropzone"] {
        background-color: #161b22 !important;
        border: 2px dashed #1f6feb !important;
        color: #ffffff !important;
        border-radius: 15px;
    }
    
    /* تعديل لون نصوص منطقة الرفع */
    section[data-testid="stFileUploadDropzone"] div div { color: #ffffff !important; }
    
    /* أزرار زرقاء ملكية واضحة */
    div.stButton > button, .stFormSubmitButton > button { 
        width: 100% !important; 
        background-color: #1f6feb !important; 
        color: #ffffff !important; 
        border-radius: 12px !important; 
        height: 3.5em !important; 
        font-weight: bold !important; 
        border: 2px solid #388bfd !important; 
    }
    
    .text-preview { background: #000000; border: 1px solid #1f6feb; padding: 15px; border-radius: 10px; color: #00ff00; font-family: monospace; overflow-y: auto; max-height: 400px; white-space: pre-wrap; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك قاعدة البيانات والتليجرام ---
DB_NAME = "ayman_final_shield.db"
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.commit()
    return conn
db_conn = init_db()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_tele(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=8)
    except: pass

# --- 3. الواجهة الرئيسية ---
st.markdown('<div style="background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 25px;"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة المعالجة الذكية للأخطاء v380.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 حماية المجتمع", "🔐 الإدارة"])

with tabs[0]: # الفحص الشامل
    st.markdown("### 📁 فحص الملفات والنصوص")
    # هنا منطقة الرفع أصبحت كحلية
    u_file = st.file_uploader("ارفع الملف هنا للفحص:", type=None)
    if st.button("🛡️ بدء فحص المحتوى"):
        if u_file:
            with st.spinner("جاري القراءة بأمان..."):
                try:
                    raw_bytes = u_file.getvalue()
                    # محاولة القراءة كنص، وإذا فشل لا يظهر خطأ أحمر بل يظهر تنبيه
                    try:
                        content = raw_bytes.decode("utf-8")
                        st.success("✅ تم قراءة الملف كنص بنجاح.")
                    except UnicodeDecodeError:
                        content = raw_bytes.decode("latin-1", errors="replace")
                        st.warning("⚠️ هذا الملف ليس نصياً عادياً (ربما ملف مضغوط أو APK).")
                    
                    st.markdown("### 📄 معاينة المحتوى:")
                    st.markdown(f'<div class="text-preview">{content[:5000]}</div>', unsafe_allow_html=True)
                    send_tele(f"📁 <b>فحص ملف:</b> {u_file.name}")
                except Exception as e:
                    st.error("حدث خطأ غير متوقع أثناء القراءة.")
        else: st.error("من فضلك اختر ملفاً.")

# (بقية الأكواد السابقة الخاصة بالتنزيل والإدارة تظل كما هي لضمان الاستقرار)
