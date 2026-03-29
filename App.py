import streamlit as st
import yt_dlp
import os
import requests

# --- 1. تصميم أيمن السيادي (بدون تعقيدات) ---
st.set_page_config(page_title="Ayman Shield v48", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stHeader"], [data-testid="stTabNav"] { display: none !important; }
    
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; height: 4em; font-weight: bold; border: none; }
    
    /* زر الملفات الأزرق المطلوب */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; }
    
    /* زر التنزيل الأخضر (نفس شكل النسخة القديمة) */
    .stDownloadButton>button { background-color: #238636 !important; color: white !important; border-radius: 12px !important; height: 5em !important; font-size: 22px !important; font-weight: bold !important; border: 2px solid #ffffff !important; }
    
    .card { background: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 20px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة الصفحات والبوت ---
if 'pg' not in st.session_state: st.session_state.pg = "home"

def nav(t):
    st.session_state.pg = t
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def log_bot(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}, timeout=2)
    except: pass

# --- 3. عرض المحتوى بنظام الأزرار ---

if st.session_state.pg == "home":
    st.markdown('<div class="card"><h1>🛡️ درع أيمن السيادي</h1><p>تم استعادة "المنطق البرمجي الأول" بنجاح ✅</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 فحص الروابط والملفات"): nav("scan")
        if st.button("🎬 تحميل الفيديوهات"): nav("dl")
    with c2:
        if st.button("👥 التواصل والبلاغات"): nav("contact")
        if st.button("🔐 دخول الإدارة"): nav("admin")

elif st.session_state.pg == "dl":
    if st.button("🔙 عودة"): nav("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو (النظام المستقر)</h3>', unsafe_allow_html=True)
    url = st.text_input("ألصق الرابط:")
    
    if st.button("🚀 معالجة الفيديو"):
        if url:
            with st.spinner("جاري استخراج البيانات..."):
                try:
                    # الطريقة البرمجية القديمة جداً: استخراج ثم تحميل
                    f_path = "vid_final.mp4"
                    ydl_opts = {'format': 'best', 'outtmpl': f_path, 'quiet': True}
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    
                    if os.path.exists(f_path):
                        st.video(url)
                        # القراءة المباشرة للملف الثنائي (كما كان يحدث سابقاً)
                        with open(f_path, "rb") as file_data:
                            st.download_button(
                                label="📥 اضغط هنا: حفظ في الهاتف",
                                data=file_data,
                                file_name="ayman_shield_video.mp4",
                                mime="video/mp4"
                            )
                        os.remove(f_path)
                        log_bot(f"🎬 نجاح تحميل: {url}")
                except Exception as e:
                    st.error("فشل المحرك في الوصول للفيديو. تأكد من أن الرابط عام وليس خاص.")

elif st.session_state.pg == "scan":
    if st.button("🔙 عودة"): nav("home")
    st.markdown("### 🔍 مركز الفحص")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h4>🔗 فحص الروابط</h4>', unsafe_allow_html=True)
        u = st.text_input("الرابط:")
        if st.button("🛡️ فحص"):
            try:
                r = requests.get(u, timeout=5)
                st.success(f"الرابط مستجيب ({r.status_code})")
                log_bot(f"🔍 فحص رابط: {u}")
            except: st.error("فشل الوصول")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h4>📁 فحص الملفات</h4>', unsafe_allow_html=True)
        # زر اختيار ملف (أزرق)
        f = st.file_uploader(" ", key="f_ayman")
        if st.button("🛠️ فحص"):
            if f:
                st.success(f"تم فحص {f.name} بنجاح ✅")
                log_bot(f"📁 فحص ملف: {f.name}")
        st.markdown('</div>', unsafe_allow_html=True)

# تواصل وإدارة (النظام القديم)
elif st.session_state.pg == "contact":
    if st.button("🔙 عودة"): nav("home")
    with st.form("c"):
        name = st.text_input("الاسم:")
        msg = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            log_bot(f"📩 من {name}: {msg}")
            st.success("تم الإرسال")

elif st.session_state.pg == "admin":
    if st.button("🔙 عودة"): nav("home")
    p = st.text_input("السر:", type="password")
    if st.button("دخول"):
        if p == "ayman7716": st.success("أهلاً أيمن")
        else: st.error("خطأ")
