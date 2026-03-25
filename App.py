import streamlit as st
import tldextract
import os

# --- 1. إدارة البيانات ---
DB_FILE = "blacklist_database.txt"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def save_all_data(list_data):
    with open(DB_FILE, "w") as f:
        for item in list_data:
            f.write(item + "\n")

# --- 2. الواجهة الاحترافية ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"], .st-emotion-cache-13ln4jf { display: none !important; }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        div.stButton > button { background-color: #ff4b4b !important; color: white !important; border-radius: 12px !important; width: 100% !important; }
        .admin-box { background-color: #f0f2f6; padding: 20px; border-radius: 15px; border: 1px dashed #00d4ff; }
    </style>
""", unsafe_allow_html=True)

# --- 3. نظام "حساب المدير" ---
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

# --- 4. واجهة المستخدم العامة ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 فحص وبلاغ", "🔐 لوحة التحكم"])

with tab1:
    # قسم الفحص (كما هو في v46)
    st.subheader("🔍 فحص أمان الروابط")
    scan_input = st.text_input("الصق الرابط للفحص :", key="scan_v47", help=None)
    if st.button("🚀 افحص الآن"):
        blacklist = load_data()
        ext = tldextract.extract(scan_input)
        d_name = f"{ext.domain}.{ext.suffix}"
        if d_name in blacklist:
            st.error(f"🚨 تحذير: هذا الرابط تم التبليغ عنه مسبقاً!")
        else:
            st.success(f"✅ الرابط ({d_name}) غير مسجل في البلاغات.")

    st.divider()
    
    st.subheader("📢 ساحة البلاغات")
    rep_url = st.text_input("رابط المحتال للتبليغ :", key="rep_v47", help=None)
    if st.button("🚩 تسجيل بلاغ"):
        if rep_url:
            ext = tldextract.extract(rep_url)
            d_name = f"{ext.domain}.{ext.suffix}"
            current_data = load_data()
            if d_name not in current_data:
                with open(DB_FILE, "a") as f: f.write(d_name + "\n")
                st.success(f"✅ تم حفظ البلاغ بنجاح.")
            else: st.info("ℹ️ الرابط موجود مسبقاً.")

with tab2:
    if not st.session_state.admin_logged_in:
        st.subheader("تسجيل دخول المدير")
        password = st.text_input("أدخل كلمة مرور الإدارة :", type="password")
        if st.button("دخول"):
            if password == "ayman7716": # يمكنك تغيير كلمة المرور هنا
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ كلمة المرور غير صحيحة")
    else:
        st.markdown('<div class="admin-box">', unsafe_allow_html=True)
        st.subheader("🛠️ لوحة تحكم أيمن")
        if st.button("تسجيل خروج"):
            st.session_state.admin_logged_in = False
            st.rerun()
            
        st.write("---")
        st.write("📊 **البلاغات الحالية في النظام:**")
        blacklist_list = load_data()
        
        if not blacklist_list:
            st.write("لا توجد بلاغات حالياً.")
        else:
            for i, domain in enumerate(blacklist_list):
                col1, col2 = st.columns([3, 1])
                col1.text(f"{i+1}. {domain}")
                if col2.button("حذف", key=f"del_{i}"):
                    blacklist_list.remove(domain)
                    save_all_data(blacklist_list)
                    st.success(f"تم حذف {domain}")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
