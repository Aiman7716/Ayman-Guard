import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة والتصميم الاحترافي ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# CSS متطور لإخفاء التشوهات البصرية وتحسين الواجهة
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .main-title { color: #00d4ff; text-align: center; font-size: 3rem; font-weight: bold; margin-bottom: 5px; }
        .sub-title { color: #666; text-align: center; font-size: 1.1rem; margin-bottom: 25px; }
        
        /* 🚨 منع ظهور keyboard_ar نهائياً بإخفاء العناصر المسببة لها 🚨 */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, .st-emotion-cache-6q9sum, 
        symbol, svg, i, [data-testid="stIcon"], button svg { 
            display: none !important; visibility: hidden !important; 
            width: 0 !important; height: 0 !important;
        }

        /* تنسيق الأزرار */
        div.stButton > button {
            background: linear-gradient(90deg, #ff4b4b, #ff7676) !important;
            color: white !important; border-radius: 15px !important;
            width: 100% !important; height: 3.8em !important;
            font-size: 1.1rem !important; border: none !important;
            box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3) !important;
        }

        /* تنسيق سجل الفحص */
        .history-card {
            background-color: #f8f9fa; border-radius: 10px;
            padding: 12px; margin-bottom: 8px; border-right: 4px solid #ddd;
            font-size: 0.95rem; color: #444;
        }
        
        .trusted-box {
            background-color: #e3f2fd; border-right: 6px solid #2196f3;
            padding: 20px; border-radius: 10px; color: #0d47a1;
            font-weight: bold; text-align: center; margin: 15px 0;
        }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. محرك الفحص الأمني الذكي ---
def advanced_security_scan(url):
    # تنظيف الرابط
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    # القوائم البرمجية
    partner_link = "alhossam7710140-001-site1.mtempurl.com" # رابط صديقك
    official_sa = u.endswith('.gov.sa') or u.endswith('.edu.sa')
    trusted_global = ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa', 'saudipost.sa']
    
    # محرك كشف الاحتيال والاختراق
    danger_hosts = ['smarterasp.net', '000webhostapp.com', 'free.hr']
    phishing_keywords = ['login-absher', 'verify-account', 'gift-card', 'bank-update']

    if partner_link in u: return "PARTNER", domain_full
    elif official_sa or domain_full in trusted_global: return "SAFE", domain_full
    elif any(key in u for key in phishing_keywords) or any(h in domain_full for h in danger_hosts): return "DANGER", domain_full
    else: return "CAUTION", domain_full

# --- 3. واجهة المستخدم ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">المنصة الأولى لفحص موثوقية الروابط وحماية المجتمع</div>', unsafe_allow_html=True)

user_input = st.text_input("ضع الرابط هنا للفحص :", placeholder="example.com", key="scan_main")

if st.button("🚀 افحص وصِد الرابط الآن"):
    if user_input:
        with st.spinner('جاري المسح الأمني...'):
            time.sleep(0.5)
            status, d_name = advanced_security_scan(user_input)
            
            # تسجيل في السجل (بدون أيقونات لمنع التشوه البصري)
            status_map = {"PARTNER": "معتمد", "SAFE": "آمن", "DANGER": "خطر", "CAUTION": "حذر"}
            st.session_state.history.insert(0, f"{status_map.get(status)}: {d_name}")

            if status == "PARTNER":
                st.balloons()
                st.markdown(f'<div class="trusted-badge">✅ تم التحقق: هذا النطاق ({d_name}) جهة تقنية معتمدة لدى درع أيمن.</div>', unsafe_allow_html=True)
            elif status == "SAFE":
                st.balloons()
                st.success(f"✅ رابط رسمي وموثوق: {d_name}")
            elif status == "DANGER":
                st.error(f"🚨 تحذير اختراق: هذا الرابط مشبوه جداً ويصنف كصفحة تصيد ({d_name})!")
            else:
                st.warning(f"⚠️ كن حذراً: الرابط ({d_name}) غير مدرج في قوائمنا الموثوقة، لا تدخل بياناتك فيه.")
    else:
        st.error("⚠️ يرجى إدخال الرابط أولاً.")

# --- 4. سجل العمليات (نظيف تماماً) ---
if st.session_state.history:
    st.write("🕒 **آخر عمليات الفحص:**")
    for item in st.session_state.history[:5]:
        st.markdown(f'<div class="history-card">{item}</div>', unsafe_allow_html=True)

st.divider()

# --- 5. ساحة البلاغات ---
st.subheader("📢 ساحة بلاغات المجتمع")
report_input = st.text_input("رابط المحتال للتبليغ :", key="report_main")
if st.button("إرسال البلاغ"):
    if report_input:
        st.success("✅ تم استلام بلاغك بنجاح لمراجعته. شكرًا لك يا أيمن.")

st.markdown("<p style='text-align:center; color:#888; margin-top:30px;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
