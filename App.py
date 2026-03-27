import streamlit as st
import requests
import sqlite3
from datetime import datetime

# --- 1. الإعدادات والربط ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

# --- 2. التصميم البصري (كحلي نيلي فخم) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 10px;
    }

    /* توحيد الأزرار للون الكحلي النيلي الواضح */
    div.stButton > button, .download-link {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.8em !important; font-weight: bold !important; 
        border: none !important; display: flex; align-items: center; justify-content: center;
        text-decoration: none; font-size: 1.1rem;
    }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. الهيكل الرئيسي ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة التحميل المباشر v52.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🎬 محمل الفيديو", "🔍 الفحص", "👥 المجتمع", "📧 تواصل", "🔐 الإدارة"])

# --- التبويب: محمل الفيديو (الحل الذي يتجاوز خطأ 403) ---
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج الوسائط (بدون حظر)")
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    
    if st.button("استخراج الفيديو الآن"):
        if v_url:
            with st.spinner("جاري كسر الحماية وجلب الملف..."):
                try:
                    # استخدام API خارجي مجاني ومستقر لتجاوز حظر TikTok/FB
                    api_url = f"https://api.douyin.wtf/api?url={v_url}"
                    response = requests.get(api_url).json()
                    
                    if response.get("status") == "success" or "url" in str(response):
                        # محاولة جلب الرابط المباشر من الاستجابة
                        download_url = response.get("url") or response.get("video_data", {}).get("nwm_video_url_HQ")
                        
                        if download_url:
                            st.success("✅ تم كسر الحماية بنجاح!")
                            # عرض الفيديو
                            st.video(download_url)
                            
                            # الزر الكحلي النيلي (التحميل المباشر)
                            st.markdown(f'''
                                <a href="{download_url}" target="_blank" class="download-link">
                                    📥 اضغط هنا لتحميل الفيديو MP4 (كحلي)
                                </a>
                            ''', unsafe_allow_html=True)
                            st.info("💡 إذا لم يبدأ التحميل تلقائياً، اضغط مطولاً على الفيديو واختر 'تنزيل'.")
                        else:
                            st.error("❌ لم نتمكن من العثور على رابط مباشر، جرب رابطاً آخر.")
                    else:
                        # حل احتياطي إذا فشل الـ API
                        st.warning("⚠️ جاري المحاولة بالطريقة الاحتياطية...")
                        st.markdown(f'<a href="https://savefrom.net/?url={v_url}" target="_blank" class="download-link">تحميل عبر السيرفر الاحتياطي</a>', unsafe_allow_html=True)
                except:
                    st.error("❌ عذراً، هذا الموقع يفرض حماية مشددة حالياً.")
    st.markdown('</div>', unsafe_allow_html=True)

# بقية التبويبات (برمجة سريعة لضمان بقائها)
with tabs[1]: st.text_input("رابط الفحص:"); st.button("بدء")
with tabs[2]: st.text_area("بلاغ جديد:"); st.button("نشر")
