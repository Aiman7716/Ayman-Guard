import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة والتنسيق الفني ---
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
        
        /* إخفاء تام لكل مسببات كلمة keyboard_ar */
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

# تهيئة الذاكرة الدائمة (في الجلسة) للبلاغات والفحص
if 'reports_db' not in st.session_state:
    st.session_state.reports_db = {} # لتخزين عدد البلاغات لكل رابط
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. محرك الفحص المتطور ---
def advanced_check(url):
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    suspicious_hosts = ['mtempurl.com', 'smarterasp.net', '000webhostapp.com', 'free.hr', 'web.app']
    
    is_official = u.endswith('.gov.sa') or u.endswith('.gov') or u.endswith('.edu.sa') or u.endswith('.edu')
    is_trusted = domain_full in ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa', 'moi.gov.sa']
    is_suspicious = any(host in domain_full for host in suspicious_hosts)

    if is_official or is_trusted:
        return "SAFE", domain_full
    elif is_suspicious:
        return "DANGER", domain_full
    else:
        return "UNKNOWN", domain_full

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

user_input = st.text_input("أدخل الرابط للفحص :", key="v28_scan")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if user_input:
        status, d_name = advanced_check(user_input)
        
        # ميزة إشعار التكرار: هل هذا الرابط مبلغ عنه؟
        report_count = st.session_state.reports_db.get(d_name, 0)
        
        with st.spinner('جاري التحليل...'):
            time.sleep(0.5)
            res_text = "آمن" if status == "SAFE" else "خطر" if status == "DANGER" else "مجهول"
            st.session_state.history.insert(0, f"{res_text}: {d_name}")
            
            if status == "SAFE":
                st.balloons()
                st.success(f"✅ هذا رابط رسمي وموثوق: {d_name}")
            else:
                if report_count > 0:
                    st.error(f"🚨 تنبيه عاجل: هذا الرابط تم التبليغ عنه {report_count} مرّات سابقة من قبل المجتمع!")
                
                if status == "DANGER":
                    st.error(f"🛑 خطر: هذا الرابط مستضاف على خادم مؤقت ({d_name}). لا تفتحه!")
                else:
                    st.warning(f"⚠️ تنبيه: الرابط ({d_name}) غير مسجل رسمياً.")
    else:
        st.error("⚠️ يرجى إدخال الرابط.")

# سجل الفحص
if st.session_state.history:
    with st.expander("🕒 عمليات الفحص الأخيرة"):
        for item in st.session_state.history[:5]:
            st.text(item)

st.divider()

# --- 4. ساحة البلاغات مع نظام العد التكراري ---
st.subheader("📢 ساحة بلاغات المجتمع")
report_input = st.text_input("رابط المحتال للتبليغ :", key="v28_report")

if st.button("إرسال البلاغ"):
    if report_input:
        status, d_name = advanced_check(report_input)
        if status == "SAFE":
            st.error(f"❌ لا يمكن التبليغ عن ({d_name}) لأنه صرح رسمي!")
        else:
            # تحديث قاعدة بيانات البلاغات
            st.session_state.reports_db[d_name] = st.session_state.reports_db.get(d_name, 0) + 1
            st.success(f"✅ تم استلام بلاغك عن ({d_name}). شكراً لمساهمتك في حماية المجتمع يا أيمن!")
    else:
        st.warning("⚠️ أدخل الرابط أولاً.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
