import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random
from datetime import datetime

# --- 1. الإعدادات والربط ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 
WHITELIST = ["google.com", "facebook.com", "whatsapp.com", "microsoft.com", "apple.com", "instagram.com"]

# دالة إرسال تنبيهات تليجرام
def send_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": text}, timeout=5)
    except: pass

# دالة فحص الملفات عبر VirusTotal
def check_file(h):
    try:
        headers = {"x-apikey": VT_API_KEY}
        res = requests.get(f"https://www.virustotal.com/api/v3/files/{h}", headers=headers, timeout=5)
        return res.json()['data']['attributes']['last_analysis_stats'] if res.status_code == 200 else None
    except: return None

# --- 2. التصميم المتجاوب (CSS) لمنع التداخل ---
st.set_page_config(page_title="Ayman Shield", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* ضبط الخط والاتجاه */
    html, body, [class*="st-"] {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }
    .stApp { background-color: #0d1117; color: #e6edf3; }

    /* هيدر الصفحة الرئيسي */
    .main-header {
        text-align: center;
        padding: 20px;
        background: #161b22;
        border-bottom: 2px solid #58a6ff;
        border-radius: 0 0 15px 15px;
        margin-bottom: 25px;
    }

    /* بطاقات العرض (للبلاغات والرسائل) */
    .card {
        background: #161b22;
        border: 1px solid #30363d;
        border-right: 5px solid #58a6ff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    /* تحسين شكل الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        background: linear-gradient(90deg, #1f6feb, #58a6ff) !important;
        color: white !important;
        font-weight: bold;
        border: none;
    }

    /* إخفاء الزوائد المزعجة */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_v28.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, category TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. الهيكل الجانبي والملاحة ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🛡️ القائمة</h2>", unsafe_allow_html=True)
    menu = st.radio("", ["📊 الإحصائيات", "🔍 الفحص الذكي", "👥 بلاغات المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])
    st.write("---")
    st.info("الإصدار الاحترافي v28.0")

st.markdown('<div class="main-header"><h1>🛡️ درع أيمن الأمني</h1></div>', unsafe_allow_html=True)

# --- 5. منطق التبويبات ---

# 1. الإحصائيات
if menu == "📊 الإحصائيات":
    r_total = c.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    m_total = c.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    col1, col2 = st.columns(2)
    with col1: st.markdown(f'<div class="card"><h3>📦 البلاغات</h3><h2 style="color:#58a6ff;">{r_total}</h2></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="card"><h3>📩 الرسائل</h3><h2 style="color:#58a6ff;">{m_total}</h2></div>', unsafe_allow_html=True)

# 2. الفحص الذكي (روابط وملفات)
elif menu == "🔍 الفحص الذكي":
    tab_f, tab_l = st.tabs(["📁 فحص ملف", "🔗 فحص رابط"])
    with tab_f:
        up = st.file_uploader("ارفع الملف للفحص:")
        if up and st.button("بدء فحص الملف"):
            h = hashlib.sha256(up.read()).hexdigest()
            res = check_file(h)
            if res and res.get('malicious', 0) > 0: st.error("🚨 ملف ضار!")
            else: st.success("✅ الملف نظيف.")
    with tab_l:
        url = st.text_input("أدخل الرابط:")
        if st.button("تحليل الرابط"):
            ext = tldextract.extract(url)
            dom = f"{ext.domain}.{ext.suffix}"
            if dom in WHITELIST: st.success(f"✅ موثوق: {dom}")
            else: st.warning(f"🔍 نطاق غير معروف: {dom}")

# 3. بلاغات المجتمع
elif menu == "👥 بلاغات المجتمع":
    txt = st.text_area("وصف حالة الاحتيال أو التهديد:")
    if st.button("نشر البلاغ"):
        if txt:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?, ?)", (txt, "عام", dt))
            conn.commit()
            st.success("تم النشر بنجاح!")
            send_msg(f"📢 بلاغ جديد: {txt}")

# 4. اتصل بنا
elif menu == "📧 اتصل بنا":
    n = st.text_input("الاسم:")
    m = st.text_area("الرسالة:")
    if st.button("إرسال"):
        if n and m:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO messages VALUES (?, ?, ?)", (n, m, dt))
            conn.commit()
            st.success("تم الإرسال!")
            send_msg(f"📩 رسالة من {n}: {m}")

# 5. الإدارة (الحل النهائي لمشكلة العرض)
elif menu == "🔐 الإدارة":
    pwd = st.text_input("كلمة المرور:", type="password")
    if pwd == "ayman7716":
        if st.button("طلب رمز التحقق (2FA)"):
            sc = str(random.randint(1000, 9999))
            st.session_state['sc'] = sc
            send_msg(f"🔐 رمز الدخول: {sc}")
        
        v = st.text_input("أدخل الرمز:")
        if v and v == st.session_state.get('sc'):
            st.success("✅ تم التحقق")
            df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
            for i, row in df.iterrows():
                st.markdown(f"""
                <div class="card">
                    <small style="color:#8b949e;">{row['dt']}</small><br>
                    <p style="font-size:1.1rem; margin-top:5px;">{row['content']}</p>
                </div>
                """, unsafe_allow_html=True)
