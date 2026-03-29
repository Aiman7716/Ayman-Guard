import streamlit as st
import yt_dlp
import requests
import time
import random

# --- 1. قاعدة البيانات الديناميكية (إدارة المسميات) ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي v60.0",
        'tab1': "🏠 الرئيسية", 'tab2': "🎬 مركز التحميل", 
        'tab3': "🔍 مركز الفحص", 'tab4': "🛡️ الحماية والدعم", 'tab5': "⚙️ الإدارة",
        'btn_download': "🚀 بدء المعالجة الرسمية",
        'btn_save': "📥 حفظ الفيديو في الاستوديو",
        'btn_scan': "🛡️ ابدأ الفحص الأمني الآن"
    }

if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None

# --- 2. محرك المصادقة الثنائية (تليجرام) ---
def send_telegram_code(code):
    TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
    MY_PERSONAL_ID = "906233240" 
    message = f"🔐 مرحباً أيمن، كود الدخول للوحة الإدارة هو: {code}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": MY_PERSONAL_ID, "text": message})
        st.success("✅ تم إرسال الكود لحسابك الشخصي (شموخي عنواني).")
    except:
        st.error("⚠️ فشل الاتصال ببوت التليجرام.")

# --- 3. التنسيق السيادي الموحد (CSS المطور) ---
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
}
div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; font-weight: bold; height: 3.5em; border: none; }
.stDownloadButton > button { 
    background: linear-gradient(90deg, #ff9100, #ff6d00) !important; /* لون بارز كما طلبت */
    width: 100% !important; height: 4.5em !important; font-size: 20px !important; 
    font-weight: bold !important; border-radius: 12px !important; border: 2px solid #ffffff !important; 
}
</style>
""", unsafe_allow_html=True)

# --- 4. الهيكل العلوي ---
st.markdown(f'<div class="hero-section"><h1>{st.session_state.settings["site_title"]}</h1><p>{st.session_state.settings["site_sub"]}</p></div>', unsafe_allow_html=True)

tabs = st.tabs([st.session_state.settings[f'tab{i}'] for i in range(1, 6)])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.markdown("### 📊 حالة النظام")
    col1, col2 = st.columns(2)
    col1.metric("المحرك الذكي", "متصل ✅")
    col2.metric("التحديث الرسمي", "v60.0")
    st.info(f"أهلاً بك يا أيمن في واجهتك السيادية. النظام محمي ببروتوكول 2FA.")

# --- التبويب 2: مركز التحميل ---
with tabs[1]:
    st.subheader(st.session_state.settings['tab2'])
    u_in = st.text_input("أدخل رابط الفيديو المراد معالجته:")
    if st.button(st.session_state.settings['btn_download']):
        if u_in:
            st.info("جاري المعالجة... يرجى الانتظار.")
            # هنا تدمج كود yt_dlp للتحميل

# --- التبويب 3: مركز الفحص (مع زر الملفات البارز) ---
with tabs[2]:
    st.subheader(st.session_state.settings['tab3'])
    st.text_input("رابط التحليل الأمني:")
    st.button(st.session_state.settings['btn_scan'])
    st.markdown("---")
    st.markdown("#### 📁 فحص الملفات الذكي")
    file = st.file_uploader("اضغط لاختيار ملف لفحصه:", type=['apk', 'pdf', 'png', 'jpg', 'zip'])
    # زر التحميل البارز جداً (برتقالي متدرج)
    st.download_button(label="📥 رفع الملف وتأكيد الفحص الشامل", data="file", file_name="scan_report.txt")

# --- التبويب 4: الحماية والدعم ---
with tabs[3]:
    st.subheader("🤖 المساعد الذكي الرسمي")
    st.markdown('<a href="https://t.me/Aiman_Guard_2026_bot" target="_blank" class="bot-btn">🤖 ابدأ المحادثة مع بوت الدرع الآن</a>', unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📞 قنوات التواصل")
    c1, c2 = st.columns(2)
    with c1: st.markdown('<a href="https://wa.me/966556868717" class="contact-btn">📱 واتساب الرسمي</a>', unsafe_allow_html=True)
    with c2: st.markdown('<a href="mailto:kebriay2030@gmail.com" class="contact-btn">📧 البريد الإلكتروني</a>', unsafe_allow_html=True)

# --- التبويب 5: لوحة الإدارة (المحرك المدمج) ---
with tabs[4]:
    if not st.session_state.is_admin:
        st.subheader("🔐 دخول المسؤول")
        admin_pwd = st.text_input("كلمة المرور:", type="password")
        if st.button("🚀 إرسال كود التحقق (2FA)"):
            if admin_pwd == "Ayman2026":
                st.session_state.auth_code = str(random.randint(111111, 999999))
                send_telegram_code(st.session_state.auth_code)
            else: st.error("كلمة المرور خاطئة!")
        
        if st.session_state.auth_code:
            v_code = st.text_input("أدخل الكود المستلم من تليجرام:")
            if st.button("✅ فتح لوحة التحكم"):
                if v_code == st.session_state.auth_code:
                    st.session_state.is_admin = True
                    st.rerun()
    else:
        st.success("🔓 أهلاً أيمن، أنت في لوحة التحكم الآن.")
        if st.button("🚪 خروج آمن"): st.session_state.is_admin = False; st.rerun()
        
        st.markdown("### 🛠️ تعديل مسميات الموقع")
        st.session_state.settings['site_title'] = st.text_input("عنوان الموقع:", st.session_state.settings['site_title'])
        st.session_state.settings['tab2'] = st.text_input("اسم تبويب التحميل:", st.session_state.settings['tab2'])
        if st.button("💾 حفظ التعديلات"):
            st.success("✅ تم تحديث مسميات الموقع فوراً!")
            time.sleep(1)
            st.rerun()
