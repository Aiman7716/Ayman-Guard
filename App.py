import streamlit as st
import tldextract
import time

# --- 1. الإعدادات البصرية (علاج تداخل الكلمات نهائياً) ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        /* إخفاء شامل لأي رمز قد يسبب تداخل keyboard_ar */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, 
        [data-testid="stIcon"], .stExpander svg, .st-emotion-cache-6q9sum { 
            display: none !important; visibility: hidden !important; 
        }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        .history-card {
            background-color: #f1f3f4; padding: 12px; border-radius: 8px;
            margin-bottom: 8px; border-right: 5px solid #00d4ff; color: #202124;
        }
        div.stButton > button {
            background-color: #ff4b4b !important; color: white !important;
            border-radius: 12px !important; width: 100% !important; height: 3.5em !important;
            font-weight: bold !important;
        }
        .trusted-badge {
            background-color: #e8f0fe; border-right: 6px solid #1a73e8;
            padding: 15px; border-radius: 10px; color: #174ea6; font-weight: bold; text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []
if 'blacklist' not in st.session_state: st.session_state.blacklist = {}

# --- 2. محرك الفحص الأمني (تصحيح المنطق البرمجي) ---
def security_scan(url):
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    partner = "alhossam7710140-001-site1.mtempurl.com"
    official = u.endswith('.gov.sa') or u.endswith('.edu.sa')
    trusted_list = ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa', 'moi.gov.sa', 'saudipost.sa']

    if partner in u: return "PARTNER", domain_full
    elif official or domain_full in trusted_list: return "SAFE", domain_full
    elif domain_full in st.session_state.blacklist or any(h in domain_full for h in ['smarterasp.net', '000webhostapp.com']): 
        return "DANGER", domain_full
    else: return "CAUTION", domain_full

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

u_input = st.text_input("أدخل الرابط للفحص الأمني الشامل :", key="v39_input")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if u_input:
        with st.spinner('جاري التحليل...'):
            time.sleep(0.4)
            status, d_name = security_scan(u_input)
            
            # تسجيل في السجل (نصوص فقط)
            st_map = {"PARTNER": "معتمد", "SAFE": "آمن", "DANGER": "خطر", "CAUTION": "تحذير"}
            st.session_state.history.insert(0, f"{st_map.get(status)}: {d_name}")
            
            # --- تصحيح جمل الشرط لمنع SyntaxError ---
            if status == "PARTNER":
                st.balloons()
                st.markdown(f'<div class="trusted-badge">✅ تم التحقق: هذا النطاق ({d_name}) جهة تقنية معتمدة.</div>', unsafe_allow_html=True)
            elif status == "SAFE":
                st.balloons()
                st.success(f"✅ رابط رسمي وموثوق: {d_name}")
            elif status == "DANGER":
                st.error(f"🚨 تحذير اختراق: هذا الرابط مشبوه ({d_name})!")
            else:
                st.warning(f"⚠️ كن حذراً: الرابط ({d_name}) غير مدرج في قوائمنا الموثوقة.")
    else:
        st.error("⚠️ يرجى إدخال الرابط أولاً.")

# سجل الفحص بنسق نظيف جداً
if st.session_state.history:
    st.write("**آخر عمليات الفحص المستلمة:**")
    for item in st.session_state.history[:5]:
        st.markdown(f'<div class="history-card">{item}</div>', unsafe_allow_html=True)

st.divider()

# --- 4. ساحة البلاغات ---
st.subheader("📢 ساحة بلاغات المجتمع")
r_url = st.text_input("رابط المحتال للتبليغ الفوري :", key="v39_report")

if st.button("🚩 إرسال البلاغ الآن"):
    if r_url:
        _, d_name = security_scan(r_url)
        st.session_state.blacklist[d_name] = True
        st.success(f"✅ شكراً لك يا أيمن، تم إدراج ({d_name}) في قائمة المحظورين.")
    else:
        st.warning("⚠️ أدخل الرابط قبل الإرسال.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
