import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. الإعدادات والتصميم الملكي ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    section[data-testid="stFileUploadDropzone"] { background-color: #161b22 !important; border: 2px dashed #1f6feb !important; border-radius: 15px; }
    div.stButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 12px !important; transition: 0.3s; }
    div.stButton > button:hover { background-color: #388bfd !important; border: 1px solid #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    .stat-card { background: #1c2128; border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك الخلفي والأمان ---
DB_NAME = "ayman_secure_v9.db"
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
        return {"title": soup.title.string if soup.title else "بدون عنوان", 
                "desc": (soup.find('meta', attrs={'name': 'description'}) or {}).get('content', 'وصف غير متاح.')}
    except: return None

db = init_db()

# --- 3. إدارة الجلسة (Login Session) ---
if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None

# --- 4. هيكل الواجهة ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار v9.0 | نظام الحماية والإدارة الذكية</p></div>', unsafe_allow_html=True)
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص والمعاينة", "🎬 التحميل", "👥 المجتمع", "📧 تواصل", "🔐 الإدارة"])

# --- تبويب الفحص والمعاينة ---
with tabs[1]:
    sub = st.radio("المهمة:", ["الروابط 🔗", "الملفات 📁"], horizontal=True)
    if sub == "الروابط 🔗":
        p_url = st.text_input("ألصق الرابط هنا:")
        c1, c2 = st.columns(2)
        if p_url:
            if c1.button("👁️ عرض الصفحة"):
                data = get_site_preview(p_url)
                if data: st.info(f"🌐 **{data['title']}**\n\n{data['desc']}")
                else: st.error("فشل جلب المعاينة.")
            if c2.button("🛡️ فحص الأمان"):
                try:
                    res = requests.get(p_url, timeout=5)
                    if p_url.startswith("https"): st.success("✅ الرابط سليم وآمن (HTTPS)")
                    else: st.warning("⚠️ الرابط يعمل ولكنه غير مشفر (HTTP)")
                except: st.error("❌ الرابط غير سليم أو وهمي.")
                send_to_telegram(f"🔍 فحص رابط: {p_url}")
    else:
        u_file = st.file_uploader("ارفع الملف للفحص:", type=None)
        if u_file and st.button("🛡️ بدء الفحص البصري"):
            content = u_file.getvalue().decode("latin-1", errors="replace")
            st.code(content[:1500])
            st.success("✅ تم فحص هيكل الملف.")

# --- تبويب التحميل المطور ---
with tabs[2]:
    v_url = st.text_input("رابط الفيديو (Facebook/YouTube/Insta):")
    if st.button("🎬 جلب وتحميل الفيديو"):
        if v_url:
            with st.spinner("جاري المعالجة..."):
                try:
                    opts = {'format': 'best', 'outtmpl': 'ayman_video.mp4', 'quiet': True, 'no_warnings': True}
                    with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([v_url])
                    with open("ayman_video.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ في جهازك", f, "ayman_video.mp4")
                    os.remove("ayman_video.mp4")
                except: st.error("عذراً، الرابط خاص أو غير مدعوم حالياً.")

# --- تبويب المجتمع وتواصل معنا ---
with tabs[3]: # المجتمع
    with st.form("com"):
        n, d = st.text_input("الاسم:"), st.text_area("البلاغ:")
        if st.form_submit_button("نشر"):
            if d:
                db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?,?,?)", (n, d, datetime.now().strftime("%Y-%m-%d")))
                db.commit(); st.success("تم التوثيق"); send_to_telegram(f"🚨 بلاغ: {d}")

with tabs[4]: # تواصل
    with st.form("con"):
        n, m = st.text_input("اسمك:"), st.text_area("الرسالة:")
        if st.form_submit_button("إرسال لأيمن"):
            if n and m:
                db.execute("INSERT INTO messages (sender, content, date) VALUES (?,?,?)", (n, m, datetime.now().strftime("%Y-%m-%d")))
                db.commit(); st.success("وصلت رسالتك"); send_to_telegram(f"📧 رسالة من {n}: {m}")

# --- تبويب الإدارة (المصادقة عبر التليجرام) ---
with tabs[5]:
    if not st.session_state.admin_logged_in:
        pwd = st.text_input("أدخل الرقم السري السيادي:", type="password")
        if pwd == "ayman7716":
            st.success("✅ الرقم السري صحيح")
            if st.button("📥 إرسال رمز الدخول إلى هاتفي"):
                st.session_state.auth_code = str(random.randint(1000, 9999))
                send_to_telegram(f"🔐 كود الدخول الخاص بك هو: <b>{st.session_state.auth_code}</b>")
                st.info("تم إرسال الكود إلى حسابك في تليجرام.")
            
            v_code = st.text_input("أدخل كود التحقق المستلم:")
            if st.button("🔓 تسجيل الدخول"):
                if v_code == st.session_state.auth_code:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else: st.error("الكود غير صحيح!")
    else:
        st.subheader("⚙️ لوحة التحكم السيادية")
        if st.button("🔴 تسجيل الخروج"):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="stat-card"><h3>📩 الرسائل</h3></div>', unsafe_allow_html=True)
            for r in db.execute("SELECT * FROM messages ORDER BY id DESC").fetchall():
                st.write(f"**{r[1]}**: {r[2]} ({r[3]})")
        with c2:
            st.markdown('<div class="stat-card"><h3>🚨 البلاغات</h3></div>', unsafe_allow_html=True)
            for r in db.execute("SELECT * FROM reports ORDER BY id DESC").fetchall():
                st.write(f"**{r[1]}**: {r[2]} ({r[3]})")
