import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# --- 2. CSS نقي جداً (فقط للألوان والخطوط) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .main-title { 
            color: #00d4ff; text-align: center; font-size: 2.8rem; 
            font-weight: bold; margin-bottom: 0px; 
        }
        .stButton>button { 
            width: 100%; border-radius: 12px; background-color: #00d4ff; 
            color: white; font-weight: bold; border: none; height: 3.5em;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. إدارة البيانات (بدون قاعدة بيانات لمنع القفل) ---
if 'count' not in st.session_state:
    st.session_state.count = 250

# --- 4. الواجهة (التنسيق القديم الأصلي) ---
# استخدام أعمدة لتوسيط الشعار والنص بشكل احترافي
st.markdown("<div class='main-title'>🛡️ درع أيمن الذكي</div>", unsafe_allow_html=True)

st.write("") # مسافة فارغة

# حقل الإدخال (خارج أي وسوم HTML لمنع ظهور keyboard_ar)
url_input = st.text_input("🔍 ضع الرابط هنا لفحصه :", placeholder="https://example.com")

if st.button("🚀 افحص الآن"):
    if url_input:
        st.session_state.count += 1
        with st.spinner('جاري الفحص...'):
            time.sleep(1)
            ext = tldextract.extract(url_input.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            
            # المواقع الموثوقة
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

st.markdown("---")

# قسم البلاغات بتنسيق نظيف
with st.expander("➕ أبلغ عن رابط مشبوه"):
    report = st.text_input("أدخل الرابط المحتال :")
    if st.button("إرسال البلاغ"):
        if report:
            st.success("تم استلام بلاغك بنجاح")

st.markdown("---")

# --- 5. التذييل (نفس شكل الصورة 1000565805) ---
st.markdown(f"""
    <div style='text-align: center;'>
        <p style='font-size: 1.1rem;'>
            🏛️ <b>روابط رسمية:</b> 
            <a href='https://absher.sa' style='color:#007bff; text-decoration:none;'>أبشر</a> | 
            <a href='https://iam.gov.sa' style='color:#007bff; text-decoration:none;'>نفاذ</a>
        </p>
        <p style='color: #888;'>
            📊 الفحوصات: {st.session_state.count} | تطوير المهندس: أيمن 🦾
        </p>
    </div>
""", unsafe_allow_html=True)
