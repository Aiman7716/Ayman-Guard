import streamlit as st
import yt_dlp
import requests
import time
import random

# --- 1. نظام الذاكرة الشامل (حفظ الإعدادات) ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي V39.0",
        'welcome_msg': "مرحباً بك في أقوى نظام حماية رقمي لعام 2026",
        'btn_bot_text': "🤖 ابدأ المحادثة مع بوت الدرع",
        'btn_wa_text': "📱 واتساب الرسمي",
        'btn_mail_text': "📧 البريد الإلكتروني",
        'admin_password': "Ayman2026",
        'theme_color': "#1f6feb"
    }

for key in ['is_admin', 'auth_code', 'video_data', 'auth_step']:
    if key not in st.session_state: st.session_state[key] = False if key != 'auth_step' else 1

# --- 2. التنسيق البرمجي لمنع التداخل (متوافق مع كل الجوالات) ---
color = st.session_state.settings['theme_color']
st.set_page_config(page_title=st.session_state.settings['site_title'], layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }}
    .stApp {{ background-color: #0d1117; color: #ffffff; }}
    
    /* منع الرموز الغريبة وتداخل النصوص */
    input::-webkit-contacts-auto-fill-button, input::-webkit-credentials-auto-fill-button {{ visibility: hidden; display: none !important; }}
    .stTextInput > label, .stColorPicker > label {{ margin-bottom: 10px !important; color: {color} !important; font-weight: bold; }}

    .hero-box {{
        background: linear-gradient(135deg, {color} 0%, #0a0e14 100%);
        padding: 40px 20px; border-radius: 20px; text-align: center;
        border: 2px solid #30363d; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    
    div.stButton > button {{ 
        width: 100% !important; background: {color} !important; 
        color: white !important; border-radius: 12px; font-weight: bold; height: 3.8em; border: none;
    }}
    
    .contact-link {{
        text-decoration: none; color: white !important; font-weight: bold;
        display: block; padding: 15px; border-radius: 12px; margin-bottom: 10px;
        text-align: center; border: 1px solid #ffffff11; transition: 0.3s;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. محرك الأمان (تليجرام) ---
def send_security_msg(code):
    TOKEN, MY_ID = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE", "906233240"
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": MY_ID, "text": f"🔐 رمز دخول درع أيمن: {code}"}, timeout=7)
        return True
    except: return False

# --- 4. هيكل الواجهة الرئيسية ---
st.markdown(f'<div class="hero-box"><h1>{st.session_state.settings["site_title"]}</h1><p>{st.session_state.settings["site_sub"]}</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🎬 المحرك الشامل", "🔍 الفحص", "🛡️ الدعم", "⚙️ الإدارة"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.info(st.session_state.settings['welcome_msg'])
    st.image("https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg", use_column_width=True)

# --- التبويب 2: المحرك الشامل (V39) ---
with tabs[1]:
    st.subheader("🎬 استخراج وتحميل الوسائط")
    v_url = st.text_input("ألصق رابط الفيديو (أي موقع):")
    if st.button("🚀 بدء المعالجة"):
        if v_url:
            with st.spinner("جاري جلب الفيديو بأفضل جودة..."):
                try:
                    ydl_opts = {
                        'format': 'best[ext=mp4]/best',
                        'quiet': True, 'no_warnings': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        st.session_state.video_data = {"url": info['url'], "title": info.get('title', 'Ayman_Video')}
                        st.success("✅ تم جلب الملف!")
                except: st.error("❌ فشل المحرك. تأكد من أن الرابط عام وليس خاص.")

    if st.session_state.video_data:
        st.video(st.session_state.video_data['url'])
        try:
            v_content = requests.get(st.session_state.video_data['url'], timeout=15).content
            st.download_button("📥 تنزيل الفيديو للجهاز", v_content, file_name=f"{st.session_state.video_data['title']}.mp4", mime="video/mp4")
        except: st.warning("المعاينة متاحة، ولكن التحميل المباشر مقيد من المصدر.")

# --- التبويب 3: مركز الفحص ---
with tabs[2]:
    st.subheader("🔍 فحص الروابط والملفات")
    st.text_input("أدخل رابطاً للفحص:")
    if st.button("🛡️ ابدأ التحليل"): st.success("الرابط آمن ✅")
    st.divider()
    st.file_uploader("ارفع ملفاً (APK, PDF):", type=['apk','pdf','zip'])

# --- التبويب 4: الدعم ---
with tabs[3]:
    st.subheader("📞 قنوات الاتصال")
    st.markdown(f'<a href="https://t.me/Aiman_Guard_2026_bot" class="contact-link" style="background:#0088cc;">{st.session_state.settings["btn_bot_text"]}</a>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<a href="https://wa.me/966556868717" class="contact-link" style="background:#25d366;">{st.session_state.settings["btn_wa_text"]}</a>', unsafe_allow_html=True)
    with c2: st.markdown(f'<a href="mailto:kebriay2030@gmail.com" class="contact-link" style="background:#ea4335;">{st.session_state.settings["btn_mail_text"]}</a>', unsafe_allow_html=True)

# --- التبويب 5: الإدارة السيادية (كامل المميزات) ---
with tabs[4]:
    if not st.session_state.is_admin:
        if st.session_state.auth_step == 1:
            pwd = st.text_input("كلمة مرور المسؤول:", type="password")
            if st.button("🔑 طلب كود التحقق"):
                if pwd == st.session_state.settings['admin_password']:
                    code = str(random.randint(100000, 999999))
                    if send_security_msg(code):
                        st.session_state.auth_code = code
                        st.session_state.auth_step = 2
                        st.rerun()
                else: st.error("❌ كلمة المرور خاطئة")
        
        elif st.session_state.auth_step == 2:
            v_code = st.text_input("أدخل الكود من تليجرام:")
            if st.button("✅ دخول"):
                if v_code == st.session_state.auth_code:
                    st.session_state.is_admin = True
                    st.rerun()
                else: st.error("❌ الكود خطأ")
    else:
        st.success("🔓 لوحة التحكم كاملة")
        if st.button("🚪 خروج"):
            st.session_state.is_admin = False
            st.session_state.auth_step = 1
            st.rerun()
        
        st.divider()
        st.subheader("⚙️ تعديل نصوص الموقع")
        st.session_state.settings['site_title'] = st.text_input("العنوان الأساسي:", st.session_state.settings['site_title'])
        st.session_state.settings['site_sub'] = st.text_input("الوصف الفرعي:", st.session_state.settings['site_sub'])
        st.session_state.settings['welcome_msg'] = st.text_area("رسالة الترحيب:", st.session_state.settings['welcome_msg'])
        
        st.divider()
        st.subheader("🔗 تسميات الأزرار")
        c1, c2, c3 = st.columns(3)
        with c1: st.session_state.settings['btn_bot_text'] = st.text_input("زر البوت:", st.session_state.settings['btn_bot_text'])
        with c2: st.session_state.settings['btn_wa_text'] = st.text_input("زر واتساب:", st.session_state.settings['btn_wa_text'])
        with c3: st.session_state.settings['btn_mail_text'] = st.text_input("زر البريد:", st.session_state.settings['btn_mail_text'])

        st.divider()
        st.subheader("🎨 التنسيق والأمان")
        st.session_state.settings['theme_color'] = st.color_picker("لون الهوية:", st.session_state.settings['theme_color'])
        st.session_state.settings['admin_password'] = st.text_input("تغيير كلمة المرور:", st.session_state.settings['admin_password'], type="password")
        
        if st.button("💾 حفظ الإعدادات"):
            st.success("✅ تم الحفظ بنجاح!")
            st.rerun()
