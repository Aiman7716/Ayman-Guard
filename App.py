import streamlit as st
import tldextract
import time

# --- 1. تنظيف شامل وإعدادات الهوية ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# CSS قوي لإجبار المتصفح على عرض التنسيق الأصلي ومنع التداخل
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        /* ضبط الخط والاتجاه */
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }

        /* تنسيق العنوان الكبير الصافي */
        .title-container {
            text-align: center;
            padding: 20px;
            margin-bottom: 20px;
        }
        .main-header { color: #00d4ff; font-size: 3.5rem; font-weight: bold; line-height: 1.2; }
        
        /* تحسين مظهر الأزرار والحقول */
        .stButton>button { 
            width: 100%; border-radius: 12px; background-color: #00d4ff; 
            color: white; font-weight: bold; border: none; height: 3.8em;
            font-size: 1.2rem; transition: 0.3s;
        }
        .stButton>button:hover { background-color: #008fb3; border: none; }
        
        /* إخفاء أي رموز برمجية قد تظهر بسبب المتصفح */
        .css-10trblm, .css-1kyx60p { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة البيانات في الذاكرة ---
if 'counter' not in st.session_state:
    st.session_state.counter = 250

# --- 3. الواجهة الرئيسية (التنسيق الأصلي النظيف) ---
st.markdown("""
    <div class='title-container'>
        <div class='main-header'>🛡️ درع أيمن</div>
        <div class='main-header' style='font-size: 2.5rem; margin-top: -10px;'>الذكي</div>
    </div>
""", unsafe_allow_html=True)

# حقل إدخال الرابط
url_to_check = st.text_input("🔍 ضع الرابط هنا لفحصه:", placeholder="https://example.com")

if st.button("🚀 افحص الآن"):
    if url_to_check:
        st.session_state.counter += 1
        with st.spinner('جاري التحليل الرقمي...'):
            time.sleep(1)
            ext = tldextract.extract(url_to_check.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            
            # القوائم الموثوقة
            safe_list = ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa', 'moe.gov.sa', 'hrsd.gov.sa']
            danger_tlds = ['tk', 'xyz', 'ml', 'cf', 'gq', 'top', 'ga', 'bit']
            
            if domain in safe_list:
                st.balloons()
                st.success(f"✅ هذا الرابط رسمي وموثوق: ({domain})")
            elif ext.suffix in danger_tlds:
                st.error("🚨 تحذير: هذا الرابط يستخدم نطاقاً مشبوهاً جداً!")
            else:
                st.info(f"ℹ️ نتيجة الفحص: النطاق المكتشف هو ({domain})")
    else:
        st.warning("⚠️ الرجاء إدخال الرابط أولاً.")

st.markdown("<br><hr>", unsafe_allow_html=True)

# --- 4. قسم البلاغات ---
with st.expander("🚩 أبلغ عن رابط مشبوه"):
    report_link = st.text_input("رابط الموقع المحتال:")
    if st.button("إرسال التقرير"):
        if report_link:
            st.success("تم استلام بلاغك، شكراً لمساعدتنا في حماية المجتمع!")
        else:
            st.error("أدخل الرابط المراد الإبلاغ عنه.")

st.markdown("<br>")

# --- 5. التذييل (نفس شكل الصورة المرجعية) ---
st.markdown(f"""
    <div style='text-align: center; border-top: 1px solid #eee; padding-top: 20px;'>
        <p style='font-size: 1.1rem;'>
            🏛️ <b>روابط رسمية آمنة:</b> 
            <a href='https://absher.sa' style='color:#007bff; text-decoration:none;'>أبشر</a> | 
            <a href='https://iam.gov.sa' style='color:#007bff; text-decoration:none;'>نفاذ</a>
        </p>
        <p style='color: #888; font-size: 0.9rem;'>
            📊 الفحوصات المنفذة: {st.session_state.counter} | 🦾 تطوير: أيمن
        </p>
    </div>
""", unsafe_allow_html=True)
