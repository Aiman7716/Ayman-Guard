import streamlit as st
import yt_dlp
import requests
import random
import time

# --- 1. محرك الذاكرة والإعدادات ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "نظام الحماية والاتصال الرسمي v65.0",
        'tab1': "🏠 الرئيسية", 'tab2': "🎬 تحميل الفيديو", 
        'tab3': "🔍 فحص الروابط والملفات", 'tab4': "🛡️ الحماية والدعم", 'tab5': "⚙️ الإدارة"
    }
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None

# --- 2. محرك التليجرام (يرسل لك أنت شخصياً) ---
def send_telegram_code(code):
    TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
    MY_ID = "906233240" # هويتك الشخصية (شموخي عنواني)
    msg = f"🔐 مرحباً أيمن، كود الدخول هو: {code}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": MY_ID, "text": msg})
        st.success("✅ وصل الكود لتليجرام! افحص حسابك الشخصي.")
    except:
        st.error("⚠️ فشل الاتصال بالبوت.")

# --- 3. تصميم الواجهة (الأناقة والجاذبية) ---
st.set_page_config(page_title=st.session_state.settings['site_title'], layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
.stApp { background-color: #0d1117; color: #ffffff; }

/* الهيدر المتدرج */
.hero-box {
    background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
    padding: 35px; border-radius: 20px; text-align: center;
    border: 1px solid #30363d; margin-bottom: 25px;
}

/* أزرار التواصل الملونة */
.contact-btn {
    display: block; padding: 15px; margin-bottom: 10px;
    text-align: center; border-radius: 12px; color: white !important;
    font-weight: bold; text-decoration: none; border: 1px solid #ffffff33;
}
.bg-tele { background: #0088cc !important; }
.bg-wa { background: #25d366 !important; }
.bg-mail { background: #ea4335 !important; }

/* زر الفحص البارز (البرتقالي) */
.stDownloadButton > button {
    background: linear-gradient(90deg, #ff9100, #ff6d00) !important;
    color: white !important; font-size: 20px !important;
    width: 100% !important; border-radius: 15px !important; height: 4.5em !important;
    border: 2px solid white !important; box-shadow: 0 4px 15px rgba(255,145,0,0.3);
}

div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; font-weight: bold; height: 3.5em; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 4. الهيكل العلوي ---
st.markdown(f'<div class="hero-box"><h1>{st.session_state.settings["site_title"]}</h1><p>{st.session_state.settings["site_sub"]}</p></div>', unsafe_allow_html=True)

tabs = st.tabs([st.session_state.settings[f'tab{i}'] for i in range(1, 6)])

# --- التبويب 1: الرئيسية (أنيقة وجذابة) ---
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div style="background:#161b22; padding:25px; border-radius:15px; border-right:5px solid #1f6feb;">
            <h3>📊 حالة الحماية</h3>
            <p>النظام يعمل بكامل طاقته تحت إشراف <b>أيمن</b> الشخصي. جميع المحركات متصلة وآمنة.</p>
        </div>
        """, unsafe_allow_html=True)
        st.metric("سرعة الفحص", "99.9%", "0.1%")
    with col2:
        st.image("https://img.icons8.com/clouds/200/shield.png")

# --- التبويب 2: تحميل الفيديو ---
with tabs[1]:
    st.subheader("🎬 محرك تحميل الوسائط")
    v_url = st.text_input("ألصق رابط الفيديو (YouTube, TikTok, FB):")
    if st.button("🚀 بدء المعالجة والتحميل"):
        if v_url: st.info("جاري فحص الرابط وسحب البيانات...")

# --- التبويب 3: فحص الروابط (زر بارز) ---
with tabs[2]:
    st.subheader("🔍 مركز التحليل الأمني")
    st.text_input("أدخل الرابط المراد تحليله:")
    st.button("🛡️ تنفيذ الفحص الآن")
    st.markdown("---")
    st.markdown("#### 📁 فحص الملفات الذكي")
    st.file_uploader("اختر ملفاً (APK, PDF, ZIP...):", type=['apk', 'pdf', 'zip', 'png', 'jpg'])
    # الزر البرتقالي البارز جداً
    st.download_button(label="📥 رفع وتحميل تقرير الفحص الشامل", data="Report", file_name="Ayman_Scan.txt")

# --- التبويب 4: الحماية والدعم ---
with tabs[3]:
    st.subheader("🤖 قنوات التواصل الرسمية")
    # زر البوت الرسمي المطور
    st.markdown(f'<a href="https://t.me/Aiman_Guard_2026_bot" target="_blank" class="contact-btn bg-tele" style="font-size:22px; padding:25px;">🤖 ابدأ المحادثة مع بوت الدرع الآن</a>', unsafe_allow_html=True)
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<a href="https://wa.me/966556868717" target="_blank" class="contact-btn bg-wa">📱 تواصل عبر واتساب</a>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<a href="mailto:kebriay2030@gmail.com" class="contact-btn bg-mail">📧 البريد الإلكتروني</a>', unsafe_allow_html=True)

# --- التبويب 5: الإدارة (العقل المدبر) ---
with tabs[4]:
    if not st.session_state.is_admin:
        st.subheader("🔐 بوابة المسؤول")
        admin_pwd = st.text_input("كلمة المرور:", type="password")
        if st.button("🚀 طلب كود الدخول (2FA)"):
            if admin_pwd == "Ayman2026":
                st.session_state.auth_code = str(random.randint(111111, 999999))
                send_telegram_code(st.session_state.auth_code)
            else: st.error("كلمة المرور غير صحيحة!")
        
        if st.session_state.auth_code:
            v_code = st.text_input("أدخل الكود المستلم من تليجرام:")
            if st.button("✅ تأكيد الهوية"):
                if v_code == st.session_state.auth_code:
                    st.session_state.is_admin = True
                    st.rerun()
    else:
        st.success("🔓 مرحباً بك في غرفة التحكم يا أيمن.")
        if st.button("🚪 تسجيل الخروج الآمن"): st.session_state.is_admin = False; st.rerun()
        st.markdown("---")
        st.subheader("🛠️ تعديل محتوى الموقع")
        st.session_state.settings['site_title'] = st.text_input("عنوان الموقع:", st.session_state.settings['site_title'])
        st.session_state.settings['site_sub'] = st.text_input("الوصف الفرعي:", st.session_state.settings['site_sub'])
        if st.button("💾 حفظ التعديلات"):
            st.success("✅ تم تحديث النظام بنجاح!")
            time.sleep(1)
            st.rerun()
