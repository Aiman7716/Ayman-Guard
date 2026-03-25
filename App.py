import streamlit as st
import tldextract
import time
import smtplib
from email.mime.text import MIMEText

# --- 1. إعدادات الواجهة الاحترافية (منع ظهور نصوص الكود عند اللصق) ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
        
        /* 🛡️ منع ظهور نصوص النظام (مثل Press Enter) عند اللصق 🛡️ */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"] { display: none !important; }
        .st-emotion-cache-13ln4jf { display: none !important; } /* إخفاء نص المساعدة الافتراضي */
        div[data-testid="stMarkdownContainer"] p { font-size: 1.1rem; }
        
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        div.stButton > button { background-color: #ff4b4b !important; color: white !important; border-radius: 12px !important; width: 100% !important; height: 3.5em !important; font-weight: bold !important; }
        
        /* تجميل مربعات الإدخال لتبدو احترافية ونظيفة */
        input { border-radius: 10px !important; border: 1px solid #00d4ff !important; padding: 10px !important; }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []
if 'blacklist' not in st.session_state: st.session_state.blacklist = {}

# --- 2. محرك الفحص الأمني (تصحيح الأقواس v42) ---
def security_scan(url):
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}" # تم إغلاق القوس بنجاح
    
    partner = "alhossam7710140-001-site1.mtempurl.com"
    trusted = ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa', 'moi.gov.sa']

    if partner in u: return "PARTNER", domain_full
    elif u.endswith('.gov.sa') or domain_full in trusted: return "SAFE", domain_full
    elif domain_full in st.session_state.blacklist: return "DANGER", domain_full
    else: return "CAUTION", domain_full

# --- 3. الواجهة المتكاملة النظيفة ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# القسم الأول: الفحص
st.subheader("🔍 فحص أمان الروابط")
# استخدمنا label_visibility لإخفاء أي نصوص تظهر فوق أو داخل المربع بشكل غير مرغوب
scan_input = st.text_input("الصق الرابط هنا للفحص :", key="s_clean", help=None, label_visibility="visible")

if st.button("🚀 افحص الرابط الآن"):
    if scan_input:
        status, d_name = security_scan(scan_input)
        st_map = {"PARTNER": "معتمد", "SAFE": "آمن", "DANGER": "خطر", "CAUTION": "تحذير"}
        st.session_state.history.insert(0, f"{st_map.get(status)}: {d_name}")
        if status == "SAFE" or status == "PARTNER": st.success(f"✅ الرابط موثوق: {d_name}")
        elif status == "DANGER": st.error(f"🚨 خطر: هذا الرابط مسجل كبلاغ احتيال!")
        else: st.warning(f"⚠️ حذر: الرابط غير مدرج في قوائمنا.")
    else: st.error("⚠️ يرجى إدخال الرابط أولاً.")

st.divider()

# القسم الثاني: البلاغات
st.subheader("📢 ساحة بلاغات المجتمع")
rep_url = st.text_input("الصق رابط المحتال للتبليغ :", key="r_clean", help=None)

if st.button("🚩 إرسال بلاغ فوري"):
    if rep_url:
        _, d_name = security_scan(rep_url)
        st.session_state.blacklist[d_name] = True
        st.success(f"✅ تم البلاغ عن {d_name} بنجاح يا أيمن.")
    else: st.warning("⚠️ يرجى إدخال الرابط.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
