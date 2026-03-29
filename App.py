import streamlit as st
import yt_dlp
import requests
import time
import random

# --- 1. التنسيق السيادي الموحد v37 مع إضافة نمط الإدارة ---
st.set_page_config(page_title="Ayman Guard Pro v37", layout="wide")

# تهيئة الذاكرة للمسميات الديناميكية والإدارة
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي v37.0"
    }
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; border: 1px solid #30363d;
    }

    .contact-btn {
        background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; border: 1px solid #ffffff !important;
        font-weight: bold !important; text-decoration: none !important;
        display: block; padding: 15px; text-align: center; transition: 0.3s; margin-bottom: 10px;
    }

    .bot-btn {
        background: linear-gradient(90deg, #0088cc, #00aaff) !important;
        color: white !important; border-radius: 15px !important;
        padding: 20px; font-size: 20px !important; text-decoration: none !important;
        display: block; text-align: center; font-weight: bold; border: 2px solid #ffffff;
        box-shadow: 0 4px 15px rgba(0,136,204,0.4); margin-bottom: 20px;
    }

    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; font-weight: bold; height: 3.5em; border: none; }
    .stDownloadButton > button { background-color: #238636 !important; width: 100% !important; height: 4.5em !important; font-size: 20px !important; font-weight: bold !important; border-radius: 12px !important; border: 2px solid #ffffff !important; }
    
    button[kind="secondary"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; font-weight: bold !important; }
    
    /* تنسيق لوحة الإدارة */
    .admin-panel { background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #1f6feb; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك إرسال الكود (تليجرام) ---
def send_admin_code(code):
    TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
    MY_ID = "906233240"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": MY_ID, "text": f"🔐 كود الدخول الخاص بك يا أيمن هو: {code}"}
    try:
        requests.post(url, data=payload)
        st.success("✅ تم إرسال الكود لحسابك الشخصي بنجاح.")
    except:
        st.error("⚠️ فشل الاتصال بالبوت.")

# --- 3. إدارة الذاكرة للوسائط ---
if 'v_ready' not in st.session_state: st.session_state.v_ready = False
if 'v_data' not in st.session_state: st.session_state.v_data = None
if 'v_url' not in st.session_state: st.session_state.v_url = ""

# --- 4. الواجهة السيادية ---
st.markdown(f'<div class="hero-section"><h1>{st.session_state.settings["site_title"]}</h1><p>{st.session_state.settings["site_sub"]}</p></div>', unsafe_allow_html=True)

# إضافة التبويب الخامس (الإدارة)
tabs = st.tabs(["🏠 الرئيسية", "🎬 مركز التحميل", "🔍 مركز الفحص", "🛡️ الحماية والدعم", "⚙️ الإدارة"])

# --- تبويب الرئيسية ---
with tabs[0]:
    st.markdown("### 📊 حالة النظام")
    c1, c2 = st.columns(2)
    c1.metric("المحرك الذكي", "متصل")
    c2.metric("التحديث الرسمي", "v37.0")
    st.info("مرحباً بك يا أيمن. تم تحديث بيانات الاتصال الرسمية بنجاح.")

# --- تبويب مركز التحميل ---
with tabs[1]:
    st.subheader("🎬 محرك الوسائط")
    u_in = st.text_input("أدخل رابط الفيديو المراد معالجته:", key="v_input")
    if st.button("🚀 بدء المعالجة الرسمية"):
        if u_in:
            with st.spinner("جاري فحص وتجهيز البيانات، يرجى الانتظار..."):
                try:
                    ydl_opts = {'format': 'best', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(u_in, download=False)
                        st.session_state.v_url = info.get('url')
                        st.session_state.v_data = requests.get(st.session_state.v_url).content
                        st.session_state.v_ready = True
                except: st.error("خطأ في معالجة الرابط.")

    if st.session_state.v_ready:
        st.video(st.session_state.v_url)
        st.download_button(label="📥 حفظ الفيديو في الاستوديو", data=st.session_state.v_data, file_name="Ayman_Guard_Video.mp4", mime="video/mp4")

# --- تبويب مركز الفحص ---
with tabs[2]:
    st.subheader("🔍 فحص الروابط والملفات")
    st.text_input("رابط التحليل:")
    st.markdown("---")
    st.markdown("#### 📁 فحص الملفات الذكي")
    st.file_uploader("اضغط لاختيار ملف لفحصه:", type=['apk', 'pdf', 'png', 'jpg', 'zip'])

# --- تبويب الحماية والدعم ---
with tabs[3]:
    st.subheader("🤖 المساعد الذكي الرسمي")
    st.markdown('<a href="https://t.me/Aiman_Guard_2026_bot" target="_blank" class="bot-btn">🤖 ابدأ المحادثة مع بوت الدرع الآن</a>', unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📞 قنوات التواصل الرسمية")
    col1, col2 = st.columns(2)
    with col1: st.markdown('<a href="https://wa.me/966556868717" target="_blank" class="contact-btn">📱 تواصل عبر واتساب</a>', unsafe_allow_html=True)
    with col2: st.markdown('<a href="mailto:kebriay2030@gmail.com" class="contact-btn">📧 البريد الإلكتروني</a>', unsafe_allow_html=True)
    st.markdown('<div style="background:#161b22; padding:20px; border-radius:12px; border-right:5px solid #1f6feb;"><h4>👥 حماية المجتمع</h4><p>نظام "درع أيمن" يلتزم بحماية خصوصيتكم.</p></div>', unsafe_allow_html=True)

# --- تبويب الإدارة (المدمج حديثاً) ---
with tabs[4]:
    if not st.session_state.is_admin:
        st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
        st.subheader("🔐 دخول المسؤول")
        pwd = st.text_input("أدخل كلمة مرور المسؤول:", type="password")
        if st.button("🔑 طلب كود التحقق"):
            if pwd == "Ayman2026":
                st.session_state.auth_code = str(random.randint(111111, 999999))
                send_admin_code(st.session_state.auth_code)
            else: st.error("كلمة المرور خاطئة!")
        
        if st.session_state.auth_code:
            v_code = st.text_input("أدخل الكود المستلم من تليجرام:")
            if st.button("✅ تأكيد الدخول"):
                if v_code == st.session_state.auth_code:
                    st.session_state.is_admin = True
                    st.rerun()
                else: st.error("كود التحقق غير صحيح!")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("🔓 أهلاً بك يا أيمن في غرفة التحكم.")
        if st.button("🚪 خروج آمن"):
            st.session_state.is_admin = False
            st.rerun()
        st.markdown("---")
        st.subheader("🛠️ إدارة مسميات الموقع")
        st.session_state.settings['site_title'] = st.text_input("تعديل عنوان الموقع:", st.session_state.settings['site_title'])
        st.session_state.settings['site_sub'] = st.text_area("تعديل الوصف الفرعي:", st.session_state.settings['site_sub'])
        if st.button("💾 حفظ التعديلات"):
            st.success("✅ تم تحديث مسميات الموقع فوراً!")
            time.sleep(1)
            st.rerun()
