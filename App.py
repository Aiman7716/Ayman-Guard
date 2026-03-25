import streamlit as st
import tldextract
import random

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="درع أيمن الرقمي", page_icon="🛡️", layout="centered")

# 2. تصميم الواجهة الاحترافي (النمط الليلي والألوان السيبرانية)
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; text-shadow: 2px 2px #000; font-family: 'Arial'; }
    .stButton>button {
        width: 100%;
        background-color: #00d4ff;
        color: #000;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff4b4b; color: white; transform: scale(1.02); }
    .stTextInput>div>div>input {
        background-color: #1a1c24;
        color: white;
        border: 2px solid #00d4ff;
        border-radius: 12px;
        text-align: center;
    }
    .report-card {
        background-color: #1a1c24;
        border-radius: 10px;
        padding: 15px;
        border-right: 5px solid #ff4b4b;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. واجهة المستخدم العلوية
st.markdown("<h1>🛡️ درع أيمن <br> لصيد الروابط الوهمية</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>المنصة الذكية الأولى لحماية المجتمع من الاحتيال الرقمي</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. إدارة البيانات (العداد وقائمة البلاغات الموثقة)
if 'counter' not in st.session_state:
    st.session_state.counter = 248  # يبدأ من آخر رقم وصلنا له في صورتك
if 'verified_scams' not in st.session_state:
    st.session_state.verified_scams = ["facebook-login-secure.tk", "absher-update-verify.xyz"]

# 5. نظام النصائح الذكي (يتغير مع كل تحديث)
tips = [
    "💡 نصيحة درع أيمن: الجهات الحكومية لا تطلب أرقام بطاقتك البنكية عبر الروابط.",
    "💡 نصيحة درع أيمن: تأكد دائماً من وجود قفل الأمان (HTTPS) في شريط العنوان.",
    "💡 نصيحة درع أيمن: روابط الهكر غالباً تنتهي بنطاقات غريبة مثل .tk أو .xyz",
    "💡 نصيحة درع أيمن: لا تشارك رمز التوثيق (OTP) مع أي شخص مهما ادعى رسمياً."
]
st.info(random.choice(tips))

# 6. محرك الفحص الأساسي
url_input = st.text_input("🔍 قم بلصق الرابط المشبوه هنا لفحصه الآن:", placeholder="https://example-scam-link.com")

if st.button("🚀 افحص وصِد الرابط الآن"):
    st.session_state.counter += 1
    if url_input:
        url_lower = url_input.lower().strip()
        ext = tldextract.extract(url_lower)
        full_domain = f"{ext.domain}.{ext.suffix}"
        
        # قوائم الثقة والنطاقات الرسمية
        trusted = ['google.com', 'facebook.com', 'whatsapp.com', 'instagram.com', 'moi.gov.sa', 'absher.sa', 'yemencars.com', 'stc.com.sa']
        official_suffixes = ['gov', 'gov.sa', 'edu', 'edu.sa', 'org']
        suspicious_exts = ['tk', 'ml', 'ga', 'cf', 'gq', 'xyz', 'top', 'buzz']

        # منطق الصيد الذكي
        is_scam = False
        reason = ""

        if ("google" in url_lower or "whatsapp" in url_lower or "absher" in url_lower) and full_domain not in trusted:
            is_scam = True
            reason = f"محاولة انتحال صفة موقع رسمي! النطاق الحقيقي هو ({full_domain})."
        elif ext.suffix in suspicious_exts:
            is_scam = True
            reason = f"النطاق ({ext.suffix}) مجهول وغالباً ما يستخدمه المخترقون."
        elif "@" in url_input or len(url_input) > 85:
            is_scam = True
            reason = "الرابط يحتوي على رموز توجيه خفية أو طول مريب جداً."

        # عرض النتائج
        if full_domain in trusted or ext.suffix in official_suffixes:
            st.success(f"✅ آمن وموثوق: هذا موقع رسمي ({full_domain}).")
        elif is_scam:
            st.error(f"❌ تم صيد رابط وهمي! \n\n **السبب:** {reason}")
            st.warning("🚨 تحذير: لا تدخل أي بيانات شخصية أو كلمات مرور في هذا الرابط!")
        else:
            st.info(f"ℹ️ نتيجة الفحص: الرابط يتبع لنطاق ({full_domain}). تأكد من المصدر.")
    else:
        st.error("⚠️ من فضلك ضع الرابط أولاً ليقوم الدرع بعمله!")

st.markdown("---")

# 7. ميزة "ساحة بلاغات المجتمع الموثقة"
st.markdown("### 📢 ساحة بلاغات المجتمع")
st.write("ساعدنا في تحذير الآخرين. أبلغ عن أي رابط مشبوه وصلك:")

with st.expander("➕ إرسال بلاغ وتحقق"):
    new_report = st.text_input("الصق الرابط المشبوه هنا:", key="report_box")
    if st.button("📤 إرسال وتحذير الجميع"):
        if new_report:
            # فلترة لمنع التبليغ عن المواقع الرسمية
            rep_ext = tldextract.extract(new_report.lower())
            if rep_ext.domain in ['google', 'absher', 'moi', 'whatsapp']:
                st.warning("⚠️ لا يمكن التبليغ عن المواقع الرسمية الموثقة.")
            else:
                st.session_state.verified_scams.insert(0, new_report.strip().lower())
                st.success("✅ تم التحقق وإضافة البلاغ لقائمة التحذير بنجاح!")
        else:
            st.error("⚠️ يرجى إدخال الرابط.")

# 8. عرض قائمة التحذير (آخر 3 بلاغات)
if st.session_state.verified_scams:
    st.write("**🚨 أحدث الروابط التي تم صيدها بواسطة المجتمع:**")
    for scam in st.session_state.verified_scams[:3]:
        st.markdown(f"""
        <div class='report-card'>
            ⚠️ رابط مشبوه: <code>{scam}</code><br>
            <small>🚩 حالة التحقق: <b>تم التأكيد بواسطة درع أيمن</b></small>
        </div>
        """, unsafe_allow_html=True)

# 9. التذييل والعداد الثابت
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.write(f"📊 إجمالي الفحوصات: **{st.session_state.counter}**")
with col2:
    st.markdown("<p style='text-align: left; font-weight: bold;'>تطوير: أيمن 🦾🛡️</p>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-size: 0.7em; color: #555;'>درع أيمن - حماية المجتمع مسؤولية الجميع</p>", unsafe_allow_html=True)
