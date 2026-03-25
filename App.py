import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        /* منع ظهور keyboard_ar نهائياً */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"] { 
            display: none !important; visibility: hidden !important; 
        }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; margin-bottom: 20px; }
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

# تهيئة الذاكرة المؤقتة للبلاغات والسجل
if 'history' not in st.session_state: st.session_state.history = []
if 'community_reports' not in st.session_state: st.session_state.community_reports = {}

# --- 2. محرك الفحص الأمني ---
def security_scan(url):
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    partner = "alhossam7710140-001-site1.mtempurl.com"
    official = u.endswith('.gov.sa') or u.endswith('.edu.sa')
    trusted = ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa', 'moi.gov.sa']

    # فحص إذا كان الرابط قد تم التبليغ عنه سابقاً
    is_reported = domain_full in st.session_state.community_reports

    if partner in u: return "PARTNER", domain_full
    elif official or domain_full in trusted: return "SAFE", domain_full
    elif is_reported or any(h in domain_full for h in ['smarterasp.net', '000webhostapp.com']): return "DANGER", domain_full
    else: return "CAUTION", domain_full

# --- 3. الواجهة الرئيسية للفحص ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

u_input = st.text_input("ضع الرابط هنا للفحص الأمني :", key="scan_input")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if u_input:
        with st.spinner('جاري تحليل الرابط...'):
            time.sleep(0.5)
            status, d_name = security_scan(u_input)
            
            # تسجيل في السجل
            st_map = {"PARTNER": "معتمد", "SAFE": "آمن", "DANGER": "خطر", "CAUTION": "تحذير"}
            st.session_state.history.insert(0, f"{st_map.get(status)}: {d_name}")
            
            if status == "PARTNER":
                st.balloons()
                st.markdown(f'<div class="trusted-badge">✅ تم التحقق: هذا النطاق ({d_name}) جهة تقنية معتمدة لدى درع أيمن.</div>', unsafe_allow_html=True)
            elif status == "SAFE":
                st.balloons()
                st.success(f"✅ رابط رسمي وموثوق: {d_name}")
            elif status == "DANGER":
                st.error(f"🚨 تحذير: هذا الرابط مشبوه أو تم التبليغ عنه سابقاً ({d_name})!")
            else:
                st.warning(f"⚠️ كن حذراً: الرابط ({d_name}) غير مسجل في قوائمنا الموثوقة.")
    else:
        st.error("⚠️ يرجى إدخال الرابط.")

# عرض السجل الصافي
if st.session_state.history:
    with st.expander("🕒 آخر عمليات الفحص"):
        for item in st.session_state.history[:5]:
            st.text(item)

st.divider()

# --- 4. ساحة بلاغات المجتمع (الجزء المفقود) ---
st.subheader("📢 ساحة بلاغات المجتمع")
st.write("ساهم في حماية الآخرين من خلال التبليغ عن الروابط المشبوهة.")

report_url = st.text_input("أدخل رابط المحتال للتبليغ عنه :", key="report_input")

if st.button("🚩 إرسال بلاغ الآن"):
    if report_url:
        status, d_name = security_scan(report_url)
        if status in ["SAFE", "PARTNER"]:
            st.error(f"❌ خطأ: لا يمكن التبليغ عن ({d_name}) لأنها جهة موثوقة.")
        else:
            # إضافة الرابط لقائمة البلاغات
            st.session_state.community_reports[d_name] = True
            st.success(f"✅ شكرًا لك يا أيمن! تم استلام البلاغ عن ({d_name}) وإضافته لقائمة الحظر.")
    else:
        st.warning("⚠️ يرجى إدخال الرابط أولاً.")

st.markdown("<br><p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
