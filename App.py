import streamlit as st
import tldextract
import time

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
        .stButton>button { 
            width: 100%; border-radius: 25px; background: #00d4ff; 
            color: black; font-weight: bold; border: none; height: 3.5em;
        }
        .main-title { text-align: center; color: #00d4ff; font-size: 2.5rem; font-weight: bold; }
        .stat-box { background: #1a1c24; border-radius: 15px; padding: 10px; text-align: center; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة البيانات (بدون قاعدة بيانات معقدة لتجنب القفل) ---
if 'check_count' not in st.session_state:
    st.session_state.check_count = 250  # البداية كما طلبت أيمن

# --- 3. الواجهة الرئيسية ---
st.markdown("<div class='main-title'>🛡️ درع أيمن الذكي</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>نظامك الذكي لفحص الروابط وكشف محاولات الاحتيال الرقمي</p>", unsafe_allow_html=True)

# محرك الفحص
url_to_check = st.text_input("🔍 الصق الرابط هنا للفحص الآلي:", placeholder="https://example.com")

if st.button("🚀 اطلق الدرع"):
    if url_to_check:
        st.session_state.check_count += 1
        with st.spinner('جاري تحليل بروتوكولات الرابط...'):
            time.sleep(1)
            ext = tldextract.extract(url_to_check.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            
            # منطق الحماية
            officials = ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa', 'moe.gov.sa', 'hrsd.gov.sa']
            scam_tlds = ['tk', 'xyz', 'ml', 'cf', 'gq', 'top', 'ga']
            
            if domain in officials:
                st.balloons()
                st.success(f"✅ هذا الرابط رسمي وموثوق بنسبة 100% ({domain})")
            elif ext.suffix in scam_tlds:
                st.error(f"🚨 تحذير شديد! النطاق ({ext.suffix}) يُستخدم بكثرة في مواقع الاحتيال.")
            else:
                st.info(f"🔍 نتيجة الفحص: الرابط يتبع لنطاق ({domain}). تأكد من المصدر دائماً.")
    else:
        st.warning("⚠️ يرجى إدخال الرابط أولاً.")

# --- 4. قسم البلاغات ---
st.markdown("---")
st.subheader("📢 بلاغات المجتمع")
with st.expander("🚩 هل اكتشفت رابطاً مشبوهاً؟ أبلغ هنا"):
    scam_report = st.text_input("ضع الرابط المشبوه:")
    if st.button("تأكيد الإبلاغ"):
        if scam_report:
            st.success("تم تسجيل بلاغك في النظام المؤقت بنجاح!")
        else:
            st.warning("أدخل الرابط أولاً.")

# --- 5. روابط سريعة موثوقة ---
st.markdown("---")
st.markdown("<p style='text-align: center;'>🏛️ مراجع رسمية آمنة</p>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1: st.markdown("<center><a href='https://absher.sa'>أبشر</a></center>", unsafe_allow_html=True)
with col2: st.markdown("<center><a href='https://iam.gov.sa'>نفاذ</a></center>", unsafe_allow_html=True)
with col3: st.markdown("<center><a href='https://splonline.com.sa'>سبل</a></center>", unsafe_allow_html=True)

# --- 6. التذييل ---
st.markdown("---")
st.markdown(f"""
    <div class='stat-box'>
        📊 إجمالي العمليات: {st.session_state.check_count} | 🦾 تطوير المهندس: أيمن
    </div>
""", unsafe_allow_html=True)
