import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime

# --- 1. التصميم الداكن الصارم (منع اللون الأبيض تماماً) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* تغيير منطقة الرفع للون الكحلي الغامق جداً */
    section[data-testid="stFileUploadDropzone"] {
        background-color: #0b0e14 !important;
        border: 2px solid #1f6feb !important;
        color: #ffffff !important;
        border-radius: 10px;
    }
    
    /* توحيد الأزرار باللون الأزرق النيلي */
    div.stButton > button, .stFormSubmitButton > button { 
        background-color: #1f6feb !important; 
        color: white !important; 
        border-radius: 8px !important;
        border: none !important;
    }
    
    .hero-banner { background: #161b22; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #1f6feb; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات ---
DB_NAME = "ayman_stable.db"
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.commit()
    return conn
db_conn = init_db()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_tele(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

# --- 3. الواجهة المبسطة ---
st.markdown('<div class="hero-banner"><h1>🛡️ درع أيمن</h1><p>نسخة مستقرة وخالية من الأخطاء البصرية</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🔍 فحص", "🎬 تحميل", "📧 تواصل", "🔐 إدارة"])

with tabs[0]: # الفحص (معالجة الملفات كبيانات خام لمنع الخطأ الأحمر)
    u_file = st.file_uploader("اختر ملفاً للفحص:", type=None)
    if st.button("بدء الفحص"):
        if u_file:
            st.info(f"تم استلام الملف: {u_file.name}")
            # قراءة البيانات كـ "Bytes" لمنع خطأ الـ Unicode نهائياً
            data_preview = str(u_file.getvalue()[:500]) 
            st.code(data_preview, language="text")
            send_tele(f"🔍 فحص ملف: {u_file.name}")
        else: st.error("يرجى اختيار ملف.")

with tabs[1]: # التحميل
    v_url = st.text_input("رابط الفيديو:")
    if st.button("تحميل الآن"):
        if v_url:
            with st.spinner("جاري العمل..."):
                try:
                    with yt_dlp.YoutubeDL({'format':'best','outtmpl':'v.mp4'}) as ydl: ydl.download([v_url])
                    st.video("v.mp4")
                    os.remove("v.mp4")
                except: st.error("تعذر التحميل.")

with tabs[2]: # تواصل معنا
    with st.form("c_form", clear_on_submit=True):
        name = st.text_input("الاسم:")
        msg = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            if name and msg:
                db_conn.execute("INSERT INTO messages (sender, content, date) VALUES (?, ?, ?)", (name, msg, datetime.now().strftime("%Y-%m-%d")))
                db_conn.commit()
                st.success("تم الإرسال.")
                send_tele(f"📧 رسالة من: {name}\n{msg}")

with tabs[3]: # الإدارة
    pw = st.text_input("كلمة السر:", type="password")
    if pw == "ayman7716":
        st.subheader("الرسائل الواردة")
        msgs = db_conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
        for m in msgs: st.write(f"**{m[1]}**: {m[2]}")
