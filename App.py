import streamlit as st
import yt_dlp
import requests
import base64

# --- 1. التنسيق السيادي الرسمي ---
st.set_page_config(page_title="Ayman Guard Pro v30", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    .hero { 
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); 
        padding: 25px; border-radius: 15px; text-align: center; 
        border: 1px solid #30363d; margin-bottom: 20px; 
    }
    
    /* أزرار النظام الرسمية */
    div.stButton > button { 
        width: 100% !important; background: #1f6feb !important; 
        color: white !important; border-radius: 10px; 
        font-weight: bold; height: 3.5em; border: none; 
    }
    
    /* زر الحفظ الداخلي المستقر */
    .stDownloadButton > button {
        background-color: #238636 !important;
        color: white !important;
        width: 100% !important;
        height: 4.5em !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>نظام التحميل الداخلي v30.0</p></div>', unsafe_allow_html=True)

# --- 2. محرك المعالجة والتحميل الداخلي ---
v_url = st.text_input("يرجى إدخال رابط الوسائط هنا:")

if st.button("🚀 بدء المعالجة الرسمية"):
    if v_url:
        with st.spinner("جاري فحص وتجهيز البيانات، يرجى الانتظار..."):
            try:
                # إعدادات المحرك لاستخراج الرابط
                ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(v_url, download=False)
                    direct_link = info.get('url', None)
                    title = info.get('title', 'Ayman_Video')

                if direct_link:
                    # عرض المعاينة (تعمل داخلياً)
                    st.video(direct_link)
                    
                    st.markdown("---")
                    
                    # جلب الفيديو لذاكرة البرنامج مباشرة لتجنب الخروج للمتصفح
                    video_response = requests.get(direct_link)
                    video_bytes = video_response.content
                    
                    # زر التحميل الرسمي المدمج (لا يخرج من التطبيق)
                    st.download_button(
                        label="📥 حفظ الفيديو في الاستوديو",
                        data=video_bytes,
                        file_name=f"{title}.mp4",
                        mime="video/mp4"
                    )
                    
                    st.success("✅ تمت المعالجة. اضغط على الزر الأخضر للحفظ مباشرة.")
                    
                else:
                    st.error("فشل النظام في استخراج البيانات.")
            except Exception as e:
                st.error(f"تنبيه رسمي: حدث خطأ أثناء المعالجة ({e})")
