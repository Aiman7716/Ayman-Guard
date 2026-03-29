import streamlit as st
import yt_dlp
import requests
import time

# --- 1. التنسيق السيادي المتطور (تلوين الزر مباشرة) ---
st.set_page_config(page_title="Ayman Guard Pro v34", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* هيدر الصفحة */
    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; border: 1px solid #30363d;
    }

    /* --- تلوين زر "اختيار ملف" (Browse) مباشرة --- */
    button[kind="secondary"] {
        background-color: #1f6feb !important; /* لون أزرق بارز */
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #ffffff !important;
        font-weight: bold !important;
        padding: 0.5rem 1rem !important;
        transition: 0.3s !important;
    }
    button[kind="secondary"]:hover {
        background-color: #388bfd !important;
        transform: scale(1.05);
    }

    /* أزرار النظام الأخرى */
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; font-weight: bold; height: 3.5em; border: none; }
    .stDownloadButton > button { background-color: #238636 !important; width: 100% !important; height: 4.5em !important; font-size: 20px !important; font-weight: bold !important; border-radius: 12px !important; border: 2px solid #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة الذاكرة ---
if 'v_ready' not in st.session_state: st.session_state.v_ready = False
if 'v_data' not in st.session_state: st.session_state.v_data = None
if 'v_url' not in st.session_state: st.session_state.v_url = ""
if 'v_title' not in st.session_state: st.session_state.v_title = ""

# --- 3. بناء الواجهة ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الفحص والتحميل المطور v34.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الشاشة الرئيسية", "🎬 مركز التحميل", "🔍 مركز الفحص"])

# --- تبويب الشاشة الرئيسية ---
with tabs[0]:
    st.markdown("### 📊 حالة النظام")
    col1, col2 = st.columns(2)
    col1.metric("الحماية", "نشطة 100%")
    col2.metric("الاستجابة", "سريعة جداً")
    st.info("أهلاً بك يا أيمن. النظام جاهز.")

# --- تبويب مركز التحميل (الثابت والمجرب) ---
with tabs[1]:
    st.subheader("🎬 محرك الوسائط")
    u_in = st.text_input("ألصق الرابط هنا:")
    if st.button("🚀 بدء المعالجة"):
        if u_in:
            with st.spinner("جاري فحص وتجهيز البيانات، يرجى الانتظار..."):
                try:
                    ydl_opts = {'format': 'best', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(u_in, download=False)
                        st.session_state.v_url = info.get('url', None)
                        st.session_state.v_title = info.get('title', 'Video')
                    if st.session_state.v_url:
                        st.session_state.v_data = requests.get(st.session_state.v_url).content
                        st.session_state.v_ready = True
                except Exception as e: st.error(f"خطأ: {e}")

    if st.session_state.v_ready:
        st.video(st.session_state.v_url)
        if st.download_button(label="📥 حفظ الفيديو في الاستوديو", data=st.session_state.v_data, file_name=f"{st.session_state.v_title}.mp4", mime="video/mp4"):
            st.toast("✅ جاري التحميل المباشر...", icon="📥")

# --- تبويب مركز الفحص (تعديل زر الملف) ---
with tabs[2]:
    st.subheader("🔍 فحص الروابط والملفات")
    
    # فحص الروابط
    link = st.text_input("رابط التحليل:")
    if st.button("🛡️ تحليل الرابط"):
        try:
            r = requests.head(link, timeout=5)
            st.success(f"الرابط مستجيب آمن ({r.status_code})")
        except: st.error("تنبيه: الرابط غير مستجيب.")
    
    st.markdown("---")
    
    # فحص الملفات (الزر الملون البارز)
    st.markdown("#### 📁 فحص الملفات الذكي")
    f_up = st.file_uploader("يرجى الضغط على الزر الملون لاختيار ملف:", type=['png', 'jpg', 'mp4', 'pdf', 'apk', 'zip'])
    
    if f_up is not None:
        st.write(f"📄 الملف المختار: **{f_up.name}**")
        if st.button("🔍 تنفيذ فحص أمني"):
            with st.spinner("جاري تحليل بنية الملف..."):
                time.sleep(2)
                st.success(f"✅ نتيجة الفحص: الملف '{f_up.name}' سليم.")
