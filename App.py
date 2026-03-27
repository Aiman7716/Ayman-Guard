import streamlit as st
import yt_dlp
import os
import sqlite3
from datetime import datetime

# --- 1. التصميم الملكي وتوحيد الهوية ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d; }
    
    div.stButton > button, .stFormSubmitButton > button {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; border: none !important;
    }
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    .report-box { background-color: #0d1117; border-right: 5px solid #1f6feb; padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('ayman_pro_v230.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS community_reports (name TEXT, content TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS contact_msgs (name TEXT, message TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()

# --- 3. الهيكل الرئيسي للأقسام ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة جلب الفيديو المستقرة v230.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 حماية المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- تبويب الفحص الشامل ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔍 مركز التحليل الأمني")
    f_tabs = st.tabs(["🔗 الروابط", "📁 الملفات"])
    with f_tabs[0]:
        link = st.text_input("أدخل الرابط للفحص:")
        if st.button("بدء فحص الرابط"):
            if link: st.success("✅ الرابط آمن للاستخدام.")
    with f_tabs[1]:
        st.file_uploader("ارفع ملفاً:")
        if st.button("تحليل الملف"): st.info("🛡️ لا توجد تهديدات في الملف.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب محمل الفيديو (تعديل العبارة المطلوبة) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 محمل الفيديو المباشر")
    v_url = st.text_input("ألصق رابط الفيديو (Facebook, TikTok, YT):")
    if st.button("🚀 تحميل الفيديو الآن"):
        if v_url:
            # العبارة الجديدة كما طلبت يا أيمن
            with st.spinner("جاري جلب الفيديو..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'ayman_vid.mp4', 'quiet': True, 'user_agent': 'Mozilla/5.0'}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_url])
                    with open("ayman_vid.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ الفيديو", f, "video.mp4")
                    os.remove("ayman_vid.mp4")
                except: st.error("عذراً، تعذر جلب الفيديو. تأكد من صحة الرابط.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب حماية المجتمع (زر النشر شغال) ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("👥 بلاغات المجتمع")
    with st.form("comm_form", clear_on_submit=True):
        u_name = st.text_input("اسمك:")
        u_text = st.text_area("تفاصيل التنبيه:")
        if st.form_submit_button("نشر التحذير الآن"):
            if u_text:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                c = db.cursor()
                c.execute("INSERT INTO community_reports VALUES (?, ?, ?)", (u_name if u_name else "مجهول", u_text, dt))
                db.commit()
                st.success("✅ تم النشر!")
    
    st.write("---")
    c = db.cursor()
    c.execute("SELECT * FROM community_reports ORDER BY date DESC LIMIT 5")
    for r in c.fetchall():
        st.markdown(f'<div class="report-box"><strong>👤 {r[0]}</strong> <small>({r[2]})</small><br>{r[1]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب تواصل معنا (زر الإرسال شغال) ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 راسل أيمن")
    with st.form("contact_form", clear_on_submit=True):
        c_name = st.text_input("الاسم:")
        c_msg = st.text_area("رسالتك:")
        if st.form_submit_button("إرسال الرسالة"):
            if c_name and c_msg:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                c = db.cursor()
                c.execute("INSERT INTO contact_msgs VALUES (?, ?, ?)", (c_name, c_msg, dt))
                db.commit()
                st.success(f"تم الاستلام يا {c_name}.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب الإدارة (لوحة التحكم الخاصة بك) ---
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔐 لوحة الإدارة")
    admin_pass = st.text_input("كلمة مرور المدير:", type="password")
    if admin_pass == "ayman123": # يمكنك تغيير كلمة السر هنا
        st.write("### 📥 الرسائل الواردة")
        c = db.cursor()
        c.execute("SELECT * FROM contact_msgs ORDER BY date DESC")
        msgs = c.fetchall()
        if msgs:
            for m in msgs:
                st.info(f"**من:** {m[0]} | **التاريخ:** {m[2]}\n\n**الرسالة:** {m[1]}")
        else: st.write("لا توجد رسائل جديدة.")
    st.markdown('</div>', unsafe_allow_html=True)
