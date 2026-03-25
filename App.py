import streamlit as st
import tldextract
import time

# إعدادات الصفحة
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# CSS لمنع التداخل تماماً وتنسيق الألوان
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .main-header { color: #00d4ff; text-align: center; font-size: 3rem; font-weight: bold; }
        .info-box { background-color: #e8f4fd; border-radius: 10px; padding: 15px; border-right: 5px solid #2196f3; color: #0d47a1; }
        div.stButton > button { 
            background-color: #ff4b4b !important; color: white !important; 
            border-radius: 12px !important; width: 100% !important; height: 3.5em !important; font-weight: bold !important; 
        }
        /* إخفاء الرموز البرمجية الغريبة */
        .st-emotion-cache-1kyx60p, .css-1kyx60p { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# العنوان
st.markdown('<div class="main-header">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>المنصة الذكية الأولى لحماية المجتمع من الاحتيال الرقمي</p>", unsafe_allow_html=True)

st.markdown("""<div class="info-box">💡 نصيحة درع أيمن: تأكد دائماً من وجود قفل الأمان (HTTPS) في الرابط.</div>""", unsafe_allow_html=True)

# منطقة الفحص
url_input = st.text_input("🔍 قم بلصق الرابط المشبوه هنا :", placeholder="https://example.com")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if url_input:
        with st.spinner('جاري التحقق...'):
            time.sleep(1)
            ext = tldextract.extract(url_input.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            trust = ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa', 'moe.gov.sa']
            
            if domain in trust:
                st.balloons()
                st.success(f"✅ آمن وموثوق: هذا موقع رسمي ({domain})")
            elif ext.suffix in ['tk', 'xyz', 'ml', 'cf', 'gq']:
                st.error("🚨 تحذير: هذا الرابط مشبوه جداً!")
            else:
                st.info(f"ℹ️ نتيجة الفحص: النطاق هو ({domain})")
    else:
        st.warning("⚠️ يرجى إدخال الرابط.")

st.divider()

# التذييل
st.markdown(f"""
    <div style='text-align: center;'>
        <p>🏛️ <b>روابط رسمية:</b> <a href='https://absher.sa'>أبشر</a> | <a href='https://iam.gov.sa'>نفاذ</a></p>
        <p style='color: #888;'>📊 تطوير المهندس: أيمن 🦾</p>
    </div>
""", unsafe_allow_html=True)
