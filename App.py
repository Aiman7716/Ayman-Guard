import streamlit as st
import tldextract
import time

# --- 1. إعدادات الأمان والتنسيق الصافي ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        /* إخفاء تام للعناصر المسببة للتشوه keyboard_ar */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"] { 
            display: none !important; visibility: hidden !important; 
        }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        .trusted-badge {
            background-color: #e3f2fd; border-right: 5px solid #2196f3;
            padding: 15px; border-radius: 10px; color: #0d47a1; font-weight: bold; text-align: center;
        }
        div.stButton > button {
            background-color: #ff4b4b !important; color: white !important;
            border-radius: 12px !important; width: 100% !important; height: 3.5em !important;
            border: none !important; font-size: 1.1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. محرك الفحص الذكي ---
def security_scan(url):
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    partner = "alhossam7710140-001-site1.mtempurl.com"
    official = u.endswith('.gov.sa') or u.endswith('.edu.sa')
    trusted = ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa', 'moi.gov.sa']

    if partner in u: return "PARTNER", domain_full
    elif official or domain_full in trusted: return "SAFE", domain_full
    elif any(h in domain_full for h in ['smarterasp.net', '000webhostapp.com']): return "DANGER", domain_full
    else: return "CAUTION", domain_full

# --- 3. الواجهة ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

u_input = st.text_input("أدخل الرابط للفحص الأمني :", key="live_input")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if u_input:
        with st.spinner('جاري التحليل...'):
            time.sleep(0.5)
            status, d_name = security_scan(u_input)
            
            st_map = {"PARTNER": "معتمد", "SAFE": "آمن", "DANGER": "خطر", "CAUTION": "حذر"}
            st.session_state.history.insert(0, f"{st_map.get(status)}: {d_name}")
            
            if status == "PARTNER":
                st.balloons()
                st.markdown(f'<div class="trusted-badge">✅ تم التحقق: هذا النطاق ({d_name}) جهة تقنية معتمدة.</div>', unsafe_allow_html=True)
            elif status == "SAFE":
                st.balloons()
                st.success(f"✅ رابط رسمي وموثوق: {d_name}")
            elif status == "DANGER":
                st.error(f"🚨 تحذير: هذا الرابط مشبوه جداً ({d_name})!")
            else:
                st.warning(f"⚠️ كن حذراً: الرابط ({d_name}) غير مدرج في قوائمنا الموثوقة.")
    else:
        st.error("⚠️ يرجى إدخال الرابط.")

# السجل الصافي تماماً
if st.session_state.history:
    st.write("🕒 **آخر عمليات الفحص:**")
    for item in st.session_state.history[:5]:
        st.text(item)

st.divider()
st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
