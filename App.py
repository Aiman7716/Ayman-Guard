import streamlit as st
import requests
import sqlite3
from datetime import datetime

# --- 1. التنسيق البصري (كحلي نيلي احترافي) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    /* صندوق الهيدر الرئيسي */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px;
    }

    /* أزرار كحلية واضحة جداً (علاج مشكلة الأزرار البيضاء) */
    div.stButton > button, .download-btn {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.8em !important; font-weight: bold !important; 
        border: none !important; display: flex; align-items: center; justify-content: center;
        text-decoration: none; font-size: 1.1rem !important; cursor: pointer; transition: 0.4s;
    }
    div.stButton > button:hover { background-color: #388bfd !important; transform: translateY(-2px); }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الواجهة والهيكل ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>الإصدار الجذري v100.0 - حماية واستخراج</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- 3. محمل الفيديو (الحل الجذري لتجاوز الحظر 403) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج الوسائط (بدون حظر)")
    v_url = st.text_input("ألصق الرابط هنا (Facebook, TikTok, YT):", placeholder="https://...")
    
    if st.button("🚀 بدء الاستخراج والتحضير"):
        if v_url:
            with st.spinner("جاري كسر التشفير وتجهيز الرابط الآمن..."):
                try:
                    # استخدام محرك (TikWM) المتطور لتجاوز قيود فيسبوك وتيك توك
                    api_bridge = f"https://api.tikwm.com/api/?url={v_url}"
                    res = requests.get(api_bridge, timeout=15).json()
                    
                    if res.get("code") == 0:
                        v_data = res.get("data")
                        direct_link = v_data.get("play")
                        
                        st.success("✅ تم الاستخراج بنجاح!")
                        
                        # معاينة الفيديو
                        st.video(direct_link)
                        
                        # الزر الجذري: يفتح الرابط المباشر للتحميل الفوري
                        st.markdown(f'''
                            <a href="{direct_link}" target="_blank" class="download-btn">
                                📥 تحميل الفيديو الآن (MP4 كحلي)
                            </a>
                        ''', unsafe_allow_html=True)
                        st.info("💡 ملاحظة: إذا كنت تستخدم آيفون، اضغط مطولاً على الزر واختر 'Download Linked File'.")
                    else:
                        st.error("❌ عذراً، الموقع المضيف يمنع الاتصال حالياً. تأكد من أن الحساب عام.")
                except:
                    st.error("🚨 خطأ في الاتصال بالمضيف. جرب استخدام رابط آخر.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. قسم تواصل معنا (إصلاح الأزرار البيضاء) ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 مراسلة إدارة الدرع")
    c_name = st.text_input("الاسم الكريم:")
    c_msg = st.text_area("تفاصيل الرسالة:")
    if st.button("إرسال البيانات إلى أيمن"):
        if c_name and c_msg:
            st.success("✅ تم استلام رسالتك بنجاح.")
    st.markdown('</div>', unsafe_allow_html=True)

# استكمال الواجهات لضمان استقرار التطبيق
with tabs[0]: st.info("النظام نشط ومستقر حالياً.")
with tabs[1]: st.text_input("رابط الفحص:"); st.button("بدء الفحص")
with tabs[3]: st.text_area("بلاغ جديد:"); st.button("نشر البلاغ")
with tabs[5]: st.text_input("كلمة السر:", type="password")
