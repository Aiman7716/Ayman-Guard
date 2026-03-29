import streamlit as st
import requests
import random
import time

# --- 1. إعدادات الهوية (لوحة التحكم) ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي v42.0",
        'tab1': "🏠 الرئيسية", 'tab2': "🎬 مركز التحميل", 
        'tab3': "🔍 مركز الفحص", 'tab4': "🛡️ الحماية والدعم", 'tab5': "⚙️ الإدارة",
        'btn_process': "🚀 بدء المعالجة الرسمية",
        'btn_tele': "💬 تليجرام الرسمي"
    }

if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None

# --- 2. محرك إرسال الكود الفعلي لبوت @Aiman_Guard_2026_bot ---
def send_telegram_code(code):
    # ⚠️ هام جداً: ضع التوكن الخاص بك هنا الذي أخذته من BotFather
    TOKEN = "YOUR_BOT_TOKEN_HERE" 
    
    # تم استخراج المعرف من صورتك يا أيمن
    CHAT_ID = "8124974140" 
    
    message = f"🔐 مرحباً أيمن، كود التحقق للدخول إلى لوحة الإدارة هو: {code}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            st.success("✅ تم إرسال الكود السري إلى حسابك في تليجرام بنجاح.")
        else:
            st.error("❌ فشل الإرسال: تأكد من صحة التوكن (Token) وأنك أرسلت /start للبوت أولاً.")
    except Exception as e:
        st.error(f"⚠️ خطأ في الاتصال: {e}")

# --- 3. تصميم الواجهة ---
st.set_page_config(page_title=st.session_state.settings['site_title'], layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }}
    .stApp {{ background-color: #0d1117; color: #ffffff; }}
    div.stButton > button {{ width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; font-weight: bold; height: 3.5em; }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f'<h1>{st.session_state.settings["site_title"]}</h1>', unsafe_allow_html=True)

tabs = st.tabs([st.session_state.settings[f'tab{i}'] for i in range(1, 6)])

# --- تبويب الإدارة (لوحة التحكم مع 2FA الفعلي) ---
with tabs[4]:
    if not st.session_state.is_admin:
        st.subheader("🔐 الدخول الآمن للمسؤول")
        admin_pwd = st.text_input("أدخل كلمة المرور:", type="password")
        
        if st.button("🚀 طلب كود التحقق (2FA)"):
            if admin_pwd == "Ayman2026":
                # توليد كود من 6 أرقام
                st.session_state.auth_code = str(random.randint(111111, 999999))
                # استدعاء دالة الإرسال
                send_telegram_code(st.session_state.auth_code)
            else:
                st.error("كلمة المرور غير صحيحة!")

        if st.session_state.auth_code:
            v_code = st.text_input("أدخل الكود الذي وصلك الآن على تليجرام:")
            if st.button("✅ تأكيد الدخول"):
                if v_code == st.session_state.auth_code:
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("الكود المدخل غير صحيح!")
    else:
        st.success("🔓 أهلاً بك يا أيمن في لوحة التحكم.")
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.is_admin = False
            st.rerun()
