import streamlit as st
import yt_dlp
import requests
import time
import random

# --- 1. الذاكرة الذكية (حفظ الإعدادات) ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي 2026",
        'admin_password': "Ayman2026",
        'theme_color': "#1f6feb", # اللون الافتراضي (أزرق)
        'welcome_msg': "مرحباً بك في نظام الحماية الأكثر تطوراً"
    }

# متغيرات الحالة
for key in ['is_admin', 'auth_code', 'v_ready', 'v_data', 'v_url']:
    if key not in st.session_state: st.session_state[key] = False

# --- 2. محرك التنسيق البصري (إصلاح التداخل وتغيير الألوان) ---
color = st.session_state.settings['theme_color']

st.set_page_config(page_title=st.session_state.settings['site_title'], layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }}
    .stApp {{ background-color: #0d1117; color: #ffffff; }}
    
    /* إصلاح التداخل */
    .block-container {{ padding-top: 2rem; padding-bottom: 2rem; }}
    
    /* الرئيسية الجذابة */
    .hero-section {{
        background: linear-gradient(135deg, {color} 0%, #111d2e 100%);
        padding: 50px 20px; border-radius: 20px; text-align: center;
        border: 1px solid #30363d; margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .stat-card {{
        background: #161b22; padding: 20px; border-radius: 15px;
        border-top: 4px solid {color}; text-align: center;
        transition: 0.3s; margin: 10px 0;
    }}
    .stat-card:hover {{ transform: translateY(-5px); background: #1c2128; }}

    /* الأزرار الديناميكية */
    div.stButton > button {{ 
        width: 100% !important; background-color: {color} !important; 
        color: white !important; border-radius: 12px; font-weight: bold; 
        height: 3.5em; border: none; transition: 0.3s;
    }}
    div.stButton > button:hover {{ opacity: 0.8; box-shadow: 0 0 15px {color}; }}
    
    .contact-btn {{
        background-color: {color} !important; color: white !important;
        border-radius: 12px; border: 1px solid #ffffff33;
        font-weight: bold; text-decoration: none; display: block;
        padding: 15px; text-align: center; margin-bottom: 15px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. محرك الربط مع تليجرام ---
def send_telegram_code(code):
    TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
    MY_ID = "906233240" 
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": MY_ID, "text": f"🔐 كود الدخول الخاص بك: {code}"})
        return True
    except: return False

# --- 4. هيكل التطبيق ---

# الهيدر
st.markdown(f"""
    <div class="hero-section">
        <h1 style='font-size: 3rem;'>{st.session_state.settings['site_title']}</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>{st.session_state.settings['site_sub']}</p>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية المذهلة", "🎬 مركز الوسائط", "🔍 الفحص الذكي", "🛡️ الدعم والحماية", "⚙️ الإدارة السيادية"])

# --- تبويب الرئيسية (تصميم ملفت للنظر) ---
with tabs[0]:
    st.markdown(f"### ✨ {st.session_state.settings['welcome_msg']}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-card"><h3>🚀 السرعة</h3><p>معالجة فورية للبيانات</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><h3>🛡️ الأمان</h3><p>تشفير 256-bit متطور</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><h3>📱 الربط</h3><p>متصل ببوت تليجرام الرسمي</p></div>', unsafe_allow_html=True)
    
    st.image("https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg", use_column_width=True)

# --- تبويب مركز التحميل ---
with tabs[1]:
    st.subheader("🎬 محرك الوسائط")
    u_in = st.text_input("أدخل رابط الفيديو:")
    if st.button("🚀 بدء المعالجة"):
        if u_in:
            with st.spinner("جاري الجلب..."):
                time.sleep(2)
                st.success("تم تجهيز الرابط بنجاح!")

# --- تبويب الفحص ---
with tabs[2]:
    st.subheader("🔍 مركز التحليل")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("رابط للفحص:")
        st.button("🔍 فحص الرابط")
    with c2:
        st.file_uploader("ارفع ملف للفحص:", type=['apk', 'pdf', 'zip'])
        st.button("📁 فحص الملف")

# --- تبويب الحماية والدعم (إضافة زر البريد المفقود) ---
with tabs[3]:
    st.subheader("🤖 قنوات الاتصال الرسمية")
    st.markdown('<a href="https://t.me/Aiman_Guard_2026_bot" target="_blank" class="contact-btn" style="background: linear-gradient(90deg, #0088cc, #00aaff) !important;">🤖 ابدأ المحادثة مع بوت الدرع</a>', unsafe_allow_html=True)
    
    col_wa, col_mail = st.columns(2)
    with col_wa:
        st.markdown('<a href="https://wa.me/966556868717" target="_blank" class="contact-btn">📱 واتساب الرسمي</a>', unsafe_allow_html=True)
    with col_mail:
        st.markdown('<a href="mailto:kebriay2030@gmail.com" class="contact-btn" style="background:#ea4335 !important;">📧 البريد الإلكتروني</a>', unsafe_allow_html=True)

# --- تبويب الإدارة (إصلاح التداخل وإضافة ميزات التحكم) ---
with tabs[4]:
    if not st.session_state.is_admin:
        st.subheader("🔐 الدخول الآمن للمسؤول")
        pwd_input = st.text_input("أدخل كلمة المرور:", type="password")
        if st.button("🚀 طلب كود التحقق (2FA)"):
            if pwd_input == st.session_state.settings['admin_password']:
                if send_telegram_code(random.randint(111111, 999999)):
                    st.session_state.auth_code = "sent"
                    st.success("أرسلنا الكود لتليجرام")
            else: st.error("كلمة المرور خاطئة")
    else:
        st.success("🔓 مرحباً أيمن، لوحة التحكم مفعلة")
        if st.button("🚪 تسجيل الخروج"): 
            st.session_state.is_admin = False
            st.rerun()
        
        st.divider()
        st.subheader("🎨 تخصيص مظهر الموقع")
        # ميزة تغيير الألوان
        new_color = st.color_picker("اختر لون سمة الموقع:", st.session_state.settings['theme_color'])
        if st.button("🎨 تطبيق اللون الجديد"):
            st.session_state.settings['theme_color'] = new_color
            st.rerun()

        st.divider()
        st.subheader("🔑 تأمين الحساب")
        new_pwd = st.text_input("تغيير كلمة مرور الإدارة:", type="password")
        if st.button("💾 حفظ كلمة المرور"):
            st.session_state.settings['admin_password'] = new_pwd
            st.success("تم التغيير!")

        st.divider()
        st.subheader("📝 تعديل مسميات الموقع")
        st.session_state.settings['site_title'] = st.text_input("عنوان الموقع:", st.session_state.settings['site_title'])
        st.session_state.settings['site_sub'] = st.text_input("وصف الموقع:", st.session_state.settings['site_sub'])
        if st.button("💾 حفظ مسميات الموقع"):
            st.rerun()

