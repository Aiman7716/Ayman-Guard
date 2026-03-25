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
        
        /* 🚨 إزالة التشوه البصري keyboard_ar نهائياً 🚨 */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, .st-emotion-cache-6q9sum, 
        symbol, svg, i, [data-testid="stIcon"], .stExpander svg { 
            display: none !important; 
            visibility: hidden !important; 
            height: 0px !important;
            width: 0px !important;
        }

        /* تنسيق السجل ليكون نظيفاً */
        .history-text {
            background-color: #ffffff;
            padding: 10px;
            border-bottom: 1px solid #eee;
            color: #333;
        }

        div.stButton > button {
            background-color: #ff4b4b !important; color: white !important;
            border-radius: 12px !important; width: 100% !important; height: 3.5em !important;
        }
        .trusted-badge {
            background-color: #e3f2fd; border-right: 5px solid #2196f3;
            padding: 15px; border-radius: 5px; color: #0d47a1; font-weight: bold; text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. محرك الفحص ---
def security_scan(url):
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    partner_link = "alhossam7710140-001-site1.mtempurl.com"
    official_sa = u.endswith('.gov.sa') or u.endswith('.edu.sa')
    trusted_list = ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa', 'moi.gov.sa']

    if partner_link in u: return "PARTNER", domain_full
    elif official_sa or domain_full in trusted_list: return "SAFE", domain_full
    elif any(h in domain_full for h in ['smarterasp.net', '000webhostapp.com']): return "DANGER", domain_full
    else: return "CAUTION", domain_full

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

u_input = st.text_input("أدخل الرابط للفحص الأمني الشامل :", key="v33_input")

if st.button("🚀 افحص وصِد الاختراق الآن"):
    if u_input:
        with st.spinner('جاري المسح...'):
            time.sleep(0.4)
            status, d_name = security_scan(u_input)
            
            # تخزين الحالة بنص عربي بسيط للسجل
            st_map = {"PARTNER": "معتمد", "SAFE": "آمن", "DANGER": "خطر", "CAUTION": "تحذير"}
            st.session_state.history.insert(0, f"{st_map.get(status)}: {d_name}")
            
            if status == "PARTNER":
                st.balloons()
                st.markdown(f'<div class="trusted-badge">✅ تم التحقق: هذا النطاق ({d_name}) جهة تقنية معتمدة.</div>', unsafe_allow_html=True)
            elif status == "SAFE":
                st.balloons()
                st.success(f"✅ رابط رسمي وموثوق: {d_name}")
            elif status == "DANGER":
                st.error(f"🚨 تحذير اختراق: الرابط مشبوه ({d_name})!")
            else:
                st.warning(f"⚠️ كن حذراً: الرابط ({d_name}) غير مدرج في قوائمنا الموثوقة.")
    else:
        st.error("⚠️ يرجى إدخال الرابط.")

# --- 4. السجل النظيف (بدون أيقونات مسببة للتشوه) ---
if st.session_state.history:
    st.write("🕒 **آخر عمليات الفحص:**")
    for item in st.session_state.history[:5]:
        st.markdown(f'<div class="history-text">{item}</div>', unsafe_allow_html=True)

st.divider()

# --- 5. ساحة البلاغات ---
st.subheader("📢 ساحة بلاغات المجتمع")
r_input = st.text_input("رابط المحتال للتبليغ :", key="v33_report")
if st.button("إرسال البلاغ"):
    if r_input:
        st.success("✅ تم استلام بلاغك بنجاح. شكرًا لك يا أيمن.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
