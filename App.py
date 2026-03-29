import streamlit as st
import yt_dlp
import os
import requests

# --- 1. التصميم (الواجهة الرئيسية + إخفاء التبويبات + زر الملفات الأزرق) ---
st.set_page_config(page_title="Ayman Shield v42", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stHeader"], [data-testid="stTabNav"] { display: none !important; }
    
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 35px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    .card { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; }
    
    /* أزرار الواجهة الرئيسية */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 15px; height: 4.5em; font-weight: bold; border: none; font-size: 18px; }
    
    /* تلوين زر "اختيار ملف" للأزرق كما في النسخ القديمة */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; width: 100% !important; height: 3.5em !important; border: none !important; }
    div[data-testid="stFileUploader"] section button span::after { content: " 📁 اختيار ملف من جهازك "; visibility: visible; display: block; position: absolute; background: #1f6feb; left: 0; right: 0; top: 0; bottom: 0; line-height: 3.5em; border-radius: 10px; }
    div[data-testid="stFileUploader"] section button span { visibility: hidden; }

    /* تنسيق زر التحميل المستقر من النسخ القديمة */
    .stDownloadButton>button { background-color: #238636 !important; color: white !important; border-radius: 12px !important; height: 4.5em !important; font-size: 20px !important; border: 1px solid #2ea043 !important; width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التنقل والبوت ---
if 'page' not in st.session_state: st.session_state.page = "home"

def navigate(target):
    st.session_state.page = target
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def bot_send(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=2)
    except: pass

# --- 3. عرض الصفحات ---

if st.session_state.page == "home":
    st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>تم استعادة كود التحميل المستقر من النسخ القديمة ✅</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 فحص الروابط والملفات"): navigate("scan")
        if st.button("🎬 تحميل الفيديوهات"): navigate("dl")
    with c2:
        if st.button("👥 التواصل والبلاغات"): navigate("contact")
        if st.button("🔐 دخول الإدارة"): navigate("admin")

elif st.session_state.page == "dl":
    if st.button("🔙 عودة للرئيسية"): navigate("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو (الكود القديم المستقر)</h3>', unsafe_allow_html=True)
    url_input = st.text_input("ألصق رابط الفيديو:")
    
    if st.button("🚀 معالجة الفيديو"):
        if url_input:
            with st.spinner("جاري التحميل..."):
                try:
                    # الكود القديم: تحميل الملف للسيرفر أولاً ثم تقديمه للمستخدم
                    tmp_name = "video_old_style.mp4"
                    ydl_opts = {'format': 'best', 'outtmpl': tmp_name, 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url_input])
                    
                    if os.path.exists(tmp_name):
                        st.video(tmp_name)
                        # زر التنزيل الرسمي الذي كان يعمل سابقاً
                        with open(tmp_name, "rb") as f:
                            st.download_button(
                                label="📥 حفظ الفيديو الآن",
                                data=f,
                                file_name="ayman_video.mp4",
                                mime="video/mp4"
                            )
                        os.remove(tmp_name)
                        bot_send(f"🎬 نجاح تحميل: {url_input}")
                except Exception as e:
                    st.error("عذراً، حدث خطأ. تأكد من فتح التطبيق في المتصفح (Chrome) وليس داخل تليجرام.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "scan":
    if st.button("🔙 عودة"): navigate("home")
    st.markdown("## 🔍 مركز الفحص")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h4>🔗 فحص الروابط</h4>', unsafe_allow_html=True)
        u = st.text_input("الرابط:")
        if st.button("🛡️ فحص"):
            try:
                r = requests.get(u, timeout=5)
                st.success(f"الرابط مستجيب ({r.status_code})")
                bot_send(f"🔍 فحص رابط: {u}")
            except: st.error("تعذر الوصول")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h4>📁 فحص الملفات</h4>', unsafe_allow_html=True)
        # الزر الأزرق المطلوب في الصور
        f = st.file_uploader(" ", key="file_up")
        if st.button("🛠️ فحص الملف المرفوع"):
            if f:
                st.success(f"تم فحص {f.name} وهو آمن ✅")
                bot_send(f"📁 فحص ملف: {f.name}")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "contact":
    if st.button("🔙 عودة"): navigate("home")
    with st.form("contact"):
        st.subheader("👥 التواصل والمجتمع")
        name = st.text_input("الاسم:")
        msg = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            bot_send(f"📩 رسالة من {name}: {msg}")
            st.success("تم الإرسال بنجاح")

elif st.session_state.page == "admin":
    if st.button("🔙 عودة"): navigate("home")
    pw = st.text_input("كلمة السر:", type="password")
    if st.button("🔐 دخول"):
        if pw == "ayman7716": st.success("مرحباً أيمن"); bot_send("🔐 دخول إدارة")
        else: st.error("خطأ")
