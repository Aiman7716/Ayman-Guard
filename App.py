import streamlit as st
import tldextract
import sqlite3
import os
import requests
from datetime import datetime

# --- إعدادات التنبيهات الفورية (تليجرام أيمن) ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, json=payload, timeout=5)
    except:
        pass

# 1. إعدادات الصفحة
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# 2. وظائف قاعدة البيانات
def init_db():
    conn = sqlite3.connect('aiman_guard.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS file_logs (file_name TEXT, status TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS community_reports (report TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (name TEXT, content TEXT, date TEXT)''')
    conn.commit()
    return conn

db_conn = init_db()

# 3. صقل الألوان والتنسيق الجمالي (Cyber Security Style)
st.markdown("""
    <style>
    /* تنسيق الواجهة العامة */
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    
    /* العنوان المتوهج */
    .main-title {
        text-align: center;
        background: linear-gradient(90deg, #00d4ff, #0055ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 15px rgba(0, 212, 255, 0.4);
        margin-bottom: 20px;
    }

    /* تنسيق التبويبات المطور */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #1a1c23;
        padding: 10px;
        border-radius: 15px;
        direction: RTL;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
        font-weight: bold;
        border-radius: 10px;
    }

    /* أزرار نيون */
    .stButton>button {
        background: linear-gradient(45deg, #00d4ff, #0055ff);
        color: white;
        border: none;
        border-radius: 12px;
        height: 3em;
        font-weight: bold;
        transition: 0.3s all ease;
        box-shadow: 0 4px 15px rgba(0, 85, 255, 0.3);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.6);
        color: #fff;
    }

    /* صناديق المعلومات */
    .stAlert, .stInfo, .stSuccess {
        background-color: #1a1c23 !important;
        border-right: 5px solid #00d4ff !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    /* توجيه النصوص للعربية */
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
    input, textarea { background-color: #161b22 !important; color: white !important; direction: RTL !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. عرض الشعار
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    st.image("1774474792146.png", use_container_width=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# 5. التبويبات الخمسة الكاملة
tabs = st.tabs(["🔍 فحص الروابط", "📁 فحص الملفات", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# --- 1. فحص الروابط ---
with tabs[0]:
    st.subheader("🔗 فحص الروابط المشبوهة")
    url_input = st.text_input("أدخل الرابط للفحص:")
    if st.button("تحليل الرابط المستهدف"):
        if url_input:
            ext = tldextract.extract(url_input)
            st.success(f"✅ تم التحليل بنجاح. النطاق المستخرج: {ext.domain}.{ext.suffix}")
        else: st.warning("يرجى إدخال رابط.")

# --- 2. فحص الملفات ---
with tabs[1]:
    st.subheader("📁 فحص الملفات المرفوعة")
    uploaded_file = st.file_uploader("ارفع الملف هنا لفحص نوعه وحمايتك:", type=None)
    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        dangerous = ['.exe', '.bat', '.py', '.js', '.msi', '.scr', '.vbs']
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if file_ext in dangerous:
            status = "⚠️ خطر (ملف تنفيذي)"
            st.error(f"تحذير! الملف {uploaded_file.name} يحمل امتداداً خطيراً.")
            send_telegram_msg(f"🚨 تحذير أمني:\nشخص حاول رفع ملف خطير: {uploaded_file.name}\nالوقت: {now}")
        else:
            status = "✅ آمن"
            st.success(f"الملف {uploaded_file.name} يبدو آمناً.")
        
        db_conn.execute("INSERT INTO file_logs (file_name, status, date) VALUES (?, ?, ?)", (uploaded_file.name, status, now))
        db_conn.commit()

# --- 3. حماية المجتمع ---
with tabs[2]:
    st.subheader("👥 بلاغات المجتمع الاحتيالية")
    st.write("ضع الروابط التي وصلت عبر الواتساب أو الرسائل هنا لتحذير الآخرين.")
    report_input = st.text_area("وصف البلاغ أو الرابط المشبوه:")
    if st.button("نشر البلاغ"):
        if report_input:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            db_conn.execute("INSERT INTO community_reports (report, date) VALUES (?, ?)", (report_input, now))
            db_conn.commit()
            send_telegram_msg(f"📢 بلاغ مجتمعي جديد:\n{report_input}")
            st.success("تم استلام بلاغك والمساهمة في حماية المجتمع.")

# --- 4. اتصل بنا ---
with tabs[3]:
    st.subheader("📧 تواصل مباشر مع الإدارة")
    u_name = st.text_input("اسمك:")
    u_msg = st.text_area("رسالتك:")
    if st.button("إرسال الرسالة الآن"):
        if u_name and u_msg:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            db_conn.execute("INSERT INTO messages (name, content, date) VALUES (?, ?, ?)", (u_name, u_msg, now))
            db_conn.commit()
            send_telegram_msg(f"📩 رسالة جديدة لـ أيمن:\nمن: {u_name}\nالرسالة: {u_msg}")
            st.success("شكراً لتواصلك، تم الإرسال.")

# --- 5. الإدارة ---
with tabs[4]:
    st.subheader("🔐 لوحة تحكم المهندس أيمن")
    pwd = st.text_input("كلمة المرور الإدارية:", type="password")
    if pwd == "ayman7716":
        st.success("مرحباً بك يا مهندس أيمن")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🗑️ تصفير كافة السجلات"):
                db_conn.execute("DELETE FROM file_logs")
                db_conn.commit()
                st.rerun()

        st.write("---")
        st.write("### 📩 أحدث الرسائل")
        msgs = db_conn.execute("SELECT * FROM messages ORDER BY date DESC LIMIT 5").fetchall()
        for m in msgs: st.info(f"**{m[0]}:** {m[1]} ({m[2]})")
        
        st.write("### 📁 سجلات الفحص")
        logs = db_conn.execute("SELECT * FROM file_logs ORDER BY date DESC LIMIT 5").fetchall()
        for l in logs: st.text(f"📄 {l[0]} - {l[1]} ({l[2]})")
