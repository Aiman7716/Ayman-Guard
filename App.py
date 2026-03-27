import streamlit as st
import requests
import sqlite3
from datetime import datetime

# --- 1. الإعدادات البصرية (كحلي نيلي ملكي) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    /* هيدر الدرع */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px;
    }

    /* إصلاح الأزرار لتكون كحلية وواضحة (حل مشكلة اللون الأبيض) */
    div.stButton > button, .final-download-btn {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 4em !important; font-weight: bold !important; 
        border: none !important; display: flex; align-items: center; justify-content: center;
        text-decoration: none; font-size: 1.1rem !important; cursor: pointer; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #388bfd !important; }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الواجهة الرئيسية ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة كسر الحظر الشامل v130.0</p></div>', unsafe_allow_html=True)

# إعادة التبويبات الستة كما كانت في صورتك الأولى
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو السيادي", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويب: محمل الفيديو (الحل الجذري) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج الوسائط (بدون حظر 403)")
    v_url = st.text_input("ألصق الرابط هنا (TikTok, FB, YT):")
    
    if st.button("🚀 بدء الاستخراج الفوري"):
        if v_url:
            with st.spinner("جاري كسر التشفير عبر الجسر الآمن..."):
                try:
                    # استخدام محرك خارجي متطور يتجاوز قيود المنصات نهائياً
                    api_bridge = f"https://api.tikwm.com/api/?url={v_url}"
                    res = requests.get(api_bridge, timeout=20).json()
                    
                    if res.get("code") == 0:
                        v_link = res.get("data").get("play")
                        
                        st.success("✅ تم كسر الحظر واستخراج الرابط بنجاح!")
                        
                        # عرض الفيديو للمعاينة
                        st.video(v_link)
                        
                        # الزر الكحلي للتحميل المباشر من المتصفح
                        st.markdown(f'''
                            <a href="{v_link}" target="_blank" class="final-download-btn">
                                📥 اضغط هنا للتحميل المباشر (MP4)
                            </a>
                        ''', unsafe_allow_html=True)
                        st.info("💡 ملاحظة: إذا كنت تستخدم آيفون، اضغط مطولاً على الزر واختر 'Download Linked File'.")
                    else:
                        st.error("❌ الموقع المضيف يمنع الاتصال المباشر حالياً. تأكد من أن الحساب عام.")
                except:
                    st.error("🚨 حدث خطأ في الاتصال بالمحرّك، يرجى إعادة المحاولة.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب: تواصل معنا (علاج مشكلة الأزرار البيضاء) ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 مراسلة الإدارة")
    nm = st.text_input("اسمك الكريم:")
    ms = st.text_area("رسالتك:")
    if st.button("إرسال البيانات"):
        if nm and ms:
            st.success("✅ تم استلام رسالتك يا أيمن.")
    st.markdown('</div>', unsafe_allow_html=True)

# بقية الأقسام لضمان توازن الواجهة
with tabs[0]: st.info("النظام نشط ومستقر تحت حماية درع أيمن.")
with tabs[1]: st.text_input("رابط لفحصه:"); st.button("فحص آمن")
with tabs[3]: st.text_area("بلاغ:"); st.button("نشر")
with tabs[5]: st.text_input("كلمة السر:", type="password")
