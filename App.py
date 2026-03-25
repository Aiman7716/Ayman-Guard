import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة والتنسيق الفائق ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        
        /* إخفاء تام وشامل لمنع تداخل كلمة keyboard_ar نهائياً */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"] { 
            display: none !important; 
            visibility: hidden !important; 
        }
        
        div.stButton > button {
            background-color: #ff4b4b !important; color: white !important;
            border-radius: 12px !important; width: 100% !important; height: 3.5em !important;
        }
    </style>
""", unsafe_allow_html=True)

# تهيئة الذاكرة
if 'reports_db' not in st.session_state: st.session_state.reports_db = {}
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. محرك الفحص الأمني الذكي ---
def security_scan(url):
    # تنظيف الرابط بعمق لضمان التعرف الصحيح
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    # قائمة الاستثناءات والموثوقية
    friend_link = "alhossam7710140-001-site1.mtempurl.com" # استثناء رابط صديقك
    official_sa = u.endswith('.gov.sa') or u.endswith('.edu.sa')
    trusted_list = ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa', 'moi.gov.sa', 'saudipost.sa']
    
    # مؤشرات الخطر والاختراق
    danger_hosts = ['mtempurl.com', 'smarterasp.net', '000webhostapp.com', 'free.hr']
    phishing_keys = ['login', 'verify', 'update-absher', 'bank-check']
    
    # منطق التصنيف
    if friend_link in u: # الاستثناء البرمجي لرابط صديقك
        return "TRUSTED_SYSTEM", domain_full
    elif official_sa or domain_full in trusted_list:
        return "SAFE", domain_full
    elif any(host in domain_full for host in danger_hosts) or any(key in u for key in phishing_keys):
        return "DANGER", domain_full
    else:
        return "UNKNOWN", domain_full

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

u_input = st.text_input("أدخل الرابط للفحص الأمني الشامل :", key="v30_input")

if st.button("🚀 افحص وصِد الاختراق الآن"):
    if u_input:
        with st.spinner('جاري المسح الأمني...'):
            time.sleep(0.5)
            status, d_name = security_scan(u_input)
            report_count = st.session_state.reports_db.get(d_name, 0)
            
            # تسجيل في السجل النظيف
            st.session_state.history.insert(0, f"{status}: {d_name}")
            
            if status == "TRUSTED_SYSTEM":
                st.balloons()
                st.info(f"🔹 نظام موثوق ومسجل (مشروع صديق أيمن): {d_name}")
            elif status == "SAFE":
                st.balloons()
                st.success(f"✅ رابط رسمي وموثوق: {d_name}")
            elif status == "DANGER":
                st.error(f"🚨 تحذير اختراق: هذا الرابط مشبوه جداً ({d_name}).")
                if report_count > 0: st.error(f"⚠️ تم التبليغ عن هذا الرابط {report_count} مرّات سابقة!")
            else:
                st.warning(f"⚠️ رابط مجهول: ({d_name}) تعامل معه بحذر.")
    else:
        st.error("⚠️ يرجى إدخال الرابط أولاً.")

# عرض السجل بدون تداخل keyboard_ar
if st.session_state.history:
    with st.expander("🕒 عمليات الفحص الأخيرة"):
        for item in st.session_state.history[:5]:
            st.text(item)

st.divider()

# --- 4. ساحة البلاغات ---
st.subheader("📢 ساحة بلاغات المجتمع")
r_input = st.text_input("أدخل الرابط المحتال للتبليغ :", key="v30_report")

if st.button("إرسال البلاغ"):
    if r_input:
        status, d_name = security_scan(r_input)
        if status in ["SAFE", "TRUSTED_SYSTEM"]:
            st.error(f"❌ خطأ: لا يمكن التبليغ عن ({d_name}) لأنه صرح موثوق!")
        else:
            st.session_state.reports_db[d_name] = st.session_state.reports_db.get(d_name, 0) + 1
            st.success(f"✅ شكرًا لك يا أيمن، تم تسجيل بلاغك بنجاح.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
