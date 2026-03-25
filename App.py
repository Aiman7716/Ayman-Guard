import streamlit as st
import tldextract
import os

# --- 1. إدارة البيانات ---
DB_FILE = "blacklist_database.txt"
MSG_FILE = "messages.txt"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f: return [line.strip() for line in f if line.strip()]
    return []

def save_all_data(list_data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        for item in list_data: f.write(item + "\n")

# --- 2. التنسيق البصري الاحترافي ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"], .st-emotion-cache-13ln4jf { display: none !important; }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; margin-bottom: 20px; }
        .stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; }
        .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 10px; padding: 10px 15px; }
        .stTabs [aria-selected="true"] { background-color: #00d4ff !important; color: white !important; }
        div.stButton > button { background-color: #ff4b4b !important; color: white !important; border-radius: 12px !important; width: 100% !important; font-weight: bold !important; }
        input, textarea { border-radius: 12px !important; border: 1px solid #00d4ff !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الهيكل الأساسي للتبويبات ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🔍 الفحص", "📢 البلاغات", "📧 اتصل بنا", "🔐 الإدارة"])

with tab1:
    st.subheader("🔍 فحص أمان الروابط")
    scan_input = st.text_input("الصق الرابط للفحص :", key="s_v52", help=None)
    if st.button("🚀 ابدأ الفحص"):
        if scan_input:
            blacklist = load_data()
            ext = tldextract.extract(scan_input)
            d_name = f"{ext.domain}.{ext.suffix}"
            if d_name in blacklist: st.error(f"🚨 تحذير: الرابط ({d_name}) مسجل كاحتيال!")
            else: st.success(f"✅ الرابط ({d_name}) يبدو آمناً.")
        else: st.warning("⚠️ أدخل الرابط.")

with tab2:
    st.subheader("📢 ساحة بلاغات المجتمع")
    st.info("بلغ عن الروابط المشبوهة لحماية الآخرين.")
    rep_url = st.text_input("رابط المحتال للتبليغ :", key="r_v52", help=None)
    if st.button("🚩 تسجيل بلاغ"):
        if rep_url:
            d_name = f"{tldextract.extract(rep_url).domain}.{tldextract.extract(rep_url).suffix}"
            with open(DB_FILE, "a", encoding="utf-8") as f: f.write(d_name + "\n")
            st.success(f"✅ تم إضافة البلاغ بنجاح.")
        else: st.warning("⚠️ أدخل الرابط أولاً.")

with tab3:
    st.subheader("📧 تواصل مباشر 📩")
    c_name = st.text_input("الاسم الكريم :", key="cn_v52")
    c_msg = st.text_area("كيف يمكننا مساعدتك؟ :", key="cm_v52")
    if st.button("📤 إرسال الرسالة"):
        if c_name and c_msg:
            with open(MSG_FILE, "a", encoding="utf-8") as f:
                f.write(f"الاسم: {c_name} | الرسالة: {c_msg}\n---\n")
            st.success("✅ شكراً لك، وصلت رسالتك للمهندس أيمن.")
        else: st.warning("⚠️ يرجى تعبئة الحقول.")

with tab4:
    if 'admin_in' not in st.session_state: st.session_state.admin_in = False
    
    if not st.session_state.admin_in:
        # السطر 84 المصحح: تأكد من إغلاق القوس وعلامة التنصيص
        pwd = st.text_input("كلمة مرور الإدارة :", type="password", key="admin_pwd")
        if st.button("دخول المدير"):
            if pwd == "ayman7716": 
                st.session_state.admin_in = True
                st.rerun()
            else: st.error("❌ كلمة المرور غير صحيحة")
    else:
        st.subheader("🛠️ لوحة تحكم المدير 🔐")
        if st.button("تسجيل خروج"):
            st.session_state.admin_in = False
            st.rerun()
        
        st.write("📊 **إدارة البلاغات:**")
        blist = load_data()
        for i, d in enumerate(blist):
            col1, col2 = st.columns([3, 1])
            col1.text(d)
            if col2.button("حذف", key=f"del_{i}"):
                blist.remove(d)
                save_all_data(blist)
                st.rerun()

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
