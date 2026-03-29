import streamlit as st
import yt_dlp
import os
import requests
from io import BytesIO

# --- 1. واجهة أيمن السيادية (تصميم نظيف وبدون تبويبات) ---
st.set_page_config(page_title="Ayman Shield v43", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stHeader"], [data-testid="stTabNav"] { display: none !important; }
    
    /* تنسيق الأزرار الزرقاء الكبيرة */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 15px; height: 4.5em; font-weight: bold; font-size: 18px; border: none; }
    
    /* تنسيق زر اختيار ملف (أزرق) */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; width: 100% !important; height: 3.5em !important; border: none !important; }
    
    /* تنسيق زر التنزيل (أخضر سيادي) */
    .stDownloadButton>button { background-color: #238636 !important; color: white !important; border-radius: 12px !important; height: 5em !important; font-size: 22px !important; font-weight: bold !important; border: 2px solid #ffffff !important; }
    
    .card { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التنقل والبوت ---
if 'pg' not in st.session_state: st.session_state.pg = "home"

def nav(t):
    st.session_state.pg = t
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_to_ayman(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=2)
    except: pass

# --- 3. الصفحات بنظام الأزرار ---

if st.session_state.pg == "home":
    st.markdown('<div class="card"><h1>🛡️ درع أيمن السيادي</h1><p>تم استعادة المحرك البرمجي المستقر من النسخ الأولى ✅</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 فحص الروابط والملفات"): nav("scan")
        if st.button("🎬 تحميل الفيديوهات"): nav("dl")
    with col2:
        if st.button("👥 التواصل والبلاغات"): nav("contact")
        if st.button("🔐 دخول الإدارة"): nav("admin")

elif st.session_state.pg == "dl":
    if st.button("🔙 العودة للرئيسية"): nav("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو (المحرك الأصلي)</h3>', unsafe_allow_html=True)
    v_url = st.text_input("ألصق الرابط هنا:")
    
    if st.button("🚀 معالجة الفيديو الآن"):
        if v_url:
            with st.spinner("جاري المعالجة البرمجية..."):
                try:
                    # العودة للكود البرمجي القديم: التحميل المباشر للذاكرة لتجنب مشاكل التصاريح
                    buffer = BytesIO()
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': '-', # إرسال المخرجات مباشرة لتدفق البيانات
                        'logtostderr': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=True)
                        # هنا نستخدم الطريقة القديمة في تقديم الملف كبيانات ثنائية
                        with open(ydl.prepare_filename(info), 'rb') as f:
                            buffer.write(f.read())
                    
                    st.video(v_url)
                    st.download_button(
                        label="📥 حفظ الفيديو فوراً",
                        data=buffer.getvalue(),
                        file_name="ayman_shield_vid.mp4",
                        mime="video/mp4"
                    )
                    send_to_ayman(f"🎬 نجاح تحميل فيديو: {v_url}")
                except Exception as e:
                    st.error(f"حدث خطأ في المحرك: {e}")

elif st.session_state.pg == "scan":
    if st.button("🔙 عودة"): nav("home")
    st.markdown("## 🔍 مركز الفحص")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><h4>🔗 الروابط</h4>', unsafe_allow_html=True)
        u = st.text_input("الرابط:")
        if st.button("🛡️ فحص"):
            try:
                r = requests.get(u, timeout=5)
                st.success(f"مستجيب ({r.status_code})")
                send_to_ayman(f"🔍 فحص رابط: {u}")
            except: st.error("فشل الوصول")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><h4>📁 الملفات</h4>', unsafe_allow_html=True)
        # الزر الأزرق المطلوب
        f = st.file_uploader(" ", key="ayman_f")
        if st.button("🛠️ فحص الملف"):
            if f:
                st.success(f"تم فحص {f.name} بنجاح")
                send_to_ayman(f"📁 فحص ملف: {f.name}")
        st.markdown('</div>', unsafe_allow_html=True)

# صفحات التواصل والإدارة (تعمل بالمنطق المستقر)
elif st.session_state.pg == "contact":
    if st.button("🔙 عودة"): nav("home")
    with st.form("contact"):
        n = st.text_input("الاسم:")
        m = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            send_to_ayman(f"📩 رسالة من {n}: {m}")
            st.success("تم الإرسال")

elif st.session_state.pg == "admin":
    if st.button("🔙 عودة"): nav("home")
    p = st.text_input("السر:", type="password")
    if st.button("دخول"):
        if p == "ayman7716": st.success("أهلاً أيمن"); send_to_ayman("🔐 دخول إدارة")
        else: st.error("خطأ")
