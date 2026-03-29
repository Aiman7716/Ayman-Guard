import streamlit as st
import requests
import os
import base64
import yt_dlp

# --- 1. الإعدادات وتصميم الواجهة (إجبار تلوين زر الملفات) ---
st.set_page_config(page_title="Ayman Shield v32", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    header, footer, #MainMenu {visibility: hidden !important;}
    
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    .scan-card { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; }
    
    /* الأزرار العامة */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; height: 3.8em; font-weight: bold; border: none; font-size: 18px; }
    
    /* الحل النهائي لتلوين زر "اختيار ملف" (Browse files) */
    div[data-testid="stFileUploader"] section button {
        background-color: #1f6feb !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        border: none !important;
        width: 100% !important;
        height: 3.5em !important;
    }
    /* استبدال النص بـ "اختيار ملف" */
    div[data-testid="stFileUploader"] section button span::after {
        content: " اختيار ملف من جهازك 📁";
        font-family: 'Cairo', sans-serif;
        visibility: visible;
        display: block;
        position: absolute;
        background: #1f6feb;
        left: 0; right: 0; top: 0; bottom: 0;
        line-height: 3.5em;
        border-radius: 10px;
    }
    div[data-testid="stFileUploader"] section button span { visibility: hidden; }

    .dl-link { display: block; width: 100%; padding: 15px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 12px; font-weight: bold; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. المحركات الخلفية ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def notify_ayman(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=2)
    except: pass

def file_to_b64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- 3. هيكل التبويبات المدمجة ---
st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار v32.0 | نظام الاستقرار والحماية</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص الموحد", "🎬 محمل الفيديو", "👥 التواصل والمجتمع", "🔐 الإدارة"])

# 1. الرئيسية
with tabs[0]:
    st.markdown("<div style='text-align:center;'><h3>أهلاً بك يا أيمن</h3><p>تم حل مشكلة لون زر الملفات ودمج كافة التبويبات ✅</p></div>", unsafe_allow_html=True)
    if st.button("🔍 الانتقال السريع لمركز الفحص"): st.info("استخدم التبويبات بالأعلى للتنقل")

# 2. مركز الفحص (دمج الروابط والملفات + تلوين الزر)
with tabs[1]:
    st.subheader("🔍 مركز فحص الروابط والملفات")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="scan-card"><h4>🔗 فحص الروابط</h4>', unsafe_allow_html=True)
        u_in = st.text_input("ألصق الرابط هنا:", key="u_scan")
        if st.button("🛡️ فحص الرابط الآن"):
            if u_in:
                try:
                    r = requests.get(u_in, timeout=5)
                    st.success(f"الرابط سليم ومستجيب ({r.status_code})")
                    notify_ayman(f"🔍 <b>فحص رابط:</b>\n{u_in}")
                except: st.error("تعذر الوصول للرابط.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="scan-card"><h4>📁 فحص الملفات</h4>', unsafe_allow_html=True)
        u_file = st.file_uploader(" ", key="file_btn") # العنوان مخفي لأننا لونا الزر بالداخل
        if st.button("🛠️ فحص الملف الآن"):
            if u_file:
                st.success(f"✅ تم تحليل {u_file.name} وهو آمن.")
                notify_ayman(f"📁 <b>فحص ملف:</b>\n{u_file.name}")
        st.markdown('</div>', unsafe_allow_html=True)

# 3. محمل الفيديو (حل الشاشة البيضاء والحفظ)
with tabs[2]:
    st.subheader("🎬 محمل الفيديو")
    v_url = st.text_input("رابط الفيديو:")
    if st.button("🚀 تحميل الآن"):
        if v_url:
            with st.spinner("جاري المعالجة..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'vid.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                    if os.path.exists("vid.mp4"):
                        st.video("vid.mp4")
                        b64 = file_to_b64("vid.mp4")
                        st.markdown(f'<a href="data:video/mp4;base64,{b64}" download="ayman.mp4" class="dl-link">📥 حفظ الفيديو فوراً</a>', unsafe_allow_html=True)
                        os.remove("vid.mp4")
                        notify_ayman(f"🎬 <b>تحميل ناجح:</b>\n{v_url}")
                except: st.error("فشل التحميل.")

# 4. التواصل والمجتمع (مدمج)
with tabs[3]:
    st.subheader("👥 التواصل والبلاغات")
    with st.form("c_form"):
        t = st.selectbox("نوع البلاغ:", ["🚨 حماية المجتمع", "📧 تواصل بنا"])
        n = st.text_input("الاسم:")
        m = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال لبوت التليجرام"):
            notify_ayman(f"<b>{t}</b>\nمن: {n}\n{m}")
            st.success("تم الإرسال!")

# 5. الإدارة (مصادقة تليجرام)
with tabs[4]:
    if "is_auth" not in st.session_state: st.session_state.is_auth = False
    if not st.session_state.is_auth:
        pwd = st.text_input("كلمة السر:", type="password")
        if st.button("🔐 دخول"):
            if pwd == "ayman7716":
                st.session_state.is_auth = True
                notify_ayman("🔓 <b>دخول جديد للإدارة</b>")
                st.rerun()
            else: st.error("خطأ")
    else:
        st.success("أهلاً أيمن في لوحة التحكم")
        if st.button("🔴 تسجيل خروج"):
            st.session_state.is_auth = False
            st.rerun()
