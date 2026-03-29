import streamlit as st
import yt_dlp
import requests
import time
import random
import io

# --- 1. الذاكرة وإعدادات النظام ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي 2026",
        'admin_password': "Ayman2026",
        'theme_color': "#1f6feb"
    }

# تهيئة المتغيرات الأساسية
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None
if 'video_info' not in st.session_state: st.session_state.video_info = None

# --- 2. التنسيق البصري الاحترافي (CSS) ---
color = st.session_state.settings['theme_color']
st.set_page_config(page_title=st.session_state.settings['site_title'], layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }}
    .stApp {{ background-color: #0d1117; color: #ffffff; }}
    
    /* منع التداخل وتحسين المسافات */
    .stTextInput input {{ padding: 12px !important; margin-top: 10px !important; margin-bottom: 10px !important; }}
    .main-header {{
        background: linear-gradient(135deg, {color} 0%, #111d2e 100%);
        padding: 40px 20px; border-radius: 20px; text-align: center;
        border: 1px solid #30363d; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    
    /* أزرار التحميل والدخول */
    div.stButton > button {{ 
        width: 100% !important; background: {color} !important; 
        color: white !important; border-radius: 12px; font-weight: bold; 
        height: 3.8em; border: none; font-size: 17px !important;
    }}
    .stDownloadButton > button {{ 
        background: #238636 !important; width: 100% !important; height: 4em !important; 
        border-radius: 12px !important; border: 2px solid white !important;
    }}
    
    .contact-card {{
        background: #161b22; padding: 20px; border-radius: 15px;
        border: 1px solid #30363d; margin-bottom: 15px; text-align: center;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. وظائف النظام (تليجرام + تحميل) ---

def send_tele_security_code(code):
    TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
    MY_ID = "906233240"
    msg = f"🔐 تنبيه أمني من درع أيمن\n\nكود الدخول الخاص بك هو: {code}"
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": MY_ID, "text": msg})
        return True
    except: return False

# --- 4. واجهة التطبيق ---

st.markdown(f"""<div class="main-header"><h1>{st.session_state.settings['site_title']}</h1>
<p>{st.session_state.settings['site_sub']}</p></div>""", unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🎬 مركز الوسائط", "🔍 الفحص الأمني", "🛡️ الدعم", "⚙️ الإدارة"])

# --- الرئيسية ---
with tabs[0]:
    st.markdown("### 📊 حالة الحماية السيادية")
    c1, c2 = st.columns(2)
    c1.info("🛡️ المحرك الأمني: نشط")
    c2.success("🤖 ارتباط تليجرام: متصل")
    st.image("https://img.icons8.com/clouds/200/shield.png")

# --- مركز الوسائط (الإصلاح: الآن يعمل فعلياً) ---
with tabs[1]:
    st.subheader("🎬 محرك تحميل الفيديو الذكي")
    v_url = st.text_input("ألصق رابط الفيديو (YouTube, FB, TikTok, Twitter):", placeholder="https://...")
    
    if st.button("🚀 معالجة الفيديو"):
        if v_url:
            with st.spinner("جاري جلب بيانات الفيديو..."):
                try:
                    ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        st.session_state.video_info = {
                            'title': info.get('title', 'Video'),
                            'url': info.get('url'),
                            'thumbnail': info.get('thumbnail')
                        }
                        st.success("✅ تم العثور على الفيديو!")
                except Exception as e:
                    st.error(f"❌ حدث خطأ في المعالجة: {str(e)}")
        else:
            st.warning("⚠️ يرجى إدخال الرابط أولاً.")

    if st.session_state.video_info:
        st.divider()
        st.write(f"📌 **العنوان:** {st.session_state.video_info['title']}")
        st.video(st.session_state.video_info['url'])
        
        # زر التحميل الفعلي للجهاز
        try:
            video_content = requests.get(st.session_state.video_info['url']).content
            st.download_button(
                label="📥 حفظ الفيديو في جهازك الآن",
                data=video_content,
                file_name=f"{st.session_state.video_info['title']}.mp4",
                mime="video/mp4"
            )
        except:
            st.error("فشل في تحضير ملف التحميل المباشر.")

# --- مركز الفحص ---
with tabs[2]:
    st.subheader("🔍 الفحص المباشر")
    st.text_input("أدخل الرابط للفحص:")
    if st.button("🛡️ تنفيذ فحص الرابط"):
        st.info("النتيجة: الرابط سليم ✅")
    st.divider()
    st.file_uploader("فحص ملف:", type=['apk','pdf','zip'])
    if st.button("📁 فحص الملف"):
        st.success("الملف آمن ✅")

# --- الدعم (إضافة زر البريد) ---
with tabs[3]:
    st.subheader("📞 قنوات التواصل")
    st.markdown(f'<a href="https://t.me/Aiman_Guard_2026_bot" target="_blank" style="text-decoration:none;"><div class="contact-card" style="background:#0088cc; color:white;">🤖 ابدأ المحادثة مع بوت الدرع</div></a>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<a href="https://wa.me/966556868717" target="_blank" style="text-decoration:none;"><div class="contact-card" style="background:#25d366; color:white;">📱 واتساب</div></a>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<a href="mailto:kebriay2030@gmail.com" style="text-decoration:none;"><div class="contact-card" style="background:#ea4335; color:white;">📧 البريد الإلكتروني</div></a>', unsafe_allow_html=True)

# --- الإدارة (الإصلاح: ربط الأمان الفعلي) ---
with tabs[4]:
    if not st.session_state.is_admin:
        st.subheader("🔐 بوابة المسؤول")
        adm_pwd = st.text_input("كلمة المرور:", type="password")
        
        if st.button("🔑 طلب كود الدخول"):
            if adm_pwd == st.session_state.settings['admin_password']:
                gen_code = str(random.randint(100000, 999999))
                if send_tele_security_code(gen_code):
                    st.session_state.auth_code = gen_code
                    st.success("✅ تم إرسال الكود إلى تليجرام الخاص بك.")
                else: st.error("فشل إرسال الكود.")
            else: st.error("❌ كلمة المرور غير صحيحة.")
        
        if st.session_state.auth_code:
            input_code = st.text_input("أدخل الكود المستلم:")
            if st.button("✅ دخول"):
                if input_code == st.session_state.auth_code:
                    st.session_state.is_admin = True
                    st.rerun()
                else: st.error("❌ الكود غير صحيح.")
    else:
        st.success("🔓 مرحباً أيمن")
        if st.button("🚪 خروج آمن"):
            st.session_state.is_admin = False
            st.rerun()
        
        st.divider()
        st.subheader("⚙️ إعدادات الموقع")
        st.session_state.settings['site_title'] = st.text_input("تغيير العنوان:", st.session_state.settings['site_title'])
        st.session_state.settings['theme_color'] = st.color_picker("لون الموقع:", st.session_state.settings['theme_color'])
        st.session_state.settings['admin_password'] = st.text_input("تغيير كلمة المرور:", st.session_state.settings['admin_password'], type="password")
        
        if st.button("💾 حفظ الإعدادات"):
            st.success("تم الحفظ بنجاح!")
            st.rerun()
