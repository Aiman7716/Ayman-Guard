import streamlit as st
import yt_dlp
import requests
import time

# --- 1. التنسيق السيادي الموحد ---
st.set_page_config(page_title="Ayman Guard Pro v36", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; border: 1px solid #30363d;
    }

    /* أزرار التواصل الزرقاء الموحدة */
    .contact-btn {
        background-color: #1f6feb !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid #ffffff !important;
        font-weight: bold !important;
        text-decoration: none !important;
        display: block;
        padding: 15px;
        text-align: center;
        transition: 0.3s;
        margin-bottom: 10px;
    }
    .contact-btn:hover { background-color: #388bfd !important; transform: scale(1.02); }

    /* زر البوت المميز */
    .bot-btn {
        background: linear-gradient(90deg, #0088cc, #00aaff) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 20px;
        font-size: 20px !important;
        text-decoration: none !important;
        display: block;
        text-align: center;
        font-weight: bold;
        border: 2px solid #ffffff;
        box-shadow: 0 4px 15px rgba(0,136,204,0.4);
    }

    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; font-weight: bold; height: 3.5em; border: none; }
    .stDownloadButton > button { background-color: #238636 !important; width: 100% !important; height: 4.5em !important; font-size: 20px !important; font-weight: bold !important; border-radius: 12px !important; border: 2px solid #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة الذاكرة ---
if 'v_ready' not in st.session_state: st.session_state.v_ready = False
if 'v_data' not in st.session_state: st.session_state.v_data = None
if 'v_url' not in st.session_state: st.session_state.v_url = ""

# --- 3. الواجهة ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الحماية والارتباط الرسمي v36.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🎬 مركز التحميل", "🔍 مركز الفحص", "🛡️ الحماية والدعم"])

# (تبويبات الرئيسية والتحميل والفحص تبقى كما هي في الكود v35)
with tabs[0]: st.info("مرحباً بك يا أيمن في الإصدار v36 المتصل بالبوت الرسمي.")
with tabs[1]:
    u_in = st.text_input("أدخل الرابط:")
    if st.button("🚀 بدء المعالجة"):
        if u_in:
            with st.spinner("جاري فحص وتجهيز البيانات..."):
                try:
                    with yt_dlp.YoutubeDL({'format': 'best', 'quiet': True}) as ydl:
                        info = ydl.extract_info(u_in, download=False)
                        st.session_state.v_url = info.get('url')
                        st.session_state.v_data = requests.get(st.session_state.v_url).content
                        st.session_state.v_ready = True
                except: st.error("خطأ في الرابط")
    if st.session_state.v_ready:
        st.video(st.session_state.v_url)
        st.download_button("📥 حفظ الفيديو في الاستوديو", st.session_state.v_data, "video.mp4", "video/mp4")

with tabs[2]:
    st.file_uploader("فحص الملفات الذكي:", type=['apk', 'pdf', 'png', 'jpg', 'zip'])

# --- التبويب المطور: الحماية والدعم (إضافة البوت) ---
with tabs[3]:
    st.subheader("🤖 المساعد الذكي الرسمي")
    st.write("للحصول على دعم فوري، بلاغات سريعة، أو تحديثات النظام، تواصل مع بوت الدرع عبر تليجرام:")
    
    # رابط البوت الرسمي الخاص بك
    st.markdown(f'<a href="https://t.me/Ayman_Guard_2026_bot" target="_blank" class="bot-btn">🤖 ابدأ المحادثة مع بوت الدرع الآن</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📞 قنوات التواصل الأخرى")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<a href="https://wa.me/yournumber" class="contact-btn">📱 واتساب الرسمي</a>', unsafe_allow_html=True)
    with c2:
        st.markdown('<a href="mailto:support@aymanguard.com" class="contact-btn">📧 البريد الإلكتروني</a>', unsafe_allow_html=True)
    
    st.markdown('<div style="background:#161b22; padding:15px; border-radius:10px; border-right:4px solid #1f6feb;"><h4>👥 حماية المجتمع</h4><p>ساهم معنا في جعل الإنترنت مكاناً آمناً عبر التبليغ عن أي نشاط مشبوه من خلال البوت أعلاه.</p></div>', unsafe_allow_html=True)
