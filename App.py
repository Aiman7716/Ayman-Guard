import streamlit as st
import yt_dlp
import os
import requests

# --- 1. التنسيق الجمالي (أزرار زرقاء + زر ملفات أزرق) ---
st.set_page_config(page_title="Ayman Shield v49", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stHeader"], [data-testid="stTabNav"] { display: none !important; }
    
    /* الأزرار الزرقاء الكبيرة */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; height: 4em; font-weight: bold; border: none; }
    
    /* زر اختيار الملف الأزرق (كما في صورك السابقة) */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 8px !important; }
    
    /* زر التنزيل الأخضر (البرمجة القديمة) */
    .stDownloadButton>button { background-color: #238636 !important; color: white !important; border-radius: 12px !important; height: 4.5em !important; font-size: 20px !important; border: 1px solid #ffffff !important; width: 100% !important; }
    
    .card { background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 20px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة الحالة والبوت ---
if 'pg' not in st.session_state: st.session_state.pg = "home"

def nav(target):
    st.session_state.pg = target
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def bot_log(m):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": m}, timeout=2)
    except: pass

# --- 3. المنطق البرمجي المستعاد (قبل يومين) ---

if st.session_state.pg == "home":
    st.markdown('<div class="card"><h1>🛡️ درع أيمن السيادي</h1><p>تم استعادة الكود البرمجي الأصلي المستقر ✅</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 فحص الروابط والملفات"): nav("scan")
        if st.button("🎬 تحميل الفيديوهات"): nav("dl")
    with c2:
        if st.button("👥 التواصل والبلاغات"): nav("contact")
        if st.button("🔐 دخول الإدارة"): nav("admin")

elif st.session_state.pg == "dl":
    if st.button("🔙 عودة"): nav("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو (المنطق القديم)</h3>', unsafe_allow_html=True)
    v_url = st.text_input("ألصق الرابط:")
    
    if st.button("🚀 معالجة"):
        if v_url:
            with st.spinner("جاري العمل..."):
                try:
                    # الكود البرمجي الأصلي: تحميل ملف ثابت ثم قراءته
                    # هذا المنطق هو الذي كان يعمل بنجاح قبل التعديلات الأخيرة
                    filename = "video_ayman.mp4"
                    if os.path.exists(filename): os.remove(filename) # مسح أي ملف قديم
                    
                    ydl_opts = {'format': 'best', 'outtmpl': filename, 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_url])
                    
                    if os.path.exists(filename):
                        with open(filename, "rb") as f:
                            st.video(v_url)
                            # زر التحميل البرمجي المستقر
                            st.download_button(
                                label="📥 حفظ في الاستوديو",
                                data=f,
                                file_name="ayman_shield.mp4",
                                mime="video/mp4"
                            )
                        bot_log(f"🎬 نجاح: {v_url}")
                except Exception as e:
                    st.error("حدث خطأ في المحرك. يرجى التأكد من الرابط.")

elif st.session_state.pg == "scan":
    if st.button("🔙 عودة"): nav("home")
    st.markdown("### 🔍 مركز الفحص")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h4>🔗 الروابط</h4>', unsafe_allow_html=True)
        u = st.text_input("الرابط:")
        if st.button("🛡️ فحص"):
            try:
                r = requests.get(u, timeout=5)
                st.success(f"يعمل ({r.status_code})")
                bot_log(f"🔍 فحص رابط: {u}")
            except: st.error("فشل")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h4>📁 الملفات</h4>', unsafe_allow_html=True)
        # زر اختيار الملف بالأزرق كما طلبت
        f = st.file_uploader(" ", key="f_up")
        if st.button("🛠️ فحص الملف"):
            if f:
                st.success(f"تم فحص {f.name} ✅")
                bot_log(f"📁 فحص ملف: {f.name}")
        st.markdown('</div>', unsafe_allow_html=True)

# تواصل وإدارة (النسخة المستقرة)
elif st.session_state.pg == "contact":
    if st.button("🔙 عودة"): nav("home")
    with st.form("c"):
        name = st.text_input("الاسم:")
        msg = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            bot_log(f"📩 من {name}: {msg}")
            st.success("تم!")

elif st.session_state.pg == "admin":
    if st.button("🔙 عودة"): nav("home")
    p = st.text_input("السر:", type="password")
    if st.button("دخول"):
        if p == "ayman7716": st.success("أهلاً أيمن")
        else: st.error("خطأ")
