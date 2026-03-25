import streamlit as st
import tldextract
import sqlite3
import time
import os
from datetime import datetime

# --- 1. إعدادات المظهر ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
        .main { background-color: #0e1117; }
        .stButton>button { width: 100%; border-radius: 20px; background: #00d4ff; color: black; font-weight: bold; }
        .report-card { background: rgba(255, 75, 75, 0.1); border: 1px dashed #ff4b4b; border-radius: 12px; padding: 10px; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك قاعدة البيانات (حل مشكلة الـ OperationalError) ---
# سنستخدم مساراً محلياً مؤقتاً تضمن المنصة الكتابة فيه
DB_PATH = os.path.join(os.getcwd(), 'ayman_final_shield.db')

def get_db_connection():
    # إضافة timeout لحل مشاكل القفل
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
    return conn

def init_db():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS reports (url TEXT, date TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS stats (count INTEGER)')
        # التأكد من وجود سجل واحد فقط للإحصائيات
        c.execute('SELECT count FROM stats WHERE rowid = 1')
        if not c.fetchone():
            c.execute('INSERT INTO stats (rowid, count) VALUES (1, 250)')
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"عذراً، حدث خطأ في النظام: {e}")

init_db()

# --- 3. لوحة التحكم ---
with st.sidebar:
    st.markdown("### 🔐 إدارة النظام")
    admin_key = st.text_input("كلمة المرور:", type="password")
    if admin_key == "ayman123":
        if st.button("🗑️ مسح البلاغات"):
            conn = get_db_connection()
            conn.execute("DELETE FROM reports")
            conn.commit()
            conn.close()
            st.rerun()

# --- 4. الواجهة الرئيسية ---
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🛡️ درع أيمن الذكي</h1>", unsafe_allow_html=True)

url_input = st.text_input("🔍 الصق الرابط هنا للفحص:", placeholder="https://example.com")

if st.button("🚀 اطلق الدرع"):
    if url_input:
        with get_db_connection() as conn:
            conn.execute("UPDATE stats SET count = count + 1 WHERE rowid = 1")
            conn.commit()
        
        with st.spinner('جاري التحليل...'):
            time.sleep(1)
            extract = tldextract.extract(url_input.lower())
            domain_name = f"{extract.domain}.{extract.suffix}"
            
            official = ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa', 'moe.gov.sa']
            if domain_name in official:
                st.balloons()
                st.success(f"✅ آمن: موقع رسمي موثق ({domain_name})")
            elif extract.suffix in ['tk', 'xyz', 'ml', 'cf', 'gq']:
                st.error("🚨 خطر! نطاق مشبوه.")
            else:
                st.info(f"ℹ️ نتيجة الفحص: النطاق هو ({domain_name})")
    else:
        st.warning("⚠️ أدخل الرابط أولاً.")

# سجل البلاغات
st.markdown("---")
with st.expander("🚩 أبلغ عن رابط مشبوه"):
    scam_url = st.text_input("الرابط:")
    if st.button("إرسال"):
        if scam_url and "." in scam_url:
            with get_db_connection() as conn:
                conn.execute("INSERT INTO reports VALUES (?, ?)", (scam_url, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
            st.success("تم تسجيل البلاغ!")

# عرض البلاغات
with get_db_connection() as conn:
    reps = conn.execute("SELECT url FROM reports ORDER BY rowid DESC LIMIT 3").fetchall()
for r in reps:
    st.markdown(f"<div class='report-card'>⚠️ مشبوه: <code>{r[0]}</code></div>", unsafe_allow_html=True)

# التذييل
st.markdown("---")
with get_db_connection() as conn:
    stat_res = conn.execute("SELECT count FROM stats WHERE rowid = 1").fetchone()
total_ops = stat_res[0] if stat_res else 250
st.markdown(f"<p style='text-align: center;'>📊 الفحوصات: {total_ops} | تطوير: <b>أيمن 🦾</b></p>", unsafe_allow_html=True)
