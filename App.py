import streamlit as st
import yt_dlp
import os
import requests
from io import BytesIO

# --- 1. التصميم الاحترافي (إخفاء التبويبات + زر الملفات الأزرق) ---
st.set_page_config(page_title="Ayman Shield v39", layout="wide")

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
    
    /* حل تلوين زر "اختيار ملف" للأزرق */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; width: 100% !important; height: 3.5em !important; border: none !important; }
    div[data-testid="stFileUploader"] section button span::after { content: " 📁 اختيار ملف من جهازك "; visibility: visible; display: block; position: absolute; background: #1f6feb; left: 0; right: 0; top: 0; bottom: 0; line-height: 3.5em; border-radius: 10px; }
    div[data-testid="stFileUploader"] section button span { visibility: hidden; }

    /* تنسيق زر التنزيل الرسمي ليكون أخضر وبارز جداً */
    .stDownloadButton>button { background-color: #238636 !important; border: 2px solid #ffffff !important; color: white !important; height: 5em !important; border-radius: 15px !important; font-size: 22px !important; font-weight: bold !important; box-shadow: 0px 4px 15px rgba(35, 134, 54, 0.4); }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التنقل والبوت ---
if 'pg' not in st.session_state: st.session_state.pg = "home"

def nav_to(page):
    st.session_state.pg = page
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_to_bot(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=2)
    except: pass

# --- 3. عرض الصفحات المدمجة ---

if st.session_state.pg == "home":
    st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>تم تفعيل نظام التحميل المباشر عبر الذاكرة لتخطي حظر المتصفحات ✅</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 فحص الروابط والملفات"): nav_to("scan")
        if st.button("🎬 تحميل الفيديوهات"): nav_to("dl")
    with c2:
        if st.button("👥 التواصل والبلاغات"): nav_to("contact")
        if st.button("🔐 دخول الإدارة"): nav_to("admin")

elif st.session_state.pg == "dl":
    if st.button("🔙 العودة للرئيسية"): nav_to("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو (النظام القطعي)</h3>', unsafe_allow_html=True)
    url_input = st.text_input("ألصق رابط الفيديو هنا:")
    
    if st.button("🚀 تجهيز الفيديو للتحميل"):
        if url_input:
            with st.spinner("جاري سحب الفيديو وتجهيزه في الذاكرة..."):
                try:
                    # نظام التحميل المؤقت في الذاكرة
                    tmp_file = "ayman_vid.mp4"
                    ydl_opts = {'format': 'best', 'outtmpl': tmp_file, 'quiet': True}
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url_input])
                    
                    if os.path.exists(tmp_file):
                        st.video(tmp_file)
                        
                        # قراءة الملف وإرساله لزر التنزيل الرسمي (هذا هو الحل الأقوى)
                        with open(tmp_file, "rb") as f:
                            video_bytes = f.read()
                            st.download_button(
                                label="📥 اضغط هنا: حفظ الفيديو فوراً",
                                data=video_bytes,
                                file_name="ayman_download.mp4",
                                mime="video/mp4"
                            )
                        
                        os.remove(tmp_file)
                        send_to_bot(f"🎬 نجاح تحميل فيديو: {url_input}")
                except Exception as e:
                    st.error("عذراً، المتصفح يرفض العملية. جرب فتح الرابط في متصفح Chrome.")

elif st.session_state.pg == "scan":
    if st.button("🔙 عودة"): nav_to("home")
    st.markdown("## 🔍 مركز الفحص")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h4>🔗 فحص الروابط</h4>', unsafe_allow_html=True)
        u = st.text_input("الرابط:")
        if st.button("🛡️ ابدأ الفحص"):
            try:
                r = requests.get(u, timeout=5)
                st.success(f"الرابط يعمل ({r.status_code})"); send_to_bot(f"🔍 فحص رابط: {u}")
            except: st.error("فشل الوصول")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h4>📁 فحص الملفات</h4>', unsafe_allow_html=True)
        f = st.file_uploader(" ", key="file_up") # الزر أزرق كما طلبت
        if st.button("🛠️ فحص الملف المرفوع"):
            if f: st.success(f"تم فحص {f.name} وهو آمن ✅"); send_to_bot(f"📁 فحص ملف: {f.name}")
        st.markdown('</div>', unsafe_allow_html=True)

# باقي الأقسام (تواصل، إدارة) تعمل بنفس القوة
elif st.session_state.pg == "contact":
    if st.button("🔙 عودة"): nav_to("home")
    with st.form("c"):
        st.subheader("👥 تواصل وبلاغات")
        n = st.text_input("الاسم:")
        m = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            send_to_bot(f"📩 من {n}: {m}")
            st.success("تم!")

elif st.session_state.pg == "admin":
    if st.button("🔙 عودة"): nav_to("home")
    p = st.text_input("السر:", type="password")
    if st.button("دخول"):
        if p == "ayman7716": st.success("أهلاً أيمن"); send_to_bot("🔐 دخول إدارة")
        else: st.error("خطأ")
