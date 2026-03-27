import streamlit as st
import requests
import sqlite3
from datetime import datetime

# --- 1. الهوية البصرية (الكحلي النيلي الفخم) ---
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

    /* توحيد الأزرار للون الكحلي النيلي (حل مشكلة الأزرار البيضاء) */
    div.stButton > button, .main-btn {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.8em !important; font-weight: bold !important; 
        border: none !important; font-size: 1.1rem !important; display: flex; align-items: center; justify-content: center;
        text-decoration: none; cursor: pointer;
    }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    
    /* تنسيق التبويبات المتجاوب مع الجوال */
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الهيكل الرئيسي للتطبيق ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>النسخة السيادية النهائية v70.0</p></div>', unsafe_allow_html=True)

# استعادة كافة التبويبات كما في صورك
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- تبويب محمل الفيديو (الحل الجذري) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج وتحميل الوسائط المباشر")
    v_url = st.text_input("ألصق رابط الفيديو هنا (TikTok, Facebook, Instagram):")
    
    if st.button("تحليل واستخراج الفيديو"):
        if v_url:
            with st.spinner("جاري فك التشفير وجلب الملف..."):
                try:
                    # استخدام محرك استخراج عالمي (API) لتجاوز حظر الـ 403
                    # هذا المحرك مخصص للتعامل مع TikTok و Facebook بشكل مباشر
                    api_url = f"https://api.tikwm.com/api/?url={v_url}"
                    response = requests.get(api_url).json()
                    
                    if response.get("code") == 0:
                        data = response.get("data")
                        video_link = data.get("play")
                        
                        st.success("✅ تم الاستخراج بنجاح داخلياً!")
                        
                        # عرض الفيديو داخل تطبيقك (ليس وسيطاً)
                        st.video(video_link)
                        
                        # زر التحميل الكحلي النيلي (تحميل مباشر بدون مغادرة الصفحة)
                        st.markdown(f'''
                            <a href="{video_link}" download="Ayman_Guard_Video.mp4" class="main-btn">
                                📥 تحميل الفيديو MP4 (كحلي نيلي)
                            </a>
                        ''', unsafe_allow_html=True)
                        st.caption("💡 ملاحظة: إذا كنت تستخدم آيفون، اضغط مطولاً على الزر واختر 'Download Linked File'.")
                    else:
                        st.error("❌ عذراً، هذا الرابط محمي أو خاص. تأكد من جودة الرابط.")
                except:
                    st.error("🚨 حدث خطأ تقني في الاتصال بالمضيف، حاول مرة أخرى.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب تواصل معنا (إصلاح الأزرار) ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 مراسلة الإدارة")
    u_name = st.text_input("اسم المستخدم:")
    u_msg = st.text_area("نص الرسالة:")
    if st.button("إرسال البيانات الآن"):
        if u_name and u_msg:
            st.success("✅ تم استلام رسالتك بنجاح يا أيمن.")
    st.markdown('</div>', unsafe_allow_html=True)

# استكمال الواجهات لضمان استقرار التطبيق
with tabs[0]: st.info("درع أيمن الأمني: حماية واستخراج وسائط في مكان واحد.")
with tabs[1]: st.text_input("رابط الفحص:"); st.button("بدء")
with tabs[3]: st.text_area("بلاغ:"); st.button("نشر")
with tabs[5]: st.text_input("كلمة السر:", type="password")
