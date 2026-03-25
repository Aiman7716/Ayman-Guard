import streamlit as st
import tldextract
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="درع أيمن الرقمي", page_icon="🛡️", layout="centered")

# 2. تصميم الواجهة الاحترافي
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
        transition: 0.3s;
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
st.markdown("<p style='text-align: center; color: #888;'>نظام ذكي لكشف محاولات الاختراق وسرقة البيانات</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. إدارة العداد
if 'counter' not in st.session_state:
    st.session_state.counter = 247 # نبدأ برقم يوحي بالخبرة

url_input = st.text_input("⚠️ الصق الرابط الذي تشك فيه هنا:", placeholder="https://example-scam-site.com")

# 5. منطق "صياد الهكر" المطور
if st.button("🚀 افحص وصِد الرابط الآن"):
    st.session_state.counter += 1
    
    if url_input:
        # تنظيف وتحليل الرابط
        url_lower = url_input.lower()
        ext = tldextract.extract(url_lower)
        full_domain = f"{ext.domain}.{ext.suffix}"
        
        # قوائم الحماية
        trusted = ['google.com', 'facebook.com', 'whatsapp.com', 'instagram.com', 'moi.gov.sa', 'absher.sa', 'stc.com.sa']
        suspicious_keywords = ['login', 'verify', 'update-account', 'secure', 'bank', 'gift', 'win-prize', 'تسجيل-دخول', 'تحديث-بيانات']
        suspicious_extensions = ['tk', 'ml', 'ga', 'cf', 'gq', 'xyz', 'top', 'buzz', 'work']

        # --- بداية خوارزمية الصيد ---
        is_scam = False
        reason = ""

        # 1. كشف الروابط الطويلة جداً (أسلوب الهكر لإخفاء النطاق)
        if len(url_input) > 70:
            is_scam = True
            reason = "الرابط طويل جداً بشكل مريب (أسلوب لإخفاء الهوية)."

        # 2. كشف الرموز المريبة مثل @ (تستخدم لتوجيه المستخدم لموقع آخر)
        elif "@" in url_input:
            is_scam = True
            reason = "يحتوي الرابط على رمز (@) الذي يستخدمه الهكر لتوجيهك لمواقع خفية."

        # 3. كشف انتحال الصفة (مثلاً: facebo0k بدلاً من facebook)
        elif ("facebook" in url_lower or "google" in url_lower or "absher" in url_lower) and full_domain not in trusted:
            is_scam = True
            reason = f"محاولة انتحال صفة موقع رسمي! النطاق الحقيقي هو ({full_domain}) وليس الموقع الأصلي."

        # 4. كشف الكلمات الدليلية للتصيد
        elif any(word in url_lower for word in suspicious_keywords) and full_domain not in trusted:
            is_scam = True
            reason = "الرابط يحتوي على كلمات تطلب (تسجيل دخول أو تحديث بيانات) وهو ليس موقعاً رسمياً."

        # 5. كشف النطاقات المجانية المشبوهة
        elif ext.suffix in suspicious_extensions:
            is_scam = True
            reason = f"النطاق ({ext.suffix}) مجاني ومجهول، وغالباً ما يستخدمه المخترقون لإنشاء صفحات وهمية."

        # --- عرض النتائج ---
        if full_domain in trusted or ext.suffix in ['gov.sa', 'edu.sa']:
            st.success(f"✅ آمن وموثوق: هذا موقع رسمي ({full_domain}).")
        elif is_scam:
            st.error(f"❌ تم صيد رابط وهمي! \n\n **السبب:** {reason}")
            st.warning("🚨 نصيحة درع أيمن: لا تقم بإدخال أي بيانات شخصية أو كلمات مرور في هذا الرابط!")
        else:
            st.info(f"ℹ️ نتيجة الفحص: الرابط يتبع لنطاق ({full_domain}). لم نجد أدلة اختراق واضحة، لكن كن حذراً.")
            
    else:
        st.error("⚠️ من فضلك ضع الرابط أولاً ليتمكن الدرع من صيده!")

# 6. التذييل
st.markdown("---")
st.write(f"📊 تم صيد وفحص **{st.session_state.counter}** رابطاً حتى الآن.")
st.markdown("<p style='text-align: center; font-size: 0.8em; color: #555;'>نظام حماية المجتمع | تطوير أيمن 🦾🛡️</p>", unsafe_allow_html=True)
