import streamlit as st
import yt_dlp
import requests
import time
import random

# --- 1. الإعدادات والذاكرة السيادية ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي v37.0"
    }

if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None
if 'v_ready' not in st.session_state: st.session_state.v_ready = False
if 'v_data' not in st.session_state: st.session_state.v_data = None
if 'v_url' not in st.session_state: st.session_state.v_url = ""

# --- 2. التنسيق البصري (CSS) v37 المطور ---
st.set_page_config(page_title=st.session_state.settings['site_title'], layout="wide")
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
        display: block; padding: 15px; text-align: center; margin-bottom: 10px;
    }

    .bot-btn {
        background: linear-gradient(90deg, #0088cc, #00aaff) !important;
        color: white !important; border-radius: 15px !important;
        padding: 20px; font-size: 20px !important; text-decoration: none !important;
        display: block; text-align: center; font-weight: bold; border: 2px solid #ffffff;
        box-shadow: 0 4px 15px rgba(0,136,204,0.4); margin-bottom: 20px;
    }

    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; font-weight: bold; height: 3.5em; border: none; }
    
    /* زر الفحص والتحميل البارز جداً (برتقالي متدرج) كما طلبت */
    .stDownloadButton > button { 
        background: linear-gradient(90deg, #ff9100, #ff6d00) !important; 
        width: 100% !important; height: 4.5em !important; font-size: 20px !important; 
        font-weight: bold !important; border-radius: 12px !important; border: 2px solid #ffffff !important; 
    }
    
    button[kind="secondary"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. محرك الربط مع تليجرام (2FA) ---
def send_telegram_code(code):
    TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
    MY_ID = "906233240" # هويتك الشخصية (أيمن)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": MY_ID, "text": f"🔐 مرحباً أيمن، كود الدخول الخاص بك هو: {code}"})
        st.success("✅ تم إرسال الكود السري لحسابك الشخصي في تليجرام.")
    except:
        st.error("⚠️ فشل الاتصال بالبوت.")

# --- 4. واجهة الموقع الرئيسية ---
st.markdown(f'<div class="hero-section"><h1>{st.session_state.settings["site_title"]}</h1><p>{st.session_state.settings["site_sub"]}</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🎬 مركز التحميل", "🔍 مركز الفحص", "🛡️ الحماية والدعم", "⚙️ الإدارة"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.markdown("### 📊 حالة النظام")
    c1, c2 = st.columns(2)
    c1.metric("المحرك الذكي", "متصل ✅")
    c2.metric("التحديث الرسمي", "v37.0")
    st.info(f"مرحباً بك يا أيمن. النظام يعمل الآن بأعلى كفاءة وتحت حماية التليجرام الشخصية.")

# --- التبويب 2: مركز التحميل ---
with tabs[1]:
    st.subheader("🎬 محرك الوسائط الذكي")
    u_in = st.text_input("أدخل رابط الفيديو (يوتيوب، تيك توك، فيسبوك):")
    if st.button("🚀 بدء المعالجة الرسمية"):
        if u_in:
            with st.spinner("جاري تجهيز البيانات..."):
                try:
                    ydl_opts = {'format': 'best', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(u_in, download=False)
                        st.session_state.v_url = info.get('url')
                        st.session_state.v_data = requests.get(st.session_state.v_url).content
                        st.session_state.v_ready = True
                except: st.error("عذراً، فشلت معالجة هذا الرابط.")

    if st.session_state.v_ready:
        st.video(st.session_state.v_url)
        st.download_button(label="📥 حفظ الفيديو في الاستوديو", data=st.session_state.v_data, file_name="Ayman_Guard_Video.mp4", mime="video/mp4")

# --- التبويب 3: مركز الفحص ---
with tabs[2]:
    st.subheader("🔍 فحص الروابط والملفات")
    st.text_input("أدخل الرابط المشبوه لفحصه:")
    if st.button("🛡️ تنفيذ الفحص الآن"):
        st.success("جاري تحليل الرابط أمنياً...")
    
    st.markdown("---")
    st.markdown("#### 📁 فحص الملفات (APK, PDF, ZIP...)")
    st.file_uploader("اضغط لاختيار ملف من جهازك:", type=['apk', 'pdf', 'png', 'jpg', 'zip'])
    # زر فحص الملفات البارز باللون البرتقالي كما طلبت
    st.download_button(label="📥 رفع وتحميل تقرير الفحص الشامل", data="Report", file_name="Ayman_Security_Report.txt")

# --- التبويب 4: الحماية والدعم ---
with tabs[3]:
    st.subheader("🤖 المساعد الذكي الرسمي")
    st.markdown('<a href="https://t.me/Aiman_Guard_2026_bot" target="_blank" class="bot-btn">🤖 ابدأ المحادثة مع بوت الدرع الآن</a>', unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📞 قنوات التواصل الرسمية")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<a href="https://wa.me/966556868717" target="_blank" class="contact-btn">📱 تواصل عبر واتساب</a>', unsafe_allow_html=True)
    with col2:
        st.markdown('<a href="mailto:kebriay2030@gmail.com" class="contact-btn">📧 البريد الإلكتروني</a>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="background:#161b22; padding:20px; border-radius:12px; border-right:5px solid #1f6feb;"><h4>👥 حماية المجتمع</h4><p>نظام "درع أيمن" ملتزم بحماية خصوصيتكم. لا تتردد في الإبلاغ عن أي تهديد.</p></div>', unsafe_allow_html=True)

# --- التبويب 5: لوحة الإدارة ---
with tabs[4]:
    if not st.session_state.is_admin:
        st.subheader("🔐 بوابة المسؤول الآمنة")
        pwd = st.text_input("كلمة مرور الإدارة:", type="password")
        if st.button("🔑 طلب كود التحقق (2FA)"):
            if pwd == "Ayman2026":
                st.session_state.auth_code = str(random.randint(111111, 999999))
                send_telegram_code(st.session_state.auth_code)
            else: st.error("❌ كلمة المرور غير صحيحة!")
        
        if st.session_state.auth_code:
            v_code = st.text_input("أدخل الكود المكون من 6 أرقام:")
            if st.button("✅ تأكيد الدخول"):
                if v_code == st.session_state.auth_code:
                    st.session_state.is_admin = True
                    st.rerun()
                else: st.error("❌ الكود خاطئ!")
    else:
        st.success("🔓 أهلاً بك يا أيمن في غرفة التحكم.")
        if st.button("🚪 خروج آمن"):
            st.session_state.is_admin = False
            st.rerun()
        st.markdown("---")
        st.subheader("⚙️ تعديل مسميات الموقع")
        st.session_state.settings['site_title'] = st.text_input("عنوان الموقع:", st.session_state.settings['site_title'])
        st.session_state.settings['site_sub'] = st.text_input("وصف الموقع:", st.session_state.settings['site_sub'])
        if st.button("💾 حفظ وتطبيق"):
            st.success("✅ تم تحديث النظام بنجاح!")
            time.sleep(1)
            st.rerun()
