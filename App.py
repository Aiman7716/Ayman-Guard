import streamlit as st
import tldextract
import os

# --- 1. إدارة البيانات ---
DB_FILE = "blacklist_database.txt"
MSG_FILE = "messages.txt"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return [line.strip() for line in f if line.strip()]
    return []

# --- 2. التنسيق البصري الاحترافي ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"], .st-emotion-cache-13ln4jf { display: none !important; }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        div.stButton > button { background-color: #ff4b4b !important; color: white !important; border-radius: 12px !important; width: 100% !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الواجهة الرئيسية بـ 4 تبويبات واضحة ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# هنا قمنا بفصلها يا أيمن لتجدها بسهولة
tab1, tab2, tab3, tab4 = st.tabs(["🔍 فحص الروابط", "📢 ساحة البلاغات", "📧 تواصل معنا", "🔐 الإدارة"])

with tab1:
    st.subheader("🔍 فحص أمان الروابط")
    scan_input = st.text_input("الصق الرابط للفحص :", key="s_v49", help=None)
    if st.button("🚀 افحص الآن"):
        blacklist = load_data()
        d_name = f"{tldextract.extract(scan_input).domain}.{tldextract.extract(scan_input).suffix}"
        if d_name in blacklist: st.error(f"🚨 تحذير: هذا الرابط مبلغ عنه كاحتيال!")
        else: st.success(f"✅ الرابط ({d_name}) يبدو آمناً.")

with tab2:
    st.subheader("📢 ساحة بلاغات المجتمع")
    st.info("هنا يمكنك حماية الآخرين عبر التبليغ عن أي رابط مشبوه.")
    rep_url = st.text_input("رابط المحتال للتبليغ الفوري :", key="r_v49", help=None)
    if st.button("🚩 إرسال بلاغ وحماية الجميع"):
        if rep_url:
            ext = tldextract.extract(rep_url)
            d_name = f"{ext.domain}.{ext.suffix}"
            with open(DB_FILE, "a") as f: f.write(d_name + "\n")
            st.success(f"✅ تم تسجيل بلاغك بنجاح في قاعدة بيانات أيمن.")
        else: st.warning("⚠️ يرجى وضع الرابط أولاً.")

with tab3:
    st.subheader("📩 تواصل مع المطور")
    # ... كود المراسلة كما في v48 ...

with tab4:
    # ... كود لوحة التحكم والإدارة كما في v47 ...
    if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
    # (باقي كود الإدارة)
