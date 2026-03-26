import streamlit as st
import tldextract
import sqlite3
import os
from datetime import datetime

# 1. إعدادات الصفحة والشعار
st.set_page_config(
    page_title="درع أيمن الذكي",
    page_icon="1774474792146.png",
    layout="centered"
)

# 2. وظائف قاعدة البيانات المحدثة
def init_db():
    conn = sqlite3.connect('aiman_guard.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports (url TEXT, email TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (name TEXT, email TEXT, msg TEXT, date TEXT)''')
    # جدول جديد لسجل فحص الملفات
    c.execute('''CREATE TABLE IF NOT EXISTS file_logs (file_name TEXT, file_type TEXT, status TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 3. التنسيق الجمالي (CSS) لدعم العربية والسمة الداكنة
st.markdown("""
    <style>
    .main, .stApp { direction: RTL; text-align: right; }
    .stTabs [data-baseweb="tab-list"] { direction: RTL; justify-content: flex-start; gap: 10px; }
    .main-title {
        text-align: center; color: #00d4ff; font-size: 2.5rem;
        font-weight: bold; margin-bottom: 10px;
    }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #00d4ff; color: white; }
    input, textarea { direction: RTL !important; text-align: right !important; }
    .report-box { padding: 10px; border-radius: 5px; background-color: #262730; margin-bottom: 5px; border-right: 5px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 4. عرض الشعار
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("1774474792146.png", use_container_width=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# 5. التبويبات المحدثة
tabs = st.tabs(["🔍 فحص الروابط", "📁 فحص الملفات", "📢 البلاغات", "📧 اتصل بنا", "🔐 الإدارة"])

# --- تبويب فحص الروابط ---
with tabs[0]:
    st.subheader("تحقق من سلامة الروابط")
    url_input = st.text_input("أدخل الرابط المراد فحصه:")
    if st.button("بدء فحص الرابط"):
        if url_input:
            ext = tldextract.extract(url_input)
            domain = f"{ext.domain}.{ext.suffix}"
            st.success(f"✅ تم تحليل الرابط بنجاح. النطاق المستخرج: {domain}")
        else: st.warning("يرجى إدخال رابط أولاً.")

# --- تبويب فحص الملفات ---
with tabs[1]:
    st.subheader("كاشف الملفات المشبوهة")
    uploaded_file = st.file_uploader("ارفع الملف هنا لفحصه أمنياً:", type=None)
    if uploaded_file is not None:
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        dangerous_exts = ['.exe', '.bat', '.msi', '.sh', '.py', '.js', '.scr', '.vbs']
        
        status = "آمن"
        if ext in dangerous_exts:
            status = "خطر/تنفيذي"
            st.error(f"⚠️ تحذير أمني: الملف ({uploaded_file.name}) هو ملف تنفيذي وقد يلحق الضرر بجهازك!")
        else:
            st.success(f"✅ فحص أولي: الملف ({uploaded_file.name}) يبدو من نوع غير تنفيذي وآمن.")
        
        # حفظ العملية في قاعدة البيانات
        conn = sqlite3.connect('aiman_guard.db')
        conn.execute("INSERT INTO file_logs VALUES (?, ?, ?, ?)", 
                     (uploaded_file.name, ext, status, datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        conn.close()

# --- تبويب البلاغات ---
with tabs[2]:
    st.subheader("الإبلاغ عن احتيال")
    bad_url = st.text_input("رابط الموقع المخادع:")
    if st.button("إرسال تقرير"):
        if bad_url:
            conn = sqlite3.connect('aiman_guard.db')
            conn.execute("INSERT INTO reports VALUES (?, ?, ?)", (bad_url, "مستخدم", datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            st.info("تمت إضافة الرابط لقائمة المراجعة. شكراً لمساهمتك.")

# --- تبويب اتصل بنا ---
with tabs[3]:
    st.subheader("تواصل مباشر مع المطور")
    name = st.text_input("الاسم:")
    msg = st.text_area("رسالتك أو اقتراحك:")
    if st.button("إرسال الآن"):
        if name and msg:
            conn = sqlite3.connect('aiman_guard.db')
            conn.execute("INSERT INTO messages VALUES (?, ?, ?, ?)", (name, "غير متوفر", msg, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            st.success(f"شكراً يا {name}، تم استلام رسالتك.")

# --- تبويب الإدارة ---
with tabs[4]:
    st.subheader("لوحة التحكم السرية")
    auth = st.text_input("كلمة المرور:", type="password")
    if auth == "ayman7716":
        st.success("مرحباً بك يا مهندس أيمن")
        conn = sqlite3.connect('aiman_guard.db')
        
        st.write("### 📂 سجل فحص الملفات الأخير")
        logs = conn.execute("SELECT * FROM file_logs ORDER BY date DESC LIMIT 10").fetchall()
        for l in logs:
            st.markdown(f'<div class="report-box">ملف: {l[0]} | نوعه: {l[1]} | الحالة: {l[2]} | التاريخ: {l[3]}</div>', unsafe_allow_html=True)
            
        st.write("---")
        if st.button("تصفير جميع البيانات"):
            conn.execute("DELETE FROM file_logs")
            conn.execute("DELETE FROM reports")
            conn.execute("DELETE FROM messages")
            conn.commit()
            st.rerun()
        conn.close()
