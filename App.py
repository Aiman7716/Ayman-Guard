import streamlit as st
import tldextract
import time

# --- 1. إعدادات الأمان والتنسيق ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
        .st-emotion-cache-1kyx60p, symbol { display: none !important; } /* إخفاء التداخل */
        div.stButton > button { background-color: #ff4b4b !important; color: white !important; border-radius: 12px !important; width: 100% !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التحقق الذكي ---
def check_official(url):
    u = url.lower().strip()
    ext = tldextract.extract(u)
    domain = f"{ext.domain}.{ext.suffix}"
    is_gov_edu = u.endswith('.gov.sa') or u.endswith('.edu.sa')
    is_trusted = domain in ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa']
    return (is_gov_edu or is_trusted), domain

# --- 3. الواجهة ---
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🛡️ درع أيمن الذكي</h1>", unsafe_allow_html=True)

# حقل الفحص
u_input = st.text_input("🔍 ضع الرابط هنا للفحص :", value="", key="scanner_unique")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if u_input and not u_input.startswith("import"): # منع قبول الكود كروابط
        official, d_name = check_official(u_input)
        with st.spinner('جاري التحقق...'):
            time.sleep(0.5)
            if official:
                st.balloons()
                st.success(f"✅ رابط رسمي موثوق: ({d_name})")
            else:
                st.warning(f"⚠️ الرابط ({d_name}) غير مسجل كجهة رسمية.")
    else:
        st.error("⚠️ يرجى إدخال رابط صحيح.")

st.divider()

# --- 4. ساحة البلاغات ---
st.subheader("📢 ساحة بلاغات المجتمع")
r_input = st.text_input("أدخل الرابط المحتال للتبليغ عنه :", value="", key="report_unique")

if st.button("إرسال البلاغ"):
    if r_input:
        official, d_name = check_official(r_input)
        if official:
            st.error(f"❌ لا يمكن التبليغ عن ({d_name}) لأنه جهة رسمية!")
        else:
            st.success("✅ تم استلام بلاغك بنجاح لمراجعته.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
