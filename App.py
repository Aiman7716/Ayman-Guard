import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# --- 2. التنسيق الجمالي الاحترافي ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .main-header { color: #00d4ff; text-align: center; font-size: 2.8rem; font-weight: bold; }
        .stButton > button { 
            background-color: #ff4b4b !important; color: white !important; 
            border-radius: 12px !important; width: 100% !important; height: 3.5em !important; font-weight: bold !important; 
        }
        /* إخفاء التداخلات البرمجية */
        .st-emotion-cache-1kyx60p, .css-1kyx60p { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الواجهة ---
st.markdown('<div class="main-header">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)
st.info("💡 معلومة: الدرع يتعرف الآن تلقائياً على كافة المواقع الحكومية والجامعية السعودية.")

# --- 4. محرك الفحص الذكي (الإضافة المطلوبة) ---
url_input = st.text_input("🔍 ضع رابط الوزارة أو الجامعة هنا :", placeholder="https://example.edu.sa", key="uni_scanner")

if st.button("🚀 افحص الرابط الآن", key="run_check"):
    if url_input:
        with st.spinner('جاري التحقق من التوثيق الرسمي...'):
            time.sleep(1)
            ext = tldextract.extract(url_input.lower())
            domain_suffix = f"{ext.domain}.{ext.suffix}"
            
            # القاعدة الذكية للتعرف التلقائي
            if url_input.lower().endswith('.gov.sa'):
                st.balloons()
                st.success(f"✅ هذا رابط جهة حكومية سعودية رسمية موثوقة.")
            elif url_input.lower().endswith('.edu.sa'):
                st.balloons()
                st.success(f"✅ هذا رابط صرح تعليمي أو جامعة سعودية معتمدة.")
            elif domain_suffix in ['absher.sa', 'iam.gov.sa', 'saudipost.sa', 'splonline.com.sa']:
                st.balloons()
                st.success(f"✅ هذا رابط رسمي موثق ومسجل لدينا.")
            else:
                st.warning("⚠️ تنبيه: هذا الرابط لا ينتهي بالامتدادات الرسمية الموثوقة (.gov.sa) أو (.edu.sa).")
    else:
        st.error("⚠️ يرجى إدخال الرابط أولاً.")

st.markdown("---")

# --- 5. قسم البلاغات ---
st.subheader("📢 بلاغات المجتمع")
with st.expander("أبلغ عن رابط انتحال شخصية"):
    rep_url = st.text_input("الرابط المشبوه :", key="rep_u")
    if st.button("إرسال البلاغ", key="rep_b"):
        st.success("شكراً لك! تم استلام بلاغك بنجاح.")

# التذييل
st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
