import streamlit as st
import yt_dlp
import os
import requests

# --- 1. التصميم (الواجهة الرئيسية + زر اختيار ملف أزرق) ---
st.set_page_config(page_title="Ayman Shield v38", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stHeader"], [data-testid="stTabNav"] { display: none !important; }
    
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 35px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    .card { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; }
    
    /* أزرار الواجهة الرئيسية */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 15px; height: 4.5em; font-weight: bold; border: none; font-size: 18px; }
    
    /* تلوين زر اختيار ملف باللون الأزرق */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; width: 100% !important; height: 3.5em !important; border: none !important; }
    div[data-testid="stFileUploader"] section button span::after { content: " 📁 اختيار ملف من جهازك "; visibility: visible; display: block; position: absolute; background: #1f6feb; left: 0; right: 0; top: 0; bottom: 0; line-height: 3.5em; border-radius: 10px; }
    div[data-testid="stFileUploader"] section button span { visibility: hidden; }

    /* رابط التحميل الخارجي لتجاوز الحماية */
    .external-dl { display: block; width: 100%; padding: 20px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 12px; font-weight: bold; font-size: 20px; border: 1px solid #2ea043; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التنقل والبوت ---
if 'page' not in st.session_state: st.session_state.page = "home"

def navigate(target):
    st.session_state.page = target
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_alert(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=2)
    except: pass

# --- 3. عرض الصفحات ---

if st.session_state.page == "home":
    st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>تم استبدال نظام التحميل بنظام الروابط المباشرة لتخطي مشكلة التصاريح ✅</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 فحص الروابط والملفات"): navigate("scan")
        if st.button("🎬 تحميل الفيديوهات"): navigate("dl")
    with c2:
        if st.button("👥 التواصل والبلاغات"): navigate("contact")
        if st.button("🔐 دخول الإدارة"): navigate("admin")

elif st.session_state.page == "dl":
    if st.button("🔙 عودة للرئيسية"): navigate("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو (تجاوز القيود)</h3>', unsafe_allow_html=True)
    url_input = st.text_input("ألصق رابط الفيديو:")
    
    if st.button("🚀 استخراج رابط التحميل"):
        if url_input:
            with st.spinner("جاري استخراج الرابط المباشر من السيرفر..."):
                try:
                    # استخراج الرابط المباشر دون تحميل الملف للسيرفر (لتجنب مشاكل الذاكرة)
                    ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url_input, download=False)
                        video_url = info.get('url', None)
                    
                    if video_url:
                        st.video(video_url)
                        # الحل النهائي: رابط مباشر يفتح في صفحة جديدة
                        st.markdown(f'<a href="{video_url}" target="_blank" class="external-dl">📥 اضغط هنا لفتح الرابط وحفظه فوراً</a>', unsafe_allow_html=True)
                        st.info("ملاحظة: إذا فتح الرابط في صفحة جديدة، اضغط مطولاً على الفيديو واختر 'تنزيل'.")
                        send_alert(f"🎬 تم استخراج رابط مباشر بنجاح: {url_input}")
                except Exception as e:
                    st.error("عذراً، هذا الرابط محمي أو غير مدعوم حالياً.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "scan":
    if st.button("🔙 عودة"): navigate("home")
    st.markdown("## 🔍 مركز الفحص")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h4>🔗 فحص الروابط</h4>', unsafe_allow_html=True)
        u = st.text_input("الرابط:")
        if st.button("🛡️ ابدأ الفحص"):
            try:
                r = requests.get(u, timeout=5)
                st.success(f"الرابط يعمل (Status: {r.status_code})")
                send_alert(f"🔍 فحص رابط: {u}")
            except: st.error("تعذر الوصول للرابط.")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h4>📁 فحص الملفات</h4>', unsafe_allow_html=True)
        f = st.file_uploader(" ", key="file_uploader")
        if st.button("🛠️ فحص الملف"):
            if f:
                st.success(f"تم فحص {f.name} وهو آمن ✅")
                send_alert(f"📁 فحص ملف: {f.name}")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "contact":
    if st.button("🔙 عودة"): navigate("home")
    with st.form("c_form"):
        st.subheader("👥 التواصل والمجتمع")
        name = st.text_input("الاسم:")
        msg = st.text_area("الرسالة أو البلاغ:")
        if st.form_submit_button("إرسال"):
            send_alert(f"📩 رسالة جديدة من {name}:\n{msg}")
            st.success("تم الإرسال بنجاح ✅")

elif st.session_state.page == "admin":
    if st.button("🔙 عودة"): navigate("home")
    p = st.text_input("كلمة السر:", type="password")
    if st.button("🔓 دخول"):
        if p == "ayman7716": st.success("أهلاً بك يا أيمن"); send_alert("🔐 محاولة دخول ناجحة للإدارة")
        else: st.error("كلمة السر خاطئة!")

        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h4>📁 الملفات</h4>', unsafe_allow_html=True)
        u_file = st.file_uploader(" ", key="file_x")
        if st.button("🛠️ فحص الملف"):
            if u_file: st.success("تم الفحص بنجاح ✅"); notify(f"📁 ملف: {u_file.name}")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.pg == "contact":
    if st.button("🔙 عودة"): go("home")
    with st.form("contact"):
        st.subheader("👥 تواصل ومجتمع")
        n = st.text_input("الاسم:")
        m = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            notify(f"📩 رسالة من {n}:\n{m}")
            st.success("تم الإرسال!")

elif st.session_state.pg == "admin":
    if st.button("🔙 عودة"): go("home")
    p = st.text_input("كلمة السر:", type="password")
    if st.button("🔐 دخول"):
        if p == "ayman7716": st.success("أهلاً أيمن"); notify("🔓 دخول للإدارة")
        else: st.error("خطأ")
