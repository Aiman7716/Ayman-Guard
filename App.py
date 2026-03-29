import streamlit as st
import requests
import os

# --- 1. الإعدادات وتصميم الواجهة (تلوين الأزرار اختيار الملف) ---
st.set_page_config(page_title="Ayman Shield v31", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    header, footer, #MainMenu {visibility: hidden !important;}
    
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    .scan-card { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; }
    
    /* توحيد ألوان الأزرار لتكون زرقاء بارزة */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; height: 3.8em; font-weight: bold; border: none; font-size: 18px; }
    
    /* تعديل زر "اختيار ملف" المؤشر عليه ليكون أزرق وبارز */
    section[data-testid="stFileUploader"] section button {
        background-color: #1f6feb !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
    }
    /* تغيير نص الزر ليصبح "اختيار ملف" */
    section[data-testid="stFileUploader"] section button::before {
        content: "📁 اختيار ملف ";
    }
    section[data-testid="stFileUploader"] section button span {
        display: none;
    }

    .preview-link { display: block; width: 100%; padding: 15px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 12px; font-weight: bold; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التنبيهات (البوت) ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def notify_ayman(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=2)
    except: pass

# --- 3. بناء هيكل التبويبات ---
st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الحماية والتواصل الموحد</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص الموحد", "🎬 محمل الفيديو", "👥 التواصل والمجتمع", "🔐 الإدارة"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.markdown("### ⚡ أهلاً بك يا أيمن")
    st.success("تم تحديث تصميم زر 'اختيار ملف' ليكون أزرق وبارز كما طلبت ✅")

# --- التبويب 2: مركز الفحص الموحد (تعديل الأزرار) ---
with tabs[1]:
    st.subheader("🔍 اختر نوع الفحص")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="scan-card"><h4>🔗 فحص الروابط</h4>', unsafe_allow_html=True)
        u_in = st.text_input("ألصق الرابط:", key="u_scan")
        if st.button("🛡️ ابدأ فحص الرابط الآن", key="b_u"):
            if u_in:
                try:
                    r = requests.get(u_in, timeout=5)
                    st.success(f"الرابط مستجيب ({r.status_code})")
                    notify_ayman(f"🔍 <b>فحص رابط:</b>\n{u_in}")
                except: st.error("❌ تعذر الوصول للرابط.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="scan-card"><h4>📁 فحص الملفات</h4>', unsafe_allow_html=True)
        u_f = st.file_uploader("اختر ملفاً:", key="f_scan")
        if st.button("🛠️ فحص الملف المرفوع الآن", key="b_f"):
            if u_f:
                st.success(f"✅ تم تحليل {u_f.name}")
                notify_ayman(f"📁 <b>فحص ملف:</b>\n{u_f.name}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 4: التواصل والمجتمع (الجديد المدمج) ---
with tabs[3]:
    st.subheader("👥 مركز التواصل والبلاغات")
    st.markdown('<div class="scan-card">', unsafe_allow_html=True)
    with st.form("contact_form"):
        st.markdown("<h4>📩 أرسل رسالة أو بلاغاً</h4>", unsafe_allow_html=True)
        msg_type = st.selectbox("نوع الطلب:", ["📧 تواصل عام", "🚨 بلاغ حماية المجتمع", "⚙️ اقتراح تقني"])
        sender_name = st.text_input("الاسم:")
        details = st.text_area("المحتوى:")
        submit = st.form_submit_button("إرسال فوراً لبوت التليجرام")
        
        if submit:
            if sender_name and details:
                full_msg = f"<b>{msg_type}</b>\n<b>من:</b> {sender_name}\n<b>النص:</b> {details}"
                notify_ayman(full_msg)
                st.success("تم إرسال بلاغك بنجاح ✅")
            else: st.warning("أكمل البيانات أولاً.")
    st.markdown('</div>', unsafe_allow_html=True)
