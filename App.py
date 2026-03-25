import streamlit as st
import tldextract
import os

# --- 1. إدارة البيانات (البناء التحتي ثابت ومحمي) ---
DB_FILE = "blacklist_database.txt"
MSG_FILE = "messages.txt"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return [line.strip() for line in f if line.strip()]
    return []

# --- 2. التنسيق البصري (لمسة الجمال بدون تخريب) ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
        
        /* إخفاء نصوص النظام */
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"], .st-emotion-cache-13ln4jf { display: none !important; }
        
        /* تجميل العنوان */
        .main-title { color: #00d4ff; text-align: center; font-size: 2.8rem; font-weight: bold; margin-bottom: 30px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
        
        /* تجميل التبويبات (Tabs) */
        .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
        .stTabs [data-baseweb="tab"] { 
            background-color: #f0f2f6; border-radius: 10px 10px 0 0; padding: 10px 20px; color: #333; font-weight: bold;
        }
        .stTabs [aria-selected="true"] { background-color: #00d4ff !important; color: white !important; }
        
        /* الأزرار والحقول */
        div.stButton > button { background-color: #ff4b4b !important; color: white !important; border-radius: 12px !important; width: 100% !important; border: none; transition: 0.3s; }
        div.stButton > button:hover { background-color: #d43f3f !important; transform: scale(1.02); }
        input { border-radius: 12px !important; border: 1px solid #00d4ff !important; padding: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الواجهة الرئيسية (4 تبويبات مستقلة وبأيقونات) ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# إضافة الأيقونات النصية للتبويبات
tab1, tab2, tab3, tab4 = st.tabs(["🔍 الفحص السريع", "📢 بلاغات المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

with tab1:
    st.subheader("🔍 فحص أمان الروابط")
    scan_input = st.text_input("الصق الرابط هنا للفحص :", key="s_v50", help=None)
    if st.button("🚀 ابدأ الفحص"):
        blacklist = load_data()
        d_name = f"{tldextract.extract(scan_input).domain}.{tldextract.extract(scan_input).suffix}"
        if d_name in blacklist: st.error(f"🚨 تحذير أمني: هذا الرابط مسجل كاحتيال!")
        else: st.success(f"✅ الرابط ({d_name}) يبدو آمناً حتى الآن.")

with tab2:
    st.subheader("📢 ساحة حماية المجتمع")
    st.info("كن سبباً في حماية غيرك، بلغ عن الروابط المشبوهة فوراً.")
    rep_url = st.text_input("رابط المحتال للتبليغ :", key="r_v50", help=None)
    if st.button("🚩 تسجيل بلاغ عام"):
        if rep_url:
            d_name = f"{tldextract.extract(rep_url).domain}.{tldextract.extract(rep_url).suffix}"
            with open(DB_FILE, "a") as f: f.write(d_name + "\n")
            st.success(f"✅ تم الحفظ. شكراً لمساهمتك في حماية المجتمع.")
        else: st.warning("⚠️ يرجى إدخال الرابط.")

with tab3:
    st.subheader("📩 تواصل مباشر")
    # ... كود المراسلة المحمي ...

with tab4:
    # ... كود الإدارة المحمي بكلمة مرور ...
    st.subheader("🔐 لوحة تحكم المدير")
