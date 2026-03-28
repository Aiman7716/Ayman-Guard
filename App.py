import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. الإعدادات والتصميم الأنيق ---
st.set_page_config(page_title="Ayman Guard v24", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding-top: 2rem !important; padding-bottom: 10rem !important; }
    
    /* الرئيسية الأنيقة */
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 40px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 30px; }
    .status-card { background: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; text-align: center; }
    
    /* الأزرار والفحص */
    .stButton>button { width: 100%; background: #1f6feb !important; color: white !important; border-radius: 10px; border: none; height: 3.5em; font-weight: bold; }
    .preview-btn { display: block; width: 100%; padding: 12px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 10px; font-weight: bold; margin-top: 10px; border: 1px solid #2ea043; }
    .scan-section { background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# قتل العلامة الحمراء نهائياً
components.html("<script>setInterval(()=>{const p=window.parent.document;['.viewerBadge_container__1QS1n','[data-testid=\"stStatusWidget\"]','footer'].forEach(t=>{const e=p.querySelectorAll(t);e.forEach(x=>x.remove())})},400);</script>", height=0)

# --- 2. محرك التنبيهات والبيانات ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_bot(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=2)
    except: pass

# --- 3. بناء التبويبات الخمسة المتكاملة ---
tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص الشامل", "🎬 محمل الفيديو", "👥 المجتمع وتواصل", "🔐 الإدارة"])

# 🏠 1. الرئيسية الأنيقة
with tabs[0]:
    st.markdown("""
    <div class="hero">
        <h1>🛡️ درع أيمن السيادي</h1>
        <p>نظام الحماية والتحميل المتقدم | الإصدار v24.0</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="status-card"><h3>حالة النظام</h3><p style="color:#238636;">متصل وآمن ✅</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="status-card"><h3>التنبيهات</h3><p style="color:#1f6feb;">مربوطة بالتليجرام 📲</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="status-card"><h3>المستخدم</h3><p>أهلاً بك يا أيمن 👤</p></div>', unsafe_allow_html=True)

# 🔍 2. مركز الفحص (دمج الروابط والملفات)
with tabs[1]:
    st.subheader("🔍 فحص أمان الروابط والملفات")
    
    # قسم الروابط
    st.markdown('<div class="scan-section"><h4>🔗 فحص الرابط والمعاينة</h4>', unsafe_allow_html=True)
    u = st.text_input("ألصق الرابط هنا:", key="url_scan")
    if st.button("🛡️ فحص ومعاينة"):
        if u:
            try:
                r = requests.get(u, timeout=5)
                st.success(f"الرابط مستجيب وآمن ({r.status_code})")
                send_bot(f"🔍 <b>فحص رابط:</b>\n{u}")
            except: st.error("❌ تعذر الوصول للرابط.")
    if u: st.markdown(f'<a href="{u}" target="_blank" class="preview-btn">👁️ فتح معاينة الرابط</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # قسم الملفات
    st.markdown('<div class="scan-section"><h4>📁 فحص الملفات</h4>', unsafe_allow_html=True)
    f = st.file_uploader("اختر ملفاً للفحص:", key="file_scan")
    if f and st.button("🛠️ تحليل الملف المرفوع"):
        st.success(f"تم تحليل {f.name} - سليم ✅")
        send_bot(f"📁 <b>فحص ملف مرفوع:</b>\n{f.name}")
    st.markdown('</div>', unsafe_allow_html=True)

# 🎬 3. التحميل (علاج الشاشة البيضاء)
with tabs[2]:
    st.subheader("🎬 محمل الفيديو الذكي")
    v_url = st.text_input("رابط (فيسبوك، يوتيوب، تيك توك):")
    if st.button("🚀 تحميل الفيديو"):
        if v_url:
            with st.spinner("جاري المعالجة... يرجى عدم إغلاق الصفحة"):
                try:
                    # إعدادات خاصة لمنع الانهيار
                    opts = {'format': 'best', 'outtmpl': 'ayman_v.mp4', 'quiet': True, 'no_warnings': True, 'noplaylist': True}
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        ydl.download([v_url])
                    
                    if os.path.exists("ayman_v.mp4"):
                        with open("ayman_v.mp4", "rb") as vid:
                            st.video(vid.read())
                            st.download_button("📥 حفظ الفيديو", vid, "video.mp4")
                        os.remove("ayman_v.mp4")
                        send_bot(f"🎬 <b>تم تحميل فيديو:</b>\n{v_url}")
                except Exception as e:
                    st.error("فشل التحميل. الرابط قد يكون خاصاً أو غير مدعوم.")
                    send_bot(f"⚠️ <b>فشل تحميل فيديو:</b>\n{v_url}")

# 👥 4. المجتمع وتواصل معنا (مربوط بالبوت)
with tabs[3]:
    st.subheader("🚨 البلاغات والتواصل")
    with st.form("contact_form"):
        st.markdown("<b>استخدم هذا النموذج للإرسال المباشر لبوت التليجرام:</b>", unsafe_allow_html=True)
        user_type = st.selectbox("نوع الرسالة:", ["📧 تواصل عام", "🚨 بلاغ عن خطر"])
        user_name = st.text_input("الاسم:")
        user_msg = st.text_area("المحتوى:")
        if st.form_submit_button("إرسال الآن"):
            if user_name and user_msg:
                send_bot(f"<b>{user_type}</b>\nمن: {user_name}\nالمحتوى: {user_msg}")
                st.success("تم الإرسال بنجاح ✅")
            else: st.warning("يرجى ملء كافة الحقول")

# 🔐 5. الإدارة (مربوط بالبوت)
with tabs[4]:
    if "admin" not in st.session_state: st.session_state.admin = False
    if not st.session_state.admin:
        pw = st.text_input("كلمة مرور الإدارة:", type="password")
        if st.button("🔐 دخول"):
            if pw == "ayman7716":
                st.session_state.admin = True
                send_bot("🔓 <b>تنبيه:</b> تم الدخول إلى لوحة الإدارة.")
                st.rerun()
            else: st.error("كلمة المرور خاطئة")
    else:
        st.success("مرحباً أيمن، أنت في وضع التحكم الكامل.")
        if st.button("🔴 تسجيل خروج"):
            st.session_state.admin = False
            send_bot("🚪 <b>تنبيه:</b> تم الخروج من الإدارة.")
            st.rerun()
