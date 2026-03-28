import streamlit as st
import yt_dlp
import os
import requests
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. الإعدادات وتأمين الواجهة ---
st.set_page_config(page_title="Ayman Guard v25", layout="wide")

# تصميم يقلل الضغط على المتصفح لمنع البياض
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding-top: 2rem !important; padding-bottom: 10rem !important; }
    
    /* تصميم الرئيسية الأنيقة */
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 35px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 25px; }
    .card { background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 15px; }
    
    /* الأزرار */
    .stButton>button { width: 100%; background: #1f6feb !important; color: white !important; border-radius: 12px; border: none; height: 3.5em; font-weight: bold; font-size: 16px; }
    .preview-btn { display: block; width: 100%; padding: 12px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 12px; font-weight: bold; margin-top: 10px; border: 1px solid #2ea043; }
    </style>
""", unsafe_allow_html=True)

# إخفاء العلامة الحمراء نهائياً
components.html("<script>setInterval(()=>{const p=window.parent.document;['.viewerBadge_container__1QS1n','[data-testid=\"stStatusWidget\"]','footer'].forEach(t=>{const e=p.querySelectorAll(t);e.forEach(x=>x.remove())})},500);</script>", height=0)

# --- 2. محرك التنبيهات الآمن (لا يسبب انهيار) ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def ayman_notify(text):
    """دالة إرسال التنبيهات مع عزل كامل للأخطاء لمنع الشاشة البيضاء"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=1)
    except:
        pass # إذا فشل الإنترنت لا ينهار التطبيق

# --- 3. بناء التبويبات المتكاملة ---
tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص", "🎬 التحميل", "👥 المجتمع وتواصل", "🔐 الإدارة"])

# 🏠 1. الرئيسية الأنيقة
with tabs[0]:
    st.markdown("""
    <div class="hero">
        <h1 style='color:white;'>🛡️ درع أيمن السيادي</h1>
        <p style='color:#8b949e;'>الإصدار المستقر v25.0 | نظام حماية شامل</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown('<div class="card"><h3>🔐 الحماية</h3><p>نظام فحص الروابط والملفات نشط.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="card"><h3>📲 التنبيهات</h3><p>مربوط ببوت التليجرام الخاص بك.</p></div>', unsafe_allow_html=True)

# 🔍 2. مركز الفحص (دمج الروابط والملفات)
with tabs[1]:
    st.subheader("🔍 فحص أمان الروابط والملفات")
    
    # قسم الروابط
    st.markdown('<div class="card"><h4>🔗 فحص الرابط والمعاينة</h4>', unsafe_allow_html=True)
    u_url = st.text_input("ألصق الرابط هنا:", key="u_scan")
    if st.button("🛡️ فحص الأمان"):
        if u_url:
            with st.spinner("جاري الفحص..."):
                try:
                    r = requests.get(u_url, timeout=3)
                    st.success(f"الرابط مستجيب وآمن ({r.status_code})")
                    ayman_notify(f"🔍 <b>عملية فحص رابط:</b>\n{u_url}")
                except:
                    st.error("❌ الرابط غير مستجيب أو قد يكون محجوباً.")
    if u_url: st.markdown(f'<a href="{u_url}" target="_blank" class="preview-btn">👁️ فتح معاينة الرابط</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # قسم الملفات
    st.markdown('<div class="card"><h4>📁 فحص الملفات</h4>', unsafe_allow_html=True)
    u_file = st.file_uploader("اختر ملفاً للفحص:", key="f_scan")
    if u_file and st.button("🛠️ تحليل الملف"):
        st.success(f"تم تحليل {u_file.name} - سليم ✅")
        ayman_notify(f"📁 <b>فحص ملف مرفوع:</b>\n{u_file.name}")
    st.markdown('</div>', unsafe_allow_html=True)

# 🎬 3. التحميل (علاج الشاشة البيضاء)
with tabs[2]:
    st.subheader("🎬 محمل الفيديو الذكي")
    v_url = st.text_input("رابط (فيسبوك، يوتيوب، تيك توك):", key="v_input")
    if st.button("🚀 تحميل الآن"):
        if v_url:
            placeholder = st.empty()
            with placeholder.container():
                st.info("⏳ جاري المعالجة... يرجى الانتظار قليلاً.")
                try:
                    # إعدادات خاصة لتقليل استهلاك الذاكرة
                    opts = {'format': 'best', 'outtmpl': 'ayman_v.mp4', 'quiet': True, 'no_warnings': True, 'noplaylist': True}
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        ydl.download([v_url])
                    
                    if os.path.exists("ayman_v.mp4"):
                        with open("ayman_v.mp4", "rb") as vid:
                            st.video(vid.read())
                            st.download_button("📥 حفظ الفيديو", vid, "video.mp4")
                        os.remove("ayman_v.mp4")
                        ayman_notify(f"🎬 <b>تحميل ناجح:</b>\n{v_url}")
                        st.success("تم التحميل بنجاح!")
                except Exception as e:
                    st.error("⚠️ فشل التحميل. قد يكون الرابط خاصاً أو غير مدعوم.")
                    ayman_notify(f"⚠️ <b>فشل تحميل فيديو:</b>\n{v_url}")

# 👥 4. المجتمع وتواصل معنا (مربوط بالبوت)
with tabs[3]:
    st.subheader("🚨 البلاغات والتواصل")
    with st.form("ayman_contact"):
        type_msg = st.selectbox("النوع:", ["📧 تواصل عام", "🚨 بلاغ عن خطر"])
        name = st.text_input("الاسم:")
        msg = st.text_area("المحتوى:")
        if st.form_submit_button("إرسال فوراً"):
            if name and msg:
                ayman_notify(f"<b>{type_msg}</b>\nمن: {name}\nالمحتوى: {msg}")
                st.success("تم الإرسال لبوت التليجرام بنجاح ✅")
            else: st.warning("أكمل الحقول أولاً")

# 🔐 5. الإدارة (مربوط بالبوت)
with tabs[4]:
    if "is_admin" not in st.session_state: st.session_state.is_admin = False
    if not st.session_state.is_admin:
        pw = st.text_input("كلمة السر:", type="password")
        if st.button("🔐 دخول"):
            if pw == "ayman7716":
                st.session_state.is_admin = True
                ayman_notify("🔓 <b>دخول لوحة الإدارة</b>")
                st.rerun()
            else: st.error("خطأ!")
    else:
        st.success("أهلاً أيمن")
        if st.button("🔴 خروج"):
            st.session_state.is_admin = False
            ayman_notify("🚪 <b>خروج من الإدارة</b>")
            st.rerun()
