import streamlit as st
import tldextract
from PIL import Image

# إعدادات واجهة الصفحة (احترافية)
st.set_page_config(page_title="درع أيمن الرقمي", page_icon="🛡️", layout="wide")

# تطبيق ثيم "الأسود الملكي"
st.markdown("""
<style>
    body {
        color: #fff;
        background-color: #1a1a1a;
    }
    .main {
        background-color: #1a1a1a;
    }
    .stTextInput>div>div>input {
        background-color: #333;
        color: #fff;
        border: 2px solid #555;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
    }
    .stAlert {
        background-color: #333;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# إضافة الشعار
logo = Image.open('image_14.png')
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo, width=150)
with col2:
    st.title("🛡️ درع أيمن لحماية الروابط")
    st.markdown("---")

st.write("انسخ الرابط الذي تشك فيه وضعه هنا لفحصه فوراً.")

# خانة إدخال الرابط (احترافية)
url_input = st.text_input("ضع الرابط هنا:", placeholder="https://example.com")

if st.button("افحص الآن"):
    if url_input:
        # تحليل الرابط
        ext = tldextract.extract(url_input)
        domain = ext.domain
        suffix = ext.suffix
        full_domain = f"{domain}.{suffix}"
        
        # القائمة البيضاء (المواقع الموثوقة)
        trusted = ['google.com', 'facebook.com', 'whatsapp.com', 'instagram.com', 'yemencars.com', 'saudi.gov.sa']
        suspicious_extensions = ['tk', 'ml', 'ga', 'cf', 'gq', 'xyz']
        shorteners = ['bit.ly', 't.co', 'tinyurl.com']

        if full_domain in trusted:
            st.success(f"✅ آمن: هذا موقع رسمي وموثوق ({full_domain})")
        
        elif suffix in suspicious_extensions:
            st.error(f"🚨 تحذير شديد: هذا الموقع يستخدم نطاقاً مجانياً مشبوهاً ({suffix})...")
            
        elif ("google" in domain or "whatsapp" in domain or "facebook" in domain) and full_domain not in trusted:
            st.error(f"🚨 خطر: انتحال صفة مواقع عالمية! النطاق الحقيقي هو: {full_domain}")
            
        elif full_domain in shorteners:
            st.warning(f"⚠️ انتباه: هذا رابط مختصر ({full_domain})...")
            
        else:
            st.info(f"ℹ️ نتيجة الفحص: الموقع هو ({full_domain})...")
    else:
        st.error("يرجى وضع رابط أولاً!")

st.markdown("---")
st.caption("تم التطوير بواسطة أيمن - خدمة لحماية المجتمع من الاحتيال الرقمي")
