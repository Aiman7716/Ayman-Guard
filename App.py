import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random
from datetime import datetime

# --- 1. الإعدادات والربط ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

def send_telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except: pass

# --- 2. التصميم البصري (نفس تصميم الصورة 1000566739.jpg) ---
st.set_page_config(page_title="Ayman Guard", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    /* الهيدر الأزرق الاحترافي */
    .hero-box {
        background: linear-gradient(135deg, #448aff 0%, #2962ff 100%);
        padding: 40px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }
    .hero-box h1 { color: white; font-size: 2.5rem; margin-bottom: 5px; }
    .hero-box p { color: #e3f2fd; font-size: 1.1rem; }

    /* تحسين شكل التبويبات العلوية */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161b22;
        padding: 10px;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent !important;
        border-radius: 8px !important;
        color: #8b949e !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f6feb !important;
        color: white !important;
    }

    /* بطاقات المحتوى */
    .content-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
    }

    /* إخفاء القائمة الجانبية والزوائد */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. الهيكل الرئيسي ---
st.markdown("""
    <div class="hero-box">
        <h1>درع أيمن الأمني</h1>
        <p>النسخة الاحترافية v32.0</p>
    </div>
    """, unsafe_allow_html=True)

# نظام التبويبات المصلح
tab1, tab2, tab3, tab4 = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "👥 المجتمع", "🔐 الإدارة"])

# محتوى التبويب الأول: الرئيسية
with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 إحصائيات النظام")
    r_count = c.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    m_count = c.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    
    col1, col2 = st.columns(2)
    col1.metric("إجمالي البلاغات", r_count)
    col2.metric("رسائل التواصل", m_count)
    st.markdown('</div>', unsafe_allow_html=True)

# محتوى التبويب الثاني: الفحص
with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔍 مركز التحليل الذكي")
    url = st.text_input("أدخل الرابط للفحص:")
    if st.button("بدء التحليل"):
        if url:
            ext = tldextract.extract(url)
            st.success(f"تم تحليل النطاق: {ext.domain}.{ext.suffix}")
        else: st.error("يرجى إدخال الرابط")
    st.markdown('</div>', unsafe_allow_html=True)

# محتوى التبويب الثالث: المجتمع
with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📢 إبلاغ عن حالة احتيال")
    report = st.text_area("وصف الحالة:")
    if st.button("إرسال البلاغ"):
        if report:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (report, dt))
            conn.commit()
            send_telegram(f"📢 بلاغ جديد: {report}")
            st.success("تم الإرسال بنجاح")
    st.markdown('</div>', unsafe_allow_html=True)

# محتوى التبويب الرابع: الإدارة
with tab4:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔐 لوحة التحكم")
    pw = st.text_input("كلمة المرور:", type="password")
    if pw == "ayman7716":
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        st.dataframe(df, use_container_width=True)
        if st.button("حذف السجل"):
            c.execute("DELETE FROM reports")
            conn.commit()
            st.warning("تم مسح البيانات")
    st.markdown('</div>', unsafe_allow_html=True)
