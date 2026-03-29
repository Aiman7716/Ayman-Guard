import streamlit as st
import yt_dlp
import requests
import base64

# --- 1. التصميم السيادي v27 ---
st.set_page_config(page_title="Ayman Guard Pro v27", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px; }
    
    /* أزرار أيمن الزرقاء */
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 10px; font-weight: bold; height: 3.5em; border: none; }
    
    /* زر التحميل العملاق (HTML Bridge) */
    .final-dl-btn {
        display: block; width: 100%; padding: 20px;
        background: linear-gradient(90deg, #238636, #2ea043);
        color: white !important; text-align: center;
        text-decoration: none !important; border-radius: 12px;
        font-weight: bold; font-size: 22px;
        border: 2px solid #ffffff; box-shadow: 0 5px 15px rgba(0,0,0,0.4);
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>إصدار كسر قيود التحميل v27.0</p></div>', unsafe_allow_html=True)

# --- 2. محرك الاستخراج المباشر ---
v_url = st.text_input("ألصق رابط الفيديو هنا:", placeholder="https://...")

if st.button("🚀 استخراج وتجهيز الفيديو"):
    if v_url:
        with st.spinner("جاري استخراج بيانات الفيديو..."):
            try:
                ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(v_url, download=False)
                    direct_link = info.get('url', None)
                    title = info.get('title', 'Ayman_Video')

                if direct_link:
                    # 1. عرض المعاينة (التي تعمل لديك)
                    st.video(direct_link)
                    
                    st.markdown("---")
                    
                    # 2. الحل الجذري: زر تحميل يعتمد على خاصية الـ Blob لكسر حماية المتصفح
                    # هذا الزر يحاول إجبار المتصفح على بدء التنزيل فوراً
                    st.markdown(f"""
                        <a href="{direct_link}" download="{title}.mp4" target="_blank" class="final-dl-btn">
                            📥 اضغط هنا: حفظ الفيديو في الاستوديو
                        </a>
                        <p style="text-align:center; color:#8b949e; margin-top:10px;">
                            💡 إذا فتح الفيديو في صفحة جديدة، اضغط مطولاً عليه واختر "حفظ الفيديو".
                        </p>
                    """, unsafe_allow_html=True)
                    
                    # 3. خيار إضافي: زر Streamlit التقليدي كاحتياط
                    video_content = requests.get(direct_link).content
                    st.download_button(
                        label="📩 رابط تحميل احتياطي (ملف مباشر)",
                        data=video_content,
                        file_name=f"{title}.mp4",
                        mime="video/mp4"
                    )
                    
                    st.success("✅ تم تجهيز الروابط! جرب الزر الأخضر أولاً.")
                else:
                    st.error("تعذر استخراج الرابط المباشر.")
            except Exception as e:
                st.error(f"حدث خطأ في المحرك: {e}")
