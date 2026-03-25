import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة والتنسيق ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        /* حماية الواجهة من تداخل keyboard_ar */
        .st-emotion-cache-1kyx60p, symbol, svg { display: none !important; visibility: hidden !important; }
        div.stButton > button {
            background-color: #ff4b4b !important; color: white !important;
            border-radius: 12px !important; width: 100% !important; height: 3.5em !important;
        }
    </style>
""", unsafe_allow_html=True)

if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# --- 2. محرك الفحص المتطور ---
def advanced_analyze(url):
    u = url.lower().strip().replace('/', '').replace('http:', '').replace('https:', '')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    # 1. فحص الموثوقية (حكومي/جامعي/قائمة بيضاء)
    is_official = u.endswith('.gov.sa') or u.endswith('.gov') or u.endswith('.edu.sa') or u.endswith('.edu')
    trusted = ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa', 'saudipost.sa']
    
    # 2. فحص النطاقات المؤقتة (المشبوهة غالباً)
    suspicious_hosting = ['mtempurl.com', 'smarterasp.net', '000webhostapp.com', 'free.hr']
    is_temp_hosting = any(host in domain_full for host in suspicious_hosting)
    
    if is_official or domain_full in trusted:
        return "SAFE", domain_full
    elif is_temp_hosting:
        return "SUSPICIOUS", domain_full
    else:
        return "UNKNOWN", domain_full

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

user_link = st.text_input("ضع الرابط للفحص (بما في ذلك الروابط المؤقتة) :", key="scan_v26")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if user_link:
        with st.spinner('جاري تحليل أمان الرابط...'):
            time.sleep(0.6)
            result, d_name = advanced_analyze(user_link)
            
            # تحديث السجل
            status_text = "✅ موثوق" if result == "SAFE" else "🚫 مشبوه" if result == "SUSPICIOUS" else "⚠️ غير معروف"
            st.session_state.search_history.insert(0, f"{status_text} : {d_name}")
            
            if result == "SAFE":
                st.balloons()
                st.success(f"✅ هذا رابط رسمي وموثق: {d_name}")
            elif result == "SUSPICIOUS":
                st.error(f"🚨 تحذير عالي: هذا الرابط مُستضاف على خادم مؤقت ({d_name}). غالباً ما يُستخدم للاحتيال!")
            else:
                st.warning(f"⚠️ تنبيه: الرابط ({d_name}) غير مسجل في قوائمنا الرسمية، كن حذراً.")
    else:
        st.error("⚠️ يرجى إدخال الرابط أولاً.")

# سجل الفحص
if st.session_state.search_history:
    with st.expander("🕒 آخر عمليات الفحص"):
        for item in st.session_state.search_history[:5]:
            st.write(item)

st.divider()

# --- 4. ساحة البلاغات ---
st.subheader("📢 ساحة بلاغات المجتمع")
report_link = st.text_input("أدخل الرابط المشبوه للتبليغ عنه :", key="report_v26")

if st.button("إرسال البلاغ"):
    if report_link:
        result, d_name = advanced_analyze(report_link)
        if result == "SAFE":
            st.error(f"❌ لا يمكن التبليغ عن ({d_name}) لأنه جهة رسمية موثوقة!")
        else:
            st.success("✅ تم استلام بلاغك بنجاح لمراجعته من قبل المهندس أيمن.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
