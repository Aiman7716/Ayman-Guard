import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. الإعدادات والتصميم الجمالي ---
st.set_page_config(page_title="Ayman Guard Pro v21", layout="wide")

# كود التنسيق وإخفاء معالم الموقع (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* إخفاء القوائم والفوتر والهيدر */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* إخفاء العلامة الحمراء وشعار ستريمليت */
    div[data-testid="stStatusWidget"], [class*="viewerBadge"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* حل مشكلة التغطية: توفير مساحة كبيرة في الأسفل لرفع الأزرار */
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 12rem !important; 
    }

    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 40px; border-radius: 25px; text-align: center;
        margin-bottom: 25px; border: 1px solid #30363d;
    }
    
    .preview-button {
        display: inline-block; width: 100%; padding: 15px;
        background-color: #238636 !important; color: white !important;
        text-align: center; text-decoration: none; border-radius: 12px;
        font-weight: bold; border: 2px solid #2ea043; margin-top: 10px;
    }
    
    div.stButton > button {
        width: 100% !important; background: linear-gradient(90deg, #1f6feb, #094cb3) !important;
        color: white !important; border-radius: 12px !important; height: 3.5em !important;
        font-weight: bold !important; border: 2px solid #58a6ff !important;
    }
    .scan-box { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 20px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# كود JavaScript لإخفاء العلامة الحمراء من الجذور
components.html("""
    <script>
    function hideElements() {
        const p = window.parent.document;
        const targets = ['.viewerBadge_container__1QS1n', '[data-testid="stStatusWidget"]', 'footer'];
        targets.forEach(t => {
            const els = p.querySelectorAll(t);
            els.forEach(el => el.remove());
        });
    }
    setInterval(hideElements, 500);
    </script>
""", height=0)

# --- 2. محرك الأمان وقواعد البيانات ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
DB_NAME = "ayman_final_v21.db"

def send_to_telegram(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 3. بناء واجهة التبويبات ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار v21.0 | تحديث محرك التحميل</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 التحميل", "👥 المجتمع", "📧 تواصل", "🔐 الإدارة"])

# تبويب التحميل (حل مشكلة الفيديو)
with tabs[2]:
    st.subheader("🎬 محمل الفيديو الذكي")
    v_url = st.text_input("أدخل رابط الفيديو (FB, YT, TikTok):", key="dl_input_v21")
    
    if st.button("🚀 تحميل الفيديو الآن"):
        if v_url:
            with st.spinner("جاري استخراج الفيديو..."):
                try:
                    # إعدادات متطورة لدعم روابط الفيسبوك وغيرها
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': 'ayman_video.mp4',
                        'quiet': True,
                        'no_warnings': True,
                        'noplaylist': True,
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_url])
                    
                    if os.path.exists("ayman_video.mp4"):
                        with open("ayman_video.mp4", "rb") as f:
                            st.video(f.read())
                            st.download_button("📥 حفظ في معرض الصور", f, "video_ayman.mp4")
                        os.remove("ayman_video.mp4")
                        st.success("تم التجهيز بنجاح!")
                except Exception as e:
                    st.error(f"حدث خطأ: تأكد من أن الرابط عام (Public) وليس خاصاً.")
                    send_to_telegram(f"❌ فشل تحميل فيديو: {v_url}")

# تبويب الفحص والمعاينة (ضمان ظهور الزر)
with tabs[1]:
    st.subheader("🛠️ مركز الاختبار")
    u_input = st.text_input("ألصق الرابط للفحص:", key="scan_v21")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🛡️ فحص الأمان"):
            if u_input:
                try:
                    r = requests.get(u_input, timeout=5)
                    st.success(f"الرابط آمن ({r.status_code})")
                except: st.error("رابط غير صالح")
    with c2:
        if u_input:
            st.markdown(f'<a href="{u_input}" target="_blank" class="preview-button">👁️ معاينة الرابط</a>', unsafe_allow_html=True)

# بقية التبويبات (المجتمع، تواصل، الإدارة)
with tabs[3]: # المجتمع
    with st.form("com_v21"):
        n, d = st.text_input("الاسم:"), st.text_area("البلاغ:")
        if st.form_submit_button("🚨 إرسال"):
            db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?,?,?)", (n, d, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("تم الإرسال")

with tabs[4]: # تواصل
    with st.form("con_v21"):
        n, m = st.text_input("الاسم:"), st.text_area("الرسالة:")
        if st.form_submit_button("📧 إرسال"):
            db.execute("INSERT INTO messages (sender, content, date) VALUES (?,?,?)", (n, m, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("وصلت رسالتك")

with tabs[5]: # الإدارة
    if not st.session_state.logged_in:
        pwd = st.text_input("كلمة السر:", type="password")
        if st.button("🔓 دخول"):
            if pwd == "ayman7716": st.session_state.logged_in = True; st.rerun()
    else:
        st.write("أهلاً أيمن")
        msgs = db.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
        for msg in msgs: st.info(f"من: {msg[1]} | {msg[2]}")
        if st.button("🔴 خروج"): st.session_state.logged_in = False; st.rerun()
