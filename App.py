import streamlit as st
import tldextract
import os

# --- 1. إدارة البيانات ---
DB_FILE = "blacklist_database.txt"
MSG_FILE = "messages.txt" # ملف جديد لحفظ الرسائل

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return [line.strip() for line in f if line.strip()]
    return []

def save_message(name, email, msg):
    with open(MSG_FILE, "a", encoding="utf-8") as f:
        f.write(f"الاسم: {name} | البريد: {email} | الرسالة: {msg}\n---\n")

# --- 2. التنسيق البصري ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"], .st-emotion-cache-13ln4jf { display: none !important; }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        div.stButton > button { background-color: #ff4b4b !important; color: white !important; border-radius: 12px !important; width: 100% !important; }
        .contact-box { background-color: #f9f9f9; padding: 20px; border-radius: 15px; border: 1px solid #00d4ff; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔍 الرئيسية", "📧 تواصل معنا", "🔐 الإدارة"])

with tab1:
    st.subheader("🔍 فحص أمان الروابط")
    scan_input = st.text_input("الصق الرابط للفحص :", key="s_v48", help=None)
    if st.button("🚀 افحص الآن"):
        blacklist = load_data()
        d_name = f"{tldextract.extract(scan_input).domain}.{tldextract.extract(scan_input).suffix}"
        if d_name in blacklist: st.error(f"🚨 تحذير: رابط محتال مسجل مسبقاً!")
        else: st.success(f"✅ الرابط ({d_name}) يبدو آمناً.")

with tab2:
    st.markdown('<div class="contact-box">', unsafe_allow_html=True)
    st.subheader("📩 أرسل رسالة للمطور أيمن")
    c_name = st.text_input("اسمك الكريم :")
    c_email = st.text_input("بريدك الإلكتروني :")
    c_msg = st.text_area("كيف يمكننا مساعدتك؟")
    if st.button("📤 إرسال الرسالة"):
        if c_name and c_msg:
            save_message(c_name, c_email, c_msg)
            st.success("✅ شكراً لك! وصلت رسالتك للمهندس أيمن.")
        else: st.warning("⚠️ يرجى ملء الاسم والرسالة.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
    
    if not st.session_state.admin_logged_in:
        pwd = st.text_input("كلمة مرور الإدارة :", type="password")
        if st.button("دخول"):
            if pwd == "ayman7716": 
                st.session_state.admin_logged_in = True
                st.rerun()
    else:
        st.subheader("🛠️ لوحة تحكم أيمن")
        if st.button("تسجيل خروج"):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        # عرض الرسائل الواردة للمدير فقط
        st.write("---")
        st.write("📩 **الرسائل الواردة:**")
        if os.path.exists(MSG_FILE):
            with open(MSG_FILE, "r", encoding="utf-8") as f:
                st.text_area("صندوق الوارد :", value=f.read(), height=200)
        else: st.write("لا توجد رسائل جديدة.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
