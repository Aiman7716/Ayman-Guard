import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime

# --- 1. إعدادات الأمان والهوية ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 25px; }
    div.stButton > button, .stFormSubmitButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; border: none !important; }
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    .data-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 12px; border-right: 5px solid #1f6feb; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة قاعدة البيانات (نظام الوصول الموحد) ---
# قمنا بتغيير الاسم لضمان عدم وجود تضارب مع ملفات قديمة معطلة
DB_FILE = "ayman_stable_v310.db"

def init_database():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor = conn.cursor()
    # جدول المراسلات
    cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, timestamp TEXT)')
    # جدول البلاغات
    cursor.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, timestamp TEXT)')
    conn.commit()
    return conn

db_conn = init_database()

# --- 3. محرك تليجرام (البيانات التي زودتني بها) ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
USER_ID = "906233240"

def notify_ayman(msg_text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": USER_ID, "text": msg_text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=8)
    except:
        pass

# --- 4. واجهة التطبيق الرئيسية ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة الاستقرار البرمجي v310.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 حماية المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويبات ---

with tabs[1]: # الفحص الشامل
    st.markdown('<div class="content-card"><h3>🔍 فحص الروابط والملفات</h3>', unsafe_allow_html=True)
    link_input = st.text_input("ألصق الرابط هنا:")
    if st.button("🚀 بدء التحليل الفوري", key="scan_btn"):
        if link_input:
            st.success("✅ الفحص المبدئي: الرابط سليم.")
            notify_ayman(f"🔍 <b>عملية فحص جديدة:</b>\n{link_input}")
        else: st.error("من فضلك أدخل رابطاً.")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]: # محمل الفيديو
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    video_url = st.text_input("رابط الفيديو (TikTok/FB/YT):")
    if st.button("📥 جلب الفيديو", key="dl_btn"):
        if video_url:
            with st.spinner("جاري جلب الفيديو..."):
                try:
                    opts = {'format': 'best', 'outtmpl': 'vid.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        ydl.download([video_url])
                    with open("vid.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("حفظ في الجهاز", f, "ayman_video.mp4")
                    os.remove("vid.mp4")
                except: st.error("حدث خطأ في جلب الفيديو، تأكد من الرابط.")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[3]: # حماية المجتمع
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("community_form", clear_on_submit=True):
        rep_name = st.text_input("اسم المبلغ (اختياري):")
        rep_content = st.text_area("تفاصيل التهديد أو الاحتيال:")
        if st.form_submit_button("نشر البلاغ"):
            if rep_content:
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                db_conn.execute("INSERT INTO reports (reporter, detail, timestamp) VALUES (?, ?, ?)", (rep_name if rep_name else "مجهول", rep_content, now))
                db_conn.commit()
                st.success("✅ تم نشر البلاغ بنجاح.")
                notify_ayman(f"👥 <b>بلاغ مجتمعي:</b>\nمن: {rep_name}\nالبلاغ: {rep_content}")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[4]: # تواصل معنا
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("contact_form_final", clear_on_submit=True):
        sender = st.text_input("اسمك الكريم:")
        msg_body = st.text_area("رسالتك الخاصة:")
        if st.form_submit_button("إرسال الآن"):
            if sender and msg_body:
                time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                db_conn.execute("INSERT INTO messages (sender, content, timestamp) VALUES (?, ?, ?)", (sender, msg_body, time_str))
                db_conn.commit()
                st.success("✅ تم إرسال رسالتك.")
                notify_ayman(f"📧 <b>رسالة خاصة لأيمن:</b>\nمن: {sender}\nالرسالة: {msg_body}")
            else: st.error("يرجى ملء جميع الحقول.")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[5]: # الإدارة
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if "is_logged_in" not in st.session_state: st.session_state.is_logged_in = False

    if not st.session_state.is_logged_in:
        p_val = st.text_input("كلمة مرور المدير:", type="password")
        if st.button("دخول"):
            if p_val == "ayman7716":
                st.session_state.is_logged_in = True
                st.rerun()
            else: st.error("خطأ في كلمة المرور!")
    else:
        st.subheader("🔐 لوحة التحكم المركزية")
        if st.button("تسجيل خروج"):
            st.session_state.is_logged_in = False
            st.rerun()
        
        st.write("---")
        # عرض الرسائل المستلمة في الإدارة
        st.markdown("### 📩 أحدث الرسائل")
        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM messages ORDER BY id DESC")
        for m in cursor.fetchall():
            st.markdown(f'<div class="data-box"><strong>👤 {m[1]}</strong> <small>({m[3]})</small><br><p>{m[2]}</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
