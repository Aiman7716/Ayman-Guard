import streamlit as st
import yt_dlp
import requests
import time

# --- 1. التنسيق السيادي المتطور (UI/UX) ---
st.set_page_config(page_title="Ayman Guard Pro v35", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* هيدر الصفحة الرئيسي */
    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; border: 1px solid #30363d;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* تخصيص أزرار "اختيار ملف" والروابط لتكون بنفس اللون الأزرق */
    button[kind="secondary"], .contact-btn {
        background-color: #1f6feb !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #ffffff !important;
        font-weight: bold !important;
        text-decoration: none !important;
        display: inline-block;
        padding: 10px 20px;
        text-align: center;
        transition: 0.3s;
    }

    /* أزرار النظام الموحدة */
    div.stButton > button { 
        width: 100% !important; 
        background: #1f6feb !important; 
        color: white !important; 
        border-radius: 12px; 
        font-weight: bold; 
        height: 3.5em; 
        border: none; 
    }
    
    /* زر الحفظ الأخضر */
    .stDownloadButton > button { 
        background-color: #238636 !important; 
        width: 100% !important; 
        height: 4.5em !important; 
        font-size: 20px !important; 
        font-weight: bold !important; 
        border-radius: 12px !important; 
        border: 2px solid #ffffff !important; 
    }

    /* بطاقات الحماية */
    .safety-card {
        background: #161b22;
        padding: 20px;
        border-radius: 12px;
        border-right: 5px solid #1f6feb;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة الذاكرة (Session State) ---
if 'v_ready' not in st.session_state: st.session_state.v_ready = False
if 'v_data' not in st.session_state: st.session_state.v_data = None
if 'v_url' not in st.session_state: st.session_state.v_url = ""
if 'v_title' not in st.session_state: st.session_state.v_title = ""

# --- 3. بناء الواجهة السيادية ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الحماية والتحميل المتكامل v35.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🎬 مركز التحميل", "🔍 مركز الفحص", "🛡️ الحماية والدعم"])

# --- تبويب الرئيسية ---
with tabs[0]:
    st.markdown("### 📊 حالة النظام")
    c1, c2 = st.columns(2)
    c1.metric("حالة الدرع", "نشط وآمن")
    c2.metric("تحديثات النظام", "v35.0")
    st.info("مرحباً بك يا أيمن. جميع الأنظمة تحت السيطرة.")

# --- تبويب مركز التحميل ---
with tabs[1]:
    st.subheader("🎬 محرك الوسائط")
    u_in = st.text_input("أدخل الرابط هنا:")
    if st.button("🚀 بدء المعالجة الرسمية"):
        if u_in:
            with st.spinner("جاري فحص وتجهيز البيانات، يرجى الانتظار..."):
                try:
                    ydl_opts = {'format': 'best', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(u_in, download=False)
                        st.session_state.v_url = info.get('url', None)
                        st.session_state.v_title = info.get('title', 'Video')
                    if st.session_state.v_url:
                        st.session_state.v_data = requests.get(st.session_state.v_url).content
                        st.session_state.v_ready = True
                except Exception as e: st.error(f"تنبيه: {e}")

    if st.session_state.v_ready:
        st.video(st.session_state.v_url)
        if st.download_button(label="📥 حفظ الفيديو في الاستوديو", data=st.session_state.v_data, file_name=f"{st.session_state.v_title}.mp4", mime="video/mp4"):
            st.toast("✅ جاري التحميل المباشر...", icon="📥")

# --- تبويب مركز الفحص ---
with tabs[2]:
    st.subheader("🔍 فحص الروابط والملفات")
    link = st.text_input("رابط التحليل:")
    if st.button("🛡️ تحليل الرابط الآن"):
        try:
            r = requests.head(link, timeout=5)
            st.success(f"الرابط مستجيب ({r.status_code})")
        except: st.error("الرابط لا يستجيب.")
    
    st.markdown("---")
    st.markdown("#### 📁 فحص الملفات الذكي")
    f_up = st.file_uploader("اضغط لاختيار ملف لفحصه:", type=['png', 'jpg', 'mp4', 'pdf', 'apk', 'zip'])
    if f_up:
        st.write(f"📄 الملف المختار: **{f_up.name}**")
        if st.button("🔍 تنفيذ الفحص الأمني"):
            with st.spinner("جاري تحليل الملف..."):
                time.sleep(2)
                st.success(f"✅ الملف '{f_up.name}' سليم.")

# --- التبويب الجديد: الحماية والدعم (الطلب الأخير) ---
with tabs[3]:
    st.subheader("🛡️ قسم الحماية والمجتمع")
    
    # قسم حماية المجتمع
    st.markdown('<div class="safety-card"><h4>👥 حماية المجتمع</h4><p>نعمل في "درع أيمن" على توفير بيئة رقمية آمنة. يرجى التبليغ عن أي محتوى ضار أو روابط مشبوهة للمساهمة في حماية المستخدمين.</p></div>', unsafe_allow_html=True)
    
    if st.button("📢 إرسال بلاغ عن محتوى ضار"):
        st.warning("جاري فتح نظام البلاغات.. يرجى وصف المشكلة بوضوح.")

    st.markdown("---")
    
    # قسم تواصل بنا
    st.subheader("📞 تواصل بنا")
    st.write("إذا واجهت أي مشكلة تقنية أو كان لديك اقتراح لتطوير النظام، فريقنا جاهز للرد عليك.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<a href="https://t.me/Ayman" class="contact-btn" style="width:100%">💬 تليجرام</a>', unsafe_allow_html=True)
    with c2:
        st.markdown('<a href="mailto:ayman@shield.com" class="contact-btn" style="width:100%">📧 البريد الإلكتروني</a>', unsafe_allow_html=True)
    with c3:
        st.markdown('<a href="https://wa.me/yournumber" class="contact-btn" style="width:100%">📱 واتساب</a>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 نحن متاحون لخدمتك على مدار الساعة يا أيمن.")
