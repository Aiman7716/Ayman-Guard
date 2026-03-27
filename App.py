import streamlit as st
import tldextract, sqlite3, requests, pandas as pd
import yt_dlp
import io
from datetime import datetime

# --- 1. الإعدادات ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

# --- 2. التصميم البصري (توحيد الألوان للكحلي) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 25px 20px; border-radius: 20px; text-align: center; margin-bottom: 10px; border: 1px solid #30363d;
    }

    .ticker-wrap {
        background: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; border-radius: 10px;
        overflow: hidden; white-space: nowrap; padding: 10px 0; margin-bottom: 20px;
    }
    .ticker { display: inline-block; animation: ticker 50s linear infinite; color: #ff4b4b; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* تنسيق أزرار Streamlit لتصبح كحلية واضحة جداً كما طلبت */
    div.stButton > button, div.stDownloadButton > button {
        width: 100% !important;
        background-color: #1f6feb !important; /* كحلي نيلي */
        color: white !important;
        border-radius: 12px !important;
        height: 3.8em !important;
        font-weight: bold !important;
        border: none !important;
        font-size: 1.1rem !important;
    }
    
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. الهيكل الرئيسي ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>Ayman Security PRO v46.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "🔐 الإدارة"])

# --- تبويب محمل الفيديو (الحل الجديد لمشكلة 403) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 محمل الوسائط الذكي")
    v_url = st.text_input("ألصق الرابط هنا (TikTok, YouTube, FB):")
    
    if st.button("استخراج ومعالجة"):
        if v_url:
            with st.spinner("جاري تجاوز الحماية وجلب الملف..."):
                try:
                    # إعدادات متقدمة للتحميل المباشر للسيرفر
                    ydl_opts = {
                        'format': 'best',
                        'quiet': True,
                        'no_warnings': True,
                        'outtmpl': '-', # إرسال البيانات للذاكرة (Buffer)
                        'logtostderr': False
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        st.video(info['url']) # معاينة الفيديو
                        
                        st.write(f"✅ تم العثور على: **{info.get('title', 'فيديو')}**")
                        
                        # طلب البيانات من الرابط وتحويلها لملف قابل للتحميل (لتجنب 403)
                        response = requests.get(info['url'], stream=True)
                        video_bytes = io.BytesIO(response.content)

                        # أزرار التحميل الجديدة (كحلية واحترافية)
                        st.download_button(
                            label="📥 تحميل الفيديو MP4 (كحلي)",
                            data=video_bytes,
                            file_name=f"ayman_video_{datetime.now().strftime('%H%M%S')}.mp4",
                            mime="video/mp4"
                        )
                        
                        st.info("💡 ملاحظة: التحميل الآن يتم عبر 'سيرفر الدرع' لضمان عدم ظهور خطأ 403.")
                        
                except Exception as e:
                    st.error(f"❌ حدث خطأ: تأكد من صحة الرابط أو جرب لاحقاً.")
    st.markdown('</div>', unsafe_allow_html=True)
