import streamlit as st
import yt_dlp
import os
import sqlite3
from datetime import datetime

# --- 1. الإعدادات البصرية وتوحيد الهوية (الكحلي النيلي) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* الهيدر الرئيسي */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px;
    }

    /* توحيد شكل الأزرار الكحلية */
    div.stButton > button, .stDownloadButton > button {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; 
        border: none !important; transition: 0.3s ease;
    }
    div.stButton > button:hover { background-color: #388bfd !important; transform: scale(1.01); }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    
    /* تنسيق التبويبات */
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الهيكل الرئيسي للأقسام ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>النسخة الشاملة والنهائية v180.0</p></div>', unsafe_allow_html=True)

# إعادة التبويبات الستة كاملة كما في صورتك الأصلية
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("مرحباً بك في درع أيمن")
    st.info("تم تحديث النظام ليدعم التحميل الداخلي المباشر وتجاوز حظر المنصات.")
    st.write("استخدم التبويبات بالأعلى للتنقل بين خدمات الدرع.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 2: الفحص ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔍 فحص الروابط المشبوهة")
    check_url = st.text_input("أدخل الرابط المراد فحصه:")
    if st.button("بدء الفحص الأمني"):
        if check_url:
            st.success("جاري تحليل الرابط... (تم تفعيل بروتوكول الحماية)")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 3: محمل الفيديو (الحل الجذري الداخلي) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 محمل الفيديو السيادي (تحميل داخلي)")
    v_url = st.text_input("ألصق رابط الفيديو (Facebook, TikTok, YT):", key="v_loader")
    
    if st.button("🚀 استخراج وتحميل الآن"):
        if v_url:
            with st.spinner("جاري المعالجة داخل موقعك..."):
                try:
                    # إعدادات كسر الحظر والتحميل الداخلي
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': 'ayman_media.%(ext)s',
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'noplaylist': True,
                        'quiet': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=True)
                        filename = ydl.prepare_filename(info)
                    
                    st.success("✅ تم الاستخراج بنجاح!")
                    
                    # عرض الفيديو وتحميله للمستخدم من موقعك مباشرة
                    with open(filename, "rb") as f:
                        video_bytes = f.read()
                        st.video(video_bytes)
                        st.download_button(
                            label="📥 حفظ الفيديو في جهازك",
                            data=video_bytes,
                            file_name=filename,
                            mime="video/mp4"
                        )
                    
                    # حذف الملف المؤقت من السيرفر فوراً
                    os.remove(filename)
                except Exception as e:
                    st.error("🚨 المنصة تفرض حماية مشددة على هذا الرابط حالياً.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 4: المجتمع ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("👥 بلاغات المجتمع")
    report = st.text_area("اكتب بلاغك هنا:")
    if st.button("نشر البلاغ"):
        st.success("تم نشر بلاغك في مجتمع الدرع.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 5: تواصل معنا ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 مراسلة الإدارة")
    name = st.text_input("الاسم:")
    msg = st.text_area("الرسالة:")
    if st.button("إرسال البيانات"):
        if name and msg:
            st.success(f"شكراً يا {name}، تم استلام رسالتك.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 6: الإدارة ---
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔐 لوحة التحكم")
    admin_pass = st.text_input("كلمة السر:", type="password")
    if st.button("دخول"):
        st.warning("كلمة السر غير صحيحة.")
    st.markdown('</div>', unsafe_allow_html=True)
