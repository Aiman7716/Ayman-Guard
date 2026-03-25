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
        
        /* إخفاء تام وشامل لكل مسببات كلمة keyboard_ar */
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

# تهيئة السجل
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. محرك الفحص المتطور (كشف الروابط المؤقتة) ---
def advanced_check(url):
    # تنظيف الرابط بعمق
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    # قائمة الاستضافات المؤقتة المشبوهة
    suspicious_hosts = ['mtempurl.com', 'smarterasp.net', '000webhostapp.com', 'free.hr', 'web.app', 'firebaseapp.com']
    
    is_official = u.endswith('.gov.sa') or u.endswith('.gov') or u.endswith('.edu.sa') or u.endswith('.edu')
    is_trusted = domain_full in ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa', 'saudipost.sa', 'moi.gov.sa']
    is_suspicious = any(host in domain_full for host in suspicious_hosts)

    if is_official or is_trusted:
        return "SAFE", domain_full
    elif is_suspicious:
        return "DANGER", domain_full
    else:
        return "UNKNOWN", domain_full

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

user_input = st.text_input("أدخل الرابط للفحص :", key="final_scan_input")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if user_input:
        with st.spinner('جاري التحليل...'):
            time.sleep(0.5)
            status, d_name = advanced_check(user_input)
            
            # تحديث السجل بدون أيقونات مسببة للتداخل
            res_text = "آمن" if status == "SAFE" else "خطر" if status == "DANGER" else "مجهول"
            st.session_state.history.insert(0, f"{res_text}: {d_name}")
            
            if status == "SAFE":
                st.balloons()
                st.success(f"✅ هذا رابط رسمي وموثق: {d_name}")
            elif status == "DANGER":
                st.error(f"🚨 خطر جداً: هذا الرابط مستضاف على خادم مؤقت ({d_name}). لا تفتح الرابط!")
            else:
                st.warning(f"⚠️ تنبيه: الرابط ({d_name}) غير مسجل في قوائمنا الرسمية.")
    else:
        st.error("⚠️ يرجى إدخال الرابط.")

# سجل الفحص بنص صافي
if st.session_state.history:
    with st.expander("🕒 عمليات الفحص الأخيرة"):
        for item in st.session_state.history[:5]:
            st.text(item)

st.divider()

# --- 4. ساحة البلاغات ---
st.subheader("📢 ساحة بلاغات المجتمع")
report_input = st.text_input("رابط المحتال للتبليغ :", key="final_report_input")

if st.button("إرسال البلاغ"):
    if report_input:
        status, d_name = advanced_check(report_input)
        if status == "SAFE":
            st.error(f"❌ لا يمكن التبليغ عن ({d_name}) لأنه جهة رسمية.")
        else:
            st.success("✅ تم استلام بلاغك بنجاح لمراجعته.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
