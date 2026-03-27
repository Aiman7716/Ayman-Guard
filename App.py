import streamlit as st
import yt_dlp
import os
import sqlite3
from datetime import datetime

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d; }
    div.stButton > button, .stFormSubmitButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; border: none !important; }
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    .data-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-right: 5px solid #1f6feb; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('ayman_pro_v240.db', check_same_thread=False)
    c = conn.cursor()
    # إنشاء الجداول والتأكد من وجودها
    c.execute('CREATE TABLE IF NOT EXISTS community_reports (name TEXT, content TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS contact_msgs (name TEXT, message TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()

# --- 3. الهيكل الرئيسي للأقسام ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة استقرار الإدارة v240.0</p></div>', unsafe_allow_html=True)
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 حماية المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- تبويب محمل الفيديو (جاري جلب الفيديو) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 محمل الفيديو المباشر")
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    if st.button("🚀 تحميل الفيديو الآن"):
        if v_url:
            with st.spinner("جاري جلب الفيديو..."): # التعديل المطلوب
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'vid_ayman.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_url])
                    with open("vid_ayman.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ في الجهاز", f, "video.mp4")
                    os.remove("vid_ayman.mp4")
                except: st.error("❌ فشل جلب الفيديو، الرابط قد يكون محمياً.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب حماية المجتمع ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("comm_v240", clear_on_submit=True):
        u_name = st.text_input("الاسم:")
        u_text = st.text_area("بلاغ عن رابط مشبوه:")
        if st.form_submit_button("نشر التحذير"):
            if u_text:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                c = db.cursor()
                c.execute("INSERT INTO community_reports VALUES (?, ?, ?)", (u_name if u_name else "مجهول", u_text, dt))
                db.commit()
                st.success("✅ تم النشر")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب تواصل معنا ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("contact_v240", clear_on_submit=True):
        c_name = st.text_input("اسمك:")
        c_msg = st.text_area("رسالتك للإدارة:")
        if st.form_submit_button("إرسال الآن"):
            if c_name and c_msg:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                c = db.cursor()
                c.execute("INSERT INTO contact_msgs VALUES (?, ?, ?)", (c_name, c_msg, dt))
                db.commit()
                st.success("✅ وصلت رسالتك")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب الإدارة (إصلاح كلمة المرور وعرض البيانات) ---
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔐 لوحة التحكم")
    # كلمة المرور التي استخدمتها في صورتك
    pwd = st.text_input("كلمة مرور المدير:", type="password")
    
    if pwd == "ayman7716": 
        st.success("تم تسجيل الدخول بنجاح")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("### 📧 الرسائل الواردة")
            c = db.cursor()
            c.execute("SELECT * FROM contact_msgs ORDER BY date DESC")
            for m in c.fetchall():
                st.markdown(f'<div class="data-box"><strong>من:</strong> {m[0]}<br><small>{m[2]}</small><p>{m[1]}</p></div>', unsafe_allow_html=True)
                
        with col2:
            st.write("### 👥 بلاغات المجتمع")
            c = db.cursor()
            c.execute("SELECT * FROM community_reports ORDER BY date DESC")
            for r in c.fetchall():
                st.markdown(f'<div class="data-box"><strong>المبلغ:</strong> {r[0]}<br><small>{r[2]}</small><p>{r[1]}</p></div>', unsafe_allow_html=True)
    elif pwd != "":
        st.error("كلمة المرور غير صحيحة!")
    st.markdown('</div>', unsafe_allow_html=True)
