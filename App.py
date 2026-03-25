import streamlit as st
import tldextract
import time
import smtplib
from email.mime.text import MIMEText

# --- 1. الإعدادات البصرية (وداعاً keyboard_ar) ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
        /* حظر الأيقونات المسببة للتشوه البصري */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"] { display: none !important; }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        div.stButton > button { background-color: #ff4b4b !important; color: white !important; border-radius: 12px !important; width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []
if 'blacklist' not in st.session_state: st.session_state.blacklist = {}

# --- 2. وظيفة التنبيه البريدي ---
def send_email_alert(link):
    sender = "ayman.shield@gmail.com"
    receiver = "ayman@example.com" # ضع بريدك هنا يا أيمن
    pw = "your_app_password"
    msg = MIMEText(f"🚨 بلاغ جديد عن رابط محتال: {link}")
    msg['Subject'] = 'تنبيه أمني من درع أيمن'
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, pw)
            server.sendmail(sender, receiver, msg.as_string())
        return True
    except: return False

# --- 3. محرك الفحص الأمني (إصلاح خطأ السطر 67) ---
def security_scan(url):
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}" # تم إغلاق القوس هنا بنجاح
    
    partner = "alhossam7710140-001-site1.mtempurl.com"
    trusted = ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa']

    if partner in u: return "PARTNER", domain_full
    elif u.endswith('.gov.sa') or domain_full in trusted: return "SAFE", domain_full
    elif domain_full in st.session_state.blacklist: return "DANGER", domain_full
    else: return "CAUTION", domain_full

# --- 4. الواجهة المتكاملة ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# القسم الأول: الفحص (الذي أضعناه سابقاً)
st.subheader("🔍 فحص الروابط")
scan_input = st.text_input("ضع الرابط هنا للفحص :", key="s_v42")
if st.button("🚀 افحص الآن"):
    if scan_input:
        status, d_name = security_scan(scan_input)
        st_map = {"PARTNER": "معتمد", "SAFE": "آمن", "DANGER": "خطر", "CAUTION": "تحذير"}
        st.session_state.history.insert(0, f"{st_map.get(status)}: {d_name}")
        if status == "SAFE" or status == "PARTNER": st.success(f"✅ الرابط موثوق: {d_name}")
        elif status == "DANGER": st.error(f"🚨 خطر: رابط محتال!")
        else: st.warning(f"⚠️ حذر: الرابط غير معروف.")
    else: st.error("⚠️ أدخل الرابط.")

st.divider()

# القسم الثاني: البلاغات
st.subheader("📢 ساحة البلاغات")
rep_url = st.text_input("رابط المحتال للتبليغ :", key="r_v42")
if st.button("🚩 إرسال بلاغ وتنبيه الإدارة"):
    if rep_url:
        _, d_name = security_scan(rep_url)
        st.session_state.blacklist[d_name] = True
        send_email_alert(rep_url)
        st.success(f"✅ تم البلاغ عن {d_name} وتنبيه المهندس أيمن.")
    else: st.warning("⚠️ أدخل الرابط أولاً.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
