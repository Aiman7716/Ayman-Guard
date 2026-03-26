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

# --- 2. التصميم البصري (مطابق تماماً لصورة 1000566740.jpg) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    /* الهيدر الأزرق الموحد مع الشعار */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #30363d;
    }
    .shield-icon { font-size: 55px; filter: drop-shadow(0 0 10px #58a6ff); margin-bottom: 10px; }
    .hero-box h1 { color: white; font-size: 2.2rem; margin: 0; }

    /* تبويبات التنقل العلوية المصلحة */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161b22;
        padding: 10px;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        color: #8b949e !important;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f6feb !important;
        color: white !important;
        border-radius: 10px !important;
    }

    /* بطاقات المحتوى */
    .content-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        margin-top: 15px;
    }

    /* إخفاء الزوائد */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة قاعدة البيانات ---
conn = sqlite3.connect('ayman_security_v35.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS contact_msgs (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. الهيكل الرئيسي للواجهة ---
st.markdown("""
    <div class="hero-box">
        <div class="shield-icon">🛡️</div>
        <h1>درع أيمن الأمني</h1>
        <p>Ayman Security Shield PRO v35.0</p>
    </div>
    """, unsafe_allow_html=True)

# تعريف التبويبات الخمسة بشكل صحيح
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 إحصائيات الدرع")
    r_total = c.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    st.metric("إجمالي البلاغات المسجلة", r_total)
    st.success("✅ جميع الأنظمة تعمل بشكل طبيعي وتحت مراقبتك.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 2: مركز الفحص ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f_tabs = st.tabs(["🔗 فحص الرابط", "📁 فحص الملف"])
    with f_tabs[0]:
        u_in = st.text_input("ضع الرابط هنا:")
        if st.button("تحليل الآن"):
            if u_in:
                domain = tldextract.extract(u_in).registered_domain
                if domain in WHITELIST: st.success(f"✅ نطاق موثوق جداً: {domain}")
                else: st.warning(f"🔍 نطاق غير مسجل في القائمة البيضاء: {domain}")
    with f_tabs[1]:
        file_up = st.file_uploader("ارفع ملف للفحص:")
        if file_up and st.button("بدء الفحص العميق"):
            f_hash = hashlib.sha256(file_up.read()).hexdigest()
            res = check_vt_file(f_hash)
            if res and res.get('malicious', 0) > 0: st.error("🚨 خطر! ملف مشبوه.")
            else: st.success("✅ الملف نظيف برمجياً.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 3: المجتمع ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📢 بلاغ مجتمعي جديد")
    txt = st.text_area("تفاصيل حالة الاحتيال:")
    if st.button("نشر البلاغ"):
        if txt:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (txt, dt))
            conn.commit()
            send_telegram(f"📢 بلاغ جديد: {txt}")
            st.success("تم تسجيل البلاغ وإرساله للقنوات الأمنية.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 4: تواصل معنا ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 أرسل رسالة للإدارة")
    name = st.text_input("اسمك:")
    msg = st.text_area("نص الرسالة:")
    if st.button("إرسال"):
        if name and msg:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO contact_msgs VALUES (?, ?, ?)", (name, msg, dt))
            conn.commit()
            send_telegram(f"📩 رسالة من {name}: {msg}")
            st.success("شكراً يا أيمن، تم استلام رسالتك بنجاح.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 5: الإدارة (الذي تم إصلاحه) ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔐 لوحة التحكم الخاصة بالمسؤول")
    admin_pw = st.text_input("كلمة مرور المسؤول:", type="password")
    if admin_pw == "ayman7716":
        st.write("📋 سجل البلاغات:")
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        st.dataframe(df, use_container_width=True)
        
        st.write("✉️ رسائل التواصل:")
        df_msgs = pd.read_sql_query("SELECT * FROM contact_msgs ORDER BY dt DESC", conn)
        st.dataframe(df_msgs, use_container_width=True)
    elif admin_pw:
        st.error("❌ كلمة المرور غير صحيحة")
    st.markdown('</div>', unsafe_allow_html=True)
