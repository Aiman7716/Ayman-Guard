import streamlit as st
import tldextract
import time
import random

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# --- 2. CSS "التطهير الشامل" لمنع تداخل keyboard_ar ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }

        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; margin-bottom: 20px; }
        
        /* تنسيق زر الفحص الأحمر */
        div.stButton > button {
            background-color: #ff4b4b !important; color: white !important;
            border-radius: 12px !important; width: 100% !important; 
            height: 3.8em !important; font-weight: bold !important; border: none !important;
        }

        /* منع ظهور أي رموز غريبة أو تداخل نصوص */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol {
            display: none !important; visibility: hidden !important;
        }
        
        .stTextInput input { border: 2px solid #00d4ff !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# توليد مفاتيح متغيرة لكل جلسة لمنع الكاش (Cache)
if 'session_key' not in st.session_state:
    st.session_state.session_key = random.randint(1000, 9999)

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

st.info("💡 معلومة: الدرع يتعرف الآن تلقائياً على كافة المواقع الحكومية والجامعية السعودية.")

# منطقة الفحص (استخدام مفتاح فريد لمنع التداخل)
url_input = st.text_input("🔍 ضع الرابط هنا (وزارة أو جامعة) :", 
                          placeholder="https://example.edu.sa", 
                          key=f"scanner_{st.session_state.session_key}")

if st.button("🚀 افحص الرابط الآن", key=f"btn_{st.session_state.session_key}"):
    if url_input:
        with st.spinner('جاري التحقق...'):
            time.sleep(1)
            ext = tldextract.extract(url_input.lower())
            
            # محرك التعرف الذكي
            if url_input.lower().endswith('.gov.sa'):
                st.balloons()
                st.success("✅ تم التحقق: هذا رابط حكومي سعودي رسمي موثوق.")
            elif url_input.lower().endswith('.edu.sa'):
                st.balloons()
                st.success("✅ تم التحقق: هذا رابط جامعة أو صرح تعليمي معتمد.")
            elif f"{ext.domain}.{ext.suffix}" in ['absher.sa', 'iam.gov.sa', 'saudipost.sa']:
                st.balloons()
                st.success("✅ تم التحقق: هذا رابط رسمي موثق ومسجل.")
            else:
                st.warning("⚠️ تنبيه: الرابط لا ينتمي للنطاقات الرسمية الحكومية أو الجامعية.")
    else:
        st.error("⚠️ فضلاً، أدخل الرابط أولاً.")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 4. ساحة البلاغات (تصميم نظيف تماماً) ---
st.subheader("📢 بلاغات المجتمع")

# وضع حقل البلاغات داخل حاوية مستقلة
with st.container():
    st.write("أبلغ عن الروابط المشبوهة لحماية الآخرين:")
    scam_url = st.text_input("رابط الموقع المحتال :", key=f"scam_{st.session_state.session_key}")
    
    if st.button("✅ إرسال البلاغ الآن", key=f"send_{st.session_state.session_key}"):
        if scam_url:
            st.success("تم استلام بلاغك بنجاح! شكراً لمساهمتك.")
        else:
            st.error("❌ يرجى كتابة الرابط أولاً.")

st.markdown("<br><p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
