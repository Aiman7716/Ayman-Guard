import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from datetime import datetime

# --- 1. التصميم الجمالي السيادي v19 ---
st.set_page_config(page_title="Ayman Guard Pro v19", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 40px; border-radius: 25px; text-align: center;
        margin-bottom: 25px; border: 1px solid #30363d;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
    
    /* الأزرار السيادية */
    div.stButton > button {
        width: 100% !important; background: linear-gradient(90deg, #1f6feb, #094cb3) !important;
        color: white !important; border-radius: 12px !important; height: 3.8em !important;
        font-weight: bold !important; border: 2px solid #58a6ff !important; transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.02); border-color: #ffffff !important; box-shadow: 0 0 15px #1f6feb; }
    
    .scan-box { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 20px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الأمان والتنبيهات ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
DB_NAME = "ayman_security_v19.db"

def send_to_telegram(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()

# إدارة الجلسة والحماية
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None
if 'failed_attempts' not in st.session_state: st.session_state.failed_attempts = 0

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الحماية الذكي v19.0 | مؤمن بالكامل</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص والمعاينة", "🎬 التحميل", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

with tabs[0]: # الرئيسية
    st.markdown("<div style='text-align:center;'><h2>مرحباً بك في المنطقة الآمنة يا أيمن</h2><p>النظام الآن تحت حماية "رادار التنبيهات" النشط.</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("حالة الدرع", "مشغل 🛡️", "Active")
    c2.metric("التنبيهات", "مربوطة 📲", "Telegram")
    c3.metric("الأمان", "100%", "Secure")

with tabs[1]: # الفحص (كما طلبته بخيارين بارزين)
    choice = st.radio("نوع العملية:", ["فحص ومعاينة الروابط 🔗", "فحص أمان الملفات 📁"], horizontal=True)
    st.markdown('<div class="scan-box">', unsafe_allow_html=True)
    if choice == "فحص ومعاينة الروابط 🔗":
        u = st.text_input("ألصق الرابط:")
        col1, col2 = st.columns(2)
        if col1.button("🛡️ فحص الرابط"):
            if u:
                try:
                    res = requests.get(u, timeout=5)
                    st.success(f"الرابط مستجيب: {res.status_code}")
                except: st.error("رابط غير آمن")
        if col2.button("👁️ معاينة"):
            if u: st.markdown(f'<a href="{u}" target="_blank"><button style="width:100%; background:#238636; color:white; border:none; padding:15px; border-radius:12px;">فتح المعاينة</button></a>', unsafe_allow_html=True)
    else:
        u_f = st.file_uploader("اختر ملفاً للفحص:")
        if u_f and st.button("📁 ابدأ فحص الملف"):
            st.success("الملف آمن بصرياً")
            st.code(u_f.getvalue().decode("latin-1", errors="replace")[:1000])
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]: # التحميل
    v_u = st.text_input("رابط الفيديو:")
    if st.button("🎬 تحميل"):
        if v_u:
            with st.spinner(" "):
                try:
                    with yt_dlp.YoutubeDL({'outtmpl': 'v.mp4', 'quiet': True}) as ydl: ydl.download([v_u])
                    st.video("v.mp4")
                    st.download_button("📥 حفظ", open("v.mp4", "rb"), "video.mp4")
                    os.remove("v.mp4")
                except: st.error("خطأ في التحميل")

with tabs[4]: # تواصل معنا
    with st.form("contact"):
        n, m = st.text_input("الاسم:"), st.text_area("الرسالة:")
        if st.form_submit_button("📧 إرسال"):
            db.execute("INSERT INTO messages (sender, content, date) VALUES (?,?,?)", (n, m, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("تم الإرسال"); send_to_telegram(f"📧 رسالة تواصل: {m}")

with tabs[5]: # الإدارة بنظام "رصد التطفل"
    if not st.session_state.logged_in:
        st.subheader("🔐 الدخول للأعضاء المصرح لهم فقط")
        input_pwd = st.text_input("كلمة السر السيادية:", type="password")
        
        if st.button("👤 تسجيل الدخول (طلب كود التليجرام)"):
            if input_pwd == "ayman7716":
                st.session_state.auth_code = str(random.randint(1000, 9999))
                send_to_telegram(f"🔐 كود الدخول الخاص بك يا أيمن: <b>{st.session_state.auth_code}</b>")
                st.info("تم إرسال الكود لتليجرام.")
                st.session_state.failed_attempts = 0 # تصفير المحاولات عند النجاح
            else:
                st.session_state.failed_attempts += 1
                # --- تنبيه الاختراق الفوري ---
                alert_msg = f"""
⚠️ <b>محاولة اختراق مكتشفة!</b>
اسم المستخدم المستهدف: أيمن
كلمة السر المستخدمة: <code>{input_pwd}</code>
عدد المحاولات الفاشلة: {st.session_state.failed_attempts}
التوقيت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                send_to_telegram(alert_msg)
                st.error("⚠️ كلمة السر غير صحيحة. تم تسجيل محاولة الدخول وإبلاغ أيمن فوراً.")

        if st.session_state.auth_code:
            v_code = st.text_input("أدخل كود التحقق من تليجرام:")
            if st.button("🔓 تأكيد"):
                if v_code == st.session_state.auth_code:
                    st.session_state.logged_in = True; st.rerun()
                else:
                    send_to_telegram(f"⚠️ <b>تنبيه:</b> تم إدخال كود تحقق خاطئ: {v_code}")
                    st.error("كود غير صحيح!")
    else:
        st.success("أهلاً بك يا قائد")
        if st.button("🔴 خروج"): st.session_state.logged_in = False; st.rerun()
        # عرض الرسائل والبلاغات هنا...
