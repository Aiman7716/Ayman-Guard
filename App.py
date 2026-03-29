import streamlit as st
import yt_dlp
import requests

# --- 1. التنسيق السيادي (UI) ---
st.set_page_config(page_title="Ayman Guard Pro v28", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px; }
    
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 10px; font-weight: bold; height: 3.5em; border: none; }
    
    /* زر التحميل الأخضر الذي يجبر المتصفح الخارجي على العمل */
    .external-dl-btn {
        display: block; width: 100%; padding: 18px;
        background: #238636; color: white !important;
        text-align: center; text-decoration: none !important;
        border-radius: 12px; font-weight: bold; font-size: 20px;
        border: 2px solid #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>إصدار ربط المتصفح الخارجي v28.0</p></div>', unsafe_allow_html=True)

# --- 2. محرك الاستخراج ---
v_url = st.text_input("ألصق رابط الفيديو هنا:")

if st.button("🚀 استخراج وتجهيز"):
    if v_url:
        with st.spinner("جاري كسر حماية الرابط..."):
            try:
                # استخراج الرابط المباشر
                ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(v_url, download=False)
                    direct_link = info.get('url', None)
                    title = info.get('title', 'ayman_video')

                if direct_link:
                    # عرض المعاينة (التي تعمل لديك بنجاح)
                    st.video(direct_link)
                    
                    st.markdown("---")
                    
                    # الحل الجذري: زر HTML يجبر الهاتف على الخروج من "الموقع المثبت" إلى "المتصفح"
                    # نستخدم target="_blank" و rel="noopener noreferrer" لضمان فتح صفحة جديدة في المتصفح الافتراضي
                    st.markdown(f"""
                        <a href="{direct_link}" download="{title}.mp4" target="_blank" rel="noopener noreferrer" class="external-dl-btn">
                            📥 اضغط هنا لبدء التحميل في المتصفح
                        </a>
                        <p style="text-align:center; color:#8b949e; margin-top:10px;">
                            💡 عند الضغط، سيقوم المتصفح الخارجي بتولي عملية الحفظ في الاستوديو.
                        </p>
                    """, unsafe_allow_html=True)
                    
                    st.success("✅ تم تجهيز الرابط المباشر للمتصفح.")
                else:
                    st.error("تعذر استخراج الرابط.")
            except Exception as e:
                st.error(f"خطأ في المحرك: {e}")
