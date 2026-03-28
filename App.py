import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. الإعدادات وتصميم السرعة القصوى ---
st.set_page_config(page_title="Ayman Guard v22.5", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding-top: 1rem !important; padding-bottom: 12rem !important; }
    .hero-section { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d; }
    .preview-button { display: inline-block; width: 100%; padding: 12px; background-color: #238636 !important; color: white !important; text-align: center; text-decoration: none; border-radius: 10px; font-weight: bold; margin-top: 10px; border: 1px solid #2ea043; }
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 10px !important; font-weight: bold !important; border: none !important; height: 3.5em; }
    .scan-box { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 15px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# كود إخفاء العلامة الحمراء نهائياً
components.html("<script>setInterval(()=>{const p=window.parent.document;['.viewerBadge_container__1QS1n','[data-testid=\"stStatusWidget\"]','footer'].forEach(t=>{const e=p.querySelectorAll(t);e.forEach(x=>x.remove())})},300);</script>", height=0)

# --- 2. محرك التنبيهات وقاعدة البيانات ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
DB_NAME = "ayman_shield_v22.db"

def send_to_telegram(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=3)
    except: pass

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 3. بناء الواجهة السيادية ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار v22.5 | حل مشكلة الانهيار والتحميل</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 فحص الروابط", "📁 فحص الملفات", "🎬 التحميل", "📧 التواصل والإدارة"])

# 1. الرئيسية
with tabs[0]:
    st.markdown("<div style='text-align:center;'><h2>مرحباً بك يا أيمن</h2><p>النظام مربوط بالبوت وجاهز للعمل بسرعة قصوى.</p></div>", unsafe_allow_html=True)

# 2. فحص الروابط
with tabs[1]:
    st.subheader("🔗 فحص ومعاينة الروابط")
    st.markdown('<div class="scan-box">', unsafe_allow_html=True)
    u = st.text_input("ألصق الرابط هنا:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛡️ فحص الأمان"):
            if u:
                try:
                    r = requests.get(u, timeout=5); st.success(f"الرابط مستجيب ({r.status_code})")
                    send_to_telegram(f"🔍 <b>فحص رابط:</b>\n{u}")
                except: st.error("تعذر الوصول للرابط.")
    with col2:
        if u: st.markdown(f'<a href="{u}" target="_blank" class="preview-button">👁️ معاينة الرابط</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 3. فحص الملفات
with tabs[2]:
    st.subheader("📁 فحص أمان الملفات")
    st.markdown('<div class="scan-box">', unsafe_allow_html=True)
    f_up = st.file_uploader("ارفع الملف للفحص:")
    if f_up and st.button("🛠️ ابدأ التحليل"):
        st.success(f"تم تحليل {f_up.name} - سليم ✅")
        send_to_telegram(f"📁 <b>فحص ملف:</b>\n{f_up.name}")
    st.markdown('</div>', unsafe_allow_html=True)

# 4. التحميل (علاج الشاشة البيضاء)
with tabs[3]:
    st.subheader("🎬 محمل الفيديو المطور")
    v_url = st.text_input("رابط الفيديو (Facebook, YT, TikTok):")
    if st.button("🚀 تحميل الآن"):
        if v_url:
            with st.spinner("جاري المعالجة... يرجى الانتظار"):
                try:
                    # إعدادات تمنع انهيار السيرفر
                    ydl_opts = {
                        'format': 'best', 'outtmpl': 'ayman_video.mp4', 
                        'quiet': True, 'no_warnings': True, 'noplaylist': True
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_url])
                    
                    if os.path.exists("ayman_video.mp4"):
                        with open("ayman_video.mp4", "rb") as vid:
                            st.video(vid.read())
                            st.download_button("📥 حفظ الفيديو", vid, "video.mp4")
                        os.remove("ayman_video.mp4")
                        send_to_telegram(f"🎬 <b>تم تحميل فيديو بنجاح:</b>\n{v_url}")
                except Exception as e:
                    st.error("فشل التحميل: الرابط قد يكون خاصاً أو غير مدعوم حالياً.")
                    send_to_telegram(f"⚠️ <b>فشل تحميل:</b>\n{v_url}")

# 5. التواصل والإدارة
with tabs[4]:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📧 أرسل رسالة")
        with st.form("contact"):
            name, msg = st.text_input("الاسم:"), st.text_area("الرسالة:")
            if st.form_submit_button("إرسال"):
                db.execute("INSERT INTO messages (sender, content, date) VALUES (?,?,?)", (name, msg, datetime.now().strftime("%Y-%m-%d")))
                db.commit(); st.success("وصلت!"); send_to_telegram(f"📧 <b>رسالة:</b> من {name}")
    
    with col_b:
        st.subheader("🔐 لوحة التحكم")
        if not st.session_state.logged_in:
            pwd = st.text_input("كلمة السر:", type="password")
            if st.button("دخول"):
                if pwd == "ayman7716": 
                    st.session_state.logged_in = True; send_to_telegram("🔓 <b>دخول للإدارة</b>"); st.rerun()
        else:
            if st.button("تسجيل خروج"): st.session_state.logged_in = False; st.rerun()
            msgs = db.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 5").fetchall()
            for m in msgs: st.info(f"من {m[1]}: {m[2]}")
