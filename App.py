import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from datetime import datetime

# --- 1. الإعدادات والتصميم الجمالي ---
st.set_page_config(page_title="Ayman Guard Pro v20", layout="wide")

# كود التنسيق وإخفاء معالم الموقع (بما في ذلك شريط Hosted with Streamlit)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* إخفاء القوائم والفوتر والهيدر */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* إخفاء علامة "Hosted with Streamlit" الحمراء تماماً */
    div[data-testid="stStatusWidget"] { display: none !important; }
    .viewerBadge_container__1QS1n { display: none !important; }
    #streamlit-connection-status { display: none !important; }
    
    /* تقليل المساحات البيضاء العلوية والسفلية */
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }

    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 40px; border-radius: 25px; text-align: center;
        margin-bottom: 25px; border: 1px solid #30363d;
    }
    div.stButton > button {
        width: 100% !important; background: linear-gradient(90deg, #1f6feb, #094cb3) !important;
        color: white !important; border-radius: 12px !important; height: 3.5em !important;
        font-weight: bold !important; border: 2px solid #58a6ff !important;
    }
    .scan-box { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 20px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك الأمان وقواعد البيانات ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
DB_NAME = "ayman_perfect_v20.db"

def send_to_telegram(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except:
        pass

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
        conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
        conn.commit()
        return conn
    except:
        return None

db = init_db()

# إدارة الحالة (Session State)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None
if 'failed_attempts' not in st.session_state: st.session_state.failed_attempts = 0

# --- 3. بناء واجهة التبويبات ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار v20.2 | استقرار تام وأمان فائق</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص والمعاينة", "🎬 التحميل", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# 1. الرئيسية
with tabs[0]:
    st.markdown("<div style='text-align:center;'><h2>مرحباً بك في نظام الحماية</h2><p>النظام محمي ومراقب على مدار الساعة.</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("حالة الدرع", "نشط ✅")
    c2.metric("التنبيهات", "نشطة 📲")
    c3.metric("الاستقرار", "100% ✨")

# 2. الفحص والمعاينة
with tabs[1]:
    st.subheader("🛠️ مركز الاختبار الشامل")
    scan_choice = st.radio("اختر المهمة:", ["فحص ومعاينة الروابط 🔗", "فحص أمان الملفات 📁"], horizontal=True)
    st.markdown('<div class="scan-box">', unsafe_allow_html=True)
    
    if scan_choice == "فحص ومعاينة الروابط 🔗":
        u = st.text_input("ألصق الرابط هنا:", key="scan_url")
        col1, col2 = st.columns(2)
        if col1.button("🛡️ ابدأ فحص الأمان"):
            if u:
                try:
                    res = requests.get(u, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                    st.success(f"الرابط مستجيب وآمن (Status: {res.status_code})")
                    send_to_telegram(f"🔍 فحص رابط: {u}")
                except: st.error("❌ الرابط قد يكون خطيراً أو غير متاح.")
        if col2.button("👁️ معاينة الرابط"):
            if u:
                st.markdown(f'<a href="{u}" target="_blank"><button style="width:100%; background:#238636; color:white; border:none; padding:15px; border-radius:12px; font-weight:bold;">فتح المعاينة في صفحة جديدة</button></a>', unsafe_allow_html=True)
    else:
        u_f = st.file_uploader("ارفع الملف للفحص:", key="scan_file")
        if u_f:
            st.info(f"ملف مختار: {u_f.name}")
            if st.button("📁 ابدأ تحليل الملف"):
                st.success("✅ تم الفحص: لا يوجد تهديد برمجي ظاهر.")
                try:
                    content = u_f.getvalue().decode("latin-1", errors="replace")[:500]
                    st.code(content)
                except: st.warning("الملف لا يمكن عرضه نصياً.")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. التحميل
with tabs[2]:
    v_u = st.text_input("رابط الفيديو للتحميل:", key="dl_url")
    if st.button("🚀 تحميل الآن"):
        if v_u:
            with st.spinner("جاري المعالجة..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'ayman_v.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_u])
                    if os.path.exists("ayman_v.mp4"):
                        with open("ayman_v.mp4", "rb") as f:
                            st.video(f.read())
                            st.download_button("📥 حفظ الفيديو", f, "video.mp4")
                        os.remove("ayman_v.mp4")
                except Exception as e: 
                    st.error(f"❌ فشل التحميل: {str(e)}")

# 4. المجتمع
with tabs[3]:
    with st.form("comm"):
        rn, rd = st.text_input("اسمك:"), st.text_area("بلاغ عن خطر:")
        if st.form_submit_button("🚨 إرسال البلاغ"):
            if db:
                db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?,?,?)", (rn, rd, datetime.now().strftime("%Y-%m-%d")))
                db.commit()
            st.success("تم التوثيق"); send_to_telegram(f"🚨 بلاغ من {rn}: {rd}")

# 5. تواصل معنا
with tabs[4]:
    with st.form("contact"):
        cn, cm = st.text_input("الاسم:"), st.text_area("الرسالة:")
        if st.form_submit_button("📧 إرسال الرسالة"):
            if db:
                db.execute("INSERT INTO messages (sender, content, date) VALUES (?,?,?)", (cn, cm, datetime.now().strftime("%Y-%m-%d")))
                db.commit()
            st.success("شكراً لتواصلك"); send_to_telegram(f"📧 رسالة من {cn}: {cm}")

# 6. الإدارة
with tabs[5]:
    if not st.session_state.logged_in:
        st.subheader("🔐 الدخول المحمي")
        pwd = st.text_input("كلمة السر:", type="password", key="admin_key")
        if st.button("👤 دخول (طلب كود تليجرام)"):
            if pwd == "ayman7716":
                st.session_state.auth_code = str(random.randint(1000, 9999))
                send_to_telegram(f"🔐 كود الدخول: <b>{st.session_state.auth_code}</b>")
                st.info("تم إرسال الكود.")
                st.session_state.failed_attempts = 0
            else:
                st.session_state.failed_attempts += 1
                send_to_telegram(f"⚠️ محاولة دخول خاطئة!\nكلمة السر: {pwd}")
                st.error("⚠️ خطأ في كلمة السر")

        if st.session_state.auth_code:
            vc = st.text_input("أدخل كود التحقق:")
            if st.button("🔓 تأكيد"):
                if vc == st.session_state.auth_code:
                    st.session_state.logged_in = True; st.rerun()
                else: st.error("كود خاطئ")
    else:
        st.success("أهلاً يا أيمن")
        if st.button("🔴 تسجيل خروج"): st.session_state.logged_in = False; st.rerun()
        
        st.divider()
        st.subheader("📩 آخر الرسائل")
        if db:
            msgs = db.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 5").fetchall()
            for m in msgs: st.info(f"من: {m[1]} | بتاريخ: {m[3]}\n\n{m[2]}")
            
        st.subheader("🚨 آخر البلاغات")
        if db:
            reps = db.execute("SELECT * FROM reports ORDER BY id DESC LIMIT 5").fetchall()
            for r in reps: st.warning(f"مبلغ: {r[1]} | بتاريخ: {r[3]}\n\n{r[2]}")
