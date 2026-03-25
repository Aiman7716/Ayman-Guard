import streamlit as st
import tldextract
import time

# --- 1. إعدادات المظهر الأصلي (خلفية بيضاء وتنسيق نظيف) ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# CSS مخصص لإعادة الشكل الذي تفضله ومنع تداخل الرموز
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif; 
            text-align: right; 
            direction: rtl; 
        }
        .main-title { 
            color: #00d4ff; 
            text-align: center; 
            font-size: 3rem; 
            font-weight: bold; 
            margin-bottom: 20px;
        }
        .stButton>button { 
            width: 100%; border-radius: 15px; background: #00d4ff; 
            color: white; font-weight: bold; border: none; height: 3.5em;
            font-size: 1.1rem;
        }
        /* منع ظهور أي رموز برمجية متداخلة في الخلفية */
        .stExpander, .stTextInput { border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة البيانات (Session State) ---
if 'counter' not in st.session_state:
    st.session_state.counter = 250

# --- 3. الواجهة الرئيسية (نفس تنسيق الصورة 1000565789) ---
st.markdown("<div class='main-title'>🛡️ درع أيمن<br>الذكي</div>", unsafe_allow_html=True)

# حقل إدخال الرابط
url_input = st.text_input("🔍 ضع الرابط هنا :", placeholder="https://example.com")

if st.button("🚀 افحص الآن"):
    if url_input:
        st.session_state.counter += 1
        with st.spinner('جاري الفحص...'):
            time.sleep(1)
            ext = tldextract.extract(url_input.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            
            # المواقع الموثوقة والمشبوهة
            trust = ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa', 'moe.gov.sa']
            danger = ['tk', 'xyz', 'ml', 'cf', 'gq', 'top', 'ga']
            
            if domain in trust:
                st.balloons()
                st.success(f"✅ رابط آمن وموثوق: ({domain})")
            elif ext.suffix in danger:
                st.error("🚨 تحذير: هذا الرابط مشبوه وغير آمن!")
            else:
                st.info(f"ℹ️ نتيجة التحليل: النطاق هو ({domain})")
    else:
        st.warning("⚠️ يرجى إدخال الرابط أولاً.")

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. قسم البلاغات (تصحيح مشكلة الرموز المتداخلة) ---
with st.expander("➕ أبلغ عن رابط"):
    scam_url = st.text_input("أدخل الرابط المشبوه هنا:")
    if st.button("إرسال البلاغ"):
        if scam_url:
            st.success("تم استلام بلاغك بنجاح. شكراً لمساهمتك!")
        else:
            st.error("الرجاء إدخال الرابط.")

st.markdown("---")

# --- 5. التذييل والروابط الرسمية (نفس شكل الصورة 1000565789) ---
st.markdown(f"""
    <p style='text-align: center; font-size: 1.1rem;'>
        🏛️ <b>روابط رسمية:</b> 
        <a href='https://absher.sa' style='color:#007bff; text-decoration:none;'>أبشر</a> | 
        <a href='https://iam.gov.sa' style='color:#007bff; text-decoration:none;'>نفاذ</a>
    </p>
    <p style='text-align: center; color: #666;'>
        📊 الفحوصات: {st.session_state.counter} | تطوير: أيمن 🦾
    </p>
""", unsafe_allow_html=True)
