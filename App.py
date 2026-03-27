import streamlit as st
import yt_dlp
import requests
import io
from datetime import datetime

# --- 1. التصميم البصري (توحيد الألوان للكحلي النيلي) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 25px 20px; border-radius: 20px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d;
    }

    /* توحيد ألوان أزرار التحميل والمعالجة (كحلي نيلي) كما طلبت */
    div.stButton > button, div.stDownloadButton > button {
        width: 100% !important;
        background-color: #1f6feb !important;
        color: white !important;
        border-radius: 12px !important;
        height: 3.8em !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الهيكل العلوي ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>Ayman Security v47.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🎬 محمل الفيديو", "🔍 الفحص أمنياً"])

with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج الفيديو المباشر")
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    
    if st.button("استخراج وتحضير الملف"):
        if v_url:
            with st.spinner("جاري معالجة الفيديو وتجهيزه للتحميل..."):
                try:
                    # إعدادات متقدمة لجلب الرابط الحقيقي
                    ydl_opts = {
                        'format': 'best',
                        'quiet': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        video_url = info['url']
                        
                        # إظهار المعاينة
                        st.video(video_url)
                        st.success(f"✅ تم العثور على: {info.get('title', 'فيديو')[:50]}...")

                        # --- الحل الجذري: سحب البيانات بهوية متصفح لضمان عدم تلف الملف ---
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        }
                        video_data = requests.get(video_url, headers=headers).content
                        video_file = io.BytesIO(video_data)

                        # زر التحميل المباشر (كحلي نيلي)
                        st.download_button(
                            label="📥 اضغط هنا للتحميل المباشر 📁",
                            data=video_file,
                            file_name=f"ayman_video_{datetime.now().strftime('%H%M%S')}.mp4",
                            mime="video/mp4"
                        )
                        
                except Exception as e:
                    st.error("❌ فشل الاستخراج. تأكد أن الرابط عام وليس خاصاً.")
    st.markdown('</div>', unsafe_allow_html=True)
