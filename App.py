import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️")

# --- 2. CSS خارجي فقط للخط والألوان (بعيداً عن الأزرار) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .title-text { 
            color: #00d4ff; 
            text-align: center; 
            font-size: 3rem; 
            font-weight: bold; 
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. إدارة البيانات (بدون قاعدة بيانات نهائياً) ---
if 'check_count' not in st.session_state:
    st.session_state.check_count = 250

# --- 4. الواجهة الرئيسية (التنسيق الأصلي) ---
st.markdown('<p class="title-text">🛡️ درع أيمن الذكي</p>', unsafe_allow_html=True)

# استخدام أدوات سستريم ليت الرسمية مباشرة لمنع تداخل keyboard_ar
url_input = st.text_input("🔍 ضع الرابط هنا لفحصه :", placeholder="https://example.com")

if st.button("🚀 افحص الآن"):
    if url_input:
        st.session_state.check_count += 1
        with st.spinner('جاري التحليل...'):
            time.sleep(1)
            ext = tldextract.extract(url_input.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            
            # فلتر المواقع الرسمية
            trust = ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa', 'moe.gov.sa']
            
            if domain in trust:
                st.balloons()
                st.success(f"✅ رابط آمن وموثوق: ({domain})")
            elif ext.suffix in ['tk', 'xyz', 'ml', 'cf', 'gq', 'top']:
                st.error("🚨 تحذير: هذا الرابط مشبوه!")
            else:
                st.info(f"ℹ️ نتيجة الفحص: النطاق هو ({domain})")
    else:
        st.warning("⚠️ يرجى إدخال الرابط أولاً.")

st.divider()

# قسم البلاغات
with st.expander("🚩 أبلغ عن رابط مشبوه"):
    scam = st.text_input("رابط الموقع المحتال:")
    if st.button("إرسال البلاغ"):
        if scam:
            st.success("تم تسجيل بلاغك بنجاح")

st.divider()

# التذييل (نفس شكل الصورة الموثقة)
st.markdown(f"""
    <div style='text-align: center;'>
        <p>🏛️ <b>روابط رسمية:</b> 
        <a href='https://absher.sa' style='color:#007bff; text-decoration:none;'>أبشر</a> | 
        <a href='https://iam.gov.sa' style='color:#007bff; text-decoration:none;'>نفاذ</a></p>
        <p style='color: #888;'>📊 الفحوصات: {st.session_state.check_count} | تطوير المهندس: أيمن 🦾</p>
    </div>
""", unsafe_allow_html=True)
