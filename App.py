import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة والتنسيق العربي ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# CSS لإجبار المتصفح على التنسيق النظيف ومنع تداخل النصوص
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .main-title { 
            color: #00d4ff; 
            text-align: center; 
            font-size: 45px; 
            font-weight: bold; 
            margin-bottom: 5px;
        }
        .stButton>button { 
            width: 100%; border-radius: 10px; background-color: #00d4ff; 
            color: white; font-weight: bold; border: none; height: 3em;
        }
        /* إخفاء أي رموز برمجية تظهر بالخطأ */
        .st-emotion-cache-1kyx60p, .css-1kyx60p { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. حفظ البيانات (حل مشكلة الخطأ الأحمر) ---
if 'check_count' not in st.session_state:
    st.session_state.check_count = 250

# --- 3. الواجهة الرئيسية (التنسيق القديم) ---
st.markdown("<div class='main-title'>🛡️ درع أيمن</div>", unsafe_allow_html=True)
st.markdown("<div class='main-title' style='font-size: 35px; margin-top: -15px;'>الذكي</div>", unsafe_allow_html=True)

# حقل الإدخال
url_input = st.text_input("🔍 ضع الرابط هنا لفحصه :", placeholder="https://example.com")

if st.button("🚀 افحص الآن"):
    if url_input:
        st.session_state.check_count += 1
        with st.spinner('جاري الفحص...'):
            time.sleep(1)
            ext = tldextract.extract(url_input.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            
            # فلتر الحماية
            trust = ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa', 'moe.gov.sa']
            if domain in trust:
                st.balloons()
                st.success(f"✅ رابط آمن وموثوق: ({domain})")
            elif ext.suffix in ['tk', 'xyz', 'ml', 'cf', 'gq']:
                st.error("🚨 تحذير: نطاق مشبوه!")
            else:
                st.info(f"ℹ️ نتيجة التحليل: النطاق هو ({domain})")
    else:
        st.warning("⚠️ الرجاء إدخال الرابط أولاً.")

st.markdown("---")

# قسم البلاغات
with st.expander("➕ أبلغ عن رابط"):
    scam_report = st.text_input("أدخل الرابط المشبوه")
    if st.button("تأكيد البلاغ"):
        st.success("تم استلام بلاغك")

st.markdown("---")

# التذييل (نفس الشكل الأصلي الموثق بالصور)
st.markdown(f"""
    <div style='text-align: center;'>
        <p>🏛️ <b>روابط رسمية:</b> 
        <a href='https://absher.sa' style='color:#007bff; text-decoration:none;'>أبشر</a> | 
        <a href='https://iam.gov.sa' style='color:#007bff; text-decoration:none;'>نفاذ</a></p>
        <p style='color: #888;'>📊 الفحوصات: {st.session_state.check_count} | تطوير: أيمن 🦾</p>
    </div>
""", unsafe_allow_html=True)
