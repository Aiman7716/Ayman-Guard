import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random
from datetime import datetime

# --- 1. التكوين الأساسي ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

# --- 2. التصميم الجمالي الموزون (Clean & Balanced) ---
st.set_page_config(page_title="Ayman Shield", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: RTL; }
    .stApp { background-color: #0d1117; }
    
    /* حاوية البطاقات لضمان عدم التداخل */
    .report-card {
        background: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
        margin-bottom: 15px;
        text-align: right;
    }
    .header-style {
        text-align: center;
        color: #58a6ff;
        padding: 10px;
        border-bottom: 1px solid #30363d;
    }
    /* تحسين الأزرار لتناسب الجوال */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #1f6feb !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_fixed.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, category TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🛡️ القائمة</h2>", unsafe_allow_html=True)
    menu = st.radio("", ["📊 الإحصائيات", "🔍 الفحص", "👥 المجتمع", "📧 التواصل", "🔐 الإدارة"])

st.markdown('<h1 class="header-style">درع أيمن الأمني</h1>', unsafe_allow_html=True)

# --- 5. منطق العمليات ---

if menu == "📊 الإحصائيات":
    r_total = c.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    m_total = c.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    
    col1, col2 = st.columns(2)
    col1.metric("إجمالي البلاغات", r_total)
    col2.metric("إجمالي الرسائل", m_total)

elif menu == "🔍 الفحص":
    st.subheader("🔍 فحص الروابط والملفات")
    link = st.text_input("أدخل الرابط للفحص:")
    if st.button("تحليل الآن"):
        if link:
            ext = tldextract.extract(link)
            st.success(f"تم تحليل النطاق: {ext.domain}.{ext.suffix}")
        else: st.error("يرجى إدخال رابط")

elif menu == "👥 المجتمع":
    st.subheader("📢 أضف بلاغاً جديداً")
    content = st.text_area("وصف حالة الاحتيال:")
    if st.button("إرسال البلاغ"):
        if content:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?, ?)", (content, "عام", dt))
            conn.commit()
            st.success("تم الحفظ بنجاح!")
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                          json={"chat_id": CHAT_ID, "text": f"📢 بلاغ جديد: {content}"})

elif menu == "🔐 الإدارة":
    st.subheader("🔐 لوحة التحكم")
    pwd = st.text_input("كلمة المرور:", type="password")
    if pwd == "ayman7716":
        # عرض البلاغات داخل الحاويات (Cards) لضمان عدم قص النص
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        for i, row in df.iterrows():
            st.markdown(f"""
            <div class="report-card">
                <small style="color: #8b949e;">{row['dt']}</small><br>
                <b>{row['content']}</b>
            </div>
            """, unsafe_allow_html=True)
