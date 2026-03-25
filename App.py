import streamlit as st
import tldextract
import sqlite3
from datetime import datetime

# 1. إعدادات الصفحة والشعار (Favicon)
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

# 3. التنسيق الجمالي (CSS) - إصلاح الاتجاه للعربية RTL
st.markdown("""
    <style>
    /* قلب اتجاه الموقع بالكامل */
    .main, .stApp {
        direction: RTL;
        text-align: right;
    }
    /* تنسيق التبويبات لتبدأ من اليمين */
    .stTabs [data-baseweb="tab-list"] {
        direction: RTL;
        justify-content: flex-start;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: bold;
    }
    .main-title {
        text-align: center;
        color: #00d4ff;
        font-size: 2.5rem;
        font-weight: bold;
        margin-top: -20px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #00d4ff;
        color: white;
    }
    /* توحيد اتجاه النصوص داخل الصناديق */
    input, textarea {
        direction: RTL !important;
        text-align: right !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. عرض الشعار في المنتصف
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("1774474792146.png", use_container_width=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# 5. التبويبات المرتبة من اليمين
tab1, tab2, tab3, tab4 = st.tabs(["🔍 فحص الروابط", "📢 البلاغات", "📧 اتصل بنا", "🔐 الإدارة"])

with tab1:
    st.subheader("افحص أي رابط الآن")
    url_input = st.text_input("أدخل الرابط المراد فحصه:")
    if st.button("بدء الفحص الذكي"):
        if url_input:
            ext = tldextract.extract(url_input)
            domain = f"{ext.domain}.{ext.suffix}"
            # قائمة تجريبية للمواقع المحظورة
            if domain in ["test-hack.com", "login-fake.net"]:
                st.error(f"⚠️ تحذير: الرابط ({domain}) مشبوه جداً!")
            else:
                st.success(f"✅ الرابط ({domain}) يبدو آمناً للاستخدام.")
        else:
            st.warning("يرجى إدخال الرابط أولاً.")

with tab2:
    st.subheader("ساحة البلاغات المجتمعية")
    bad_url = st.text_input("رابط الموقع المحتال:")
    u_mail = st.text_input("بريدك الإلكتروني (اختياري):")
    if st.button("إرسال البلاغ"):
        if bad_url:
            conn = sqlite3.connect('aiman_guard.db')
            conn.execute("INSERT INTO reports VALUES (?, ?, ?)", (bad_url, u_mail if u_mail else "مجهول", datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            st.info("تم استلام بلاغك بنجاح، شكراً لتعاونك.")
        else:
            st.error("يرجى كتابة الرابط المبلّغ عنه.")

with tab3:
    st.subheader("تواصل مع المطور")
    n = st.text_input("اسمك الكريم:")
    e = st.text_input("بريدك الإلكتروني:")
    m = st.text_area("رسالتك:")
    if st.button("إرسال الرسالة"):
        if n and m:
            conn = sqlite3.connect('aiman_guard.db')
            conn.execute("INSERT INTO messages VALUES (?, ?, ?, ?)", (n, e, m, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            st.success("تم إرسال رسالتك لـ أيمن بنجاح!")
        else:
            st.error("يرجى إكمال البيانات المطلوبة.")

with tab4:
    st.subheader("دخول الإدارة")
    pw = st.text_input("كلمة مرور المدير:", type="password")
    if pw == "ayman7716":
        st.success("أهلاً بك يا مهندس أيمن")
        conn = sqlite3.connect('aiman_guard.db')
        
        st.write("---")
        st.write("### 📢 البلاغات الواردة")
        reps = conn.execute("SELECT * FROM reports").fetchall()
        for r in reps:
            st.text(f"الرابط: {r[0]} | من: {r[1]} | بتاريخ: {r[2]}")
            
        st.write("---")
        st.write("### 📧 رسائل الزوار")
        msgs = conn.execute("SELECT * FROM messages").fetchall()
        for msg in msgs:
            st.text(f"من: {msg[0]} | الرسالة: {msg[2]}")
            
        if st.button("مسح كافة البيانات"):
            conn.execute("DELETE FROM reports")
            conn.execute("DELETE FROM messages")
            conn.commit()
            st.rerun()
        conn.close()
