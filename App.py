import streamlit as st
import yt_dlp
import requests

# --- 1. التنسيق السيادي الرسمي (UI) ---
st.set_page_config(page_title="Ayman Guard Pro v29", layout="wide")
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
    
    /* زر الحفظ الرسمي الفخم */
    .save-btn {
        display: block; width: 100%; padding: 18px;
        background: #238636; color: white !important;
        text-align: center; text-decoration: none !important;
        border-radius: 12px; font-weight: bold; font-size: 20px;
        border: 1px solid #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>نظام المعالجة الرسمي v29.0</p></div>', unsafe_allow_html=True)

# --- 2. محرك المعالجة الرسمي ---
v_url = st.text_input("يرجى إدخال رابط الوسائط هنا:")

if st.button("🚀 بدء المعالجة الرسمية"):
    if v_url:
        # الرسالة الرسمية المطلوبة أثناء الجلب
        with st.spinner("جاري فحص وتجهيز البيانات، يرجى الانتظار..."):
            try:
                # إعدادات المحرك لاستخراج الرابط
                ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(v_url, download=False)
                    direct_link = info.get('url', None)
                    title = info.get('title', 'Video_File')

                if direct_link:
                    # عرض المعاينة
                    st.video(direct_link)
                    
                    st.markdown("---")
                    
                    # الزر بالمسمى الرسمي الجديد (حفظ الفيديو في الاستوديو)
                    # مع خاصية الفتح في متصفح خارجي لضمان التحميل في "الموقع المثبت"
                    st.markdown(f"""
                        <a href="{direct_link}" download="{title}.mp4" target="_blank" rel="noopener noreferrer" class="save-btn">
                            📥 حفظ الفيديو في الاستوديو
                        </a>
                        <p style="text-align:center; color:#8b949e; margin-top:10px;">
                            نظام الدرع: تم استخراج الرابط بنجاح، يرجى الضغط للحفظ.
                        </p>
                    """, unsafe_allow_html=True)
                    
                    st.success("✅ تمت معالجة الرابط بنجاح.")
                else:
                    st.error("فشل النظام في استخراج البيانات، تأكد من صحة الرابط.")
            except Exception as e:
                st.error(f"تنبيه رسمي: حدث خطأ أثناء المعالجة ({e})")
