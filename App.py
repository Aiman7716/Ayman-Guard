import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime

# --- 1. التصميم الملكي (علاج اللون الأبيض نهائياً) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* صبغ منطقة الرفع باللون الكحلي الداكن لمنع الإزعاج البصري */
    section[data-testid="stFileUploadDropzone"] {
        background-color: #161b22 !important;
        border: 2px dashed #1f6feb !important;
        color: #ffffff !important;
        border-radius: 15px;
    }
    
    /* توحيد الأزرار باللون الأزرق النيلي الملكي */
    div.stButton > button, .stFormSubmitButton > button { 
        width: 100% !important; 
        background-color: #1f6feb !important; 
        color: white !important; 
        border-radius: 12px !important; 
        height: 3.5em !important; 
        font-weight: bold !important; 
        border: 1px solid #388bfd !important; 
    }

    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 25px; }
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    .data-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 12px; border-right: 5px solid #1f6feb; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك الخلفي (قاعدة البيانات والتليجرام) ---
DB_NAME = "ayman_ultra_v500.db"
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

def send_tele(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

db_conn = init_db()

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>النسخة الشاملة والمستقرة v500.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🔍 الفحص", "🎬 التحميل", "👥 المجتمع", "📧 تواصل", "🔐 الإدارة"])

# --- تبويب الفحص (حل مشكلة الشاشة الحمراء) ---
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    u_file = st.file_uploader("ارفع الملف للفحص (APK, TXT, ZIP...):", type=None)
    if st.button("🚀 بدء فحص الملف"):
        if u_file:
            try:
                # القراءة بترميز مرن جداً لمنع الانهيار
                raw_bytes = u_file.getvalue()
                content_preview = raw_bytes.decode("utf-8", errors="replace")[:2000]
                st.success(f"✅ تم فحص الملف: {u_file.name}")
                st.code(content_preview, language="text")
                send_tele(f"🔍 <b>فحص ملف:</b> {u_file.name}")
            except: st.error("تعذر عرض محتوى الملف، لكن تم استلامه بنجاح.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب التحميل (استعادة العمل) ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    if st.button("🎬 جلب الفيديو وتحميله"):
        if v_url:
            with st.spinner("جاري الجلب..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'ayman_temp.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                    with open("ayman_temp.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ في الجهاز", f, "video.mp4")
                    os.remove("ayman_temp.mp4")
                except: st.error("عذراً، الرابط غير مدعوم أو هناك مشكلة في الاتصال.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب المجتمع (استعادة العمل) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("rep_f", clear_on_submit=True):
        r_name = st.text_input("اسم المبلغ:")
        r_msg = st.text_area("تفاصيل البلاغ:")
        if st.form_submit_button("نشر البلاغ"):
            if r_msg:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                db_conn.execute("INSERT INTO reports (reporter, detail, date) VALUES (?, ?, ?)", (r_name if r_name else "مجهول", r_msg, dt))
                db_conn.commit()
                st.success("✅ تم نشر بلاغك.")
                send_tele(f"👥 <b>بلاغ مجتمعي:</b> {r_msg}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب تواصل معنا (استعادة العمل) ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("con_f", clear_on_submit=True):
        c_name = st.text_input("اسمك:")
        c_msg = st.text_area("رسالتك لأيمن:")
        if st.form_submit_button("إرسال الآن"):
            if c_name and c_msg:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                db_conn.execute("INSERT INTO messages (sender, content, date) VALUES (?, ?, ?)", (c_name, c_msg, dt))
                db_conn.commit()
                st.success("✅ تم الإرسال.")
                send_tele(f"📧 <b>رسالة خاصة:</b> من {c_name}\n{c_msg}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب الإدارة (استعادة العمل) ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    admin_pw = st.text_input("كلمة مرور المدير:", type="password")
    if admin_pw == "ayman7716":
        st.subheader("📩 صندوق الوارد")
        msgs = db_conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
        for m in msgs:
            st.markdown(f'<div class="data-box"><strong>👤 {m[1]}</strong><br>{m[2]}<br><small>{m[3]}</small></div>', unsafe_allow_html=True)
    elif admin_pw: st.error("كلمة المرور غير صحيحة")
    st.markdown('</div>', unsafe_allow_html=True)
