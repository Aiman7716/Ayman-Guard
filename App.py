import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random
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

# --- 2. التصميم البصري (v33.0 Ultra Stable) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    /* الهيدر الأزرق الفاخر */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 35px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #30363d;
    }
    .hero-box h1 { color: white; font-size: 2.2rem; margin: 0; }

    /* تبويبات التنقل العلوية */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #161b22;
        padding: 10px;
        border-radius: 15px;
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
        border-radius: 10px !important;
    }

    /* بطاقات المحتوى الموحدة */
    .content-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        margin-top: 15px;
    }

    /* تحسين شكل الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #1f6feb !important;
        color: white !important;
        border: none;
    }

    /* إخفاء القائمة الجانبية والزوائد */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_final_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
conn.commit()

# --- 4. الهيكل الرئيسي ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>المنصة المتكاملة للحماية الرقمية</p></div>', unsafe_allow_html=True)

# التبويبات الرئيسية
tab1, tab2, tab3, tab4 = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص", "👥 المجتمع", "🔐 الإدارة"])

# التبويب 1: الرئيسية
with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 حالة النظام")
    col1, col2 = st.columns(2)
    col1.metric("حالة الدرع", "نشط وآمن")
    col2.metric("التحديثات", "تلقائية")
    st.info("نظام أيمن جارد يراقب التهديدات بنجاح.")
    st.markdown('</div>', unsafe_allow_html=True)

# التبويب 2: مركز الفحص (دمج الملفات والروابط)
with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔍 مركز التحليل الشامل")
    
    # تبويبات داخلية للفحص
    sub_tab1, sub_tab2 = st.tabs(["🔗 فحص الرابط", "📁 فحص الملف"])
    
    with sub_tab1:
        u_in = st.text_input("أدخل الرابط للفحص:")
        if st.button("تحليل الرابط الآن"):
            if u_in:
                ext = tldextract.extract(u_in)
                dom = f"{ext.domain}.{ext.suffix}"
                if dom in WHITELIST: st.success(f"✅ هذا النطاق موثوق: {dom}")
                else: st.warning(f"🔍 تم التحليل: النطاق هو ({dom}) - يرجى الحذر إذا لم تكن تعرف المصدر.")
            else: st.error("يرجى إدخال رابط.")

    with sub_tab2:
        up = st.file_uploader("ارفع الملف المشبوه هنا:")
        if up and st.button("بدء فحص الملف"):
            data = up.read()
            f_hash = hashlib.sha256(data).hexdigest()
            st.info(f"بصمة الملف الرقمية: `{f_hash[:32]}...`")
            res = check_vt_file(f_hash)
            if res and res.get('malicious', 0) > 0:
                st.error("🚨 خطر! تم اكتشاف تهديد في هذا الملف.")
                send_telegram(f"🚨 تنبيه أمني: تم فحص ملف ضار باسم: {up.name}")
            else: st.success("✅ الملف يبدو آمناً وفقاً للفحص الأولي.")
    st.markdown('</div>', unsafe_allow_html=True)

# التبويب 3: المجتمع
with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("👥 أبلغ عن حالة احتيال")
    txt = st.text_area("أدخل تفاصيل الحالة:")
    if st.button("نشر وتحذير المجتمع"):
        if txt:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (txt, dt))
            conn.commit()
            send_telegram(f"📢 بلاغ جديد من المجتمع: {txt}")
            st.success("شكراً لك، تم تسجيل البلاغ بنجاح.")
    st.markdown('</div>', unsafe_allow_html=True)

# التبويب 4: الإدارة
with tab4:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔐 لوحة التحكم")
    pw = st.text_input("كلمة المرور:", type="password")
    if pw == "ayman7716":
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        st.write("سجل البلاغات المستلمة:")
        st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
