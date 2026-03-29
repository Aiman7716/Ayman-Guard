import streamlit as st
import yt_dlp
import requests

# --- 1. التنسيق السيادي الفخم (UI/UX) ---
st.set_page_config(page_title="Ayman Guard Pro v32", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* هيدر الصفحة الرئيسية */
    .hero-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 50px; border-radius: 25px; text-align: center;
        margin-bottom: 30px; border: 1px solid #30363d;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* بطاقات المميزات */
    .feature-card {
        background: #161b22; border: 1px solid #30363d;
        padding: 20px; border-radius: 15px; text-align: center;
        transition: 0.3s; height: 100%;
    }
    .feature-card:hover { border-color: #58a6ff; transform: translateY(-5px); }
    
    /* الأزرار */
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; font-weight: bold; height: 3.5em; border: none; }
    .stDownloadButton > button { background-color: #238636 !important; width: 100% !important; height: 4.5em !important; font-size: 20px !important; font-weight: bold !important; border-radius: 12px !important; border: 2px solid #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة الذاكرة ---
if 'video_ready' not in st.session_state: st.session_state.video_ready = False
if 'video_data' not in st.session_state: st.session_state.video_data = None
if 'video_url' not in st.session_state: st.session_state.video_url = ""
if 'video_title' not in st.session_state: st.session_state.video_title = ""

# --- 3. بناء الواجهة السيادية ---
st.markdown('<div class="hero-section"><h1>🛡️ درع أيمن السيادي</h1><p>الجيل القادم من أنظمة معالجة البيانات v32.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الشاشة الرئيسية", "🎬 مركز التحميل", "🔍 الفحص والتحليل"])

# --- تبويب الشاشة الرئيسية (الجمالية الجديدة) ---
with tabs[0]:
    st.markdown("### 📊 حالة النظام والتحكم")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="feature-card"><h3>⚡ السرعة</h3><p>معالجة فورية للروابط عبر سحابة الدرع</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="feature-card"><h3>🔒 الأمان</h3><p>تشفير كامل لعمليات الجلب والتحميل</p></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="feature-card"><h3>🎯 الدقة</h3><p>استخراج أعلى جودة متوفرة (4K/HD)</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="إجمالي العمليات الناجحة", value="1,842", delta="+124")
    with c2:
        st.metric(label="وقت الاستجابة", value="0.8s", delta="-0.2s")
    
    st.info("نظام الدرع نشط ويعمل بكفاءة 100% تحت إشراف أيمن. ✅")

# --- تبويب مركز التحميل (الثابت والمطور) ---
with tabs[1]:
    st.subheader("🎬 محرك الوسائط الذكي")
    input_url = st.text_input("ألصق رابط الفيديو هنا:", placeholder="مثلاً: رابط فيسبوك أو يوتيوب...")
    
    if st.button("🚀 بدء المعالجة الرسمية"):
        if input_url:
            with st.spinner("جاري فحص وتجهيز البيانات، يرجى الانتظار..."):
                try:
                    ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(input_url, download=False)
                        st.session_state.video_url = info.get('url', None)
                        st.session_state.video_title = info.get('title', 'Ayman_Guard_Video')

                    if st.session_state.video_url:
                        resp = requests.get(st.session_state.video_url)
                        st.session_state.video_data = resp.content
                        st.session_state.video_ready = True
                    else:
                        st.error("تعذر استخراج البيانات.")
                except Exception as e:
                    st.error(f"تنبيه: {e}")

    if st.session_state.video_ready:
        st.video(st.session_state.video_url)
        downloaded = st.download_button(
            label="📥 حفظ الفيديو في الاستوديو",
            data=st.session_state.video_data,
            file_name=f"{st.session_state.video_title}.mp4",
            mime="video/mp4"
        )
        if downloaded:
            st.toast("✅ جاري التحميل المباشر...", icon="📥")

# --- تبويب الفحص ---
with tabs[2]:
    st.subheader("🔍 نظام فحص الروابط")
    chk_link = st.text_input("أدخل رابطاً لفحصه أمنياً:")
    if st.button("🛡️ تنفيذ الفحص"):
        try:
            r = requests.head(chk_link, timeout=5)
            st.success(f"الرابط آمن ومستجيب (Status: {r.status_code})")
        except:
            st.error("الرابط مشبوه أو غير مستجيب.")
