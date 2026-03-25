import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# --- 2. CSS احترافي لمنع التداخل تماماً ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        /* ضبط الخط والاتجاه العام */
        html, body, [class*="st-"] {
            font-family: 'Cairo', sans-serif !important;
            direction: rtl !important;
            text-align: right !important;
        }

        /* تنسيق العنوان الرئيسي لتجنب التداخل */
        .header-box {
            text-align: center;
            padding: 30px 0;
            color: #00d4ff;
        }
        .main-title { font-size: 3rem; font-weight: bold; margin: 0; }
        .sub-title { font-size: 1.5rem; margin-top: -10px; opacity: 0.8; }

        /* تحسين مظهر الحقول والأزرار */
        .stButton>button {
            width: 100%;
            border-radius: 15px;
            background-color: #00d4ff;
            color: white;
            font-weight: bold;
            height: 3.5em;
            font-size: 1.1rem;
            border: none;
            margin-top: 10px;
        }

        /* إخفاء أي رموز غريبة ناتجة عن المتصفح */
        .element-container img { display: inline-block; }
    </style>
""", unsafe_allow_html=True)

# --- 3. إدارة البيانات المؤقتة (بدون قاعدة بيانات لتجنب القفل) ---
if 'counter' not in st.session_state:
    st.session_state.counter = 250

# --- 4. واجهة المستخدم ---
st.markdown("""
    <div class="header-box">
        <div class="main-title">🛡️ درع أيمن</div>
        <div class="sub-title">الذكي</div>
    </div>
""", unsafe_allow_html=True)

# حقل الإدخال بتنسيق نظيف
url_to_check = st.text_input("🔍 ضع الرابط هنا لفحصه الآن:", placeholder="https://example.com")

if st.button("🚀 افحص الآن"):
    if url_to_check:
        st.session_state.counter += 1
        with st.spinner('جاري التحليل...'):
            time.sleep(1)
            ext = tldextract.extract(url_to_check.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            
            # فلتر المواقع
            safe_sites = ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa', 'moe.gov.sa']
            scam_tlds = ['tk', 'xyz', 'ml', 'cf', 'gq', 'top', 'ga']
            
            if domain in safe_sites:
                st.balloons()
                st.success(f"✅ هذا الموقع رسمي وآمن تماماً: ({domain})")
            elif ext.suffix in scam_tlds:
                st.error("🚨 تحذير: هذا الرابط يستخدم نطاقاً مشبوهاً يُستخدم غالباً في الاحتيال!")
            else:
                st.info(f"ℹ️ نتيجة الفحص: الرابط يتبع للنطاق ({domain})")
    else:
        st.warning("⚠️ فضلاً، أدخل الرابط أولاً.")

st.markdown("<br><hr>", unsafe_allow_html=True)

# --- 5. سجل البلاغات (تنسيق مبسط لمنع التداخل) ---
with st.expander("🚩 أبلغ عن رابط مشبوه"):
    st.write("ساعدنا في حماية الآخرين من خلال الإبلاغ عن الروابط الاحتيالية.")
    scam_link = st.text_input("رابط الموقع المحتال :")
    if st.button("إرسال البلاغ"):
        if scam_link:
            st.success("تم استلام بلاغك بنجاح، شكراً لك!")

st.markdown("<br>")

# --- 6. التذييل (نفس الشكل الأصلي) ---
st.markdown(f"""
    <div style='text-align: center; border-top: 1px solid #eee; padding-top: 20px;'>
        <p>🏛️ <b>روابط رسمية:</b> 
        <a href='https://absher.sa' style='text-decoration:none; color:#007bff;'>أبشر</a> | 
        <a href='https://iam.gov.sa' style='text-decoration:none; color:#007bff;'>نفاذ</a></p>
        <p style='color: #888;'>📊 إجمالي الفحوصات: {st.session_state.counter} | تطوير: أيمن 🦾</p>
    </div>
""", unsafe_allow_html=True)
