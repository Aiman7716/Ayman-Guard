import streamlit as st
import yt_dlp
import requests
import io
from datetime import datetime

# --- 1. التصميم البصري (توحيد الهوية بالكحلي النيلي) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d;
    }

    /* توحيد الأزرار للون الكحلي النيلي الواضح جداً كما طلبت */
    div.stButton > button, div.stDownloadButton > button {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.8em !important; font-weight: bold !important; 
        border: none !important; font-size: 1.1rem !important;
    }
    
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الهيكل الرئيسي ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>Ayman Guard Ultimate v50.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🎬 محمل الفيديو الذكي", "🔍 فحص الروابط", "📧 تواصل معنا"])

# --- التبويب: محمل الفيديو (الحل النهائي) ---
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج وتحميل الوسائط")
    v_url = st.text_input("ألصق رابط الفيديو (TikTok, FB, YouTube) هنا:")
    
    if st.button("بدء المعالجة والاستخراج"):
        if v_url:
            with st.spinner("جاري استخراج البيانات وضمان استقرار الملف..."):
                try:
                    # إعدادات قوية لجلب الفيديو بأفضل جودة وتجاوز حظر المتصفحات
                    ydl_opts = {
                        'format': 'best',
                        'quiet': True,
                        'no_warnings': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        video_direct_url = info['url']
                        
                        # عرض الفيديو للمعاينة
                        st.video(video_direct_url)
                        st.success(f"✅ تم العثور على: {info.get('title', 'فيديو')[:40]}...")

                        # --- الحل التقني لمشكلة الجوال الثاني ---
                        # نقوم بطلب الفيديو عبر السيرفر لإرساله للجوال كملف جاهز وليس كرابط
                        headers = {'User-Agent': 'Mozilla/5.0'}
                        video_response = requests.get(video_direct_url, headers=headers, stream=True)
                        
                        # تحويل الرد إلى ملف في الذاكرة
                        video_bytes = io.BytesIO()
                        for chunk in video_response.iter_content(chunk_size=1024*1024):
                            if chunk:
                                video_bytes.write(chunk)
                        video_bytes.seek(0)

                        # زر التحميل "الكحلي" الذي يرسل الملف كاملاً للجوال مباشرة
                        st.download_button(
                            label="📥 تحميل الفيديو MP4 (كحلي واضح)",
                            data=video_bytes,
                            file_name=f"ayman_video_{datetime.now().strftime('%H%M%S')}.mp4",
                            mime="video/mp4"
                        )
                        
                except Exception as e:
                    st.error("❌ فشل التحميل: الموقع المضيف يمنع الوصول المباشر حالياً، جرب رابطاً آخر.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويبات الأخرى ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.text_input("ضع الرابط للفحص أمنياً:")
    st.button("بدء فحص الدرع")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.text_input("الاسم:")
    st.text_area("الرسالة:")
    st.button("إرسال الرسالة")
    st.markdown('</div>', unsafe_allow_html=True)
