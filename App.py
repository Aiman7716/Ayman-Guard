import streamlit as st
import tldextract
import sqlite3
import os
import requests
from datetime import datetime

# --- إعدادات التنبيهات (تليجرام أيمن) ---
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

# 3. التنسيق الجمالي (RTL)
st.markdown("""<style>.main { direction: RTL; text-align: right; } .stTabs [data-baseweb="tab-list"] {direction: RTL; gap: 10px;}</style>""", unsafe_allow_html=True)

st.title("🛡️ درع أيمن الذكي")

# 4. التبويبات (تمت إضافة جميع الأقسام المطلوبة)
tabs = st.tabs(["🔍 فحص الروابط", "📁 فحص الملفات", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# --- 1. فحص الروابط ---
with tabs[0]:
    st.subheader("🔗 فحص سلامة الروابط")
    url_input = st.text_input("أدخل الرابط المراد فصحه:")
    if st.button("بدء تحليل الرابط"):
        if url_input:
            ext = tldextract.extract(url_input)
            st.success(f"✅ تم تحليل الرابط. النطاق الأساسي: {ext.domain}.{ext.suffix}")
        else: st.warning("يرجى إدخال رابط.")

# --- 2. فحص الملفات (موجود الآن) ---
with tabs[1]:
    st.subheader("📁 كاشف الملفات المشبوهة")
    uploaded_file = st.file_uploader("ارفع الملف للفحص الأمني:", type=None)
    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        dangerous = ['.exe', '.bat', '.py', '.js', '.msi', '.scr']
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if file_ext in dangerous:
            status = "⚠️ خطر (ملف تنفيذي)"
            st.error(f"تحذير! هذا النوع من الملفات ({file_ext}) قد يضر بجهازك.")
            send_telegram_msg(f"🚨 تنبيه أمني:\nشخص حاول رفع ملف خطير: {uploaded_file.name}\nالوقت: {current_time}")
        else:
            status = "✅ آمن"
            st.success(f"الملف {uploaded_file.name} يبدو آمناً للاستخدام.")
        
        db_conn.execute("INSERT INTO file_logs (file_name, status, date) VALUES (?, ?, ?)", (uploaded_file.name, status, current_time))
        db_conn.commit()

# --- 3. حماية المجتمع (موجود الآن) ---
with tabs[2]:
    st.subheader("👥 قسم البلاغات المجتمعية")
    st.info("ساهم في حماية الآخرين عبر الإبلاغ عن الروابط الاحتيالية المنتشرة.")
    report_input = st.text_area("أدخل الرابط أو المحتوى الاحتيالي هنا:")
    if st.button("إرسال بلاغ"):
        if report_input:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            db_conn.execute("INSERT INTO community_reports (report, date) VALUES (?, ?)", (report_input, current_time))
            db_conn.commit()
            send_telegram_msg(f"📢 بلاغ مجتمعي جديد:\nالمحتوى: {report_input}")
            st.success("شكراً لمساهمتك! تم استلام بلاغك وسوف نتحقق منه.")

# --- 4. اتصل بنا ---
with tabs[3]:
    st.subheader("📧 تواصل مباشر")
    u_name = st.text_input("الاسم:")
    u_msg = st.text_area("الرسالة:")
    if st.button("إرسال الرسالة"):
        if u_name and u_msg:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            db_conn.execute("INSERT INTO messages (name, content, date) VALUES (?, ?, ?)", (u_name, u_msg, current_time))
            db_conn.commit()
            send_telegram_msg(f"📩 رسالة جديدة من: {u_name}\nالرسالة: {u_msg}")
            st.success("تم الإرسال بنجاح.")

# --- 5. الإدارة ---
with tabs[4]:
    pwd = st.text_input("كلمة المرور:", type="password")
    if pwd == "ayman7716":
        st.write("### 📊 إحصائيات النظام")
        if st.button("🗑️ مسح جميع السجلات"):
            db_conn.execute("DELETE FROM file_logs"); db_conn.execute("DELETE FROM messages"); db_conn.execute("DELETE FROM community_reports")
            db_conn.commit(); st.rerun()
            
        st.write("---")
        st.write("### 📩 آخر الرسائل")
        msgs = db_conn.execute("SELECT * FROM messages ORDER BY date DESC").fetchall()
        for m in msgs: st.info(f"**{m[0]}:** {m[1]} ({m[2]})")
