import streamlit as st
import tldextract
import sqlite3
import os
import requests
from datetime import datetime

# --- إعدادات التنبيهات ---
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

# 2. وظائف قاعدة البيانات (تحديث لضمان تسجيل الرسائل)
def init_db():
    conn = sqlite3.connect('aiman_guard.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS file_logs (file_name TEXT, status TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (name TEXT, content TEXT, date TEXT)''')
    conn.commit()
    return conn

db_conn = init_db()

# 3. التنسيق الجمالي
st.markdown("""<style>.main { direction: RTL; text-align: right; }</style>""", unsafe_allow_html=True)

st.title("🛡️ درع أيمن الذكي")

tabs = st.tabs(["🔍 فحص", "📧 اتصل بنا", "🔐 الإدارة"])

# --- اتصل بنا (تم تحسين الحفظ) ---
with tabs[1]:
    u_name = st.text_input("الاسم:")
    u_msg = st.text_area("الرسالة:")
    if st.button("إرسال"):
        if u_name and u_msg:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # حفظ في قاعدة البيانات أولاً
            db_conn.execute("INSERT INTO messages (name, content, date) VALUES (?, ?, ?)", (u_name, u_msg, current_time))
            db_conn.commit()
            
            # إرسال للتليجرام ثانياً
            send_telegram_msg(f"📩 رسالة جديدة من الموقع:\nمن: {u_name}\nالرسالة: {u_msg}")
            
            st.success("تم الإرسال والحفظ بنجاح!")

# --- لوحة الإدارة ---
with tabs[2]:
    pwd = st.text_input("كلمة المرور:", type="password")
    if pwd == "ayman7716":
        st.subheader("📩 الرسائل الواردة")
        msgs = db_conn.execute("SELECT * FROM messages ORDER BY date DESC").fetchall()
        if msgs:
            for m in msgs:
                st.info(f"**من:** {m[0]} | **التاريخ:** {m[2]}\n\n**الرسالة:** {m[1]}")
        else:
            st.write("لا توجد رسائل بعد.")
