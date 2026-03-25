import streamlit as st
import tldextract
import os

# --- 1. إعدادات الذاكرة الدائمة (بدون جداول خارجية) ---
DB_FILE = "blacklist_database.txt"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_data(domain):
    with open(DB_FILE, "a") as f:
        f.write(domain + "\n")

# --- 2. الواجهة الاحترافية (منع التشوه والنصوص الزائدة) ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
        /* إخفاء تام لأيقونات النظام ونصوص المساعدة المزعجة */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"], .st-emotion-cache-13ln4jf { display: none !important; }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; margin-bottom: 25px; }
        div.stButton > button { background-color: #ff4b4b !important; color: white !important; border-radius: 12px !important; width: 100% !important; font-weight: bold !important; height: 3.5em !important; }
        input { border-radius: 10px !important; border: 1px solid #00d4ff !important; padding: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# تحميل البلاغات عند تشغيل الموقع
if 'blacklist' not in st.session_state:
    st.session_state.blacklist = load_data()

# --- 3. محرك الفحص والواجهة ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# قسم الفحص
st.subheader("🔍 فحص أمان الروابط")
scan_input = st.text_input("الصق الرابط هنا للفحص :", key="scan_v46", help=None)

if st.button("🚀 افحص الرابط الآن"):
    if scan_input:
        ext = tldextract.extract(scan_input)
        d_name = f"{ext.domain}.{ext.suffix}"
        
        if d_name in st.session_state.blacklist:
            st.error(f"🚨 تحذير: هذا الرابط ({d_name}) مسجل في قاعدة بلاغات أيمن!")
        elif scan_input.endswith('.gov.sa') or d_name in ['absher.sa', 'iam.gov.sa', 'google.com', 'najm.sa']:
            st.success(f"✅ رابط آمن وموثوق: {d_name}")
        else:
            st.warning(f"⚠️ حذر: الرابط ({d_name}) غير مسجل، يرجى توخي الحذر.")
    else:
        st.error("⚠️ يرجى إدخال الرابط.")

st.divider()

# قسم البلاغات
st.subheader("📢 ساحة البلاغات")
rep_url = st.text_input("رابط المحتال للتبليغ عنه :", key="rep_v46", help=None)

if st.button("🚩 تسجيل بلاغ في الذاكرة"):
    if rep_url:
        ext = tldextract.extract(rep_url)
        d_name = f"{ext.domain}.{ext.suffix}"
        
        if d_name not in st.session_state.blacklist:
            save_data(d_name) # حفظ في الملف النصي
            st.session_state.blacklist.add(d_name) # تحديث الجلسة الحالية
            st.success(f"✅ تم حفظ {d_name} في قاعدة البيانات بنجاح.")
        else:
            st.info(f"ℹ️ الرابط ({d_name}) موجود مسبقاً في القائمة.")
    else:
        st.warning("⚠️ أدخل الرابط أولاً.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾 (الإصدار المستقر v46)</p>", unsafe_allow_html=True)
