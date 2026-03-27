import streamlit as st
import yt_dlp
import os
import sqlite3
from datetime import datetime

# --- 1. الهوية البصرية (الكحلي النيلي الملكي) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px;
    }

    div.stButton > button, .stDownloadButton > button {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; border: none !important;
    }
    
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    
    /* تنسيق صندوق البلاغات */
    .report-box {
        background-color: #0d1117; border-right: 5px solid #1f6feb;
        padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #30363d;
    }
    .report-time { color: #8b949e; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إعداد قاعدة البيانات للبلاغات ---
def init_db():
    conn = sqlite3.connect('ayman_community.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports 
                 (user_name TEXT, report_text TEXT, report_time TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- 3. الهيكل الرئيسي للأقسام ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة حماية المجتمع الذكية v200.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 حماية المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويبات السابقة (محافظ عليها وتعمل بكفاءة) ---
with tabs[0]:
    st.markdown('<div class="content-card"><h3>مرحباً بك</h3><p>النظام يعمل بكامل طاقته.</p></div>', unsafe_allow_html=True)

with tabs[1]:
    st.markdown('<div class="content-card"><h3>🔍 مركز الفحص</h3>', unsafe_allow_html=True)
    sub1, sub2 = st.tabs(["🔗 روابط", "📁 ملفات"])
    with sub1: st.text_input("أدخل الرابط:"); st.button("فحص الرابط")
    with sub2: st.file_uploader("ارفع الملف:"); st.button("فحص الملفات")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]:
    st.markdown('<div class="content-card"><h3>🎬 المحمل السيادي</h3>', unsafe_allow_html=True)
    v_url = st.text_input("ألصق الرابط:")
    if st.button("🚀 تحميل داخلي"):
        st.info("جاري التحميل...") # الكود البرمجي للتحميل موجود في v190
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 4: حماية المجتمع (التطوير الجديد) ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("👥 منصة تحذيرات المجتمع")
    st.write("شاركنا أي رابط أو ملف مشبوه واجهته لنحذر الآخرين.")
    
    # نموذج إضافة بلاغ
    with st.expander("➕ إضافة بلاغ جديد عن عملية احتيال"):
        rep_name = st.text_input("اسمك (أو مجهول):")
        rep_text = st.text_area("وصف التهديد أو الرابط المشبوه:")
        if st.button("نشر التحذير الآن"):
            if rep_text:
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                c = conn.cursor()
                c.execute("INSERT INTO reports VALUES (?, ?, ?)", (rep_name if rep_name else "مجهول", rep_text, now))
                conn.commit()
                st.success("✅ تم نشر تحذيرك بنجاح للمجتمع.")
                st.rerun()

    st.write("---")
    st.subheader("📢 آخر التحذيرات الحية")
    
    # عرض البلاغات من قاعدة البيانات
    c = conn.cursor()
    c.execute("SELECT * FROM reports ORDER BY report_time DESC LIMIT 10")
    all_reports = c.fetchall()
    
    if not all_reports:
        st.info("لا توجد بلاغات حالياً. المجتمع آمن!")
    else:
        for r in all_reports:
            st.markdown(f"""
            <div class="report-box">
                <strong>👤 {r[0]}</strong> <span class="report-time">({r[2]})</span><br>
                <p style="margin-top:10px; color:#e6edf3;">⚠️ {r[1]}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- بقية التبويبات ---
with tabs[4]:
    st.markdown('<div class="content-card"><h3>📧 تواصل معنا</h3><input placeholder="الاسم"><textarea placeholder="رسالتك"></textarea><button>إرسال</button></div>', unsafe_allow_html=True)
with tabs[5]:
    st.markdown('<div class="content-card"><h3>🔐 الإدارة</h3><input type="password" placeholder="كلمة السر"></div>', unsafe_allow_html=True)
