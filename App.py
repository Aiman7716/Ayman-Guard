import streamlit as st
import tldextract
import re
import random

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="درع أيمن الرقمي", page_icon="🛡️", layout="centered")

# 2. تصميم الواجهة
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
        padding: 12px;
        border: none;
    }
    .stButton>button:hover { background-color: #ff4b4b; color: white; }
    .stTextInput>div>div>input {
        background-color: #1a1c24;
        color: white;
        border: 2px solid #00d4ff;
        border-radius: 12px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 3. واجهة المستخدم
st.markdown("<h1>🛡️ درع أيمن <br> لصيد الروابط الوهمية</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>نظام ذكي متطور لكشف محاولات سرقة البيانات والاحتيال</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. إدارة العداد (Session State)
if 'counter' not in st.session_state:
    st.session_state.counter = 248

# 5. شريط النصائح العشوائية
tips = [
    "💡 نصيحة: البنوك لا تطلب أرقام بطاقتك البنكية عبر الروابط.",
    "💡 نصيحة: تأكد دائماً من وجود قفل الأمان (HTTPS) في الرابط.",
    "💡 نصيحة: روابط الهكر غالباً تنتهي بنطاقات غريبة مثل .tk أو .xyz",
    "💡 نصيحة: لا تشارك رمز التوثيق (OTP) مع أي شخص أبداً."
]
st.info(random.choice(tips))

# 6. خانة إدخال الرابط
url_input = st.text_input("⚠️ قم بلصق الرابط المشبوه هنا لفحصه:", placeholder="https://example-scam.com")

# 7. منطق الفحص والصيد
if st.button("🚀 افحص وصِد الرابط الآن"):
    st.session_state.counter += 1
    
    if url_input:
        url_lower = url_input.lower()
        ext = tldextract.extract(url_lower)
        full_domain = f"{ext.domain}.{ext.suffix}"
        
        # القوائم البرمجية
        trusted = ['google.com', 'facebook.com', 'whatsapp.com', 'instagram.com', 'moi.gov.sa', 'absher.sa', 'stc.com.sa', 'yemencars.com']
        official_suffixes = ['gov', 'gov.sa', 'edu', 'edu.sa', 'org', 'mil']
        suspicious_keywords = ['login', 'verify', 'update', 'secure', 'bank', 'gift', 'win', 'تسجيل', 'تحديث', 'دخول']
        suspicious_extensions = ['tk', 'ml', 'ga', 'cf', 'gq', 'xyz', 'top', 'buzz', 'work']

        is_scam = False
        reason = ""

        if ("google" in url_lower or "whatsapp" in url_lower or "absher" in url_lower) and full_domain not in trusted:
            is_scam = True
            reason = f"محاولة انتحال صفة موقع رسمي! النطاق هو ({full_domain}) وليس الأصلي."
        elif ext.suffix in suspicious_extensions:
            is_scam = True
            reason = f"النطاق ({ext.suffix}) مجاني ومجهول ويستخدمه الهكر غالباً."
        elif "@" in url_input or len(url_input) > 80:
            is_scam = True
            reason = "الرابط يحتوي على رموز توجيه مريبة أو طول مريب جداً."
        elif any(word in url_lower for word in suspicious_keywords) and full_domain not in trusted and ext.suffix not in official_suffixes:
            is_scam = True
            reason = "الرابط يطلب بيانات حساسة وهو ليس موقعاً معتمداً."

        # عرض النتائج
        if full_domain in trusted or ext.suffix in official_suffixes:
            st.success(f"✅ آمن وموثوق: هذا موقع رسمي ({full_domain}).")
        elif is_scam:
            st.error(f"❌ تم صيد رابط وهمي! \n\n **السبب:** {reason}")
            st.warning("🚨 نصيحة درع أيمن: لا تدخل أي بيانات شخصية في هذا الرابط!")
        else:
            st.info(f"ℹ️ نتيجة الفحص: الرابط يتبع لنطاق ({full_domain}). كن حذراً.")
    else:
        st.error("⚠️ من فضلك ضع الرابط أولاً!")

# 8. التذييل والعداد (تم تصحيح علامات التنصيص هنا)
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.write(f"📊 تم الصيد والفحص حتى الآن: **{st.session_state.counter}**")
with col2:
    st.markdown("<p style='text-align: left; font-size: 0.8em; color: #555;'>تطوير: أيمن 🦾🛡️</p>", unsafe_allow_html=True)
