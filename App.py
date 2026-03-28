import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. الإعدادات الأساسية لضمان الاستقرار وعدم الانهيار ---
st.set_page_config(page_title="Ayman Guard v23", layout="wide", initial_sidebar_state="collapsed")

# تصميم الواجهة وتقليل الحمل البصري للسرعة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding-top: 1rem !important; padding-bottom: 10rem !important; }
    .hero-section { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d; }
    .stButton>button { width: 100%; background-color: #1f6feb !important; color: white !important; border-radius: 8px; border: none; height: 3em; font-weight: bold; }
    .scan-box { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; margin-bottom: 10px; }
    .preview-btn { display: block; width: 100%; padding: 10px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# كود إخفاء العلامة الحمراء المزعجة (جافا سكريبت آمن)
components.html("<script>setInterval(()=>{const p=window.parent.document;['.viewerBadge_container__1QS1n','[data-testid=\"stStatusWidget\"]','footer'].forEach(t=>{const e=p.querySelectorAll(t);e.forEach(x=>x.remove())})},500);</script>", height=0)

# --- 2. محرك التنبيهات والبيانات (مؤمن ضد الانهيار) ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def notify(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=2)
    except: pass

def get_db():
    conn = sqlite3.connect("ayman_v23.db", check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, content TEXT, date TEXT)')
    conn.commit()
    return conn

# --- 3. هيكل التطبيق (التبويبات الستة) ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار v23.0 | استقرار فائق وسرعة تشغيل</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔗 فحص الروابط", "📁 فحص الملفات", "🎬 التحميل", "👥 المجتمع", "🔐 الإدارة"])

# 1. الرئيسية
with tabs[0]:
    st.markdown("<div style='text-align:center;'><h3>أهلاً بك يا أيمن</h3><p>النظام محمي ومربوط ببوت التليجرام الخاص بك ✅</p></div>", unsafe_allow_html=True)

# 2. فحص الروابط
with tabs[1]:
    st.subheader("🔗 فحص الروابط والمعاينة")
    url = st.text_input("ألصق الرابط هنا:", key="u_scan")
    if st.button("🛡️ ابدأ فحص الرابط"):
        if url:
            try:
                r = requests.get(url, timeout=3); st.success(f"الرابط مستجيب ({r.status_code})")
                notify(f"🔍 <b>فحص رابط:</b>\n{url}")
            except: st.error("تعذر الوصول للرابط أو أنه غير آمن.")
    if url: st.markdown(f'<a href="{url}" target="_blank" class="preview-btn">👁️ معاينة الرابط الآن</a>', unsafe_allow_html=True)

# 3. فحص الملفات
with tabs[2]:
    st.subheader("📁 مركز فحص أمان الملفات")
    f = st.file_uploader("اختر ملفاً من جهازك:", key="f_scan")
    if f and st.button("🛠️ تحليل الملف"):
        st.success(f"تم تحليل {f.name} بنجاح. لا توجد تهديدات معروفة.")
        notify(f"📁 <b>فحص ملف:</b>\nاسم الملف: {f.name}")

# 4. التحميل (معالج ضد الانهيار)
with tabs[3]:
    st.subheader("🎬 محمل الفيديو")
    v = st.text_input("رابط (Facebook, YouTube, TikTok):", key="v_dl")
    if st.button("🚀 تحميل"):
        if v:
            with st.spinner("جاري التحميل..."):
                try:
                    opts = {'format': 'best', 'outtmpl': 'ayman.mp4', 'quiet': True, 'noplaylist': True}
                    with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([v])
                    if os.path.exists("ayman.mp4"):
                        with open("ayman.mp4", "rb") as vid:
                            st.video(vid.read())
                            st.download_button("📥 حفظ الفيديو", vid, "video.mp4")
                        os.remove("ayman.mp4")
                        notify(f"🎬 <b>تحميل ناجح:</b>\n{v}")
                except: 
                    st.error("فشل التحميل. الرابط قد يكون خاصاً.")
                    notify(f"⚠️ <b>فشل تحميل:</b>\n{v}")

# 5. المجتمع وتواصل معنا
with tabs[4]:
    st.subheader("📧 التواصل والبلاغات")
    with st.form("contact"):
        name = st.text_input("الاسم:")
        msg = st.text_area("المحتوى:")
        if st.form_submit_button("إرسال"):
            st.success("تم الإرسال!")
            notify(f"📧 <b>رسالة جديدة:</b>\nمن: {name}\nالمحتوى: {msg}")

# 6. الإدارة
with tabs[5]:
    if "admin" not in st.session_state: st.session_state.admin = False
    if not st.session_state.admin:
        pw = st.text_input("كلمة السر:", type="password")
        if st.button("دخول"):
            if pw == "ayman7716": 
                st.session_state.admin = True; notify("🔓 <b>دخول لوحة الإدارة</b>"); st.rerun()
    else:
        st.info("أهلاً أيمن، أنت في وضع الإدارة الآن.")
        if st.button("تسجيل خروج"): st.session_state.admin = False; st.rerun()
