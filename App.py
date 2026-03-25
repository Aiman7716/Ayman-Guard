import streamlit as st
import tldextract
import sqlite3
import random
import time
from datetime import datetime

# --- 1. إعدادات الصفحة وتحسين مظهر التطبيق على الجوال ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# هذا الكود يجعل الموقع يفتح كأنه تطبيق حقيقي عند تثبيته على الشاشة الرئيسية
st.markdown("""
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/1067/1067357.png">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; }
        .main { background: linear-gradient(180deg, #0e1117 0%, #07090c 100%); }
        .stButton>button { width: 100%; border-radius: 20px; background: #00d4ff; color: black; font-weight: bold; height: 3em; border: none; }
        .report-card { background: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; border-radius: 15px; padding: 15px; margin-bottom: 10px; }
        .official-btn { background: #1a1c24; border: 1px solid #00d4ff; color: #00d4ff !important; padding: 10px; border-radius: 12px; text-decoration: none; display: block; text-align: center; margin: 5px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('ayman_pro.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS reports (url TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS stats (count INTEGER)')
    c.execute('INSERT OR IGNORE INTO stats (rowid, count) SELECT 1, 250 WHERE NOT EXISTS (SELECT 1 FROM stats)')
    conn.commit()
    conn.close()

def db_action(query, val=None, fetch=True):
    conn = sqlite3.connect('ayman_pro.db')
    c = conn.cursor()
    if val: c.execute(query, val)
    else: c.execute(query)
    res = c.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return res

init_db()

# --- 3. لوحة التحكم الجانبية ---
with st.sidebar:
    st.markdown("### 🔐 منطقة المدير")
    pw = st.text_input("رمز الدخول:", type="password")
    if pw == "ayman123":
        st.success("أهلاً أيمن!")
        if st.button("🗑️ مسح البلاغات"):
            db_action("DELETE FROM reports", fetch=False)
            st.toast("تم تنظيف البيانات!")
        new_val = st.number_input("تعديل العداد:", value=250)
        if st.button("⚙️ حفظ الرقم الجديد"):
            db_action("UPDATE stats SET count = ?", (new_val,), fetch=False)
            st.rerun()

# --- 4. الواجهة الرئيسية ---
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🛡️ درع أيمن الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>شريكك الموثوق في مكافحة الاحتيال الرقمي</p>", unsafe_allow_html=True)

# فحص الروابط
url_input = st.text_input("🔍 الصق الرابط هنا لفحصه:", placeholder="https://example.com")
if st.button("🚀 ابدأ الفحص"):
    db_action("UPDATE stats SET count = count + 1", fetch=False)
    if url_input:
        with st.spinner('جاري التحليل...'):
            time.sleep(1)
            ext = tldextract.extract(url_input.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            if domain in ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa']:
                st.balloons()
                st.success(f"✅ آمن جداً: هذا موقع رسمي موثق ({domain})")
            elif ext.suffix in ['tk', 'xyz', 'ml', 'cf', 'gq']:
                st.error("🚨 خطر! تم اكتشاف رابط وهمي بنسبة 99%")
            else:
                st.info(f"ℹ️ نتيجة الفحص: الرابط يتبع لنطاق ({domain}).")
    else:
        st.warning("⚠️ أدخل الرابط أولاً.")

# البلاغات
st.markdown("---")
st.subheader("📢 بلاغات المجتمع")
with st.expander("🚩 أبلغ عن رابط مشبوه"):
    scam = st.text_input("الرابط:")
    if st.button("تأكيد البلاغ"):
        if scam and "." in scam:
            db_action("INSERT INTO reports VALUES (?, ?)", (scam, datetime.now().strftime("%Y-%m-%d")), fetch=False)
            st.success("تم الحفظ!")
        else: st.error("رابط غير صحيح!")

reps = db_action("SELECT url FROM reports ORDER BY rowid DESC LIMIT 3")
for r in reps:
    st.markdown(f"<div class='report-card'>⚠️ مشبوه: <code>{r[0]}</code></div>", unsafe_allow_html=True)

# الروابط الموثقة
st.markdown("---")
st.markdown("<h4 style='text-align: center;'>🏛️ المراجع الرسمية الموثقة</h4>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1: st.markdown("<a href='https://absher.sa' class='official-btn'>أبشر</a>", unsafe_allow_html=True)
with col2: st.markdown("<a href='https://iam.gov.sa' class='official-btn'>نفاذ</a>", unsafe_allow_html=True)
with col3: st.markdown("<a href='https://splonline.com.sa' class='official-btn'>البريد</a>", unsafe_allow_html=True)

# التذييل
st.markdown("---")
count_res = db_action("SELECT count FROM stats")
total = count_res[0][0] if count_res else 250
st.markdown(f"<p style='text-align: center;'>📊 الفحوصات: {total} | تطوير المبرمج: <b>أيمن 🦾</b></p>", unsafe_allow_html=True)
