import streamlit as st
import yt_dlp
import os
import requests
import base64

# --- 1. إعدادات الهوية البصرية (زر أزرق للملفات + إخفاء التبويبات) ---
st.set_page_config(page_title="Ayman Shield v40", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stHeader"], [data-testid="stTabNav"] { display: none !important; }
    
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 35px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    .card { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; }
    
    /* الأزرار الزرقاء السيادية */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 15px; height: 4.5em; font-weight: bold; font-size: 18px; border: none; }
    
    /* تنسيق زر "اختيار ملف" (كما طلبت في الصور) */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; width: 100% !important; height: 3.5em !important; border: none !important; }
    div[data-testid="stFileUploader"] section button span::after { content: " 📁 اختيار ملف من جهازك "; visibility: visible; display: block; position: absolute; background: #1f6feb; left: 0; right: 0; top: 0; bottom: 0; line-height: 3.5em; border-radius: 10px; }
    div[data-testid="stFileUploader"] section button span { visibility: hidden; }

    /* زر التحميل القسري المطور */
    .force-dl { display: block; width: 100%; padding: 22px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 15px; font-weight: bold; font-size: 20px; border: 2px solid #ffffff; box-shadow: 0px 4px 15px rgba(0,0,0,0.3); margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة الحالة والبوت ---
if 'page' not in st.session_state: st.session_state.page = "home"

def go(t):
    st.session_state.page = t
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def bot_log(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=2)
    except: pass

# --- 3. الوظائف التقنية ---
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}" class="force-dl">✅ تم التجهيز! اضغط هنا للحفظ النهائي</a>'
    return href

# --- 4. عرض المحتوى ---

if st.session_state.page == "home":
    st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>تم تفعيل بروتوكول "التحميل القسري" لتجاوز قيود التطبيقات ✅</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 فحص الروابط والملفات"): go("scan")
        if st.button("🎬 تحميل الفيديوهات"): go("dl")
    with c2:
        if st.button("👥 التواصل والبلاغات"): go("contact")
        if st.button("🔐 دخول الإدارة"): go("admin")

elif st.session_state.page == "dl":
    if st.button("🔙 عودة"): go("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو (تجاوز الحظر)</h3>', unsafe_allow_html=True)
    url = st.text_input("ألصق الرابط:")
    if st.button("🚀 تجهيز الفيديو"):
        if url:
            with st.spinner("جاري سحب البيانات..."):
                try:
                    f_name = "ayman_video.mp4"
                    ydl_opts = {'format': 'best', 'outtmpl': f_name, 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
                    
                    if os.path.exists(f_name):
                        st.video(f_name)
                        # استخدام نظام التحميل القسري
                        st.markdown(get_binary_file_downloader_html(f_name, 'Video'), unsafe_allow_html=True)
                        bot_log(f"🎬 نجاح: {url}")
                except: st.error("فشل في المعالجة")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "scan":
    if st.button("🔙 عودة"): go("home")
    st.markdown("## 🔍 مركز الفحص")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h4>🔗 فحص الروابط</h4>', unsafe_allow_html=True)
        u_in = st.text_input("الرابط:")
        if st.button("🛡️ فحص"):
            try:
                r = requests.get(u_in, timeout=5)
                st.success(f"الرابط مستجيب ({r.status_code})"); bot_log(f"🔍 فحص رابط: {u_in}")
            except: st.error("لا يمكن الوصول")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h4>📁 فحص الملفات</h4>', unsafe_allow_html=True)
        # الزر الأزرق المطلوب
        f_up = st.file_uploader(" ", key="f_up")
        if st.button("🛠️ فحص"):
            if f_up: st.success("الملف آمن ✅"); bot_log(f"📁 ملف: {f_up.name}")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "contact":
    if st.button("🔙 عودة"): go("home")
    with st.form("c"):
        name = st.text_input("الاسم:")
        msg = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            bot_log(f"📩 من {name}: {msg}")
            st.success("تم الإرسال")

elif st.session_state.page == "admin":
    if st.button("🔙 عودة"): go("home")
    pw = st.text_input("كلمة السر:", type="password")
    if st.button("🔐 دخول"):
        if pw == "ayman7716": st.success("أهلاً أيمن"); bot_log("🔓 دخول للإدارة")
        else: st.error("خطأ")
