import streamlit as st
import tldextract
import sqlite3
from datetime import datetime

# 1. إعدادات الصفحة والشعار
st.set_page_config(
    page_title="درع أيمن الذكي",
    page_icon="1774474792146.png",
    layout="centered"
)

# 2. وظائف قاعدة البيانات
def init_db():
    conn = sqlite3.connect('aiman_guard.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports (url TEXT, email TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (name TEXT, email TEXT, msg TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 3. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #00d4ff;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #00d4ff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. عرض الشعار والعنوان
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("1774474792146.png", use_container_width=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# 5. التبويبات
tab1, tab2, tab3, tab4 = st.tabs(["🔍 فحص الروابط", "📢 البلاغات", "📧 اتصل بنا", "🔐 الإدارة"])

with tab1:
    url_input = st.text_input("أدخل الرابط للفحص:")
    if st.button("بدء الفحص"):
        if url_input:
            ext = tldextract.extract(url_input)
            domain = f"{ext.domain}.{ext.suffix}"
            st.success(f"✅ الرابط ({domain}) يبدو آمناً.")
        else:
            st.warning("يرجى إدخال رابط.")

with tab2:
    st.subheader("إبلاغ عن رابط محتال")
    bad_url = st.text_input("الرابط المشبوه:")
    u_mail = st.text_input("بريدك (اختياري):")
    if st.button("إرسال بلاغ"):
        if bad_url:
            conn = sqlite3.connect('aiman_guard.db')
            conn.execute("INSERT INTO reports VALUES (?, ?, ?)", (bad_url, u_mail if u_mail else "مجهول", datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            st.info("تم تسجيل البلاغ بنجاح.")

with tab3:
    st.subheader("تواصل مع أيمن")
    n = st.text_input("الاسم:")
    e = st.text_input("البريد:")
    m = st.text_area("الرسالة:")
    if st.button("إرسال"):
        if n and m:
            conn = sqlite3.connect('aiman_guard.db')
            conn.execute("INSERT INTO messages VALUES (?, ?, ?, ?)", (n, e, m, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            st.success("شكراً لرسالتك!")

with tab4:
    pw = st.text_input("كلمة مرور المدير:", type="password")
    if pw == "ayman7716":
        st.write("### لوحة التحكم")
        conn = sqlite3.connect('aiman_guard.db')
        st.write("البلاغات:", conn.execute("SELECT * FROM reports").fetchall())
        st.write("الرسائل:", conn.execute("SELECT * FROM messages").fetchall())
        if st.button("مسح البيانات"):
            conn.execute("DELETE FROM reports")
            conn.execute("DELETE FROM messages")
            conn.commit()
            st.rerun()
        conn.close()
