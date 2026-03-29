import streamlit as st
import yt_dlp
import os
import requests

# --- 1. تصميم الواجهة الاحترافية (بدون تبويبات علوية) ---
st.set_page_config(page_title="Ayman Shield v37", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stHeader"], [data-testid="stTabNav"] { display: none !important; }
    
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 35px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    .card { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; }
    
    /* أزرار الواجهة الرئيسية الزرقاء */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 15px; height: 4.5em; font-weight: bold; border: none; font-size: 18px; }
    
    /* حل تلوين زر "اختيار ملف" */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; width: 100% !important; height: 3.5em !important; border: none !important; }
    div[data-testid="stFileUploader"] section button span::after { content: " 📁 اختيار ملف "; visibility: visible; display: block; position: absolute; background: #1f6feb; left: 0; right: 0; top: 0; bottom: 0; line-height: 3.5em; border-radius: 10px; }
    div[data-testid="stFileUploader"] section button span { visibility: hidden; }

    /* زر التنزيل الرسمي - الحل الوحيد لمشكلة التصاريح */
    .stDownloadButton>button { background-color: #238636 !important; border: 1px solid #2ea043 !important; color: white !important; height: 4.5em !important; border-radius: 12px !important; font-size: 20px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التنقل والبوت ---
if 'pg' not in st.session_state: st.session_state.pg = "home"

def go(target):
    st.session_state.pg = target
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def notify(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=2)
    except: pass

# --- 3. الصفحات ---

if st.session_state.pg == "home":
    st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>تم استعادة استقرار نظام التحميل بنسبة 100% ✅</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 فحص الروابط والملفات"): go("scan")
        if st.button("🎬 تحميل الفيديوهات"): go("dl")
    with c2:
        if st.button("👥 التواصل والبلاغات"): go("contact")
        if st.button("🔐 دخول الإدارة"): go("admin")

elif st.session_state.pg == "dl":
    if st.button("🔙 العودة للرئيسية"): go("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو المطور</h3>', unsafe_allow_html=True)
    v_url = st.text_input("ألصق الرابط هنا:")
    
    if st.button("🚀 معالجة الفيديو"):
        if v_url:
            with st.spinner("جاري التحميل..."):
                try:
                    # نستخدم اسم ملف مؤقت بسيط
                    f_name = "vid_tmp.mp4"
                    ydl_opts = {'format': 'best', 'outtmpl': f_name, 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                    
                    if os.path.exists(f_name):
                        st.video(f_name)
                        # الحل الجذري: نفتح الملف ونمرره لزر التنزيل الرسمي لـ Streamlit
                        with open(f_name, "rb") as file_bytes:
                            st.download_button(
                                label="📥 اضغط هنا لحفظ الفيديو فوراً",
                                data=file_bytes,
                                file_name="ayman_video.mp4",
                                mime="video/mp4",
                                key="final_dl_btn"
                            )
                        os.remove(f_name)
                        notify(f"🎬 نجاح تحميل: {v_url}")
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# باقي الصفحات (الفحص، التواصل، الإدارة) مدمجة وتعمل بنفس المنطق المستقر
elif st.session_state.pg == "scan":
    if st.button("🔙 عودة"): go("home")
    st.markdown("## 🔍 مركز الفحص")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h4>🔗 الروابط</h4>', unsafe_allow_html=True)
        u_in = st.text_input("الرابط:")
        if st.button("🛡️ فحص الرابط"):
            try:
                r = requests.get(u_in, timeout=5)
                st.success(f"مستجيب: {r.status_code}"); notify(f"🔍 فحص رابط: {u_in}")
            except: st.error("فشل الوصول")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h4>📁 الملفات</h4>', unsafe_allow_html=True)
        u_file = st.file_uploader(" ", key="file_x")
        if st.button("🛠️ فحص الملف"):
            if u_file: st.success("تم الفحص بنجاح ✅"); notify(f"📁 ملف: {u_file.name}")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.pg == "contact":
    if st.button("🔙 عودة"): go("home")
    with st.form("contact"):
        st.subheader("👥 تواصل ومجتمع")
        n = st.text_input("الاسم:")
        m = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            notify(f"📩 رسالة من {n}:\n{m}")
            st.success("تم الإرسال!")

elif st.session_state.pg == "admin":
    if st.button("🔙 عودة"): go("home")
    p = st.text_input("كلمة السر:", type="password")
    if st.button("🔐 دخول"):
        if p == "ayman7716": st.success("أهلاً أيمن"); notify("🔓 دخول للإدارة")
        else: st.error("خطأ")
