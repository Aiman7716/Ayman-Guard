import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime

# --- 1. التصميم وتوحيد الهوية ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px; }
    div.stButton > button, .stFormSubmitButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; border: none !important; }
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    .data-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-right: 5px solid #1f6feb; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك التليجرام المحسن ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_to_ayman_tele(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

# --- 3. قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('ayman_pro_v290.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS community_reports (name TEXT, content TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS contact_msgs (name TEXT, message TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()

# --- 4. الهيكل الرئيسي ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة المصادقة والربط المضمون v290.0</p></div>', unsafe_allow_html=True)
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 حماية المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- تبويب الفحص الشامل ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f1, f2 = st.tabs(["🔗 الروابط", "📁 الملفات"])
    with f1:
        u_l = st.text_input("أدخل الرابط للفحص:")
        if st.button("🚀 فحص وإرسال تقرير"):
            if u_l:
                res = send_to_ayman_tele(f"🔍 <b>تقرير فحص رابط:</b>\n{u_l}")
                if res: st.success("✅ تم الفحص وإرسال إشعار لتليجرام.")
                else: st.warning("⚠️ تم الفحص، ولكن تعذر إرسال الإشعار (تأكد من تشغيل البوت).")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب محمل الفيديو ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    v_u = st.text_input("رابط الفيديو:")
    if st.button("🚀 جلب الفيديو الآن"):
        if v_u:
            with st.spinner("جاري جلب الفيديو..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'ayman_v.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_u])
                    with open("ayman_v.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ الفيديو", f, "video.mp4")
                    os.remove("ayman_v.mp4")
                except: st.error("عذراً، تعذر الجلب.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب تواصل معنا ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("contact_v290", clear_on_submit=True):
        cn = st.text_input("اسمك:")
        cm = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال الآن"):
            if cn and cm:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                db.cursor().execute("INSERT INTO contact_msgs VALUES (?, ?, ?)", (cn, cm, dt))
                db.commit()
                res = send_to_ayman_tele(f"📧 <b>رسالة جديدة من: {cn}</b>\n{cm}")
                if res: st.success("✅ وصلت رسالتك لتليجرام أيمن.")
                else: st.error("❌ تعذر الإرسال لتليجرام. تأكد من إرسال /start للبوت.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب الإدارة (تفعيل المصادقة المحمي) ---
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔐 لوحة التحكم المصادقة")
    
    # ميزة المصادقة: لا يتم عرض البيانات إلا بعد التحقق
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        pwd_input = st.text_input("أدخل كلمة مرور المدير:", type="password")
        if st.button("تسجيل الدخول"):
            if pwd_input == "ayman7716":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("كلمة المرور خاطئة!")
    else:
        st.success("✅ تم تسجيل الدخول بنجاح")
        if st.button("تسجيل الخروج"):
            st.session_state.authenticated = False
            st.rerun()
            
        st.write("---")
        # عرض البيانات فقط للمصادقين
        data = db.cursor().execute("SELECT * FROM contact_msgs ORDER BY date DESC").fetchall()
        for m in data:
            st.markdown(f'<div class="data-box"><strong>من: {m[0]}</strong><br><small>{m[2]}</small><p>{m[1]}</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
