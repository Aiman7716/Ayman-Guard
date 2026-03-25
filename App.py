import streamlit as st
import tldextract

# إعدادات واجهة الصفحة
st.set_page_config(page_title="درع أيمن الرقمي", page_icon="🛡️")
st.title("🛡️ درع أيمن لحماية الروابط")
st.markdown("---")

st.write("انسخ الرابط الذي تشك فيه وضعه هنا لفحصه فوراً.")

# خانة إدخال الرابط
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
        # القائمة السوداء (نطاقات مشبوهة وروابط اختصار)
        suspicious_extensions = ['tk', 'ml', 'ga', 'cf', 'gq', 'xyz']
        shorteners = ['bit.ly', 't.co', 'tinyurl.com']

        if full_domain in trusted:
            st.success(f"✅ آمن: هذا موقع رسمي وموثوق ({full_domain})")
        
        elif suffix in suspicious_extensions:
            st.error(f"🚨 تحذير شديد: هذا الموقع يستخدم نطاقاً مجانياً مشبوهاً ({suffix}) وغالباً ما يُستخدم في الاحتيال!")
            
        elif ("google" in domain or "whatsapp" in domain or "facebook" in domain) and full_domain not in trusted:
            st.error(f"🚨 خطر: انتحال صفة مواقع عالمية! النطاق الحقيقي هو: {full_domain}")
            
        elif full_domain in shorteners:
            st.warning(f"⚠️ انتباه: هذا رابط مختصر ({full_domain}). الروابط المختصرة قد تخفي خلفها مواقع ضارة.")
            
        else:
            st.info(f"ℹ️ نتيجة الفحص: الموقع هو ({full_domain}). إذا لم تكن تتوقع هذا الرابط، فننصح بالحذر.")
    else:
        st.error("يرجى وضع رابط أولاً!")

st.markdown("---")
st.caption("تم التطوير بواسطة أيمن - خدمة لحماية المجتمع من الاحتيال الرقمي")
