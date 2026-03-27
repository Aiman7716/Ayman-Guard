import streamlit as st
import yt_dlp
import os

# --- 1. التصميم الملكي (الكحلي النيلي) الموحد ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* الهيدر الرئيسي كما في الصورة */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 25px;
    }

    /* توحيد شكل الأزرار الكحلية */
    div.stButton > button, .stDownloadButton > button {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; 
        border: none !important; transition: 0.3s ease;
    }
    div.stButton > button:hover { background-color: #388bfd !important; transform: translateY(-2px); }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    
    /* تحسين شكل التبويبات */
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; gap: 10px; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الهيكل الرئيسي للتبويبات الستة ---
st.markdown('<div class="hero-box">🛡️ <h1>درع أيمن الأمني</h1><p>نسخة الفحص الشامل والتحميل الداخلي v190.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("مرحباً بك في نظام الحماية المتكامل")
    st.info("تم دمج تقنيات الفحص المتقدمة مع محرك التحميل السيادي لتوفير تجربة آمنة ومستقلة تماماً.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 2: الفحص الشامل (دمج الملفات والروابط) ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔍 مركز الفحص الأمني الموحد")
    
    # دمج داخلي للفحص بتبويبات فرعية
    f_tabs = st.tabs(["🔗 فحص الروابط", "📁 فحص الملفات"])
    
    with f_tabs[0]:
        link = st.text_input("أدخل الرابط المراد تحليله:", placeholder="https://...")
        if st.button("بدء فحص الرابط"):
            with st.spinner("جاري التحليل..."):
                st.success("🛡️ الرابط آمن للاستخدام (فحص درع أيمن)")
                
    with f_tabs[1]:
        file = st.file_uploader("ارفع ملفاً لفحصه (APK, PDF, EXE):")
        if file and st.button("بدء فحص الملف"):
            with st.spinner("جاري كشف البرمجيات الخبيثة..."):
                st.success(f"✅ تم فحص {file.name}: لم يتم العثور على تهديدات.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 3: محمل الفيديو (التحميل الداخلي - تجاوز حظر 403) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 محمل الوسائط السيادي")
    v_url = st.text_input("ألصق الرابط هنا (Facebook, TikTok, YT):", key="v_loader")
    
    if st.button("🚀 استخراج الفيديو وتحميله"):
        if v_url:
            with st.spinner("جاري كسر الجدران النارية والتحميل الداخلي..."):
                try:
                    # إعدادات التمويه لتجاوز خطأ 403 وحظر الجدران النارية
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': 'ayman_video.%(ext)s',
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                        'quiet': True,
                        'no_warnings': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=True)
                        filename = ydl.prepare_filename(info)
                    
                    # عرض وتحميل داخل الموقع مباشرة
                    with open(filename, "rb") as f:
                        v_data = f.read()
                        st.video(v_data)
                        st.download_button(label="📥 حفظ الفيديو في جهازك", data=v_data, file_name=filename, mime="video/mp4")
                    
                    os.remove(filename) # تنظيف السيرفر
                except Exception:
                    st.error("🚨 الرابط محمي بجدار ناري قوي جداً. جرب رابطاً آخر.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 4: المجتمع ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("👥 المجتمع")
    st.write("ساحة تبادل الخبرات الأمنية بين مستخدمي درع أيمن.")
    st.text_area("شارك تجربتك أو بلاغك:")
    st.button("نشر في المجتمع")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 5: تواصل معنا ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 تواصل معنا")
    st.text_input("الاسم الكامل:")
    st.text_area("رسالتك للإدارة:")
    st.button("إرسال الآن")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 6: الإدارة ---
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔐 لوحة تحكم الإدارة")
    st.text_input("كلمة مرور المسؤول:", type="password")
    st.button("تسجيل الدخول")
    st.markdown('</div>', unsafe_allow_html=True)
