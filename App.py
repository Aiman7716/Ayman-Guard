import streamlit as st
import tldextract
import random

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="درع أيمن الرقمي", page_icon="🛡️", layout="centered")

# 2. تصميم الواجهة المتقدم (CSS)
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
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    .official-card {
        background: linear-gradient(90deg, #0e1117 0%, #1a1c24 100%);
        border: 1px solid #00d4ff;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 3. واجهة المستخدم العلوية
st.markdown("<h1>🛡️ درع أيمن الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>المنصة الأولى لحماية المجتمع من الاحتيال الرقمي</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. إدارة البيانات (العداد والبلاغات)
if 'counter' not in st.session_state:
    st.session_state.counter = 250
if 'verified_scams' not in st.session_state:
    st.session_state.verified_scams = ["facebook-login-secure.tk", "absher-update-verify.xyz"]

# 5. نظام النصائح المتغير
tips = [
    "💡 نصيحة: تأكد من وجود (HTTPS) وقفل الأمان في شريط العنوان.",
    "💡 نصيحة: لا تضغط على روابط الجوائز التي تصلك من أرقام مجهولة.",
    "💡 نصيحة: رمز التوثيق (OTP) سرّي للغاية، لا تطلبه منك أي جهة رسمية.",
    "💡 نصيحة: روابط الهكر غالباً تنتهي بنطاقات غريبة مثل .tk أو .xyz"
]
st.info(random.choice(tips))

# 6. محرك الفحص الأساسي
url_input = st.text_input("🔍 قم بلصق الرابط المشبوه هنا لفحصه:", placeholder="https://example-scam-link.com")

if st.button("🚀 افحص وصِد الرابط الآن"):
    st.session_state.counter += 1
    if url_input:
        url_lower = url_input.lower().strip()
        ext = tldextract.extract(url_lower)
        full_domain = f"{ext.domain}.{ext.suffix}"
        
        # قوائم الثقة والنطاقات الرسمية
        trusted = ['google.com', 'facebook.com', 'whatsapp.com', 'instagram.com', 'moi.gov.sa', 'absher.sa', 'yemencars.com', 'stc.com.sa', 'iam.gov.sa', 'splonline.com.sa']
        official_suffixes = ['gov', 'gov.sa', 'edu', 'edu.sa', 'org']
        suspicious_exts = ['tk', 'ml', 'ga', 'cf', 'gq', 'xyz', 'top', 'buzz', 'work']

        # منطق الصيد
        is_scam = False
        reason = ""

        if ("google" in url_lower or "whatsapp" in url_lower or "absher" in url_lower or "nafath" in url_lower) and full_domain not in trusted:
            is_scam = True
            reason = f"محاولة انتحال صفة موقع رسمي! النطاق الحقيقي هو ({full_domain})."
        elif ext.suffix in suspicious_exts:
            is_scam = True
            reason = f"النطاق ({ext.suffix}) مجهول وغير موثوق، وغالباً ما يستخدمه المخترقون."
        elif "@" in url_input or len(url_input) > 85:
            is_scam = True
            reason = "الرابط يحتوي على رموز توجيه مريبة أو طول مبالغ فيه لإخفاء الهوية."

        # عرض النتائج
        if full_domain in trusted or ext.suffix in official_suffixes:
            st.success(f"✅ آمن وموثوق: هذا موقع رسمي ({full_domain}).")
        elif is_scam:
            st.error(f"❌ تم صيد رابط وهمي! \n\n **السبب:** {reason}")
            st.warning("🚨 تحذير: لا تدخل أي بيانات شخصية في هذا الرابط أبداً!")
        else:
            st.info(f"ℹ️ نتيجة الفحص: الرابط يتبع لنطاق ({full_domain}). تأكد من المصدر بعناية.")
    else:
        st.error("⚠️ من فضلك ضع الرابط أولاً!")

st.markdown("---")

# 7. ساحة بلاغات المجتمع الموثقة
st.markdown("### 📢 ساحة بلاغات المجتمع")
with st.expander("➕ إرسال بلاغ وتحقق"):
    new_report = st.text_input("أدخل الرابط المشبوه هنا:", key="report_box")
    if st.button("📤 إرسال وتحذير الجميع"):
        if new_report:
            rep_ext = tldextract.extract(new_report.lower())
            if rep_ext.domain in ['google', 'absher', 'moi', 'whatsapp', 'iam', 'splonline']:
                st.warning("⚠️ لا يمكن التبليغ عن المواقع الرسمية الموثقة.")
            else:
                st.session_state.verified_scams.insert(0, new_report.strip().lower())
                st.success("✅ تم التحقق وإضافة البلاغ بنجاح!")
        else:
            st.error("⚠️ يرجى إدخال الرابط.")

if st.session_state.verified_scams:
    st.write("**🚨 أحدث الروابط التي تم التبليغ عنها:**")
    for scam in st.session_state.verified_scams[:3]:
        st.markdown(f"<div class='report-card'>⚠️ رابط مشبوه: <code>{scam}</code> <br><small>🚩 حالة التحقق: تم التأكيد بواسطة درع أيمن</small></div>", unsafe_allow_html=True)

# 8. التحديث الجديد: قسم الروابط المرجعية الرسمية
st.markdown("---")
st.markdown("### 🏛️ المرجع الآمن للروابط الرسمية")
st.write("استخدم هذه الروابط دائماً للوصول للخدمات الحكومية بأمان:")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='official-card'>🇸🇦 أبشر<br><a href='https://www.absher.sa' style='color:#00d4ff; text-decoration:none;'>انقر هنا</a></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='official-card'>🔑 نفاذ<br><a href='https://iam.gov.sa' style='color:#00d4ff; text-decoration:none;'>انقر هنا</a></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='official-card'>📦 البريد<br><a href='https://splonline.com.sa' style='color:#00d4ff; text-decoration:none;'>انقر هنا</a></div>", unsafe_allow_html=True)

# 9. التذييل
st.markdown("---")
col_stat, col_dev = st.columns(2)
with col_stat:
    st.write(f"📊 إجمالي الفحوصات: **{st.session_state.counter}**")
with col_dev:
    st.markdown("<p style='text-align: left; font-weight: bold;'>تطوير: أيمن 🦾🛡️</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 0.7em; color: #555;'>درع أيمن - حماية المجتمع مسؤولية الجميع</p>", unsafe_allow_html=True)
