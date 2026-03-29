import streamlit as st
import requests
import random
import time

# --- 1. إعدادات الهوية والديناميكية ---
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'site_title': "🛡️ درع أيمن السيادي",
        'site_sub': "بوابتك الآمنة للتحميل والفحص الأمني الذكي",
        'tab1': "🏠 الرئيسية", 'tab2': "🎬 تحميل الفيديو", 
        'tab3': "🔍 فحص الروابط", 'tab4': "🛡️ الحماية والدعم", 'tab5': "⚙️ الإدارة",
    }

if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'auth_code' not in st.session_state: st.session_state.auth_code = None

# --- 2. محرك الإرسال (بوت أيمن) ---
def send_telegram_code(code):
    TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
    MY_PERSONAL_ID = "906233240" 
    message = f"🔐 كود الدخول للوحة الإدارة: {code}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, data={"chat_id": MY_PERSONAL_ID, "text": message})
    except: pass

# --- 3. التنسيق البصري الجذاب (CSS) ---
st.set_page_config(page_title=st.session_state.settings['site_title'], layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; }
    
    /* هيدر جذاب */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 40px; border-radius: 20px; text-align: center;
        border: 1px solid #30363d; margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* بطاقات الرئيسية */
    .feature-card {
        background: #161b22; padding: 20px; border-radius: 15px;
        border-right: 5px solid #1f6feb; margin-bottom: 15px;
    }
    
    /* أزرار التواصل */
    .btn-tele { background: #0088cc !important; color: white !important; border-radius: 10px !important; }
    .btn-wa { background: #25d366 !important; color: white !important; border-radius: 10px !important; }
    .btn-mail { background: #ea4335 !important; color: white !important; border-radius: 10px !important; }
    
    /* زر تحميل الملف البارز */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #ff9100, #ff6d00) !important;
        color: white !important; font-size: 20px !important;
        width: 100% !important; border-radius: 15px !important; height: 3em !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. هيكل الموقع ---
st.markdown(f'''
    <div class="hero-box">
        <h1 style="color:white; margin:0;">{st.session_state.settings['site_title']}</h1>
        <p style="color:#8b949e; font-size:1.2em;">{st.session_state.settings['site_sub']}</p>
    </div>
''', unsafe_allow_html=True)

tabs = st.tabs([st.session_state.settings[f'tab{i}'] for i in range(1, 6)])

# --- الرئيسية (تصميم جذاب) ---
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 سرعة فائقة</h3>
            <p>نستخدم أحدث التقنيات لضمان وصولك للمحتوى بأسرع وقت ممكن وبأعلى جودة.</p>
        </div>
        <div class="feature-card" style="border-right-color: #238636;">
            <h3>🛡️ أمان مطلق</h3>
            <p>جميع الروابط والملفات تمر عبر فحص أمني دقيق قبل وصولها إليك.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.image("https://img.icons8.com/clouds/200/shield.png")

# --- تحميل الفيديو ---
with tabs[1]:
    st.subheader("🎬 مركز تحميل الوسائط")
    v_url = st.text_input("ألصق رابط الفيديو هنا (يوتيوب، تيك توك، فيسبوك):")
    if st.button("🚀 تحليل الرابط وجلب الفيديو"):
        st.info("جاري المعالجة... يرجى الانتظار.")

# --- فحص الروابط والملفات (زر بارز) ---
with tabs[2]:
    st.subheader("🔍 مركز الفحص الأمني")
    st.text_input("أدخل الرابط المشبوه لفحصه:")
    st.button("🛡️ ابدأ الفحص الآن")
    st.markdown("---")
    st.write("📂 **رفع ملف لفحصه:**")
    # زر تحميل بارز بلون برتقالي متدرج كما طلبت
    st.download_button(label="📥 اضغط هنا لرفع وتحميل الملف للفحص", data="file", file_name="scan.txt")

# --- الحماية والدعم (أزرار التواصل) ---
with tabs[3]:
    st.subheader("💬 قنوات التواصل الرسمية")
    st.info("نحن هنا لخدمتك على مدار الساعة، اختر الوسيلة المناسبة لك:")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🤖 بوت تليجرام", key="tele"):
            st.markdown("[إضغط هنا للذهاب للبوت](https://t.me/Aiman_Guard_2026_bot)")
    with c2:
        if st.button("📱 واتساب مباشر", key="wa"):
            st.markdown("[إضغط هنا لمراسلة أيمن](https://wa.me/967xxxxxxx)") # ضع رقمك هنا
    with c3:
        if st.button("📧 البريد الإلكتروني", key="mail"):
            st.write("aiman@example.com")

# --- الإدارة ---
with tabs[4]:
    if not st.session_state.is_admin:
        pwd = st.text_input("كلمة مرور المسؤول:", type="password")
        if st.button("🔑 طلب كود التحقق"):
            if pwd == "Ayman2026":
                st.session_state.auth_code = str(random.randint(111111, 999999))
                send_telegram_code(st.session_state.auth_code)
                st.success("تم إرسال الكود لهاتفك.")
    else:
        st.success("أهلاً أيمن، لوحة التحكم جاهزة.")
        if st.button("🚪 خروج"): st.session_state.is_admin = False; st.rerun()
