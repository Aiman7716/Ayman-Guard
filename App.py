import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة والتنسيق ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# منع التداخل البصري keyboard_ar وحماية التنسيق
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        .st-emotion-cache-1kyx60p, symbol, svg { display: none !important; visibility: hidden !important; }
        div.stButton > button {
            background-color: #ff4b4b !important; color: white !important;
            border-radius: 12px !important; width: 100% !important; 
            height: 3.5em !important; font-weight: bold !important;
        }
        .history-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# تهيئة سجل الفحص في ذاكرة الجلسة
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# --- 2. محرك الفحص الذكي (المحلي والعالمي) ---
def analyze_url(url):
    # تنظيف الرابط من الرموز الزائدة
    u = url.lower().strip().replace('/', '').replace('http:', '').replace('https:', '')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    # التعرف على الجهات الحكومية والتعليمية عالمياً ومحلياً
    is_gov = u.endswith('.gov.sa') or u.endswith('.gov')
    is_edu = u.endswith('.edu.sa') or u.endswith('.edu')
    trusted = ['absher.sa', 'iam.gov.sa', 'google.com', 'microsoft.com', 'najm.sa']
    
    return (is_gov or is_edu or domain_full in trusted), domain_full

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# حقل البحث
user_link = st.text_input("ضع الرابط للفحص (جهة حكومية أو جامعة) :", key="scan_input")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if user_link:
        with st.spinner('جاري الفحص...'):
            time.sleep(0.5)
            safe, d_name = analyze_url(user_link)
            
            # إضافة النتيجة للسجل (بحد أقصى 5 عمليات)
            status_icon = "✅ موثوق" if safe else "⚠️ غير معروف"
            st.session_state.search_history.insert(0, f"{status_icon} : {d_name}")
            st.session_state.search_history = st.session_state.search_history[:5]
            
            if safe:
                st.balloons()
                st.success(f"✅ رابط رسمي موثق: {d_name}")
            else:
                st.warning(f"⚠️ الرابط {d_name} غير مدرج كجهة رسمية مباشرة.")
    else:
        st.error("⚠️ يرجى إدخال الرابط.")

# --- 4. سجل العمليات الأخيرة (الميزة الجديدة) ---
if st.session_state.search_history:
    with st.expander("🕒 عمليات الفحص الأخيرة في جلستك"):
        for item in st.session_state.search_history:
            st.write(item)

st.divider()

# --- 5. ساحة البلاغات ---
st.subheader("📢 ساحة بلاغات المجتمع")
report_link = st.text_input("أدخل الرابط المشبوه للتبليغ :", key="report_input")

if st.button("إرسال البلاغ"):
    if report_link:
        is_safe, d_name = analyze_url(report_link)
        if is_safe:
            st.error(f"❌ لا يمكن التبليغ عن ({d_name}) لأنه صرح رسمي!")
        else:
            st.success("✅ تم استلام بلاغك بنجاح لمراجعته من قبل المهندس أيمن.")
    else:
        st.warning("⚠️ أدخل الرابط أولاً.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
