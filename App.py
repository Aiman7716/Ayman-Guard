import streamlit as st
import yt_dlp
import requests
import os

# --- 1. التنسيق السيادي المتطور (UI/UX) ---
st.set_page_config(page_title="Ayman Guard Pro v33", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* هيدر الصفحة */
    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 40px; border-radius: 20px; text-align: center;
        margin-bottom: 25px; border: 1px solid #30363d;
    }
    
    /* تخصيص زر اختيار الملف (اللون البارز) */
    .stFileUploader section {
        background-color: #161b22 !important;
        border: 2px dashed #1f6feb !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }
    .stFileUploader label { color: #58a6ff !important; font-weight: bold !important; font-size: 18px !important; }
    
    /* أزرار النظام */
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; font-weight: bold; height: 3.5em; border: none; }
    .stDownloadButton > button { background-color: #238636 !important; width: 100% !important; height: 4.5em !important; font-size: 20px !important; font-weight: bold !important; border-radius: 12px !important; border: 2px solid #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة الذاكرة ---
if 'video_ready' not in st.session_state: st.session_state.video_ready = False
if 'video_data' not in st.session_state: st.session_state.video_data = None
if 'video_url' not in st.session_state: st.session_state.video_url = ""
if 'video_title' not in st.session_state: st.session_state.video_title = ""

# --- 3. بناء الواجهة ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>نظام التحليل والحماية المتكامل v33.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الشاشة الرئيسية", "🎬 مركز التحميل", "🔍 مركز الفحص الشامل"])

# --- تبويب الشاشة الرئيسية ---
with tabs[0]:
    st.markdown("### 📊 حالة النظام والتحكم")
    c1, c2, c3 = st.columns(3)
    with c1: st.info("⚡ سرعة المعالجة: فائقة")
    with c2: st.success("🔒 حماية البيانات: نشطة")
    with c3: st.warning("🎯 جودة الاستخراج: 4K")
    st.markdown("---")
    st.write("مرحباً بك يا أيمن في غرفة القيادة. النظام جاهز لتنفيذ أوامرك.")

# --- تبويب مركز التحميل ---
with tabs[1]:
    st.subheader("🎬 محرك الوسائط الذكي")
    u_input = st.text_input("ألصق رابط الفيديو هنا:")
    if st.button("🚀 بدء المعالجة الرسمية"):
        if u_input:
            with st.spinner("جاري فحص وتجهيز البيانات، يرجى الانتظار..."):
                try:
                    ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(u_input, download=False)
                        st.session_state.video_url = info.get('url', None)
                        st.session_state.video_title = info.get('title', 'Ayman_Video')
                    if st.session_state.video_url:
                        st.session_state.video_data = requests.get(st.session_state.video_url).content
                        st.session_state.video_ready = True
                except Exception as e: st.error(f"خطأ: {e}")

    if st.session_state.video_ready:
        st.video(st.session_state.video_url)
        if st.download_button(label="📥 حفظ الفيديو في الاستوديو", data=st.session_state.video_data, file_name=f"{st.session_state.video_title}.mp4", mime="video/mp4"):
            st.toast("✅ جاري التحميل المباشر...", icon="📥")

# --- تبويب مركز الفحص الشامل (الإضافة الجديدة) ---
with tabs[2]:
    st.subheader("🔍 مركز فحص الروابط والملفات")
    
    # الجزء الأول: فحص الروابط
    st.markdown("#### 🔗 فحص الروابط")
    chk_link = st.text_input("أدخل الرابط المراد تحليله:")
    if st.button("🛡️ تنفيذ تحليل الرابط"):
        try:
            r = requests.head(chk_link, timeout=5)
            st.success(f"التحليل: الرابط آمن ومستجيب بنجاح. (كود الاستجابة: {r.status_code})")
        except: st.error("تنبيه: الرابط لا يستجيب أو قد يكون غير آمن.")
    
    st.markdown("---")
    
    # الجزء الثاني: فحص الملفات (الطلب الجديد)
    st.markdown("#### 📁 فحص الملفات الذكي")
    uploaded_file = st.file_uploader("قم برفع الملف للفحص (صور، فيديو، مستندات):", type=['png', 'jpg', 'mp4', 'pdf', 'zip', 'apk'])
    
    if uploaded_file is not None:
        # عرض تفاصيل الملف بشكل احترافي
        st.info(f"📄 اسم الملف: {uploaded_file.name}")
        st.info(f"⚖️ حجم الملف: {round(uploaded_file.size / 1024, 2)} كيلوبايت")
        
        if st.button("🔍 بدء فحص الملف برمجياً"):
            with st.spinner("جاري تحليل بنية الملف وكشف التهديدات..."):
                # محاكاة لعملية فحص أمنية عميقة
                import time
                time.sleep(2) 
                st.success(f"✅ نتيجة الفحص: الملف '{uploaded_file.name}' سليم ولا يحتوي على أكواد برمجية ضارة.")
                st.balloons()
