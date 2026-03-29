import streamlit as st
import yt_dlp
import requests
import random

# --- 1. إعداد مخزن البيانات الديناميكي (لوحة التحكم) ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي v38.0",
        'tab1_name': "🏠 الرئيسية",
        'tab2_name': "🎬 مركز التحميل",
        'tab3_name': "🔍 مركز الفحص",
        'tab4_name': "🛡️ الحماية والدعم",
        'btn_process': "🚀 بدء المعالجة الرسمية",
        'btn_save': "📥 حفظ الفيديو في الاستوديو"
    }

if 'auth_code' not in st.session_state: st.session_state.auth_code = None
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 2. التنسيق السيادي الموحد ---
st.set_page_config(page_title=st.session_state.settings['site_title'], layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }}
    .stApp {{ background-color: #0d1117; color: #ffffff; }}
    .hero-section {{
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; border: 1px solid #30363d;
    }}
    div.stButton > button {{ width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; font-weight: bold; height: 3.5em; }}
    </style>
""", unsafe_allow_html=True)

# --- 3. الواجهة الرئيسية (ديناميكية) ---
st.markdown(f'<div class="hero-section"><h1>{st.session_state.settings["site_title"]}</h1><p>{st.session_state.settings["site_sub"]}</p></div>', unsafe_allow_html=True)

tabs = st.tabs([
    st.session_state.settings['tab1_name'], 
    st.session_state.settings['tab2_name'], 
    st.session_state.settings['tab3_name'], 
    st.session_state.settings['tab4_name'],
    "⚙️ الإدارة"
])

# --- تبويب مركز التحميل (يستخدم المسميات الديناميكية) ---
with tabs[1]:
    st.subheader(st.session_state.settings['tab2_name'])
    u_in = st.text_input("أدخل الرابط:")
    if st.button(st.session_state.settings['btn_process']):
        st.info("جاري المعالجة...")
    # هنا تضع كود التحميل السابق v37 كما هو

# --- تبويب الإدارة (لوحة التحكم مع 2FA) ---
with tabs[4]:
    if not st.session_state.is_admin:
        st.subheader("🔐 تسجيل دخول الإدارة")
        pwd = st.text_input("أدخل كلمة مرور المسؤول:", type="password")
        
        if st.button("🚀 طلب كود التحقق (2FA)"):
            if pwd == "aiman2026": # كلمة المرور الافتراضية
                st.session_state.auth_code = str(random.randint(1000, 9999))
                # إرسال الكود للبوت (محاكاة الربط مع API التليجرام)
                # ملاحظة: يتطلب توكن البوت الحقيقي لإرسال الرسالة فعلياً
                st.warning(f"تم إرسال كود التحقق إلى بوت التليجرام الخاص بك @Aiman_Guard_2026_bot")
                st.info(f"💡 (لغرض التجربة حالياً الكود هو: {st.session_state.auth_code})")
            else:
                st.error("كلمة المرور خاطئة!")

        if st.session_state.auth_code:
            v_code = st.text_input("أدخل كود التحقق المستلم من التليجرام:")
            if st.button("✅ تأكيد الدخول"):
                if v_code == st.session_state.auth_code:
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("كود التحقق غير صحيح!")
    else:
        st.success("🔓 مرحباً أيمن! أنت الآن في لوحة التحكم الديناميكية.")
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.is_admin = False
            st.rerun()
            
        st.markdown("---")
        
        # خيارات التحكم في مسميات الموقع
        st.subheader("🛠️ تعديل إعدادات الواجهة")
        
        with st.expander("📝 تعديل النصوص والترويسة"):
            new_title = st.text_input("تغيير عنوان الموقع:", st.session_state.settings['site_title'])
            new_sub = st.text_input("تغيير وصف الترويسة:", st.session_state.settings['site_sub'])
            
        with st.expander("📂 تغيير مسميات التبويبات"):
            t1 = st.text_input("اسم تبويب الرئيسية:", st.session_state.settings['tab1_name'])
            t2 = st.text_input("اسم تبويب التحميل:", st.session_state.settings['tab2_name'])
            
        with st.expander("🔘 تغيير مسميات الأزرار"):
            b1 = st.text_input("نص زر المعالجة:", st.session_state.settings['btn_process'])
            b2 = st.text_input("نص زر الحفظ:", st.session_state.settings['btn_save'])

        if st.button("💾 حفظ التعديلات وتطبيقها فوراً"):
            st.session_state.settings.update({
                'site_title': new_title, 'site_sub': new_sub,
                'tab1_name': t1, 'tab2_name': t2,
                'btn_process': b1, 'btn_save': b2
            })
            st.success("✅ تم تحديث إعدادات الموقع بنجاح!")
            time.sleep(1)
            st.rerun()

# (بقية التبويبات v37 تظل كما هي)
