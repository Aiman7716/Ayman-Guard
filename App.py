import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# --- 2. CSS "الحماية القصوى" لمنع التداخل تماماً ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .main-header { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        div.stButton > button { 
            background-color: #ff4b4b !important; color: white !important; 
            border-radius: 12px !important; width: 100% !important; height: 3.5em !important; font-weight: bold !important; 
        }
        /* منع ظهور رموز keyboard_ar نهائياً */
        symbol, .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الوظائف البرمجية (المنطق الذكي) ---
def is_official(url):
    """وظيفة للتحقق من أن الرابط جهة رسمية أو تعليمية"""
    url = url.lower().strip()
    ext = tldextract.extract(url)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    # القوائم الموثوقة
    trusted = ['absher.sa', 'iam.gov.sa', 'splonline.com.sa', 'saudipost.sa', 'moj.gov.sa', 'google.com']
    suffixes = ['.gov.sa', '.edu.sa']
    
    if any(url.endswith(s) for s in suffixes) or domain_full in trusted:
        return True, domain_full
    return False, domain_full

# --- 4. الواجهة الرئيسية ---
st.markdown('<div class="main-header">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# حقل الفحص
check_url = st.text_input("🔍 ضع الرابط هنا للفحص :", placeholder="https://example.gov.sa", key="fحص")

if st.button("🚀 افحص وصِد الرابط الآن", key="btn_fحص"):
    if check_url:
        official, d_name = is_official(check_url)
        with st.spinner('جاري التحقق...'):
            time.sleep(1)
            if official:
                st.balloons()
                st.success(f"✅ أبشر! هذا رابط رسمي موثوق: ({d_name})")
            else:
                st.warning(f"⚠️ الرابط ({d_name}) غير مسجل لدينا كجهة رسمية.")
    else:
        st.error("⚠️ يرجى إدخال الرابط أولاً.")

st.divider()

# --- 5. ساحة البلاغات (مع قفل الحماية) ---
st.subheader("📢 ساحة بلاغات المجتمع")
report_input = st.text_input("أدخل الرابط المحتال للتبليغ عنه :", key="بلاغ_نص")

if st.button("إرسال البلاغ", key="btn_بلاغ"):
    if report_input:
        official, d_name = is_official(report_input)
        
        # منع التبليغ عن الروابط الرسمية (إصلاح الخطأ السابق)
        if official:
            st.error(f"❌ خطأ: لا يمكن التبليغ عن ({d_name}) لأنه رابط رسمي موثق!")
        else:
            st.success("✅ تم استلام بلاغك بنجاح لمراجعته من قبل المهندس أيمن.")
    else:
        st.warning("⚠️ يرجى وضع الرابط المشبوه أولاً.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
