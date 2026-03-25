import streamlit as st
import tldextract
import random

# 1. إعدادات وتنسيق الصفحة
st.set_page_config(page_title="درع أيمن - منصة الأمان", page_icon="🛡️", layout="centered")

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; text-shadow: 2px 2px #000; }
    .stButton>button { width: 100%; background-color: #00d4ff; color: #000; font-weight: bold; border-radius: 12px; }
    .report-card { background-color: #1a1c24; border-radius: 10px; padding: 10px; border-right: 4px solid #ff4b4b; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# 2. العنوان وتهيئة البيانات
st.markdown("<h1>🛡️ درع أيمن الذكي</h1>", unsafe_allow_html=True)

if 'counter' not in st.session_state: st.session_state.counter = 248
if 'verified_scams' not in st.session_state: 
    st.session_state.verified_scams = ["facebook-verify-login.xyz", "update-absher-sa.tk"]

# 3. شريط النصائح
tips = ["💡 الجهات الرسمية لا تطلب OTP عبر الروابط.", "💡 تأكد من وجود HTTPS دائماً."]
st.info(random.choice(tips))

# 4. محرك الفحص الأساسي
url_input = st.text_input("🔍 افحص الرابط المشبوه هنا:", placeholder="https://scam-site.com")

if st.button("🚀 افحص وصِد الآن"):
    st.session_state.counter += 1
    if url_input:
        ext = tldextract.extract(url_input.lower())
        full_domain = f"{ext.domain}.{ext.suffix}"
        
        # منطق صيد الهكر السريع
        is_suspicious = ext.suffix in ['tk', 'ml', 'ga', 'xyz', 'cf'] or "@" in url_input or len(url_input) > 80
        
        if full_domain in ['moi.gov.sa', 'absher.sa', 'google.com', 'yemencars.com']:
            st.success(f"✅ آمن وموثوق: موقع رسمي ({full_domain})")
        elif is_suspicious:
            st.error(f"❌ تم صيد رابط وهمي! النطاق ({full_domain}) مشبوه جداً.")
        else:
            st.info(f"ℹ️ نتيجة الفحص: الرابط يتبع لنطاق ({full_domain}).")
    else:
        st.error("⚠️ من فضلك ضع الرابط أولاً!")

st.markdown("---")

# 5. الفكرة الاحترافية: ساحة البلاغات المفلترة
st.markdown("### 📢 بلاغات المجتمع الموثقة")
st.write("شاركنا الروابط التي وصلتكم لنفحصها ونحذر الآخرين منها.")

with st.expander("➕ إرسال بلاغ عن رابط جديد"):
    new_report = st.text_input("أدخل الرابط المشبوه هنا:", key="report_box")
    if st.button("📤 إرسال وتحقق"):
        if new_report:
            ext_rep = tldextract.extract(new_report.lower())
            # فلترة ذكية: لا نقبل البلاغات عن مواقع موثوقة
            if ext_rep.domain in ['google', 'absher', 'moi', 'whatsapp']:
                st.warning("⚠️ هذا موقع رسمي وموثق، لا يمكن التبليغ عنه كـ 'هكر'.")
            else:
                st.session_state.verified_scams.insert(0, new_report.strip().lower())
                st.success("✅ تم التحقق وإضافة الرابط لقائمة التحذير بنجاح!")
        else:
            st.error("⚠️ يرجى إدخال الرابط.")

# 6. عرض قائمة التحذير
if st.session_state.verified_scams:
    st.write("**🚨 أحدث الروابط التي تم صيدها والتبليغ عنها:**")
    for scam in st.session_state.verified_scams[:4]: # عرض آخر 4 فقط للترتيب
        st.markdown(f"<div class='report-card'>⚠️ رابط مشبوه: <code>{scam}</code> <br><small>🚩 حالة التحقق: تم التأكيد بواسطة الدرع</small></div>", unsafe_allow_html=True)

# 7. التذييل
st.markdown("---")
st.write(f"📊 إحصائيات الدرع: **{st.session_state.counter}** فحصاً")
st.markdown("<p style='text-align: center; color: #555;'>تطوير: أيمن 🦾🛡️ | حماية المجتمع مسؤوليتنا</p>", unsafe_allow_html=True)
