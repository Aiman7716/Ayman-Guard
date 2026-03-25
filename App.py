import streamlit as st
import tldextract

st.set_page_config(page_title="درع أيمن الرقمي", page_icon="🛡️")
st.title("🛡️ درع أيمن لحماية الروابط")
st.write("انسخ الرابط الذي تشك فيه وضعه هنا لفحصه فوراً.")

url_input = st.text_input("ضع الرابط هنا:", placeholder="https://example.com")

if st.button("افحص الآن"):
    if url_input:
        ext = tldextract.extract(url_input)
        domain = ext.domain
        full_domain = f"{domain}.{ext.suffix}"
        trusted = ['google.com', 'facebook.com', 'whatsapp.com', 'instagram.com', 'yemencars.com']
        
        if full_domain in trusted:
            st.success(f"✅ آمن: هذا الموقع رسمي ({full_domain})")
        elif "google" in domain and full_domain != "google.com":
            st.error(f"🚨 خطر: انتحال صفة جوجل! النطاق الحقيقي: {full_domain}")
        else:
            st.warning(f"⚠️ انتبه: الموقع غير مسجل في قائمتنا الموثوقة: {full_domain}")
    else:
        st.error("يرجى وضع رابط أولاً!")

st.markdown("---")
st.caption("تم التطوير بواسطة أيمن - خدمة لحماية المجتمع من الاحتيال الرقمي")

