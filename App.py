import streamlit as st
import requests
import random
import time

# --- 1. إعدادات الموقع الديناميكية ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي v48.0",
        'tab1': "🏠 الرئيسية", 'tab2': "🎬 مركز التحميل", 
        'tab3': "🔍 مركز الفحص", 'tab4': "🛡️ الحماية والدعم", 'tab5': "⚙️ الإدارة",
        'btn_process': "🚀 بدء المعالجة الرسمية",
        'btn_tele': "💬 تليجرام الرسمي",
        'btn_wa': "📱 واتساب الرسمي"
    }

if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None

# --- 2. محرك الإرسال (بوت أيمن يرسل لأيمن شخصياً) ---
def send_telegram_code(code):
    # توكن البوت الخاص بك
    TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
    # الـ ID الشخصي الخاص بك (الذي أرسلته الآن)
    MY_PERSONAL_ID = "906233240" 
    
    message = f"🔐 مرحباً أيمن، كود الدخول للوحة الإدارة هو: {code}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    try:
        response = requests.post(url, data={"chat_id": MY_PERSONAL_ID, "text": message})
        if response.status_code == 200:
            st.success("✅ الكود وصل لحسابك الشخصي (شموخي عنواني)!")
        else:
            # توضيح إذا كان البوت يحتاج تفعيل
            st.error("❌ فشل الإرسال! تأكد أنك ضغطت Start داخل بوتك @Aiman_Guard_2026_bot")
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

# --- 4. بناء الواجهة السيادية ---
st.markdown(f'<h1 style="text-align:center;">{st.session_state.settings["site_title"]}</h1>', unsafe_allow_html=True)

tabs = st.tabs([st.session_state.settings[f'tab{i}'] for i in range(1, 6)])

# --- تبويب الإدارة (التحكم الكامل) ---
with tabs[4]:
    if not st.session_state.is_admin:
        st.subheader("🔐 بوابة الإدارة الآمنة")
        admin_pwd = st.text_input("كلمة المرور:", type="password")
        
        if st.button("🚀 إرسال كود التحقق لهاتفي"):
            if admin_pwd == "Ayman2026":
                st.session_state.auth_code = str(random.randint(111111, 999999))
                send_telegram_code(st.session_state.auth_code)
            else:
                st.error("كلمة المرور خاطئة!")

        if st.session_state.auth_code:
            v_code = st.text_input("أدخل الكود الذي وصلك على تليجرام:")
            if st.button("✅ فتح النظام"):
                if v_code == st.session_state.auth_code:
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("الكود غير صحيح!")
    else:
        st.success("🔓 أهلاً بك يا أيمن. يمكنك الآن تعديل أي نص في الموقع.")
        if st.button("🚪 خروج"): 
            st.session_state.is_admin = False
            st.rerun()
        
        st.markdown("---")
        # قسم التحكم الديناميكي (طلبك الثاني)
        st.subheader("🛠️ لوحة تغيير المسميات")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.settings['site_title'] = st.text_input("عنوان الموقع:", st.session_state.settings['site_title'])
            st.session_state.settings['btn_process'] = st.text_input("نص زر المعالجة:", st.session_state.settings['btn_process'])
        with col2:
            st.session_state.settings['tab1'] = st.text_input("اسم التبويب 1:", st.session_state.settings['tab1'])
            st.session_state.settings['btn_tele'] = st.text_input("نص زر تليجرام:", st.session_state.settings['btn_tele'])

        if st.button("💾 حفظ التعديلات"):
            st.success("✅ تم تحديث جميع أزرار الموقع بنجاح!")
            time.sleep(1)
            st.rerun()
