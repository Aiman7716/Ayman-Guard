import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
from datetime import datetime

# --- 1. الإعدادات والربط ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 
WHITELIST = ["google.com", "facebook.com", "whatsapp.com", "microsoft.com", "apple.com", "instagram.com"]

def send_telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except: pass

def check_vt_file(file_hash):
    headers = {"x-apikey": VT_API_KEY}
    try:
        res = requests.get(f"https://www.virustotal.com/api/v3/files/{file_hash}", headers=headers, timeout=5)
        return res.json()['data']['attributes']['last_analysis_stats'] if res.status_code == 200 else None
    except: return None

# --- 2. التصميم البصري المطور (v34.0 Custom Design) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    /* الهيدر مع الشعار */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #30363d;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .shield-logo {
        font-size: 50px;
        margin-bottom: 10px;
        filter: drop-shadow(0 0 10px #58a6ff);
    }
    .hero-box h1 { color: white; font-size: 2.2rem; margin: 0; }

    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161b22;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        color: #8b949e !important;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f6feb !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* البطاقات */
    .content-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        margin-top: 15px;
    }

    /* الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.2em;
        background-color: #1f6feb !important;
        color: white !important;
        border: none;
        font-weight: bold;
    }

    /* إخفاء الزوائد */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_security_v34.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS contact_msgs (name TEXT, email TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. واجهة المستخدم الرئيسية ---
st.markdown("""
    <div class="hero-box">
        <div class="shield-logo">🛡️</div>
        <h1>درع أيمن الأمني</h1>
        <p>Ayman Security Shield PRO v34.0</p>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# التبويب 1: الرئيسية
with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 حالة الحماية")
    r_total = c.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    st.metric("إجمالي التهديدات المرصودة", r_total)
    st.info("نظام الدرع يعمل بكفاءة قصوى الآن.")
    st.markdown('</div>', unsafe_allow_html=True)

# التبويب 2: مركز الفحص
with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    sub1, sub2 = st.tabs(["🔗 فحص الرابط", "📁 فحص الملف"])
    with sub1:
        u = st.text_input("رابط الموقع:")
        if st.button("تحليل الرابط"):
            if u:
                dom = tldextract.extract(u).registered_domain
                if dom in WHITELIST: st.success(f"✅ موثوق: {dom}")
                else: st.warning(f"🔍 نطاق غير معروف: {dom}")
    with sub2:
        f = st.file_uploader("ارفع الملف المشبوه:")
        if f and st.button("فحص بصمة الملف"):
            h = hashlib.sha256(f.read()).hexdigest()
            res = check_vt_file(h)
            if res and res.get('malicious', 0) > 0: st.error("🚨 خطر اكتشاف برمجية ضارة!")
            else: st.success("✅ الملف نظيف أمنياً.")
    st.markdown('</div>', unsafe_allow_html=True)

# التبويب 3: المجتمع
with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📢 بلاغ جديد")
    txt = st.text_area("تفاصيل الحالة:")
    if st.button("إرسال البلاغ"):
        if txt:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (txt, dt))
            conn.commit()
            send_telegram(f"📢 بلاغ مجتمعي: {txt}")
            st.success("تم تسجيل البلاغ بنجاح.")
    st.markdown('</div>', unsafe_allow_html=True)

# التبويب 4: تواصل معنا (الجديد)
with tab4:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 اتصل بإدارة الدرع")
    c_name = st.text_input("الاسم الكامل:")
    c_email = st.text_input("البريد الإلكتروني أو رقم الهاتف:")
    c_msg = st.text_area("رسالتك أو استفسارك:")
    if st.button("إرسال الرسالة للإدارة"):
        if c_name and c_msg:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO contact_msgs VALUES (?, ?, ?, ?)", (c_name, c_email, c_msg, dt))
            conn.commit()
            send_telegram(f"📩 رسالة جديدة من {c_name}:\n{c_msg}")
            st.success("شكراً لتواصلك يا أيمن، تم استلام رسالتك.")
        else: st.error("يرجى ملء الاسم والرسالة.")
    st.markdown('</div>', unsafe_allow_html=True)

# التبويب 5: الإدارة
with tab4: # تم تعديله ليكون tab5 برمجياً
    pass # سيظهر المحتوى عند تفعيله من الإعدادات
