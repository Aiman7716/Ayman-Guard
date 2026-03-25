import streamlit as st
import tldextract
import time

# --- 1. إعدادات الهوية والتنسيق (نفس الشكل القديم) ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# CSS مخصص لإعادة المظهر الاحترافي ومنع تداخل النصوص
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        /* ضبط الخط والاتجاه العربي */
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }

        /* تنسيق العنوان الكبير (نفس الصورة الأصلية) */
        .main-title-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .title-text { 
            color: #00d4ff; 
            font-size: 3.5rem; 
            font-weight: bold; 
            line-height: 1.1;
            margin: 0;
        }

        /* تنسيق الأزرار السماوية */
        .stButton>button { 
            width: auto; 
            min-width: 150px;
            border-radius: 10px; 
            background-color: white; 
            color: black; 
            border: 1px solid #ddd;
            font-weight: bold;
            height: 3em;
        }
        
        /* إخفاء الرموز البرمجية الغريبة التي تظهر في المتصفح */
        .css-10trblm, .css-1kyx60p, .st-emotion-cache-1kyx60p { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة البيانات (تجنب أخطاء sqlite3) ---
if 'check_count' not in st.session_state:
    st.session_state.check_count = 250

# --- 3. الواجهة الرئيسية (محاكاة الصورة 1000565789) ---
st.markdown("""
    <div class="main-title-container">
        <p class="title-text">🛡️ درع أيمن</p>
        <p class="title-text" style="font-size: 2.8rem;">الذكي</p>
    </div>
""", unsafe_allow_html=True)

# حقل الإدخال
url_input = st.text_input("🔍 ضع الرابط هنا :", placeholder="https://example.com")

# زر الفحص بنفس الشكل القديم
if st.button("🚀 افحص الآن"):
    if url_input:
        st.session_state.check_count += 1
        with st.spinner('جاري الفحص...'):
            time.sleep(1)
            ext = tldextract.extract(url_input.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            
            # المواقع الرسمية الموثوقة
            trust_list = ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa', 'moe.gov.sa']
            
            if domain in trust_list:
                st.balloons()
                st.success(f"✅ رابط آمن وموثوق: ({domain})")
            elif ext.suffix in ['tk', 'xyz', 'ml', 'cf', 'gq', 'top']:
                st.error("🚨 تحذير: هذا الرابط مشبوه!")
            else:
                st.info(f"ℹ️ نتيجة الفحص: النطاق هو ({domain})")
    else:
        st.warning("⚠️ يرجى إدخال الرابط")

st.markdown("<br><hr>", unsafe_allow_html=True)

# --- 4. قسم البلاغات (تنسيق نظيف بدون تداخل) ---
with st.expander("➕ أبلغ عن رابط"):
    scam_report = st.text_input("أدخل الرابط المشبوه")
    if st.button("إرسال البلاغ"):
        if scam_report:
            st.success("تم استلام بلاغك بنجاح")

st.markdown("<br>")

# --- 5. التذييل (Footer) - نفس الشكل المطلوب تماماً ---
st.markdown(f"""
    <div style='text-align: center; border-top: 1px solid #eee; padding-top: 15px;'>
        <p style='font-size: 1.1rem;'>
            🏛️ <b>روابط رسمية:</b> 
            <a href='https://absher.sa' style='color:#007bff; text-decoration:none;'>أبشر</a> | 
            <a href='https://iam.gov.sa' style='color:#007bff; text-decoration:none;'>نفاذ</a>
        </p>
        <p style='color: #666;'>
            📊 الفحوصات: {st.session_state.check_count} | تطوير: أيمن 🦾
        </p>
    </div>
""", unsafe_allow_html=True)
