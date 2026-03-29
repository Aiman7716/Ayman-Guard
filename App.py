import streamlit as st
import requests
import random
import time

# --- 1. إعدادات الذاكرة للهوية (لتخزين التعديلات) ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي 2026",
        'btn_download': "🚀 بدء التحميل",
        'tab_name_1': "🏠 الرئيسية",
        'status': "متصل ✅"
    }

if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None

# --- 2. دالة الربط مع تليجرام (المصادقة الثنائية) ---
def send_telegram_2fa(code):
    # بياناتك التي استخرجناها من المحادثة
    TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
    MY_ID = "906233240" # هويتك الشخصية (أيمن)
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": MY_ID,
        "text": f"🔐 محاولة دخول للنظام!\n\nمرحباً أيمن، كود التحقق الخاص بك هو: {code}\nإذا لم تكن أنت، يرجى تأمين حسابك."
    }
    try:
        requests.post(url, data=payload)
        st.success("✅ تم إرسال الكود السري إلى حسابك الشخصي في تليجرام.")
    except:
        st.error("⚠️ فشل الاتصال بالبوت، تأكد من جودة الإنترنت.")

# --- 3. تصميم واجهة تبويب الإدارة ---
def admin_tab():
    st.markdown("### ⚙️ لوحة التحكم المركزية")
    
    if not st.session_state.is_admin:
        # --- مرحلة تسجيل الدخول ---
        with st.container():
            st.info("هذا القسم مخصص للمسؤول فقط. يرجى إثبات الهوية.")
            admin_pwd = st.text_input("أدخل كلمة المرور الرئيسية:", type="password")
            
            if st.button("🚀 طلب كود التحقق (2FA)"):
                if admin_pwd == "Ayman2026":
                    # توليد كود عشوائي وإرساله
                    st.session_state.auth_code = str(random.randint(111111, 999999))
                    send_telegram_2fa(st.session_state.auth_code)
                else:
                    st.error("❌ كلمة المرور غير صحيحة!")

            if st.session_state.auth_code:
                v_code = st.text_input("أدخل الكود المكون من 6 أرقام (من تليجرام):")
                if st.button("✅ تأكيد الدخول"):
                    if v_code == st.session_state.auth_code:
                        st.session_state.is_admin = True
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ الكود خاطئ، حاول مجدداً.")
    else:
        # --- مرحلة التحكم (بعد الدخول بنجاح) ---
        st.success(f"🔓 أهلاً بك يا أيمن. النظام تحت سيطرتك الآن.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚪 تسجيل الخروج الآمن"):
                st.session_state.is_admin = False
                st.rerun()
        
        st.markdown("---")
        st.subheader("🛠️ تعديل محتوى الموقع (بث مباشر)")
        
        # نماذج التعديل
        new_title = st.text_input("تعديل عنوان الموقع الرئيسي:", st.session_state.settings['site_title'])
        new_sub = st.text_area("تعديل الوصف الفرعي:", st.session_state.settings['site_sub'])
        new_btn = st.text_input("تعديل مسمى زر التحميل:", st.session_state.settings['btn_download'])
        
        if st.button("💾 حفظ وتطبيق التعديلات فوراً"):
            st.session_state.settings['site_title'] = new_title
            st.session_state.settings['site_sub'] = new_sub
            st.session_state.settings['btn_download'] = new_btn
            st.success("✅ تم تحديث جميع الواجهات بنجاح!")
            time.sleep(1)
            st.rerun()

# استدعاء التبويب (للتجربة)
admin_tab()
