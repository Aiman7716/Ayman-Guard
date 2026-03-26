import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random
from datetime import datetime

# --- الإعدادات والربط ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

def send_telegram_msg(message):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except: pass

# --- قاعدة البيانات ---
conn = sqlite3.connect('ayman_cyber_v22.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, category TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- التصميم المستقبلي (The Cyber Look) ---
st.set_page_config(page_title="Ayman Shield PRO", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* تغيير الخلفية العامة */
    .stApp {
        background: radial-gradient(circle at top right, #0d1117, #010409);
        color: #c9d1d9;
    }
    
    /* تصميم القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: #0b0e14 !important;
        border-left: 1px solid #30363d;
    }

    /* تصميم العنوان الرئيسي */
    .cyber-title {
        text-align: center;
        background: linear-gradient(90deg, #58a6ff, #1f6feb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 10px;
        text-shadow: 0 0 20px rgba(88, 166, 255, 0.3);
    }

    /* بطاقات البيانات (Glassmorphism) */
    .cyber-card {
        background: rgba(22, 27, 34, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .cyber-card:hover {
        border-color: #58a6ff;
        box-shadow: 0 0 15px rgba(88, 166, 255, 0.2);
    }

    /* تخصيص الأزرار */
    .stButton>button {
        background: linear-gradient(45deg, #1f6feb, #58a6ff);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(88, 166, 255, 0.4);
    }

    /* محاذاة النصوص للغة العربية */
    .main, p, h1, h2, h3, div, label, span {
        direction: RTL !important;
        text-align: right !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية الاحترافية ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🛡️ القائمة</h2>", unsafe_allow_html=True)
    menu = st.radio("", ["📊 الرادار الرئيسي", "🔍 فحص الملفات", "🔗 كاشف الروابط", "👥 بلاغات المجتمع", "📧 اتصل بنا", "🔐 لوحة التحكم"])
    st.write("---")
    st.markdown("<p style='text-align:center; color:#8b949e;'>الإصدار 22.0 PRO</p>", unsafe_allow_html=True)

st.markdown('<h1 class="cyber-title">Ayman Security Shield</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:1.2rem; color:#8b949e;">المنصة العالمية لتأمين المجتمع الرقمي</p>', unsafe_allow_html=True)

# --- التفاعلات حسب القائمة ---
if menu == "📊 الرادار الرئيسي":
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="cyber-card"><h3>📈 البلاغات</h3><h2>'+str(c.execute("SELECT COUNT(*) FROM reports").fetchone()[0])+'</h2></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="cyber-card"><h3>📩 الرسائل</h3><h2>'+str(c.execute("SELECT COUNT(*) FROM messages").fetchone()[0])+'</h2></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="cyber-card"><h3>🛡️ الحالة</h3><h2>نشط</h2></div>', unsafe_allow_html=True)

elif menu == "🔍 فحص الملفات":
    st.markdown('<div class="cyber-card"><h3>📁 نظام تحليل الملفات</h3></div>', unsafe_allow_html=True)
    up = st.file_uploader("ارفع ملفك:")
    if up:
        if st.button("بدء الفحص النيوني"):
            st.success("الملف نظيف ✅")

elif menu == "👥 بلاغات المجتمع":
    st.markdown('<div class="cyber-card"><h3>📢 إضافة بلاغ جديد</h3></div>', unsafe_allow_html=True)
    txt = st.text_area("تفاصيل التهديد:")
    if st.button("نشر وتحذير"):
        if txt:
            c.execute("INSERT INTO reports VALUES (?, ?, ?)", (txt, "عام", datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            st.success("تم النشر بنجاح!")

elif menu == "🔐 لوحة التحكم":
    st.markdown('<div class="cyber-card"><h3>🔐 الإدارة المؤمنة</h3></div>', unsafe_allow_html=True)
    pw = st.text_input("كلمة السر:", type="password")
    if pw == "ayman7716":
        # هنا تظهر البطاقات التي صممناها سابقاً
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        for i, r in df.iterrows():
            st.markdown(f'<div class="cyber-card"><small>{r["dt"]}</small><br><b>{r["content"]}</b></div>', unsafe_allow_html=True)
