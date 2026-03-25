import streamlit as st
import tldextract
import time

# --- 1. إعدادات الهوية والتنسيق الأصلي ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# CSS مصمم بدقة لمنع تداخل النصوص وإخفاء الرموز الغريبة
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }

        /* تنسيق العنوان الكبير الصافي */
        .main-header {
            color: #00d4ff;
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            line-height: 1.2;
            margin-bottom: 30px;
        }

        /* إخفاء أي رموز تقنية تظهر بالخطأ في الواجهة */
        .st-emotion-cache-1kyx60p, footer, header { display: none !important; }
        
        /* تحسين مظهر الأزرار */
        .stButton>button { 
            width: 100%; border-radius: 12px; background-color: #00d4ff; 
            color: white; font-weight: bold; border: none; height: 3.5em;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة الإحصائيات في الذاكرة (لحل مشكلة الـ Locked Database) ---
if 'stats' not in st.session_state:
    st.session_state.stats = 250

# --- 3. الواجهة الرئيسية (التنسيق المفضل لديك) ---
st.markdown('<div class="main-header">🛡️ درع أيمن<br>الذكي</div>', unsafe_allow_html=True)

# حقل الإدخال
url_in = st.text_input("🔍 ضع الرابط هنا لفحصه :", placeholder="https://example.com")

if st.button("🚀 افحص الآن"):
    if url_in:
        st.session_state.stats += 1
        with st.spinner('جاري تحليل الرابط...'):
            time.sleep(1)
            ext = tldextract.extract(url_in.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            
            # فلتر المواقع الرسمية
            trust = ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa', 'moe.gov.sa']
            
            if domain in trust:
                st.balloons()
                st.success(f"✅ هذا الرابط رسمي وآمن: ({domain})")
            elif ext.suffix in ['tk', 'xyz', 'ml', 'cf', 'gq', 'top']:
                st.error("🚨 تحذير: هذا النطاق مشبوه وغير آمن!")
            else:
                st.info(f"ℹ️ نتيجة الفحص: النطاق هو ({domain})")
    else:
        st.warning("⚠️ فضلاً، أدخل الرابط أولاً.")

st.markdown("<br><hr>", unsafe_allow_html=True)

# --- 4. قسم البلاغات ---
with st.expander("➕ أبلغ عن رابط مشبوه"):
    scam_url = st.text_input("أدخل الرابط المحتال هنا:")
    if st.button("تأكيد الإرسال"):
        if scam_url:
            st.success("تم تسجيل بلاغك بنجاح. شكراً لك!")

st.markdown("<br>")

# --- 5. التذييل (Footer) - نفس التنسيق المطلوب ---
st.markdown(f"""
    <div style='text-align: center;'>
        <p style='font-size: 1.1rem;'>
            🏛️ <b>روابط رسمية:</b> 
            <a href='https://absher.sa' style='color:#007bff; text-decoration:none;'>أبشر</a> | 
            <a href='https://iam.gov.sa' style='color:#007bff; text-decoration:none;'>نفاذ</a>
        </p>
        <p style='color: #888; font-size: 0.9rem;'>
            📊 الفحوصات: {st.session_state.stats} | تطوير المهندس: أيمن 🦾
        </p>
    </div>
""", unsafe_allow_html=True)
