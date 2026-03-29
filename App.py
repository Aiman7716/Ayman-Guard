import streamlit as st
import requests
import random
import time

# --- 1. إعدادات الهوية والديناميكية (التحكم الكامل) ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي v45.0",
        'tab1': "🏠 الرئيسية", 'tab2': "🎬 مركز التحميل", 
        'tab3': "🔍 مركز الفحص", 'tab4': "🛡️ الحماية والدعم", 'tab5': "⚙️ الإدارة",
        'btn_process': "🚀 بدء المعالجة الرسمية",
        'btn_tele': "💬 تليجرام الرسمي",
        'btn_wa': "📱 واتساب الرسمي",
        'btn_mail': "📧 البريد الإلكتروني"
    }

if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None

# --- 2. محرك إرسال الكود الحقيقي لبوت @Aiman_Guard_2026_bot ---
def send_telegram_code(code):
    # التوكن الرسمي الذي أرسلته يا أيمن
    TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
    # معرفك الشخصي المستخرج من الصورة
    CHAT_ID = "8124974140"
    
    message = f"🔐 مرحباً أيمن، كود الدخول للوحة الإدارة هو: {code}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    try:
        response = requests.post(url, data={"chat_id": CHAT_ID, "text": message})
        if response.status_code == 200:
            st.success("✅ تم إرسال الكود لهاتفك بنجاح عبر تليجرام!")
        else:
            error_details = response.json().get('description', 'خطأ غير معروف')
            st.error(f"❌ خطأ من تليجرام: {error_details} (تأكد من الضغط على Start في البوت)")
    except Exception as e:
        st.error(f"⚠️ فشل الاتصال بالشبكة: {e}")

# --- 3. التنسيق السيادي الموحد ---
st.set_page_config(page_title=st.session_state.settings['site_title'], layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }}
    .stApp {{ background-color: #0d1117; color: #ffffff; }}
    .hero-section {{ background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d; }}
    div.stButton > button {{ width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; font-weight: bold; height: 3.5em; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. بناء الواجهة ---
st.markdown(f'<div class="hero-section"><h1>{st.session_state.settings["site_title"]}</h1><p>{st.session_state.settings["site_sub"]}</p></div>', unsafe_allow_html=True)

tabs = st.tabs([st.session_state.settings[f'tab{i}'] for i in range(1, 6)])

# --- تبويب الإدارة (لوحة التحكم مع 2FA الفعلي) ---
with tabs[4]:
    if not st.session_state.is_admin:
        st.subheader("🔐 الدخول الآمن للمسؤول")
        admin_pwd = st.text_input("أدخل كلمة مرور المسؤول:", type="password")
        
        if st.button("🚀 طلب كود التحقق (2FA)"):
            if admin_pwd == "Ayman2026":
                st.session_state.auth_code = str(random.randint(111111, 999999))
                send_telegram_code(st.session_state.auth_code) # إرسال فعلي للبوت
            else:
                st.error("كلمة المرور خاطئة!")

        if st.session_state.auth_code:
            v_code = st.text_input("أدخل الكود المستلم من التليجرام:")
            if st.button("✅ تأكيد الهوية وفتح الإدارة"):
                if v_code == st.session_state.auth_code:
                    st.session_state.is_admin = True
                    st.success("أهلاً بك يا أيمن. جاري فتح غرفة التحكم...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("كود التحقق خاطئ!")
    else:
        st.success("🔓 لوحة التحكم الكاملة مفتوحة الآن.")
        if st.button("🚪 خروج آمن"): st.session_state.is_admin = False; st.rerun()
        
        # هنا تضع مربعات تعديل مسميات الأزرار والتبويبات كما فعلنا في v40
        st.markdown("### ⚙️ إدارة مسميات النظام")
        st.session_state.settings['site_title'] = st.text_input("عنوان الموقع:", st.session_state.settings['site_title'])
        # وبقية الأزرار...
