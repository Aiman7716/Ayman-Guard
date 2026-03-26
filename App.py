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
        requests.post(url, json=payload)
    except Exception as e:
        pass

# 1. إعدادات الصفحة والشعار
st.set_page_config(page_title="درع أيمن الذكي", page_icon="1774474792146.png", layout="centered")

# 2. وظائف قاعدة البيانات
def init_db():
    conn = sqlite3.connect('aiman_guard.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS file_logs (file_name TEXT, file_type TEXT, status TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 3. التنسيق الجمالي (دعم العربية RTL)
st.markdown("""
    <style>
    .main, .stApp { direction: RTL; text-align: right; }
    .main-title { text-align: center; color: #00d4ff; font-size: 2.5rem; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { width: 100%; background-color: #00d4ff; color: white; border-radius: 10px; height: 3em; font-size: 1.2rem; }
    .report-box { padding: 15px; border-radius: 10px; background-color: #1e1e1e; border-right: 5px solid #00d4ff; margin-bottom: 10px; }
    input, textarea { direction: RTL !important; text-align: right !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. عرض الشعار
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("1774474792146.png", use_container_width=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# 5. التبويبات الرئيسية
tabs = st.tabs(["🔍 فحص الروابط", "📁 فحص الملفات", "📧 اتصل بنا", "🔐 الإدارة"])

# --- تبويب فحص الروابط ---
with tabs[0]:
    st.subheader("تحقق من سلامة الروابط")
    url_input = st.text_input("أدخل الرابط هنا:")
    if st.button("بدء فحص الرابط"):
        if url_input:
            ext = tldextract.extract(url_input)
            st.success(f"✅ تم تحليل الرابط بنجاح. النطاق: {ext.domain}.{ext.suffix}")
        else: st.warning("يرجى إدخال رابط.")

# --- تبويب فحص الملفات (مع التنبيهات) ---
with tabs[1]:
    st.subheader("كاشف الملفات المشبوهة")
    uploaded_file = st.file_uploader("ارفع الملف للفحص الأمنـي:", type=None)
    if uploaded_file:
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        dangerous_exts = ['.exe', '.bat', '.msi', '.py', '.js', '.scr']
        
        if ext in dangerous_exts:
            status = "⚠️ خطر/تنفيذي"
            st.error(f"تحذير أمني: الملف ({uploaded_file.name}) قد يكون ضاراً!")
            send_telegram_msg(f"🚨 تنبيه أمني من الدرع:\nمحاولة رفع ملف مشبوه!\nالاسم: {uploaded_file.name}\nالنوع: {ext}\nالوقت: {datetime.now().strftime('%H:%M')}")
        else:
            status = "✅ آمن"
            st.success(f"فحص أولي: الملف ({uploaded_file.name}) يبدو آمناً.")
            
        conn = sqlite3.connect('aiman_guard.db')
        conn.execute("INSERT INTO file_logs VALUES (?, ?, ?, ?)", (uploaded_file.name, ext, status, datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        conn.close()

# --- تبويب اتصل بنا ---
with tabs[2]:
    st.subheader("تواصل مع المهندس أيمن")
    u_name = st.text_input("اسمك الكريم:")
    u_msg = st.text_area("رسالتك أو بلاغك:")
    if st.button("إرسال الرسالة"):
        if u_name and u_msg:
            send_telegram_msg(f"📩 رسالة جديدة من الموقع:\nمن: {u_name}\nالرسالة: {u_msg}")
            st.success(f"شكراً يا {u_name}، تم إرسال رسالتك بنجاح.")

# --- تبويب الإدارة ---
with tabs[3]:
    st.subheader("لوحة التحكم الخاصة")
    pwd = st.text_input("كلمة مرور الإدارة:", type="password")
    if pwd == "ayman7716":
        st.success("مرحباً بك يا مهندس أيمن")
        conn = sqlite3.connect('aiman_guard.db')
        st.write("### 📂 سجل فحص الملفات الأخير")
        logs = conn.execute("SELECT * FROM file_logs ORDER BY date DESC LIMIT 10").fetchall()
        for l in logs:
            st.markdown(f'<div class="report-box">ملف: {l[0]} | الحالة: {l[2]} | التاريخ: {l[3]}</div>', unsafe_allow_html=True)
        conn.close()
