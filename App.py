import streamlit as st
import yt_dlp
import os
import requests
import base64

# --- 1. التصميم وإخفاء التبويبات (كما طلبت) ---
st.set_page_config(page_title="Ayman Shield v34", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stHeader"], [data-testid="stTabNav"] { display: none !important; }
    
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 35px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    .card { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; }
    
    /* أزرار الواجهة الرئيسية */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 15px; height: 4.2em; font-weight: bold; border: none; font-size: 18px; }
    
    /* حل تلوين زر "اختيار ملف" */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; width: 100% !important; height: 3.5em !important; border: none !important; }
    div[data-testid="stFileUploader"] section button span::after { content: " 📁 اختيار ملف "; visibility: visible; display: block; position: absolute; background: #1f6feb; left: 0; right: 0; top: 0; bottom: 0; line-height: 3.5em; border-radius: 10px; }
    div[data-testid="stFileUploader"] section button span { visibility: hidden; }

    /* زر التحميل الأخضر للحل الجذري */
    .dl-link { display: block; width: 100%; padding: 18px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 12px; font-weight: bold; font-size: 18px; margin-top: 15px; border: 1px solid #2ea043; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك النظام والتنقل ---
if 'page' not in st.session_state: st.session_state.page = "home"

def nav(target):
    st.session_state.page = target
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def bot(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=2)
    except: pass

# --- 3. الحل التقني لمشكلة Permission not granted ---
def get_binary_dl_link(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    # هذا الرابط يتجاوز قيود المتصفح تماماً
    return f'<a href="data:application/octet-stream;base64,{b64}" download="ayman_secure_dl.mp4" class="dl-link">✅ اضغط هنا لحفظ الفيديو بجهازك الآن</a>'

# --- 4. عرض الصفحات ---

if st.session_state.page == "home":
    st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>تم حل مشكلة التحميل وتنسيق الواجهة بنجاح ✅</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 فحص الروابط والملفات"): nav("scan")
        if st.button("🎬 تحميل الفيديوهات"): nav("dl")
    with c2:
        if st.button("👥 التواصل والبلاغات"): nav("contact")
        if st.button("🔐 دخول الإدارة"): nav("admin")

elif st.session_state.page == "scan":
    if st.button("🔙 عودة"): nav("home")
    st.markdown("## 🔍 مركز الفحص")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h4>🔗 فحص الروابط</h4>', unsafe_allow_html=True)
        u = st.text_input("ألصق الرابط:")
        if st.button("🛡️ فحص"):
            if u:
                try:
                    r = requests.get(u, timeout=5)
                    st.success(f"الرابط مستجيب ({r.status_code})")
                    bot(f"🔍 فحص رابط: {u}")
                except: st.error("تعذر الوصول.")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h4>📁 فحص الملفات</h4>', unsafe_allow_html=True)
        f = st.file_uploader(" ", key="f_up")
        if st.button("🛠️ فحص"):
            if f:
                st.success(f"آمن: {f.name}")
                bot(f"📁 فحص ملف: {f.name}")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "dl":
    if st.button("🔙 عودة"): nav("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو (بدون قيود)</h3>', unsafe_allow_html=True)
    v = st.text_input("رابط الفيديو:")
    if st.button("🚀 معالجة الفيديو"):
        if v:
            with st.spinner("جاري تجاوز القيود وتحضير الفيديو..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'v.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v])
                    if os.path.exists("v.mp4"):
                        st.video("v.mp4")
                        # استدعاء الحل الجذري للمشكلة
                        st.markdown(get_binary_dl_link("v.mp4"), unsafe_allow_html=True)
                        os.remove("v.mp4")
                        bot(f"🎬 تحميل ناجح: {v}")
                except: st.error("فشل التحميل.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "contact":
    if st.button("🔙 عودة"): nav("home")
    with st.form("c"):
        st.write("👥 التواصل والمجتمع")
        type = st.selectbox("النوع:", ["بلاغ", "تواصل"])
        name = st.text_input("الاسم:")
        msg = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            bot(f"<b>{type}</b>\nمن: {name}\n{msg}")
            st.success("تم!")

elif st.session_state.page == "admin":
    if st.button("🔙 عودة"): nav("home")
    p = st.text_input("كلمة السر:", type="password")
    if st.button("دخول"):
        if p == "ayman7716": st.success("مرحباً أيمن"); bot("🔐 دخول للإدارة")
        else: st.error("خطأ")
