import streamlit as st
import tldextract
import sqlite3
import os
import requests
import hashlib
from datetime import datetime

# --- إعدادات الحماية والتنبيهات الفورية ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
# رمز VirusTotal الخاص بك الذي أرسلته
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, json=payload, timeout=5)
    except: pass

def check_virustotal(file_content):
    file_hash = hashlib.sha256(file_content).hexdigest()
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": VT_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['data']['attributes']['last_analysis_stats']
    except: return None
    return None

# --- التصميم السيبراني الفاخر ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .main-title {
        text-align: center;
        background: linear-gradient(90deg, #00d4ff, #0055ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem; font-weight: bold;
        text-shadow: 2px 2px 15px rgba(0, 212, 255, 0.4);
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #1a1c23; padding: 10px; border-radius: 15px; direction: RTL; }
    .stButton>button { background: linear-gradient(45deg, #00d4ff, #0055ff); color: white; border-radius: 12px; font-weight: bold; width: 100%; height: 3.5em; border: none; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5); }
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
    input, textarea { background-color: #161b22 !important; color: white !important; direction: RTL !important; text-align: right !important; }
    </style>
    """, unsafe_allow_html=True)

# عرض الشعار
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    st.image("1774474792146.png", use_container_width=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي</div>', unsafe_allow_html=True)

# قاعدة البيانات
def init_db():
    conn = sqlite3.connect('aiman_guard.db', check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS logs (name TEXT, status TEXT, date TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, date TEXT)''')
    conn.commit()
    return conn
db = init_db()

tabs = st.tabs(["🔍 فحص ذكي (AI)", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# --- التبويب الأول: فحص الفيروسات العالمي ---
with tabs[0]:
    st.subheader("📁 فحص الملفات عبر قاعدة بيانات عالمية")
    up_file = st.file_uploader("ارفع الملف ليتم فحصه عبر 70 محرك حماية:", type=None)
    if up_file:
        with st.spinner('جاري التحليل السيبراني...'):
            content = up_file.read()
            res = check_virustotal(content)
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            if res:
                malicious = res.get('malicious', 0)
                if malicious > 0:
                    st.error(f"🚨 تحذير: تم اكتشاف {malicious} تهديد في هذا الملف!")
                    send_telegram_msg(f"🚨 إنذار خطير يا أيمن!\nتم كشف ملف ضار: {up_file.name}\nعدد التهديدات: {malicious}")
                    status = f"🚩 خطر ({malicious})"
                else:
                    st.success("✅ فحص نظيف: الملف آمن وموثوق عالمياً.")
                    status = "✅ آمن"
            else:
                st.info("هذا الملف جديد، سيتم فحصه بناءً على النوع...")
                ext = os.path.splitext(up_file.name)[1].lower()
                status = "⚠️ فحص يدوي" if ext in ['.exe', '.bat', '.py'] else "✅ آمن"
            db.execute("INSERT INTO logs VALUES (?, ?, ?)", (up_file.name, status, now))
            db.commit()

# --- حماية المجتمع ---
with tabs[1]:
    st.subheader("👥 ساهم في بلاغات الاحتيال")
    report = st.text_area("أدخل الرابط أو الرسالة المشبوهة:")
    if st.button("إرسال بلاغ"):
        if report:
            send_telegram_msg(f"📢 بلاغ مجتمعي جديد:\n{report}")
            st.success("تم استلام بلاغك، شكراً لمساهمتك.")

# --- اتصل بنا ---
with tabs[2]:
    st.subheader("📧 تواصل مع الإدارة")
    u_name = st.text_input("اسمك:")
    u_msg = st.text_area("رسالتك:")
    if st.button("إرسال الآن"):
        if u_name and u_msg:
            db.execute("INSERT INTO messages VALUES (?, ?, ?)", (u_name, u_msg, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            send_telegram_msg(f"📩 رسالة جديدة من: {u_name}\nالرسالة: {u_msg}")
            st.success("تم الإرسال بنجاح!")

# --- الإدارة ---
with tabs[3]:
    st.subheader("🔐 لوحة التحكم الإدارية")
    pwd = st.text_input("كلمة المرور:", type="password")
    if pwd == "ayman7716":
        st.success("مرحباً بك يا مهندس أيمن")
        st.write("### 📩 آخر الرسائل")
        for m in db.execute("SELECT * FROM messages ORDER BY date DESC LIMIT 5").fetchall():
            st.info(f"**{m[0]}:** {m[1]} ({m[2]})")
