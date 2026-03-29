import streamlit as st
import yt_dlp
import requests
import io

# --- 1. التنسيق السيادي (UI) ---
st.set_page_config(page_title="Ayman Guard Pro v25", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 15px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px; }
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 10px; font-weight: bold; height: 3.5em; border: none; }
    /* زر الحفظ الأخضر السيادي */
    .stDownloadButton > button { background-color: #238636 !important; height: 4.5em !important; font-size: 20px !important; border: 2px solid #ffffff !important; box-shadow: 0 4px 15px rgba(0,0,0,0.4); }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>إصدار المعالجة المباشرة v25.0</p></div>', unsafe_allow_html=True)

# --- 2. المحرك (معالجة البيانات في الذاكرة) ---
t = st.tabs(["🎬 محمل الفيديو", "🏠 الرئيسية"])

with t[0]:
    st.subheader("🎬 مركز التحميل المباشر")
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    
    if st.button("🚀 تجهيز الفيديو"):
        if v_url:
            with st.spinner("جاري استخراج البيانات وفك التشفير..."):
                try:
                    # إعدادات المحرك لاستخراج الرابط المباشر فقط
                    ydl_opts = {
                        'format': 'best',
                        'quiet': True,
                        'no_warnings': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        direct_url = info.get('url', None)
                        v_title = info.get('title', 'Ayman_Shield_Video')

                    if direct_url:
                        # الحل الجذري للمعاينة: جلب الفيديو كبيانات ثنائية
                        # لضمان ظهوره في المشغل وتفعيل زر التحميل
                        resp = requests.get(direct_url, stream=True)
                        video_bytes = resp.content # تحميل البيانات للذاكرة
                        
                        # عرض الفيديو من الذاكرة (لحل مشكلة الشاشة السوداء)
                        st.video(video_bytes)
                        
                        st.markdown("---")
                        
                        # تفعيل زر التحميل المباشر من الذاكرة
                        st.download_button(
                            label="📥 اضغط هنا لحفظ الفيديو فوراً",
                            data=video_bytes,
                            file_name=f"{v_title}.mp4",
                            mime="video/mp4"
                        )
                        st.success("✅ تم استخراج الفيديو بنجاح! جاهز للحفظ.")
                    else:
                        st.error("فشل استخراج الرابط المباشر.")
                except Exception as e:
                    st.error(f"حدث خطأ في المحرك: {e}")

with t[1]:
    st.write(f"يا **أيمن**، تم تحديث النظام ليعمل بنظام **'الضخ المباشر'**. هذا الكود يقرأ الفيديو كبيانات خام ويضعها في يدك مباشرة دون وسيط.")
