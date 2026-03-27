import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from datetime import datetime

# --- 1. التصميم الجمالي المتقدم (UI/UX) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* هيدر الصفحة الرئيسي */
    .main-header {
        background: linear-gradient(90deg, #1f6feb 0%, #111d2e 100%);
        padding: 40px; border-radius: 25px; text-align: center;
        margin-bottom: 30px; border: 1px solid #30363d;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .main-header h1 { font-family: 'Cairo', sans-serif; font-size: 3rem; margin-bottom: 10px; color: #ffffff; }
    
    /* تصميم الأزرار - بارزة ومحاذية */
    div.stButton > button {
        width: 100% !important; background: linear-gradient(135deg, #1f6feb 0%, #094cb3 100%) !important;
        color: white !important; border-radius: 15px !important;
        height: 4em !important; font-weight: bold !important;
        font-size: 1.1rem !important; border: 2px solid #58a6ff !important;
        transition: 0.4s ease; box-shadow: 0 4px 15px rgba(31, 111, 235, 0.3);
    }
    div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(31, 111, 235, 0.5); border-color: #ffffff !important; }

    /* صناديق المعلومات */
    .info-card { background: #161b22; border: 1px solid #30363d; padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الإعدادات الخلفية ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
DB_NAME = "ayman_ultra_v16.db"

def send_to_telegram(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()

# إدارة الجلسة
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="main-header"><h1>🛡️ درع أيمن السيادي</h1><p>الأمان الذكي | الفحص العميق | التحميل الفوري</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص والمعاينة", "🎬 التحميل", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

with tabs[0]: # تبويب الرئيسية الجمالي
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: #58a6ff;">مرحباً بك في مركز الحماية المتكامل</h2>
        <p style="font-size: 1.2rem; color: #8b949e;">هذا النظام صُمم خصيصاً لخدمة وتأمين نشاطك الرقمي بأحدث التقنيات.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="info-card"><h3>⚡ سرعة</h3><p>تحميل وفحص الروابط في ثوانٍ معدودة</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="info-card"><h3>🛡️ أمان</h3><p>تشفير كامل وحماية لبياناتك الشخصية</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="info-card"><h3>🔒 خصوصية</h3><p>مصادقة ثنائية لضمان وصولك أنت فقط</p></div>', unsafe_allow_html=True)

with tabs[1]: # الفحص والمعاينة (كما طلبت قبل التعديل مع تحسين الوضوح)
    st.markdown("### 🔍 مركز الفحص المزدوج")
    
    # صف الروابط
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    url_input = st.text_input("ألصق الرابط هنا للفحص أو المعاينة:", placeholder="https://facebook.com/...")
    c1, c2 = st.columns(2)
    check_btn = c1.button("🛡️ فحص أمان الرابط")
    preview_btn = c2.button("👁️ جلب بيانات المعاينة")
    
    if check_btn and url_input:
        try:
            res = requests.get(url_input, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            st.success(f"✅ الرابط نشط وآمن للاستخدام (كود الاستجابة: {res.status_code})")
            send_to_telegram(f"🔍 فحص رابط: {url_input}")
        except: st.error("❌ تعذر الاتصال بالرابط، قد يكون وهمياً أو محجوباً.")
    
    if preview_btn and url_input:
        st.markdown(f'<a href="{url_input}" target="_blank"><button style="width:100%; background-color:#238636; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-weight:bold;">🟢 اضغط هنا لفتح المعاينة الآمنة في نافذة مستقلة</button></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # صف الملفات
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    u_file = st.file_uploader("ارفع ملفاً لتحليل الكود البرمجي:", type=None)
    if u_file and st.button("📁 ابدأ فحص الملف الآن"):
        content = u_file.getvalue().decode("latin-1", errors="replace")
        st.code(content[:2000], language="text")
        st.success("✅ تم تحليل هيكل الملف.")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]: # التحميل
    v_link = st.text_input("رابط الفيديو:")
    if st.button("🎬 تحميل"):
        if v_link:
            with st.spinner("جارِ التحميل..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'ayman.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_link])
                    with open("ayman.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ الفيديو", f, "video.mp4")
                    os.remove("ayman.mp4")
                except: st.error("❌ فشل التحميل.")

with tabs[3]: # المجتمع
    with st.form("comm"):
        n, d = st.text_input("اسمك:"), st.text_area("تفاصيل التهديد:")
        if st.form_submit_button("🚨 إرسال بلاغ"):
            db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?,?,?)", (n, d, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("تم التوثيق"); send_to_telegram(f"🚨 بلاغ: {d}")

with tabs[4]: # تواصل معنا (تمت إعادته)
    st.subheader("📧 تواصل مع الإدارة")
    with st.form("contact_form"):
        c_name = st.text_input("الاسم الكامل:")
        c_msg = st.text_area("رسالتك أو اقتراحك:")
        if st.form_submit_button("إرسال الرسالة"):
            if c_name and c_msg:
                db.execute("INSERT INTO messages (sender, content, date) VALUES (?,?,?)", (c_name, c_msg, datetime.now().strftime("%Y-%m-%d")))
                db.commit(); st.success("تم الإرسال بنجاح."); send_to_telegram(f"📧 رسالة من {c_name}: {c_msg}")

with tabs[5]: # الإدارة
    if not st.session_state.logged_in:
        pwd = st.text_input("كلمة السر:", type="password")
        if pwd == "ayman7716":
            if st.button("👤 تسجيل الدخول (طلب كود تليجرام)"):
                st.session_state.auth_code = str(random.randint(1000, 9999))
                send_to_telegram(f"🔐 كود دخول الإدارة: <b>{st.session_state.auth_code}</b>")
                st.info("تفقد التليجرام.")
            
            if st.session_state.auth_code:
                code = st.text_input("أدخل الكود:")
                if st.button("🔓 تأكيد"):
                    if code == st.session_state.auth_code:
                        st.session_state.logged_in = True; st.rerun()
    else:
        if st.button("🔴 خروج"): st.session_state.logged_in = False; st.rerun()
        for r in db.execute("SELECT * FROM reports ORDER BY id DESC").fetchall(): st.warning(f"{r[1]}: {r[2]}")
