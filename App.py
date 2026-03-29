import streamlit as st
import yt_dlp
import os
import requests

# --- 1. الإعدادات الكلاسيكية (عودة التبويبات والمنطق القديم) ---
st.set_page_config(page_title="Ayman Shield - Original", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* تنسيق زر اختيار ملف (الأزرق الأصلي) */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 8px !important; }
    
    /* تنسيق زر التنزيل الأخضر الذي كان يعمل بنجاح */
    .stDownloadButton>button { background-color: #238636 !important; color: white !important; border-radius: 10px !important; height: 4em !important; width: 100% !important; font-weight: bold; border: 1px solid #ffffff; }
    
    .main-title { text-align: center; color: #1f6feb; margin-bottom: 30px; border-bottom: 2px solid #30363d; padding-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🛡️ درع أيمن السيادي (النسخة المستعادة)</h1>', unsafe_allow_html=True)

# --- 2. نظام البوت المستقر ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_to_telegram(message):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": message}, timeout=2)
    except:
        pass

# --- 3. عودة التبويبات (Tabs) كما كانت قبل يومين ---
tab1, tab2, tab3, tab4 = st.tabs(["🎬 تحميل الفيديو", "🔍 مركز الفحص", "👥 تواصل معنا", "🔐 الإدارة"])

with tab1:
    st.subheader("🎬 محمل الفيديوهات الذكي")
    video_url = st.text_input("أدخل رابط الفيديو (فيسبوك، يوتيوب، تيك توك):", placeholder="https://...")
    
    if st.button("🚀 معالجة الفيديو"):
        if video_url:
            with st.spinner("جاري التحميل..."):
                try:
                    # الطريقة القديمة: ملف مؤقت مباشر
                    filename = "video_ayman.mp4"
                    ydl_opts = {'format': 'best', 'outtmpl': filename, 'quiet': True}
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                    
                    if os.path.exists(filename):
                        with open(filename, "rb") as f:
                            st.video(f.read())
                            st.download_button(
                                label="📥 اضغط هنا لحفظ الملف",
                                data=f,
                                file_name="Ayman_Video.mp4",
                                mime="video/mp4"
                            )
                        os.remove(filename) # مسح الملف بعد التحميل لضمان الخصوصية
                        send_to_telegram(f"🎬 نجاح تحميل فيديو: {video_url}")
                except Exception as e:
                    st.error(f"خطأ في التحميل: {e}")

with tab2:
    st.subheader("🔍 فحص الروابط والملفات")
    col1, col2 = st.columns(2)
    with col1:
        st.info("🔗 فحص الروابط")
        url_to_check = st.text_input("ألصق الرابط هنا:")
        if st.button("🛡️ ابدأ الفحص"):
            try:
                res = requests.get(url_to_check, timeout=5)
                st.success(f"الرابط آمن ومستجيب ({res.status_code})")
                send_to_telegram(f"🔍 فحص رابط: {url_to_check}")
            except:
                st.error("الرابط غير مستجيب أو مشبوه")
    
    with col2:
        st.info("📁 فحص الملفات")
        uploaded_file = st.file_uploader(" ", type=["jpg", "png", "pdf", "zip", "apk"])
        if uploaded_file:
            st.success(f"تم رفع {uploaded_file.name} بنجاح. جاري الفحص...")
            send_to_telegram(f"📁 فحص ملف: {uploaded_file.name}")

with tab3:
    st.subheader("👥 تواصل مع المطور")
    with st.form("contact_form"):
        u_name = st.text_input("اسمك:")
        u_msg = st.text_area("رسالتك:")
        if st.form_submit_button("إرسال الآن"):
            send_to_telegram(f"📩 رسالة جديدة من {u_name}:\n{u_msg}")
            st.success("تم إرسال رسالتك بنجاح ✅")

with tab4:
    st.subheader("🔐 لوحة التحكم")
    admin_pass = st.text_input("كلمة السر:", type="password")
    if st.button("دخول"):
        if admin_pass == "ayman7716":
            st.success("أهلاً بك يا أيمن في لوحة التحكم")
            send_to_telegram("🔐 محاولة دخول ناجحة للإدارة")
        else:
            st.error("كلمة السر خاطئة")
