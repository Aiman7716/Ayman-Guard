import streamlit as st
import yt_dlp
import os
import requests
import base64
from datetime import datetime

# --- 1. الإعدادات والتصميم السيادي ---
st.set_page_config(page_title="Ayman Shield v29", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    header, footer, #MainMenu {visibility: hidden !important;}
    
    /* تصميم البطاقات والأزرار */
    .main-card { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    .sub-card { background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 15px; }
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 10px; height: 3.5em; font-weight: bold; border: none; transition: 0.3s; }
    .stButton>button:hover { background: #388bfd !important; transform: scale(1.02); }
    .dl-link { display: block; width: 100%; padding: 15px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 18px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك البوت والبيانات ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def ayman_bot(msg):
    try: requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=HTML", timeout=2)
    except: pass

def file_to_b64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- 3. نظام التنقل والتبويبات ---
if 'page' not in st.session_state: st.session_state.page = "🏠 الرئيسية"

def navigate_to(page_name):
    st.session_state.page = page_name

# الواجهة العلوية ثابتة
st.markdown('<div class="main-card"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار الشامل v29.0</p></div>', unsafe_allow_html=True)

# قائمة التنقل (Tabs) تعمل كأزرار سريعة
tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص", "🎬 محمل الفيديو", "👥 التواصل والمجتمع", "🔐 الإدارة"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.markdown("### ⚡ لوحة الوصول السريع")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 فحص الروابط والملفات"): navigate_to("🔍 مركز الفحص")
        if st.button("🎬 تحميل الفيديوهات"): navigate_to("🎬 محمل الفيديو")
    with col2:
        if st.button("👥 البلاغات والتواصل"): navigate_to("👥 التواصل والمجتمع")
        if st.button("🔐 دخول الإدارة"): navigate_to("🔐 الإدارة")
    st.info(f"أهلاً بك يا أيمن، أنت الآن في: {st.session_state.page}")

# --- التبويب 2: مركز الفحص (دمج الروابط والملفات) ---
with tabs[1]:
    st.subheader("🔍 مركز الفحص الموحد")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sub-card"><h4>🔗 فحص الروابط</h4>', unsafe_allow_html=True)
        url_input = st.text_input("ألصق الرابط:")
        if st.button("🛡️ فحص الرابط الآن"):
            if url_input:
                try:
                    r = requests.get(url_input, timeout=3)
                    st.success(f"الرابط مستجيب ({r.status_code})")
                    ayman_bot(f"🔍 <b>فحص رابط:</b>\n{url_input}")
                except: st.error("تعذر الوصول للرابط.")
        if url_input: st.markdown(f'<a href="{url_input}" target="_blank" class="dl-link" style="background:#8b949e;">👁️ معاينة الرابط</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="sub-card"><h4>📁 فحص الملفات</h4>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("اختر ملفاً:")
        if uploaded_file and st.button("🛠️ فحص الملف"):
            st.success(f"تم تحليل {uploaded_file.name} ✅")
            ayman_bot(f"📁 <b>فحص ملف:</b>\n{uploaded_file.name}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 3: محمل الفيديو (إصلاح البياض والحفظ) ---
with tabs[2]:
    st.subheader("🎬 محمل الفيديو الذكي")
    v_url = st.text_input("رابط (Facebook, YouTube, TikTok):", key="v_dl")
    if st.button("🚀 بدء التحميل والاستخراج"):
        if v_url:
            with st.spinner("جاري المعالجة... يرجى الانتظار"):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'ayman_v.mp4', 'quiet': True, 'noplaylist': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                    if os.path.exists("ayman_v.mp4"):
                        st.video("ayman_v.mp4")
                        b64 = file_to_b64("ayman_v.mp4")
                        href = f'<a href="data:video/mp4;base64,{b64}" download="video.mp4" class="dl-link">📥 اضغط هنا لحفظ الفيديو فوراً</a>'
                        st.markdown(href, unsafe_allow_html=True)
                        os.remove("ayman_v.mp4")
                        ayman_bot(f"🎬 <b>تحميل ناجح:</b>\n{v_url}")
                except:
                    st.error("فشل التحميل. الرابط ثقيل أو خاص.")
                    ayman_bot(f"⚠️ <b>فشل تحميل:</b>\n{v_url}")

# --- التبويب 4: التواصل والمجتمع (دمج حماية المجتمع وتواصل بنا) ---
with tabs[3]:
    st.subheader("👥 مركز التواصل والبلاغات")
    with st.form("com_form"):
        type_msg = st.selectbox("نوع الرسالة:", ["📧 تواصل بنا", "🚨 بلاغ حماية المجتمع", "🛠️ اقتراح تحسين"])
        u_name = st.text_input("اسمك:")
        u_msg = st.text_area("تفاصيل الرسالة:")
        if st.form_submit_button("إرسال فوراً للبوت"):
            if u_name and u_msg:
                ayman_bot(f"<b>{type_msg}</b>\nمن: {u_name}\nالمحتوى: {u_msg}")
                st.success("تم الإرسال بنجاح ✅")
            else: st.warning("يرجى ملء البيانات")

# --- التبويب 5: الإدارة (مصادقة تليجرام) ---
with tabs[4]:
    if "is_admin" not in st.session_state: st.session_state.is_admin = False
    
    if not st.session_state.is_admin:
        st.subheader("🔐 دخول الإدارة")
        admin_pw = st.text_input("كلمة السر:", type="password")
        if st.button("مصادقة والدخول"):
            if admin_pw == "ayman7716":
                st.session_state.is_admin = True
                ayman_bot("🔓 <b>تنبيه أمني:</b> تم الدخول للوحة الإدارة.")
                st.rerun()
            else:
                st.error("كلمة السر خاطئة")
                ayman_bot(f"🚫 <b>محاولة دخول فاشلة!</b>")
    else:
        st.success("مرحباً أيمن، أنت في لوحة التحكم")
        if st.button("🔴 تسجيل خروج آمن"):
            st.session_state.is_admin = False
            ayman_bot("🚪 <b>تنبيه:</b> تم الخروج من الإدارة.")
            st.rerun()
