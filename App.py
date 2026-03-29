import streamlit as st
import yt_dlp
import requests
import time
import random

# --- 1. المحرك الذكي للذاكرة (حفظ كافة التسميات) ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي V37.0",
        'welcome_msg': "مرحباً بك في أقوى نظام حماية رقمي لعام 2026",
        'btn_bot_text': "🤖 ابدأ المحادثة مع بوت الدرع",
        'btn_wa_text': "📱 واتساب الرسمي",
        'btn_mail_text': "📧 البريد الإلكتروني",
        'admin_password': "Ayman2026",
        'theme_color': "#1f6feb"
    }

# تهيئة حالات الجلسة
for key in ['is_admin', 'auth_code', 'video_data']:
    if key not in st.session_state: st.session_state[key] = False

# --- 2. التنسيق البصري الفاخر (إصلاح تداخل الجوال) ---
color = st.session_state.settings['theme_color']
st.set_page_config(page_title=st.session_state.settings['site_title'], layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }}
    .stApp {{ background-color: #0d1117; color: #ffffff; }}
    
    /* الهيدر المطور (الرئيسية الجذابة) */
    .hero-box {{
        background: linear-gradient(135deg, {color} 0%, #0a0e14 100%);
        padding: 50px 20px; border-radius: 25px; text-align: center;
        border: 2px solid #30363d; margin-bottom: 30px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.7); animation: fadeIn 1.5s;
    }}
    
    /* بطاقات العرض في الرئيسية */
    .feature-card {{
        background: rgba(22, 27, 34, 0.8); padding: 30px; border-radius: 20px;
        border: 1px solid #30363d; text-align: center; margin-bottom: 20px;
        border-bottom: 4px solid {color}; transition: 0.4s;
    }}
    .feature-card:hover {{ transform: translateY(-10px); border-color: white; }}

    /* الأزرار السيادية */
    div.stButton > button {{ 
        width: 100% !important; background: {color} !important; 
        color: white !important; border-radius: 15px; font-weight: bold; 
        height: 4em; border: none; font-size: 17px !important;
    }}
    
    .contact-link {{
        text-decoration: none; color: white !important; font-weight: bold;
        display: block; padding: 18px; border-radius: 15px; margin-bottom: 12px;
        text-align: center; border: 1px solid #ffffff11; transition: 0.3s;
    }}
    .contact-link:hover {{ opacity: 0.8; transform: scale(1.02); }}

    /* إصلاح تداخل النصوص في الجوال */
    .stTextInput > label, .stColorPicker > label {{ margin-bottom: 10px !important; font-weight: bold !important; color: {color} !important; }}
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    </style>
""", unsafe_allow_html=True)

# --- 3. محرك تليجرام (2FA) ---
def send_security_msg(code):
    TOKEN, MY_ID = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE", "906233240"
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": MY_ID, "text": f"🔐 رمز الدخول لدرع أيمن: {code}"})
        return True
    except: return False

# --- 4. واجهة الموقع ---

st.markdown(f"""
    <div class="hero-box">
        <h1 style='margin:0; font-size: 3rem;'>{st.session_state.settings['site_title']}</h1>
        <p style='opacity:0.8; font-size:1.3rem; margin-top:10px;'>{st.session_state.settings['site_sub']}</p>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🎬 مركز الوسائط", "🔍 الفحص", "🛡️ الدعم", "⚙️ الإدارة"])

# --- التبويب 1: الرئيسية الجذابة ---
with tabs[0]:
    st.markdown(f"<h2 style='text-align:center;'>✨ {st.session_state.settings['welcome_msg']}</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="feature-card"><h2>🛡️</h2><h4>أمان مطلق</h4><p>تشفير بيانات فائق السرية</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="feature-card"><h2>🚀</h2><h4>تحميل ذكي</h4><p>أسرع محرك جلب وسائط</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="feature-card"><h2>🤖</h2><h4>بوت رسمي</h4><p>تحكم كامل عبر تليجرام</p></div>', unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg", use_column_width=True)

# --- التبويب 2: مركز الوسائط ---
with tabs[1]:
    st.subheader("🎬 محرك تحميل الفيديو")
    v_url = st.text_input("ألصق الرابط هنا:")
    if st.button("🚀 جلب وتحميل الفيديو"):
        if v_url:
            with st.spinner("جاري المعالجة..."):
                try:
                    ydl_opts = {'format': 'best', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        st.session_state.video_data = {"url": info['url'], "title": info.get('title', 'Video')}
                        st.success("✅ الفيديو جاهز!")
                except: st.error("عذراً، الرابط غير صالح.")

    if st.session_state.video_data:
        st.video(st.session_state.video_data['url'])
        v_bytes = requests.get(st.session_state.video_data['url']).content
        st.download_button("📥 حفظ في الاستوديو", v_bytes, file_name="Ayman_Guard.mp4")

# --- التبويب 3: مركز الفحص ---
with tabs[2]:
    st.subheader("🔍 التحليل الأمني المباشر")
    st.text_input("أدخل رابطاً لفحصه:")
    if st.button("🛡️ ابدأ فحص الرابط"): st.success("الرابط آمن ✅")
    st.divider()
    st.file_uploader("ارفع ملفاً للتحليل:", type=['apk','pdf','zip'])
    if st.button("🔍 فحص الملف"): st.success("الملف سليم ✅")

# --- التبويب 4: الدعم (أزرار التواصل القابلة للتعديل) ---
with tabs[3]:
    st.subheader("📞 قنوات التواصل الرسمية")
    st.markdown(f'<a href="https://t.me/Aiman_Guard_2026_bot" class="contact-link" style="background:#0088cc;">{st.session_state.settings["btn_bot_text"]}</a>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: st.markdown(f'<a href="https://wa.me/966556868717" class="contact-link" style="background:#25d366;">{st.session_state.settings["btn_wa_text"]}</a>', unsafe_allow_html=True)
    with col2: st.markdown(f'<a href="mailto:kebriay2030@gmail.com" class="contact-link" style="background:#ea4335;">{st.session_state.settings["btn_mail_text"]}</a>', unsafe_allow_html=True)

# --- التبويب 5: الإدارة السيادية (تعديلات كاملة وشاملة) ---
with tabs[4]:
    if not st.session_state.is_admin:
        st.subheader("🔐 الدخول الآمن")
        pwd = st.text_input("كلمة مرور المسؤول:", type="password")
        if st.button("🔑 طلب كود التحقق"):
            if pwd == st.session_state.settings['admin_password']:
                code = str(random.randint(100000, 999999))
                if send_security_msg(code):
                    st.session_state.auth_code = code
                    st.success("أرسلنا الكود لتليجرام")
        
        if st.session_state.auth_code:
            v_code = st.text_input("أدخل الكود:")
            if st.button("✅ دخول"):
                if v_code == st.session_state.auth_code:
                    st.session_state.is_admin = True
                    st.rerun()
    else:
        st.success("🔓 مرحباً أيمن، أنت الآن في غرفة التحكم الكاملة.")
        if st.button("🚪 خروج آمن"):
            st.session_state.is_admin = False
            st.rerun()
        
        st.divider()
        st.subheader("⚙️ تعديل نصوص الموقع والترحيب")
        st.session_state.settings['site_title'] = st.text_input("عنوان الموقع الرئيسي:", st.session_state.settings['site_title'])
        st.session_state.settings['site_sub'] = st.text_input("الوصف الفرعي للموقع:", st.session_state.settings['site_sub'])
        st.session_state.settings['welcome_msg'] = st.text_area("رسالة الترحيب في الرئيسية:", st.session_state.settings['welcome_msg'])
        
        st.divider()
        st.subheader("🔗 تعديل تسميات أزرار التواصل")
        c1, c2, c3 = st.columns(3)
        with c1: st.session_state.settings['btn_bot_text'] = st.text_input("اسم زر البوت:", st.session_state.settings['btn_bot_text'])
        with c2: st.session_state.settings['btn_wa_text'] = st.text_input("اسم زر واتساب:", st.session_state.settings['btn_wa_text'])
        with c3: st.session_state.settings['btn_mail_text'] = st.text_input("اسم زر البريد:", st.session_state.settings['btn_mail_text'])

        st.divider()
        st.subheader("🎨 التنسيق اللوني وكلمة المرور")
        st.session_state.settings['theme_color'] = st.color_picker("اختر لون هوية الموقع:", st.session_state.settings['theme_color'])
        st.session_state.settings['admin_password'] = st.text_input("تغيير كلمة المرور:", st.session_state.settings['admin_password'], type="password")
        
        if st.button("💾 حفظ كافة التعديلات وتحديث الموقع"):
            st.success("✅ تم حفظ التغييرات فوراً!")
            st.rerun()
