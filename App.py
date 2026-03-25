import streamlit as st
import tldextract
import re
import random

# 1. إعدادات الصفحة
st.set_page_config(page_title="درع أيمن الرقمي", page_icon="🛡️", layout="centered")

# 2. تصميم الواجهة المطور
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; font-family: 'Arial'; text-shadow: 2px 2px #000; }
    .stButton>button {
        width: 100%;
        background-color: #00d4ff;
        color: #000;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px;
    }
    .report-box {
        background-color: #1a1c24;
        border: 1px dashed #ff4b4b;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 3. العنوان
st.markdown("<h1>🛡️ درع أيمن <br> لصيد الروابط الوهمية</h1>", unsafe_allow_html=True)
st.markdown("---")

# 4. العداد وقائمة البلاغات (Session State)
if 'counter' not in st.session_state:
    st.session_state.counter = 248
if 'reports' not in st.session_state:
    st.session_state.reports = ["رابط وهمي لشركة شحن (تم صيده)", "رابط منتحل لخدمة أبشر (تم صيده)"]

# 5. شريط النصائح
tips = ["💡 نصيحة: تأكد دائماً من وجود قفل الأمان (HTTPS).", "💡 نصيحة: لا تشارك رمز (OTP) مع أحد."]
st.info(random.choice(tips))

# 6. خانة الفحص الأساسية
url_input = st.text_input("🔍 افحص رابطاً الآن:", placeholder="https://example-scam.com")

if st.button("🚀 افحص وصِد الآن"):
    st.session_state.counter += 1
    if url_input:
        # (منطق الفحص المعتاد)
        ext = tldextract.extract(url_input.lower())
        full_domain = f"{ext.domain}.{ext.suffix}"
        if full_domain in ['google.com', 'moi.gov.sa', 'absher.sa']:
            st.success(f"✅ آمن وموثوق: ({full_domain})")
        else:
            st.warning(f"ℹ️ نتيجة الفحص: الرابط يتبع لنطاق ({full_domain}). كن حذراً.")
    else:
        st.error("⚠️ ضع الرابط أولاً!")

st.markdown("---")

# 7. ميزة "زر مشاركة رابط من الزوار"
st.markdown("### 📢 ساحة بلاغات المجتمع")
st.write("هل وجدت رابطاً مشبوهاً؟ شاركه معنا لنحذر الجميع!")

with st.expander("➕ اضغط هنا للمشاركة وإرسال بلاغ"):
    user_report = st.text_input("الصق الرابط المشبوه هنا:", key="report_input")
    if st.button("📤 إرسال البلاغ الآن"):
        if user_report:
            st.session_state.reports.insert(0, user_report) # إضافة البلاغ في بداية القائمة
            st.success("✅ شكراً لك! تم استلام بلاغك وإضافته لقائمة التحذير.")
        else:
            st.error("⚠️ الرجاء كتابة الرابط قبل الإرسال.")

# 8. عرض آخر البلاغات
if st.session_state.reports:
    st.write("**⚠️ آخر الروابط التي أبلغ عنها الزوار:**")
    for r in st.session_state.reports[:5]: # عرض آخر 5 بلاغات فقط
        st.markdown(f"- `{r}`")

# 9. التذييل والعداد
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.write(f"📊 الفحوصات: **{st.session_state.counter}**")
with col2:
    st.markdown("<p style='text-align: left;'>تطوير: أيمن 🦾🛡️</p>", unsafe_allow_html=True)
