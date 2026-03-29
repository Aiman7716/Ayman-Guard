import streamlit as st
import yt_dlp
import requests

# --- 1. التصميم الجمالي السيادي ---
st.set_page_config(page_title="Ayman Guard Pro v26", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 15px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px; }
    
    /* أزرار أيمن الزرقاء */
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 10px; font-weight: bold; height: 3.5em; border: none; }
    
    /* زر الحفظ الأخضر (المطور برمجياً) */
    .stDownloadButton > button { 
        background-color: #238636 !important; 
        height: 4.5em !important; 
        font-size: 22px !important; 
        font-weight: bold !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>حل مشكلة زر التحميل v26.0</p></div>', unsafe_allow_html=True)

# --- 2. المحرك (نظام الاستخراج المزدوج) ---
t = st.tabs(["🎬 محمل الفيديو", "🏠 الرئيسية"])

with t[0]:
    st.subheader("🎬 مركز التحميل المستقر")
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    
    if st.button("🚀 تجهيز الفيديو"):
        if v_url:
            with st.spinner("جاري استخراج الرابط المباشر..."):
                try:
                    # إعدادات المحرك لجلب الرابط المباشر
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
                        # 1. عرض المعاينة (التي عملت معك بنجاح)
                        st.video(direct_url)
                        
                        st.markdown("---")
                        
                        # 2. حل مشكلة التحميل: نستخدم تقنية "التحميل اليدوي الآمن"
                        # نقوم بتحميل جزء صغير من البيانات للتأكد من الرابط
                        try:
                            video_response = requests.get(direct_url, stream=True, timeout=10)
                            
                            # نستخدم الزر البرمجي ولكن مع إرسال البيانات بشكل مباشر لضمان الاستجابة
                            st.download_button(
                                label="📥 اضغط هنا لحفظ الفيديو فوراً",
                                data=video_response.content,
                                file_name=f"{v_title}.mp4",
                                mime="video/mp4"
                            )
                            st.success("✅ تم التجهيز! إذا ضغطت ولم يحفظ، استخدم الزر البديل بالأسفل:")
                            
                            # زر احتياطي (رابط مباشر) إذا فشل زر Streamlit
                            st.markdown(f'''
                                <a href="{direct_url}" download="{v_title}.mp4" target="_blank" 
                                style="display: block; width: 100%; padding: 15px; background-color: #8b949e; 
                                color: white; text-align: center; border-radius: 10px; text-decoration: none; 
                                font-weight: bold; margin-top: 10px;">
                                🔗 رابط تحميل احتياطي (اضغط مطولاً ثم حفظ)
                                </a>
                            ''', unsafe_allow_html=True)
                            
                        except:
                            st.error("السيرفر بطيء جداً، جرب الرابط الاحتياطي:")
                            st.markdown(f'<a href="{direct_url}" target="_blank">📥 تحميل مباشر</a>', unsafe_allow_html=True)

                    else:
                        st.error("فشل استخراج الرابط.")
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")

with t[1]:
    st.write("يا **أيمن**، هذا الإصدار يجمع بين المعاينة الشغالة وبين زر تحميل 'مزدوج' لضمان الحفظ مهما كانت قيود المتصفح.")
