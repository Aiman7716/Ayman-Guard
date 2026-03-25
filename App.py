import streamlit as st
import tldextract
import os

# --- 1. وظائف قاعدة البيانات (الحفظ الدائم) ---
DB_FILE = "blacklist_db.txt"

def load_blacklist():
    """تحميل البلاغات من الملف عند تشغيل الموقع"""
    if not os.path.exists(DB_FILE):
        return set()
    with open(DB_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_to_blacklist(domain):
    """حفظ بلاغ جديد في الملف للأبد"""
    with open(DB_FILE, "a") as f:
        f.write(domain + "\n")

# --- 2. إعدادات الواجهة النظيفة (منع نصوص الكود) ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"], .st-emotion-cache-13ln4jf { display: none !important; }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        div.stButton > button { background-color: #ff4b4b !important; color: white !important; border-radius: 12px !important; width: 100% !important; font-weight: bold !important; }
        input { border-radius: 10px !important; border: 1px solid #00d4ff !important; }
    </style>
""", unsafe_allow_html=True)

# تحميل البيانات عند البدء
if 'permanent_blacklist' not in st.session_state:
    st.session_state.permanent_blacklist = load_blacklist()

# --- 3. محرك الفحص الذكي ---
def security_scan(url):
    u = url.lower().strip().split('?')[0].replace('https://', '').replace('http://', '').strip('/')
    ext = tldextract.extract(u)
    domain_full = f"{ext.domain}.{ext.suffix}"
    
    trusted = ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa']
    
    if domain_full in st.session_state.permanent_blacklist:
        return "DANGER", domain_full
    elif u.endswith('.gov.sa') or domain_full in trusted:
        return "SAFE", domain_full
    else:
        return "CAUTION", domain_full

# --- 4. الواجهة الرئيسية ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# قسم الفحص
st.subheader("🔍 فحص أمان الروابط")
scan_input = st.text_input("الصق الرابط للفحص :", key="s_v44", help=None)

if st.button("🚀 افحص الآن"):
    if scan_input:
        status, d_name = security_scan(scan_input)
        if status == "DANGER":
            st.error(f"🚨 تحذير: هذا الرابط ({d_name}) تم التبليغ عنه مسبقاً في قاعدة بيانات أيمن!")
        elif status == "SAFE":
            st.success(f"✅ رابط آمن وموثوق: {d_name}")
        else:
            st.warning(f"⚠️ حذر: الرابط غير مسجل، كن حذراً.")
    else:
        st.error("⚠️ أدخل الرابط أولاً.")

st.divider()

# قسم البلاغات (الحفظ الدائم)
st.subheader("📢 ساحة البلاغات الدائمة")
rep_url = st.text_input("رابط المحتال للتبليغ :", key="r_v42", help=None)

if st.button("🚩 تسجيل بلاغ نهائي"):
    if rep_url:
        ext = tldextract.extract(rep_url)
        d_name = f"{ext.domain}.{ext.suffix}"
        
        if d_name not in st.session_state.permanent_blacklist:
            save_to_blacklist(d_name) # حفظ في الملف
            st.session_state.permanent_blacklist.add(d_name) # تحديث الجلسة
            st.success(f"✅ تم تسجيل {d_name} في قاعدة البيانات الدائمة بنجاح.")
        else:
            st.info(f"ℹ️ هذا الرابط ({d_name}) موجود بالفعل في قائمة الحظر.")
    else:
        st.warning("⚠️ أدخل الرابط للتبليغ.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾 (نسخة قاعدة البيانات v44)</p>", unsafe_allow_html=True)
