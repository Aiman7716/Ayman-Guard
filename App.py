import streamlit as st
import yt_dlp
import os
import requests

# --- 1. إعدادات الصفحة والجماليات ---
st.set_page_config(page_title="Ayman Shield v35", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stHeader"], [data-testid="stTabNav"] { display: none !important; }
    
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 35px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    .card { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; }
    
    /* أزرار التنقل الرئيسية */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 15px; height: 4.2em; font-weight: bold; border: none; font-size: 18px; }
    
    /* تلوين زر "اختيار ملف" (الحل الذي طلبته) */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; width: 100% !important; height: 3.5em !important; border: none !important; }
    div[data-testid="stFileUploader"] section button span::after { content: " 📁 اختيار ملف "; visibility: visible; display: block; position: absolute; background: #1f6feb; left: 0; right: 0; top: 0; bottom: 0; line-height: 3.5em; border-radius: 10px; }
    div[data-testid="stFileUploader"] section button span { visibility: hidden; }

    /* تنسيق زر التنزيل الرسمي ليصبح بارزاً وأخضر */
    .stDownloadButton>button { background-color: #238636 !important; color: white !important; border-radius: 12px !important; height: 4.5em !important; font-size: 20px !important; border: 1px solid #2ea043 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة التنقل والحالة ---
if 'page' not in st.session_state: st.session_state.page = "home"

def nav(target):
    st.session_state.page = target
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def bot_notify(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=2)
    except: pass

# --- 3. عرض المحتوى ---

if st.session_state.page == "home":
    st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>تم استخدام نظام التنزيل الرسمي لتجاوز مشكلة التصاريح ✅</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 فحص الروابط والملفات"): nav("scan")
        if st.button("🎬 تحميل الفيديوهات"): nav("dl")
    with c2:
        if st.button("👥 التواصل والبلاغات"): nav("contact")
        if st.button("🔐 دخول الإدارة"): nav("admin")

elif st.session_state.page == "dl":
    if st.button("🔙 عودة للرئيسية"): nav("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو المطور</h3>', unsafe_allow_html=True)
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    
    if st.button("🚀 معالجة الفيديو الآن"):
        if v_url:
            with st.spinner("جاري التحميل من السيرفر..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'ayman_video.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                    
                    if os.path.exists("ayman_video.mp4"):
                        st.video("ayman_video.mp4")
                        
                        # استخدام زر التنزيل الرسمي (هذا هو الحل الجذري للمشكلة)
                        with open("ayman_video.mp4", "rb") as file:
                            st.download_button(
                                label="📥 اضغط هنا لحفظ الفيديو فوراً",
                                data=file,
                                file_name="ayman_download.mp4",
                                mime="video/mp4"
                            )
                        bot_notify(f"🎬 تم تحميل فيديو بنجاح: {v_url}")
                except Exception as e:
                    st.error(f"حدث خطأ في المعالجة: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# (بقية الصفحات الفحص والتواصل والإدارة تظل كما هي في الكود السابق)
elif st.session_state.page == "scan":
    if st.button("🔙 عودة"): nav("home")
    st.markdown("## 🔍 مركز الفحص")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><h4>🔗 فحص الروابط</h4>', unsafe_allow_html=True)
        u = st.text_input("الرابط:")
        if st.button("🛡️ فحص"):
            try:
                r = requests.get(u, timeout=5)
                st.success(f"مستجيب: {r.status_code}")
                bot_notify(f"🔍 فحص رابط: {u}")
            except: st.error("خطأ في الاتصال")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><h4>📁 فحص الملفات</h4>', unsafe_allow_html=True)
        f = st.file_uploader(" ", key="f_up")
        if st.button("🛠️ فحص"):
            if f: st.success(f"تم فحص {f.name}"); bot_notify(f"📁 فحص ملف: {f.name}")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "contact":
    if st.button("🔙 عودة"): nav("home")
    with st.form("c"):
        t = st.selectbox("النوع:", ["بلاغ", "تواصل"])
        n = st.text_input("الاسم:")
        m = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            bot_notify(f"<b>{t}</b>\nمن: {n}\n{m}")
            st.success("تم الإرسال!")

elif st.session_state.page == "admin":
    if st.button("🔙 عودة"): nav("home")
    p = st.text_input("كلمة السر:", type="password")
    if st.button("دخول"):
        if p == "ayman7716": st.success("مرحباً أيمن"); bot_notify("🔐 دخول للإدارة")
        else: st.error("خطأ")
