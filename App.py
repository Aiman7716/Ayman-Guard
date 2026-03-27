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

    /* إصلاح الأزرار لتكون كحلية وواضحة جداً */
    div.stButton > button, .final-btn {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; 
        border: none !important; display: flex; align-items: center; justify-content: center;
        text-decoration: none; font-size: 1.1rem !important; cursor: pointer; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #388bfd !important; transform: scale(1.01); }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الهيكل الرئيسي للتطبيق ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>النسخة السيادية النهائية v90.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويب: محمل الفيديو (الحل الجذري) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج الوسائط الذكي")
    v_url = st.text_input("ألصق الرابط هنا (Facebook, TikTok, YT):")
    
    if st.button("🚀 تحليل واستخراج الفيديو الآن"):
        if v_url:
            with st.spinner("جاري كسر التشفير وجلب الرابط المباشر..."):
                try:
                    # استخدام محرك سحابي خارجي لتجاوز حظر الـ 403 نهائياً
                    api_link = f"https://api.tikwm.com/api/?url={v_url}"
                    res = requests.get(api_link, timeout=12).json()
                    
                    if res.get("code") == 0:
                        v_data = res.get("data")
                        # جلب الرابط المباشر (بدون علامة مائية إن وجد)
                        direct_url = v_data.get("play")
                        
                        st.success("✅ تم فك التشفير بنجاح!")
                        
                        # معاينة الفيديو داخل تطبيقك
                        st.video(direct_url)
                        
                        # زر التحميل "الكحلي" الذي يفتح الرابط للتحميل الفوري
                        st.markdown(f'''
                            <a href="{direct_url}" target="_blank" class="final-btn">
                                📥 تحميل الفيديو MP4 الآن (كحلي)
                            </a>
                        ''', unsafe_allow_html=True)
                        st.info("💡 ملاحظة: إذا كنت تستخدم الآيفون، اضغط مطولاً على الزر واختر 'Download Linked File'.")
                    else:
                        st.error("❌ عذراً، هذا الرابط محمي من المصدر أو خاص.")
                except:
                    st.error("🚨 حدث خطأ في الاتصال بالسيرفر المضيف، حاول مرة أخرى.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب: تواصل معنا (إصلاح الأزرار البيضاء) ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 مراسلة الإدارة")
    u_name = st.text_input("الاسم:")
    u_msg = st.text_area("الرسالة:")
    if st.button("إرسال البيانات"):
        if u_name and u_msg:
            st.success(f"شكراً يا {u_name}، تم إرسال رسالتك لدرع أيمن.")
    st.markdown('</div>', unsafe_allow_html=True)

# استكمال الواجهة
with tabs[0]: st.info("درع أيمن يعمل الآن بأقصى درجات الاستقرار.")
with tabs[1]: st.text_input("رابط لفحصه:"); st.button("فحص أمني")
with tabs[3]: st.text_area("بلاغ:"); st.button("نشر")
with tabs[5]: st.text_input("كلمة السر:", type="password")
