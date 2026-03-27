import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from datetime import datetime

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="Ayman Guard v15", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d; }
    /* جعل الأزرار ظاهرة وبارزة دائماً */
    div.stButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; height: 3.5em !important; font-weight: bold !important; border: 1px solid #58a6ff !important; }
    .status-card { background: #1c2128; border: 1px solid #30363d; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك التقني والأمان ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
DB_NAME = "ayman_v15_final.db"

def send_to_telegram(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()

# إدارة الجلسة (لضمان عمل التبويبات)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None

# --- 3. الواجهة البرمجية ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الحماية والمصادقة v15.0</p></div>', unsafe_allow_html=True)

# التبويبات (تعريفها بشكل مستقل لضمان الفعالية)
tab_scan, tab_dl, tab_comm, tab_admin = st.tabs(["🔍 الفحص والمعاينة", "🎬 التحميل الذكي", "👥 حماية المجتمع", "🔐 الإدارة"])

with tab_scan:
    st.subheader("🔗 فحص الروابط والملفات")
    target_url = st.text_input("ألصق الرابط هنا للفحص فوراً:", placeholder="https://example.com")
    
    col1, col2 = st.columns(2)
    # الأزرار خارج أي شرط لتكون ظاهرة دائماً كما طلبت
    if col1.button("🛡️ ابدأ فحص الأمان"):
        if target_url:
            try:
                res = requests.get(target_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                st.success(f"✅ الرابط نشط (كود: {res.status_code})")
                send_to_telegram(f"🔍 فحص رابط: {target_url}")
            except: st.error("❌ الرابط غير مستجيب.")
        else: st.warning("ألصق رابطاً أولاً.")

    if target_url:
        st.markdown(f'<a href="{target_url}" target="_blank"><button style="width:100%; background-color:#238636; color:white; border:none; padding:15px; border-radius:10px; cursor:pointer; font-weight:bold;">👁️ معاينة الرابط في نافذة جديدة آمنة</button></a>', unsafe_allow_html=True)
        st.caption("تم تفعيل المعاينة الخارجية لتجنب حجب المواقع (مثل فيسبوك).")

with tab_dl:
    st.subheader("🎬 محرك التحميل")
    v_link = st.text_input("رابط الفيديو (Facebook / YouTube):")
    if st.button("🚀 بدء التحميل الآن"):
        if v_link:
            with st.spinner("جارِ المعالجة..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'v.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_link])
                    with open("v.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ الفيديو", f, "video.mp4")
                    os.remove("v.mp4")
                except: st.error("⚠️ فشل التحميل. الرابط قد يكون خاصاً.")
        else: st.warning("ألصق الرابط أولاً.")

with tab_comm:
    st.subheader("🚨 بلاغات المجتمع")
    with st.form("com_form"):
        reporter = st.text_input("الاسم:")
        details = st.text_area("تفاصيل النشاط المشبوه:")
        if st.form_submit_button("إرسال البلاغ"):
            db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?,?,?)", (reporter, details, datetime.now().strftime("%Y-%m-%d")))
            db.commit()
            st.success("تم التوثيق بنجاح.")
            send_to_telegram(f"🚨 بلاغ جديد من {reporter}: {details}")

with tab_admin:
    if not st.session_state.logged_in:
        st.subheader("🔐 منطقة الإدارة السيادية")
        pwd = st.text_input("كلمة السر:", type="password")
        if pwd == "ayman7716":
            # زر تسجيل الدخول والمصادقة الثنائية
            if st.button("👤 تسجيل الدخول (طلب رمز التليجرام)"):
                st.session_state.auth_code = str(random.randint(1000, 9999))
                send_to_telegram(f"🔐 كود الدخول الخاص بك يا أيمن: <b>{st.session_state.auth_code}</b>")
                st.info("تم إرسال الرمز لحسابك.")

            if st.session_state.auth_code:
                code_input = st.text_input("أدخل الرمز المستلم:")
                if st.button("🔓 تأكيد الدخول"):
                    if code_input == st.session_state.auth_code:
                        st.session_state.logged_in = True
                        st.rerun()
                    else: st.error("الرمز غير صحيح.")
    else:
        st.success("🔓 مرحباً بك في لوحة التحكم يا أيمن")
        if st.button("🔴 خروج"):
            st.session_state.logged_in = False
            st.rerun()
        st.write("---")
        st.write("🚨 أرشيف البلاغات:")
        for r in db.execute("SELECT * FROM reports ORDER BY id DESC").fetchall():
            st.warning(f"📅 {r[3]} | المبلغ: {r[1]}\n\nالتفاصيل: {r[2]}")
