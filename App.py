import streamlit as st
import sqlite3
import requests
from datetime import datetime

# --- 1. إعدادات التصميم (إعادة الهوية الكحلية الكاملة) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    /* الهيدر الاحترافي */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px;
    }

    /* توحيد الأزرار لتكون كحلية نيليّة داخل التطبيق دائماً */
    div.stButton > button, div.stDownloadButton > button {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.8em !important; font-weight: bold !important; 
        border: none !important; font-size: 1.1rem !important; cursor: pointer;
    }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الهيكل الرئيسي ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>النسخة المستقلة v55.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- 3. تبويب المحمل (الحل المستقل داخل التطبيق) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج الوسائط المباشر")
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    
    if st.button("تحليل واستخراج الفيديو"):
        if v_url:
            with st.spinner("جاري المعالجة داخل الدرع..."):
                try:
                    # استخدام API صامت (بدون إعادة توجيه) لجلب البيانات الخام
                    # سنستخدم سيرفر وسيط "صامت" لجلب الفيديو كمقطع بيانات
                    api_endpoint = f"https://api.tikwm.com/api/?url={v_url}"
                    res = requests.get(api_endpoint).json()
                    
                    if res.get("code") == 0:
                        video_data = res.get("data")
                        video_url = video_data.get("play")
                        
                        # عرض الفيديو داخل تطبيقك (ليس وسيطاً)
                        st.video(video_url)
                        st.success("✅ تم الاستخراج بنجاح داخلياً.")

                        # جلب الفيديو كملف لتحميله مباشرة من سيرفرك
                        v_content = requests.get(video_url).content
                        
                        # زر تحميل داخلي (Download Button) لا يخرج من الصفحة
                        st.download_button(
                            label="📥 تحميل الفيديو الآن (كحلي)",
                            data=v_content,
                            file_name=f"ayman_guard_{datetime.now().strftime('%M%S')}.mp4",
                            mime="video/mp4"
                        )
                    else:
                        st.error("❌ تعذر الاستخراج المباشر. تأكد من أن الرابط عام وليس خاصاً.")
                except Exception as e:
                    st.error("🚨 عذراً، الموقع المضيف يرفض الاتصال حالياً.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. تبويب تواصل معنا (تصحيح الأزرار كما في الصورة) ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 مراسلة الإدارة")
    name = st.text_input("الاسم:")
    msg = st.text_area("الرسالة:")
    # الزر هنا سيظهر كحلياً كما في التصميم الأصلي
    if st.button("إرسال الآن"):
        if name and msg:
            st.success(f"شكراً لك يا {name}، تم استلام رسالتك.")
    st.markdown('</div>', unsafe_allow_html=True)

# بقية التبويبات للحفاظ على شكل التطبيق
with tabs[0]: st.info("النظام يعمل بكفاءة.")
with tabs[1]: st.text_input("فحص الروابط:"); st.button("بدء الفحص")
with tabs[3]: st.text_area("بلاغات:"); st.button("نشر")
with tabs[5]: st.text_input("كلمة السر:", type="password")
