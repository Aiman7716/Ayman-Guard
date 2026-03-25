import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# --- 2. CSS احترافي صلب (يمنع أي تداخل خارجي) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        /* ضبط الخط والاتجاه */
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }

        /* تنسيق العنوان الكبير */
        .header-text {
            color: #00d4ff;
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 20px;
        }

        /* تنسيق الأزرار الحمراء لمنع تداخل keyboard_ar */
        div.stButton > button {
            background-color: #ff4b4b !important;
            color: white !important;
            border-radius: 12px !important;
            width: 100% !important;
            height: 3.5em !important;
            font-weight: bold !important;
            border: none !important;
        }

        /* إخفاء أي رموز غريبة أو أيقونات متداخلة */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, .css-1kyx60p {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. قاعدة البيانات الذكية ---
OFFICIAL_DOMAINS = [
    'absher.sa', 'iam.gov.sa', 'splonline.com.sa', 'moe.gov.sa', 
    'moj.gov.sa', 'hrsd.gov.sa', 'zatca.gov.sa', 'moh.gov.sa',
    'saudipost.sa', 'stc.com.sa', 'tawakkalna.gov.sa', 'najm.sa'
]

# --- 4. الواجهة الرئيسية ---
st.markdown('<div class="header-text">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# صندوق النصيحة بتصميم نظيف
st.info("💡 نصيحة درع أيمن: المواقع الرسمية الحكومية تنتهي دائماً بـ (.gov.sa) أو (.sa).")

# حقل الفحص
url_to_check = st.text_input("🔍 قم بلصق الرابط المشبوه هنا :", placeholder="https://example.com", key="main_scanner")

if st.button("🚀 افحص وصِد الرابط الآن", key="check_btn"):
    if url_to_check:
        with st.spinner('جاري التحقق من هوية الرابط...'):
            time.sleep(1)
            ext = tldextract.extract(url_to_check.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            
            if domain in OFFICIAL_DOMAINS or domain.endswith('.gov.sa'):
                st.balloons()
                st.success(f"✅ هذا رابط رسمي وموثوق: ({domain})")
            elif ext.suffix in ['tk', 'xyz', 'ml', 'cf', 'gq', 'top']:
                st.error("🚨 تحذير: هذا النطاق مشبوه وغير آمن!")
            else:
                st.warning(f"⚠️ الرابط ({domain}) غير مدرج كجهة رسمية، تعامل معه بحذر.")
    else:
        st.warning("⚠️ فضلاً، أدخل الرابط أولاً.")

st.markdown("---")

# --- 5. قسم البلاغات (تم إصلاح التداخل هنا) ---
st.subheader("📢 ساحة بلاغات المجتمع")

with st.container():
    st.write("ساعدنا في تحذير الآخرين من الروابط المحتالة:")
    scam_url = st.text_input("رابط الموقع المشبوه :", key="report_url")
    scam_type = st.selectbox("نوع الاحتيال:", 
                            ["انتحال شخصية أبشر", "جائزة وهمية", "تحديث بنكي", "شحنة بريدية"], 
                            key="report_type")
    
    if st.button("✅ تأكيد إرسال البلاغ", key="report_btn"):
        if scam_url:
            st.success("تم استلام بلاغك بنجاح! شكراً لمساهمتك في حماية المجتمع.")
        else:
            st.error("❌ يرجى كتابة الرابط أولاً.")

st.markdown("<br><br>", unsafe_allow_html=True)

# التذييل
st.markdown(f"""
    <div style='text-align: center; border-top: 1px solid #eee; padding-top: 20px;'>
        <p>🏛️ <b>روابط سريعة:</b> <a href='https://absher.sa'>أبشر</a> | <a href='https://iam.gov.sa'>نفاذ</a></p>
        <p style='color: #888;'>📊 تطوير المهندس: أيمن 🦾</p>
    </div>
""", unsafe_allow_html=True)
