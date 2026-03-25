import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة والتنسيق الاحترافي ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.8rem; font-weight: bold; margin-bottom: 20px; }
        
        /* إخفاء مسببات تداخل نصوص keyboard_ar */
        .st-emotion-cache-1kyx60p, symbol, svg { display: none !important; visibility: hidden !important; }
        
        div.stButton > button {
            background-color: #ff4b4b !important; color: white !important;
            border-radius: 12px !important; width: 100% !important; 
            height: 3.5em !important; font-weight: bold !important; border: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك البحث والتعرف الذكي ---
def analyze_url(url):
    # تنظيف الرابط من الرموز الزائدة مثل / أو الفراغات
    clean_url = url.lower().strip().replace('/', '').replace('http:', '').replace('https:', '')
    ext = tldextract.extract(clean_url)
    domain_name = f"{ext.domain}.{ext.suffix}"
    
    # القواعد الذكية للتعرف
    is_gov = clean_url.endswith('.gov.sa') or clean_url.endswith('.gov') # حكومي محلي وعالمي
    is_edu = clean_url.endswith('.edu.sa') or clean_url.endswith('.edu') # جامعات محلية وعالمية
    
    # قائمة المؤسسات العالمية والمحلية الموثوقة يدوياً
    trusted_list = ['absher.sa', 'iam.gov.sa', 'google.com', 'microsoft.com', 'apple.com', 'najm.sa']
    
    if is_gov or is_edu or domain_name in trusted_list:
        return True, domain_name, "رسمي/حكومي/جامعي"
    return False, domain_name, "غير معروف"

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

st.info("💡 المحرك الآن يتعرف تلقائياً على كافة النطاقات الحكومية (.gov) والتعليمية (.edu) عالمياً ومحلياً.")

# حقل البحث (بدون أيقونات لمنع التداخل)
user_link = st.text_input("ضع الرابط للفحص (وزارة، جامعة، مؤسسة) :", key="main_search")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if user_link:
        with st.spinner('جاري تحليل الرابط...'):
            time.sleep(0.7)
            is_official, d_name, category = analyze_url(user_link)
            
            if is_official:
                st.balloons()
                st.success(f"✅ تم التحقق: هذا رابط موثوق ({category}): {d_name}")
            else:
                st.warning(f"⚠️ تنبيه: الرابط ({d_name}) غير مسجل كجهة رسمية مباشرة، تعامل معه بحذر.")
    else:
        st.error("⚠️ يرجى إدخال الرابط أولاً.")

st.divider()

# --- 4. ساحة البلاغات ---
st.subheader("📢 ساحة بلاغات المجتمع")
report_link = st.text_input("أدخل الرابط المشبوه للتبليغ عنه :", key="report_field")

if st.button("إرسال البلاغ"):
    if report_link:
        is_official, d_name, _ = analyze_url(report_link)
        if is_official:
            st.error(f"❌ خطأ: لا يمكن التبليغ عن ({d_name}) لأنه صرح رسمي أو تعليمي موثوق!")
        else:
            st.success("✅ تم استلام بلاغك بنجاح لمراجعته من قبل المهندس أيمن.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
