import streamlit as st
import yt_dlp
import requests
import io

# --- 1. التصميم الجمالي السيادي (تنسيق أيمن المعتمد) ---
st.set_page_config(page_title="Ayman Guard Ultra v24", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 15px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px; }
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 10px; font-weight: bold; height: 3.5em; border: none; }
    /* زر الحفظ الأخضر العملاق */
    .stDownloadButton > button { background-color: #238636 !important; height: 4em !important; font-size: 18px !important; border: 2px solid #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>إصدار إصلاح المعاينة v24.0</p></div>', unsafe_allow_html=True)

# --- 2. محرك التحميل الذكي (بدون ملفات مؤقتة) ---
t = st.tabs(["🎬 محمل الفيديو", "🏠 الرئيسية"])

with t[0]:
    st.subheader("🎬 مركز استخراج الوسائط")
    v_url = st.text_input("أدخل رابط الفيديو (Facebook, YouTube, etc):")
    
    if st.button("🚀 تجهيز الفيديو للتحميل"):
        if v_url:
            with st.spinner("جاري كسر الحماية وجلب البيانات..."):
                try:
                    # إعدادات المحرك لجلب الرابط المباشر فقط
                    ydl_opts = {
                        'format': 'best',
                        'quiet': True,
                        'no_warnings': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        direct_url = info.get('url', None)
                        title = info.get('title', 'ayman_video')

                    if direct_url:
                        # حل مشكلة المعاينة: نرسل الرابط المباشر للمشغل
                        st.video(direct_url)
                        
                        # حل مشكلة زر الحفظ: نقوم بتحميل الفيديو للذاكرة أولاً
                        video_data = requests.get(direct_url).content
                        
                        st.download_button(
                            label="📥 اضغط هنا لحفظ الفيديو فوراً",
                            data=video_data,
                            file_name=f"{title}.mp4",
                            mime="video/mp4"
                        )
                        st.success("✅ تم تجهيز الملف بنجاح! اضغط على الزر الأخضر أعلاه.")
                    else:
                        st.error("لم نتمكن من العثور على رابط مباشر.")
                except Exception as e:
                    st.error(f"حدث خطأ في المحرك: {e}")
                    st.info("💡 جرب فتح التطبيق في متصفح Chrome للحصول على أفضل النتائج.")

with t[1]:
    st.write(f"مرحباً بك يا **أيمن**. هذا الإصدار يعالج مشكلة المعاينة عبر جلب البيانات مباشرة للذاكرة.")
