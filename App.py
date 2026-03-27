import streamlit as st
import yt_dlp
import os

# --- 1. التصميم الملكي (الكحلي النيلي) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px;
    }

    div.stButton > button {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; 
        border: none !important; transition: 0.3s;
    }
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الواجهة ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة التحميل الداخلي المباشر v170.0</p></div>', unsafe_allow_html=True)

v_url = st.text_input("أدخل رابط الفيديو (Facebook, TikTok, YT):", placeholder="https://...")

if st.button("🚀 استخراج وتحميل مباشر"):
    if v_url:
        with st.spinner("جاري كسر الحماية والتحميل إلى موقعك..."):
            try:
                # إعدادات التمويه لتجاوز خطأ 403
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': 'ayman_download.%(ext)s',
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'noplaylist': True,
                    'quiet': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(v_url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                st.success("✅ تم التحميل بنجاح داخل موقعك!")
                
                # عرض الفيديو داخل موقعك
                with open(filename, "rb") as file:
                    st.video(file.read())
                    
                    # زر التحميل النهائي من موقعك مباشرة
                    st.download_button(
                        label="📥 حفظ الفيديو في جهازك الآن",
                        data=file,
                        file_name=filename,
                        mime="video/mp4"
                    )
                
                # تنظيف الملفات المؤقتة من السيرفر
                os.remove(filename)

            except Exception as e:
                st.error("🚨 الجدار الناري للمنصة قوي جداً على هذا السيرفر.")
                st.info("💡 نصيحة: إذا استمر الخطأ، فالمشكلة في 'آي بي' السيرفر المجاني، والحل هو استضافة مدفوعة أو تغيير الموقع.")
