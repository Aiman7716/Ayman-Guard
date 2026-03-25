import streamlit as st
import tldextract

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="درع أيمن الرقمي", page_icon="🛡️", layout="centered")

# 2. تصميم الواجهة (الأسود الملكي والألوان الاحترافية)
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; font-family: 'Arial'; }
    .stButton>button {
        width: 100%;
        background-color: #00d4ff;
        color: #000;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 10px;
    }
    .stTextInput>div>div>input {
        background-color: #1a1c24;
        color: white;
        border: 1px solid #00d4ff;
        border-radius: 10px;
        text-align: center;
    }
    .stAlert { border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# 3. العنوان والشعار
st.markdown("<h1>🛡️ درع أيمن <br> لحماية الروابط</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>أداة ذكية لفحص الروابط وحمايتك من الاحتيال الرقمي</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. إدارة العداد (Session State)
if 'counter' not in st.session_state:
    st.session_state.counter = 150

# 5. خانة المدخلات
url_input = st.text_input("قم بلصق الرابط المشبوه هنا:", placeholder="https://example.com")

# 6. زر الفحص ومنطق المعالجة
if st.button("🚀 افحص الرابط الآن"):
    # زيادة العداد عند الضغط
    st.session_state.counter += 1
    
    if url_input:
        # تنظيف الرابط واستخراج النطاق
        ext = tldextract.extract(url_input)
        full_domain = f"{ext.domain}.{ext.suffix}"
        
        # القوائم البرمجية
        trusted = ['google.com', 'facebook.com', 'whatsapp.com', 'instagram.com', 'youtube.com', 'yemencars.com', 'ayman-guard-ntmpb.streamlit.app']
        suspicious_extensions = ['tk', 'ml', 'ga', 'cf', 'gq', 'xyz']
        shorteners = ['bit.ly', 't.co', 'tinyurl.com']

        # معايير الفحص
        if full_domain in trusted:
            st.success(f"✅ آمن: هذا موقع رسمي وموثوق ({full_domain})")
        elif ext.suffix in suspicious_extensions:
            st.error(f"🚨 تحذير شديد: هذا الرابط يستخدم نطاقاً مجانياً ({ext.suffix}) يُستخدم غالباً في الاختراق!")
        elif ("google" in url_input or "whatsapp" in url_input or "facebook" in url_input) and full_domain not in trusted:
            st.error(f"⚠️ خطر: محاولة انتحال صفة! هذا ليس موقع {full_domain} الرسمي.")
        elif full_domain in shorteners:
            st.warning(f"⚠️ انتباه: هذا رابط مختصر قد يخفي خلفه محتوى ضار.")
        else:
            st.info(f"ℹ️ نتيجة الفحص: الرابط يتبع لنطاق ({full_domain}). تأكد من مصدره.")
    else:
        st.error("⚠️ من فضلك ضع الرابط أولاً!")

# 7. التذييل والعداد
st.markdown("---")
st.write(f"📊 تم فحص **{st.session_state.counter}** رابطاً حتى الآن بواسطة درع أيمن.")
st.markdown("<p style='text-align: center; font-size: 0.8em; color: #555;'>تم التطوير بواسطة أيمن 🦾 | خدمة لحماية المجتمع</p>", unsafe_allow_html=True)
