import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# --- 2. CSS لمنع تداخل نصوص keyboard_ar نهائياً ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        /* منع ظهور أي نصوص برمجية غريبة في الواجهة */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg { 
            display: none !important; 
            visibility: hidden !important;
        }
        div.stButton > button { 
            background-color: #ff4b4b !important; color: white !important; 
            border-radius: 12px !important; width: 100% !important; font-weight: bold !important; 
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. محرك الفحص الذكي (مع تنظيف الروابط) ---
def smart_check(url):
    # تنظيف الرابط من المسافات والعلامات الزائدة مثل / في الصورة الأخيرة
    u = url.lower().strip().replace('/', '').replace('http:', '').replace('https:', '')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    # التحقق من الامتدادات الحكومية والتعليمية
    is_official_sa = u.endswith('.gov.sa') or u.endswith('.edu.sa')
    # قائمة موثوقة إضافية
    trusted_list = ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa', 'moi.gov.sa']
    
    return (is_official_sa or domain_full in trusted_list), domain_full

# --- 4. الواجهة ---
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🛡️ درع أيمن الذكي</h1>", unsafe_allow_html=True)

# حقل الفحص بدون أيقونات لمنع التداخل
u_input = st.text_input("أدخل الرابط للفحص :", placeholder="مثال: moi.gov.sa", key="clean_scan")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if u_input:
        is_safe, d_name = smart_check(u_input)
        with st.spinner('جاري التحقق...'):
            time.sleep(0.5)
            if is_safe:
                st.balloons()
                st.success(f"✅ أبشر! رابط رسمي موثوق: ({d_name})")
            else:
                st.warning(f"⚠️ الرابط ({d_name}) غير مسجل كجهة رسمية مباشرة.")
    else:
        st.error("⚠️ يرجى إدخال الرابط.")

st.divider()

# --- 5. ساحة البلاغات ---
st.subheader("📢 ساحة بلاغات المجتمع")
r_input = st.text_input("أدخل الرابط المحتال للتبليغ عنه :", key="clean_report")

if st.button("إرسال البلاغ"):
    if r_input:
        is_safe, d_name = smart_check(r_input)
        if is_safe:
            st.error(f"❌ خطأ: لا يمكن التبليغ عن ({d_name}) لأنه رابط رسمي!")
        else:
            st.success("✅ تم استلام بلاغك بنجاح لمراجعته.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
