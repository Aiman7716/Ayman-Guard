import streamlit as st
import yt_dlp
import requests

# --- 1. التنسيق السيادي الرسمي v31 ---
st.set_page_config(page_title="Ayman Guard Pro v31", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px; }
    
    /* أزرار النظام */
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 10px; font-weight: bold; height: 3.5em; border: none; }
    
    /* زر الحفظ الرسمي */
    .stDownloadButton > button {
        background-color: #238636 !important;
        width: 100% !important; height: 4.5em !important;
        font-size: 20px !important; font-weight: bold !important;
        border-radius: 12px !important; border: 2px solid #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة ذاكرة الجلسة لضمان عدم اختفاء الفيديو ---
if 'video_ready' not in st.session_state:
    st.session_state.video_ready = False
if 'video_data' not in st.session_state:
    st.session_state.video_data = None
if 'video_url' not in st.session_state:
    st.session_state.video_url = ""
if 'video_title' not in st.session_state:
    st.session_state.video_title = ""

st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>نظام المعالجة الثابت v31.0</p></div>', unsafe_allow_html=True)

# --- 3. محرك المعالجة ---
input_url = st.text_input("يرجى إدخال رابط الوسائط هنا:")

if st.button("🚀 بدء المعالجة الرسمية"):
    if input_url:
        with st.spinner("جاري فحص وتجهيز البيانات، يرجى الانتظار..."):
            try:
                ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(input_url, download=False)
                    direct_link = info.get('url', None)
                    st.session_state.video_title = info.get('title', 'Ayman_Video')
                    st.session_state.video_url = direct_link

                if direct_link:
                    # جلب الفيديو للذاكرة ليبقى متاحاً للتحميل
                    resp = requests.get(direct_link)
                    st.session_state.video_data = resp.content
                    st.session_state.video_ready = True
                else:
                    st.error("فشل النظام في استخراج البيانات.")
            except Exception as e:
                st.error(f"تنبيه رسمي: حدث خطأ أثناء المعالجة ({e})")

st.markdown("---")

# --- 4. عرض النتائج (يظل ظاهراً حتى بعد التحميل) ---
if st.session_state.video_ready:
    # المعاينة تظل ثابتة هنا
    st.video(st.session_state.video_url)
    
    # زر التحميل الرسمي
    # عند الضغط عليه، لن تختفي المعاينة لأنها مخزنة في Session State
    download = st.download_button(
        label="📥 حفظ الفيديو في الاستوديو",
        data=st.session_state.video_data,
        file_name=f"{st.session_state.video_title}.mp4",
        mime="video/mp4"
    )
    
    # إشعار رسمي يظهر بعد الضغط
    if download:
        st.toast("✅ جاري بدء تحميل الفيديو إلى جهازك...", icon="📥")
        st.success("نظام الدرع: تم إرسال طلب التحميل بنجاح. يرجى مراجعة سجل التحميلات في جهازك.")
