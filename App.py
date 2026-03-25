import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة والتنسيق الاحترافي ---
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
        
        /* إخفاء شامل وكامل لمنع تداخل كلمة keyboard_ar في السجل */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"], .st-emotion-cache-6q9sum { 
            display: none !important; 
            visibility: hidden !important; 
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

# --- 2. محرك الفحص الأمني الذكي ---
def security_scan(url):
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    # القوائم
    partner_link = "alhossam7710140-001-site1.mtempurl.com"
    official_sa = u.endswith('.gov.sa') or u.endswith('.edu.sa')
    trusted_list = ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa', 'moi.gov.sa', 'saudipost.sa']
    
    # مؤشرات الخطر (الاختراق المؤكد)
    danger_hosts = ['smarterasp.net', '000webhostapp.com', 'free.hr'] # أزلنا mtempurl مؤقتاً لتعمل كـ "حذر" إلا إذا كانت اختراقاً
    phishing_keys = ['login-absher', 'verify-bank', 'update-account']

    if partner_link in u:
        return "PARTNER", domain_full
    elif official_sa or domain_full in trusted_list:
        return "SAFE", domain_full
    elif any(key in u for key in phishing_keys) or any(h in domain_full for h in danger_hosts):
        return "DANGER", domain_full
    else:
        # أي رابط آخر غير معروف
        return "CAUTION", domain_full

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

u_input = st.text_input("أدخل الرابط للفحص الأمني :", key="v32_input")

if st.button("🚀 افحص وصِد الاختراق الآن"):
    if u_input:
        with st.spinner('جاري تحليل الرابط...'):
            time.sleep(0.5)
            status, d_name = security_scan(u_input)
            
            # تسجيل في السجل بنص صافي (يمنع تداخل الكلمات)
            st.session_state.history.insert(0, f"{status}: {d_name}")
            
            if status == "PARTNER":
                st.balloons()
                st.markdown(f'<div class="trusted-badge">✅ تم التحقق: هذا النطاق ({d_name}) جهة تقنية معتمدة.</div>', unsafe_allow_html=True)
            elif status == "SAFE":
                st.balloons()
                st.success(f"✅ رابط رسمي وموثوق: {d_name}")
            elif status == "DANGER":
                st.error(f"🚨 تحذير اختراق: هذا الرابط مشبوه جداً ويصنف كصفحة تصيد ({d_name})!")
            else:
                # الرسالة المطلوبة: كن حذراً
                st.warning(f"⚠️ كن حذراً: الرابط ({d_name}) غير مدرج في قوائمنا الموثوقة، لا تقم بإدخال بياناتك الشخصية فيه.")
    else:
        st.error("⚠️ يرجى إدخال الرابط أولاً.")

# السجل النظيف
if st.session_state.history:
    with st.expander("🕒 آخر عمليات الفحص"):
        for item in st.session_state.history[:5]:
            st.text(item)

st.divider()

# --- 4. ساحة البلاغات ---
st.subheader("📢 ساحة بلاغات المجتمع")
r_input = st.text_input("رابط المحتال للتبليغ :", key="v32_report")

if st.button("إرسال البلاغ"):
    if r_input:
        status, _ = security_scan(r_input)
        if status in ["SAFE", "PARTNER"]:
            st.error("❌ لا يمكن التبليغ عن جهات موثوقة!")
        else:
            st.success("✅ تم استلام بلاغك بنجاح. شكرًا لك يا مهندس أيمن.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
