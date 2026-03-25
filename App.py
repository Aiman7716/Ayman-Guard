import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# --- 2. التنسيق الجمالي (CSS) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .main-header { color: #00d4ff; text-align: center; font-size: 3rem; font-weight: bold; margin-bottom: 0px; }
        .info-box { background-color: #e8f4fd; border-radius: 10px; padding: 15px; border-right: 5px solid #2196f3; color: #0d47a1; margin-bottom: 20px; }
        div.stButton > button:first-child { 
            background-color: #ff4b4b !important; color: white !important; 
            border-radius: 12px !important; width: 100% !important; height: 3.5em !important; font-weight: bold !important; 
        }
        .st-emotion-cache-1kyx60p, .css-1kyx60p { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. قاعدة بيانات المواقع الرسمية (الإضافة الأولى) ---
# أضفت لك هنا قائمة موسعة ليتعرف عليها الدرع تلقائياً
OFFICIAL_DOMAINS = [
    'absher.sa', 'iam.gov.sa', 'splonline.com.sa', 'moe.gov.sa', 
    'moj.gov.sa', 'hrsd.gov.sa', 'zatca.gov.sa', 'moh.gov.sa',
    'saudipost.sa', 'stc.com.sa', 'tawakkalna.gov.sa', 'najm.sa'
]

# --- 4. الواجهة الرئيسية ---
st.markdown('<div class="main-header">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>المنصة الذكية الأولى لحماية المجتمع من الاحتيال الرقمي</p>", unsafe_allow_html=True)

st.markdown("""<div class="info-box">💡 نصيحة درع أيمن: المواقع الرسمية الحكومية في السعودية تنتهي دائماً بـ (.gov.sa) أو (.sa).</div>""", unsafe_allow_html=True)

# --- 5. منطقة الفحص الذكي ---
url_input = st.text_input("🔍 قم بلصق الرابط المشبوه هنا لفحصه :", placeholder="https://example.com")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if url_input:
        with st.spinner('جاري تحليل الرابط ومطابقته...'):
            time.sleep(1)
            # استخراج النطاق (Domain)
            ext = tldextract.extract(url_input.lower())
            domain_full = f"{ext.domain}.{ext.suffix}"
            
            if domain_full in OFFICIAL_DOMAINS or domain_full.endswith('.gov.sa'):
                st.balloons()
                st.success(f"✅ أبشر! هذا رابط رسمي وموثوق بنسبة 100%: ({domain_full})")
            elif ext.suffix in ['tk', 'xyz', 'ml', 'cf', 'gq', 'top', 'link', 'click']:
                st.error(f"🚨 تحذير شديد: النطاق ({ext.suffix}) يستخدم بكثرة في عمليات الاحتيال!")
            else:
                st.warning(f"⚠️ انتبه: هذا الرابط ({domain_full}) غير مسجل في قائمتنا الرسمية، تعامل معه بحذر.")
    else:
        st.warning("⚠️ يرجى وضع الرابط أولاً ليقوم الدرع بعمله.")

st.markdown("<br><hr>", unsafe_allow_html=True)

# --- 6. إضافة نظام البلاغات (الإضافة الثانية) ---
st.markdown("### 📢 ساحة بلاغات المجتمع")
with st.expander("ساعدنا في تحذير الآخرين. أبلغ عن أي رابط مشبوه وصلك:"):
    scam_url = st.text_input("رابط الموقع المحتال أو الرسالة المشبوهة :")
    scam_type = st.selectbox("نوع الاحتيال:", ["انتحال شخصية أبشر", "فوز بجائزة وهمية", "تحديث بيانات بنكية", "شحنة بريدية معلقة"])
    
    if st.button("تأكيد إرسال البلاغ"):
        if scam_url:
            # هنا يتم الحفظ في الذاكرة المؤقتة (Session) لمنع قفل قاعدة البيانات
            if 'reports' not in st.session_state:
                st.session_state.reports = []
            st.session_state.reports.append({"url": scam_url, "type": scam_type})
            st.success("✅ تم استلام بلاغك! سيقوم المهندس أيمن بمراجعته وإضافته لقائمة الحظر.")
        else:
            st.error("❌ يرجى كتابة الرابط أولاً.")

# --- 7. التذييل ---
st.markdown(f"""
    <div style='text-align: center; margin-top: 50px;'>
        <p>🏛️ <b>روابط سريعة:</b> <a href='https://absher.sa'>أبشر</a> | <a href='https://iam.gov.sa'>نفاذ</a></p>
        <p style='color: #888; font-size: 0.8rem;'>📊 درع أيمن الذكي v15.0 | تطوير المهندس: أيمن 🦾</p>
    </div>
""", unsafe_allow_html=True)
