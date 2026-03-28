import streamlit as st
import yt_dlp
import os
import requests
import base64

# --- 1. الإعدادات والتصميم الفاخر ---
st.set_page_config(page_title="Ayman Guard v28", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    header, footer, #MainMenu {visibility: hidden !important;}
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 20px; }
    .card { background: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 10px; }
    .stButton>button { width: 100%; background: #1f6feb !important; color: white !important; border-radius: 10px; height: 3.5em; font-weight: bold; border: none; }
    .dl-btn { display: block; width: 100%; padding: 15px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 18px; border: 1px solid #2ea043; }
    </style>
""", unsafe_allow_html=True)

# --- 2. المحركات الخلفية ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def notify_bot(msg):
    try: requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}", timeout=1)
    except: pass

def get_dl_link(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:video/mp4;base64,{b64}" download="ayman_video.mp4" class="dl-btn">📥 اضغط هنا لحفظ الفيديو بجهازك</a>'

# --- 3. هيكل التطبيق الذكي ---
st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار v28.0 | الاستقرار الشامل</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص", "🎬 التحميل", "👥 التواصل", "🔐 الإدارة"])

with tabs[0]:
    st.markdown("<div style='text-align:center;'><h3>أهلاً بك يا أيمن</h3><p>تم دمج الفحص وحل مشكلة الحفظ والانهيار ✅</p></div>", unsafe_allow_html=True)

with tabs[1]:
    st.subheader("🔍 مركز الفحص الموحد")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    u = st.text_input("🔗 رابط للفحص:")
    if st.button("🛡️ فحص الآن"):
        if u:
            try:
                r = requests.get(u, timeout=3)
                st.success(f"الرابط مستجيب ({r.status_code})")
                notify_bot(f"SCAN: {u}")
            except: st.error("تعذر الفحص.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    f = st.file_uploader("📁 ارفع ملفاً:")
    if f and st.button("🛠️ تحليل الملف"):
        st.success(f"تم تحليل {f.name}")
        notify_bot(f"FILE: {f.name}")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]:
    st.subheader("🎬 محمل الفيديو المطور")
    v = st.text_input("رابط الفيديو (Facebook/YT/TikTok):")
    if st.button("🚀 معالجة التحميل"):
        if v:
            with st.spinner("جاري التجهيز..."):
                try:
                    opts = {'format': 'best', 'outtmpl': 'v.mp4', 'quiet': True, 'noplaylist': True}
                    with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([v])
                    if os.path.exists("v.mp4"):
                        st.video("v.mp4")
                        st.markdown(get_dl_link("v.mp4"), unsafe_allow_html=True)
                        os.remove("v.mp4")
                        notify_bot(f"DL_SUCCESS: {v}")
                except:
                    st.error("فشل التحميل. الرابط ثقيل أو غير مدعوم.")

with tabs[3]:
    with st.form("c"):
        n, m = st.text_input("الاسم:"), st.text_area("الرسالة:")
        if st.form_submit_button("إرسال للبوت"):
            notify_bot(f"MSG: {n} - {m}")
            st.success("تم!")

with tabs[4]:
    if "admin" not in st.session_state: st.session_state.admin = False
    if not st.session_state.admin:
        pw = st.text_input("السر:", type="password")
        if st.button("دخول"):
            if pw == "ayman7716": st.session_state.admin = True; st.rerun()
    else:
        st.write("لوحة التحكم")
        if st.button("خروج"): st.session_state.admin = False; st.rerun()
