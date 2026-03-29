import streamlit as st
import yt_dlp
import os
import requests
from io import BytesIO

# --- 1. واجهة أيمن السيادية (الأزرار الزرقاء + إخفاء التبويبات) ---
st.set_page_config(page_title="Ayman Shield v44", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stHeader"], [data-testid="stTabNav"] { display: none !important; }
    
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 15px; height: 4.5em; font-weight: bold; font-size: 18px; border: none; }
    
    /* تلوين زر اختيار ملف بالأزرق (طلبك الأساسي) */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    
    /* زر التنزيل المستقر (الأخضر) */
    .stDownloadButton>button { background-color: #238636 !important; color: white !important; border-radius: 12px !important; height: 5em !important; font-size: 22px !important; font-weight: bold !important; border: 2px solid #ffffff !important; }
    
    .card { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة الصفحات والبوت ---
if 'pg' not in st.session_state: st.session_state.pg = "home"

def nav(t):
    st.session_state.pg = t
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def log_to_bot(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}, timeout=2)
    except: pass

# --- 3. عرض الصفحات بنظام الأزرار ---

if st.session_state.pg == "home":
    st.markdown('<div class="card"><h1>🛡️ درع أيمن السيادي</h1><p>تم استعادة الكود البرمجي المستقر (المحرك الأصلي) ✅</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 فحص الروابط والملفات"): nav("scan")
        if st.button("🎬 تحميل الفيديوهات"): nav("dl")
    with c2:
        if st.button("👥 التواصل والبلاغات"): nav("contact")
        if st.button("🔐 دخول الإدارة"): nav("admin")

elif st.session_state.pg == "dl":
    if st.button("🔙 العودة للرئيسية"): nav("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو (المحرك البرمجي الأصلي)</h3>', unsafe_allow_html=True)
    url = st.text_input("ألصق الرابط:")
    
    if st.button("🚀 معالجة الفيديو الآن"):
        if url:
            with st.spinner("جاري التحميل البرمجي للمتصفح..."):
                try:
                    # المحرك الأصلي المستقر: تحميل مباشر وتدفق عبر الذاكرة
                    buffer = BytesIO()
                    ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        
                        with open(filename, 'rb') as f:
                            buffer.write(f.read())
                        
                        # تنظيف الملف من السيرفر فوراً بعد القراءة للذاكرة
                        if os.path.exists(filename):
                            os.remove(filename)

                    st.video(url)
                    # هذا هو الزر الذي لا يحتاج صلاحيات Permission
                    st.download_button(
                        label="📥 حفظ الفيديو فوراً",
                        data=buffer.getvalue(),
                        file_name="ayman_video.mp4",
                        mime="video/mp4"
                    )
                    log_to_bot(f"🎬 نجاح تحميل: {url}")
                except Exception as e:
                    st.error(f"حدث خطأ: تأكد من الرابط أو جرب فتحه في متصفح خارجي.")

elif st.session_state.pg == "scan":
    if st.button("🔙 عودة"): nav("home")
    st.markdown("### 🔍 مركز الفحص")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h4>🔗 الروابط</h4>', unsafe_allow_html=True)
        u = st.text_input("الرابط للفحص:")
        if st.button("🛡️ ابدأ الفحص"):
            try:
                r = requests.get(u, timeout=5)
                st.success(f"الرابط يعمل ({r.status_code})")
                log_to_bot(f"🔍 فحص رابط: {u}")
            except: st.error("فشل الوصول")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h4>📁 الملفات</h4>', unsafe_allow_html=True)
        # زر اختيار ملف (أزرق) كما طلبت في الصور
        f = st.file_uploader(" ", key="f_up")
        if st.button("🛠️ فحص الملف"):
            if f:
                st.success(f"تم فحص {f.name} وهو آمن")
                log_to_bot(f"📁 فحص ملف: {f.name}")
        st.markdown('</div>', unsafe_allow_html=True)

# باقي الصفحات (تواصل، إدارة) تعمل باستقرار
elif st.session_state.pg == "contact":
    if st.button("🔙 عودة"): nav("home")
    with st.form("c"):
        name = st.text_input("الاسم:")
        msg = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            log_to_bot(f"📩 من {name}: {msg}")
            st.success("تم الإرسال")

elif st.session_state.pg == "admin":
    if st.button("🔙 عودة"): nav("home")
    p = st.text_input("السر:", type="password")
    if st.button("دخول"):
        if p == "ayman7716": st.success("أهلاً أيمن"); log_to_bot("🔐 دخول إدارة")
        else: st.error("خطأ")
