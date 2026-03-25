import streamlit as st
import tldextract
import os
from datetime import datetime

# --- 1. إدارة البيانات ---
DB_FILE = "blacklist_database.txt"
MSG_FILE = "messages.txt"

def load_blacklist():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f: return [line.strip() for line in f if line.strip()]
    return []

def save_blacklist(list_data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        for item in list_data: f.write(item + "\n")

# --- 2. التنسيق البصري ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"], .st-emotion-cache-13ln4jf { display: none !important; }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        div.stButton > button { background-color: #ff4b4b !important; color: white !important; border-radius: 12px !important; width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🔍 الفحص", "📢 البلاغات", "📧 اتصل بنا", "🔐 الإدارة"])

# --- التبويب الأول: الفحص ---
with tab1:
    st.subheader("🔍 فحص أمان الروابط")
    scan_input = st.text_input("الصق الرابط للفحص :", key="s_v53", help=None)
    if st.button("🚀 ابدأ الفحص"):
        if scan_input:
            blacklist = load_blacklist()
            d_name = f"{tldextract.extract(scan_input).domain}.{tldextract.extract(scan_input).suffix}"
            if any(d_name in entry for entry in blacklist): st.error("🚨 تحذير: هذا الرابط مسجل كاحتيال!")
            else: st.success(f"✅ الرابط ({d_name}) يبدو آمناً.")

# --- التبويب الثاني: البلاغات (مع تسجيل البريد) ---
with tab2:
    st.subheader("📢 ساحة بلاغات المجتمع")
    rep_url = st.text_input("رابط المحتال :", key="r_v53")
    rep_email = st.text_input("بريدك الإلكتروني (اختياري) :", key="re_v53")
    if st.button("🚩 تسجيل بلاغ"):
        if rep_url:
            d_name = f"{tldextract.extract(rep_url).domain}.{tldextract.extract(rep_url).suffix}"
            email_info = rep_email if rep_email else "مجهول"
            with open(DB_FILE, "a", encoding="utf-8") as f:
                f.write(f"{d_name} (بواسطة: {email_info})\n")
            st.success("✅ تم تسجيل البلاغ بنجاح.")

# --- التبويب الثالث: تواصل معنا ---
with tab3:
    st.subheader("📧 أرسل رسالة للمهندس أيمن")
    c_name = st.text_input("الاسم :")
    c_email = st.text_input("بريدك الإلكتروني (إلزامي لرد عليك) :")
    c_msg = st.text_area("رسالتك :")
    if st.button("📤 إرسال الآن"):
        if c_name and c_email and c_msg:
            with open(MSG_FILE, "a", encoding="utf-8") as f:
                f.write(f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')} | الاسم: {c_name} | البريد: {c_email} | الرسالة: {c_msg}\n---\n")
            st.success("✅ وصلت رسالتك بنجاح.")
        else: st.warning("⚠️ يرجى تعبئة جميع الحقول.")

# --- التبويب الرابع: الإدارة (لرؤية الرسائل والإيميلات) ---
with tab4:
    if 'admin_in' not in st.session_state: st.session_state.admin_in = False
    if not st.session_state.admin_in:
        pwd = st.text_input("كلمة مرور الإدارة :", type="password")
        if st.button("دخول"):
            if pwd == "ayman7716": st.session_state.admin_in = True; st.rerun()
    else:
        st.subheader("🛠️ لوحة تحكم المدير")
        if st.button("خروج"): st.session_state.admin_in = False; st.rerun()
        
        st.write("📩 **صندوق الرسائل والبريد:**")
        if os.path.exists(MSG_FILE):
            with open(MSG_FILE, "r", encoding="utf-8") as f:
                st.text_area("الرسائل الواردة :", value=f.read(), height=300)
        
        st.write("---")
        st.write("📊 **قائمة البلاغات وعناوين المبلغين:**")
        blist = load_blacklist()
        for i, entry in enumerate(blist):
            c1, c2 = st.columns([4, 1])
            c1.text(entry)
            if c2.button("حذف", key=f"d_{i}"):
                blist.remove(entry); save_blacklist(blist); st.rerun()

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)

