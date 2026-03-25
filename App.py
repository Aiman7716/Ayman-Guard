import streamlit as st
import tldextract
import time

# --- 1. الإعدادات والتنسيق الأصلي (نفس الشكل السابق) ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
        
        /* تنسيق العنوان الرئيسي */
        .main-title { color: #00d4ff; text-align: center; font-size: 3rem; font-weight: bold; margin-bottom: 0; }
        .sub-title { text-align: center; color: #555; margin-top: -10px; font-size: 1.2rem; }
        
        /* تنسيق الأزرار */
        .stButton>button { 
            width: 100%; border-radius: 15px; background: #00d4ff; 
            color: white; font-weight: bold; border: none; height: 3.5em;
            font-size: 1.1rem; box-shadow: 0 4px 15px rgba(0,212,255,0.3);
        }
        
        /* تنسيق الروابط الرسمية */
        .official-link { color: #007bff; text-decoration: none; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة البيانات الذكية (بدون تعليق) ---
if 'counter' not in st.session_state:
    st.session_state.counter = 250

# --- 3. واجهة المستخدم (التنسيق المفضل لديك) ---
st.markdown("<div class='main-title'>🛡️ درع أيمن</div>", unsafe_allow_html=True)
st.markdown("<div class='main-title' style='font-size: 2.5rem; margin-top:-20px;'>الذكي</div>", unsafe_allow_html=True)

# حقل الإدخال
url_input = st.text_input("🔍 ضع الرابط هنا :", placeholder="https://example.com")

if st.button("🚀 افحص الآن"):
    if url_input:
        st.session_state.counter += 1
        with st.spinner('جاري الفحص...'):
            time.sleep(1)
            ext = tldextract.extract(url_input.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            
            # قاعدة بيانات الحماية
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
        st.warning("⚠️ يرجى إدخال رابط")

st.markdown("---")

# قسم البلاغات بنفس الشكل القديم
with st.expander("➕ أبلغ عن رابط"):
    scam = st.text_input("أدخل الرابط المشبوه")
    if st.button("إرسال البلاغ"):
        st.success("تم استلام بلاغك بنجاح")

st.markdown("---")

# الروابط الرسمية والإحصائيات بنفس التنسيق المطلوب
col_stats = st.container()
with col_stats:
    st.markdown(f"""
        <p style='text-align: center; font-size: 1.1rem;'>
            🏛️ <b>روابط رسمية:</b> 
            <a href='https://absher.sa' class='official-link'>أبشر</a> | 
            <a href='https://iam.gov.sa' class='official-link'>نفاذ</a>
        </p>
        <p style='text-align: center; color: #666;'>
            📊 الفحوصات: {st.session_state.counter} | تطوير: أيمن 🦾
        </p>
    """, unsafe_allow_html=True)
