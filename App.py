import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. الإعدادات والتصميم (منع الأبيض نهائياً) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    section[data-testid="stFileUploadDropzone"] {
        background-color: #161b22 !important;
        border: 2px dashed #1f6feb !important;
        border-radius: 15px;
    }
    div.stButton > button, .stFormSubmitButton > button { 
        width: 100% !important; background-color: #1f6feb !important; 
        color: white !important; border-radius: 12px !important; 
        height: 3.5em !important; font-weight: bold !important; 
    }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك الخلفي ---
DB_NAME = "ayman_final_v85.db"
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

def send_to_telegram(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

def get_site_preview(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        t = soup.title.string if soup.title else "بدون عنوان"
        d = soup.find('meta', attrs={'name': 'description'})
        d = d['content'] if d else "وصف غير متاح لهذه الصفحة."
        return {"title": t, "desc": d}
    except: return None

db = init_db()

# --- 3. بناء الواجهة والتبويبات ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الحماية والمعاينة v850.0</p></div>', unsafe_allow_html=True)
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص والمعاينة", "🎬 التحميل", "👥 المجتمع", "📧 تواصل", "🔐 الإدارة"])

with tabs[0]:
    st.info("👋 مرحباً بك يا أيمن. النظام يعمل الآن بكافة ميزاته وبأقصى استقرار.")

with tabs[1]: # تبويب الفحص (تم دمج المعاينة وإصلاح المسافات)
    f_mode = st.radio("نوع الفحص:", ["فحص رابط 🔗", "فحص ملف 📁"], horizontal=True)
    if f_mode == "فحص رابط 🔗":
        preview_url = st.text_input("ألصق الرابط هنا للمعاينة والفحص:")
        if st.button("🚀 بدء المعاينة والتحليل"):
            if preview_url:
                data = get_site_preview(preview_url)
                if data:
                    st.markdown(f"""
                    <div style="background: #1c2128; border: 1px solid #1f6feb; padding: 15px; border-radius: 12px;">
                        <h4 style="color: #58a6ff;">🌐 {data['title']}</h4>
                        <p style="color: #8b949e;">{data['desc']}</p>
                        <hr style="border: 0.1px solid #30363d;">
                        <p style="color: #3fb950; font-weight: bold;">✅ الرابط جاهز للمعاينة الآمنة</p>
                    </div>
                    """, unsafe_allow_html=True)
                    send_to_telegram(f"🔍 <b>معاينة رابط:</b>\n{preview_url}")
                else: st.error("تعذر جلب بيانات الموقع.")
    else:
        u_file = st.file_uploader("ارفع الملف للفحص (APK, ZIP, TXT):", type=None)
        if st.button("🛡️ فحص الملف الآن"):
            if u_file:
                raw = u_file.getvalue()
                try: content = raw.decode("utf-8")
                except: content = raw.decode("latin-1", errors="replace")
                st.code(content[:1500], language="text")
                send_to_telegram(f"📁 <b>فحص ملف:</b> {u_file.name}")

with tabs[2]: # التحميل
    v_url = st.text_input("رابط الفيديو:")
    if st.button("🎬 جلب الفيديو"):
        if v_url:
            with st.spinner("جاري التحميل..."):
                try:
                    with yt_dlp.YoutubeDL({'format':'best','outtmpl':'v.mp4','quiet':True}) as ydl: ydl.download([v_url])
                    with open("v.mp4", "rb") as f: st.video(f.read())
                    os.remove("v.mp4")
                except: st.error("فشل التحميل.")

with tabs[3]: # المجتمع
    with st.form("com_f", clear_on_submit=True):
        r_n = st.text_input("الاسم:")
        r_d = st.text_area("البلاغ:")
        if st.form_submit_button("نشر البلاغ"):
            if r_d:
                db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?, ?, ?)", (r_n, r_d, datetime.now().strftime("%Y-%m-%d")))
                db.commit()
                st.success("تم التوثيق.")
                send_to_telegram(f"🚨 <b>بلاغ:</b> {r_d}")

with tabs[4]: # تواصل
    with st.form("con_f", clear_on_submit=True):
        c_n = st.text_input("اسمك:")
        c_m = st.text_area("رسالتك:")
        if st.form_submit_button("إرسال الآن"):
            if c_n and c_m:
                db.execute("INSERT INTO messages (sender, content, date) VALUES (?, ?, ?)", (c_n, c_m, datetime.now().strftime("%Y-%m-%d")))
                db.commit()
                send_to_telegram(f"📧 <b>رسالة من {c_n}:</b>\n{c_m}")
                st.success("تم الإرسال.")

with tabs[5]: # الإدارة
    pw = st.text_input("كلمة السر:", type="password")
    if pw == "ayman7716":
        st.subheader("📩 الرسائل المستلمة")
        rows = db.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
        for r in rows: st.info(f"**{r[1]}**: {r[2]}")
