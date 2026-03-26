import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random
from datetime import datetime

# --- 1. الإعدادات والربط ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 
WHITELIST = ["google.com", "facebook.com", "whatsapp.com", "microsoft.com", "apple.com", "instagram.com"]

def send_telegram_msg(message):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except: pass

def check_vt_file(file_hash):
    headers = {"x-apikey": VT_API_KEY}
    try:
        res = requests.get(f"https://www.virustotal.com/api/v3/files/{file_hash}", headers=headers, timeout=5)
        return res.json()['data']['attributes']['last_analysis_stats'] if res.status_code == 200 else None
    except: return None

# --- 2. قاعدة البيانات ---
conn = sqlite3.connect('ayman_final_shield.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, category TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 3. التصميم الفاخر (Ultra Neon CSS) ---
st.set_page_config(page_title="Ayman Global Shield", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background: #05070a; color: #e6edf3; }
    
    /* الهيدر المتوهج */
    .main-header {
        text-align: center; padding: 25px;
        background: linear-gradient(180deg, rgba(31, 111, 235, 0.15) 0%, rgba(5, 7, 10, 0) 100%);
        border-bottom: 2px solid #1f6feb; margin-bottom: 30px;
    }
    
    /* البطاقات السيبرانية */
    .neon-card {
        background: #0d1117; border: 1px solid #30363d;
        border-radius: 15px; padding: 20px; margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    
    /* الأزرار الاحترافية */
    .stButton>button {
        background: linear-gradient(90deg, #1f6feb, #58a6ff) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important; font-weight: bold !important;
        height: 3.5rem !important; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 0 20px rgba(88, 166, 255, 0.4); }
    
    /* إخفاء شعارات ستريمليت */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. الهيكل الجانبي (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🛡️ لوحة التحكم</h2>", unsafe_allow_html=True)
    menu = st.radio("", ["📊 الرادار الرئيسي", "🔍 فحص الملفات", "🔗 كاشف الروابط", "👥 بلاغات المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])
    st.write("---")
    st.markdown("<p style='text-align:center; color:#8b949e;'>Ayman Shield v24.0</p>", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🛡️ درع أيمن العالمي</h1><p>Ayman Security Shield PRO</p></div>', unsafe_allow_html=True)

# --- 5. منطق الوظائف المتكامل ---

# 1. الرادار (الإحصائيات)
if menu == "📊 الرادار الرئيسي":
    col1, col2 = st.columns(2)
    with col1:
        count_r = c.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
        st.markdown(f'<div class="neon-card"><h3>📈 البلاغات</h3><h2 style="color:#58a6ff;">{count_r}</h2></div>', unsafe_allow_html=True)
    with col2:
        count_m = c.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        st.markdown(f'<div class="neon-card"><h3>📩 الرسائل</h3><h2 style="color:#58a6ff;">{count_m}</h2></div>', unsafe_allow_html=True)
    st.info("النظام يعمل بكفاءة عالية ويرصد التهديدات لحظياً.")

# 2. فحص الملفات
elif menu == "🔍 فحص الملفات":
    st.markdown('<div class="neon-card"><h3>📁 فحص الملفات العالمي</h3></div>', unsafe_allow_html=True)
    up = st.file_uploader("ارفع الملف المشبوه:")
    if up:
        f_hash = hashlib.sha256(up.read()).hexdigest()
        st.info(f"بصمة الملف: `{f_hash[:32]}...`")
        if st.button("بدء التحليل الآن"):
            res = check_vt_file(f_hash)
            if res and res.get('malicious', 0) > 0:
                st.error("🚨 ملف ضار!")
                send_telegram_msg(f"🚨 تنبيه: ملف ضار مكتشف: {up.name}")
            else: st.success("✅ الملف نظيف.")

# 3. كاشف الروابط
elif menu == "🔗 كاشف الروابط":
    st.markdown('<div class="neon-card"><h3>🔗 فحص الروابط</h3></div>', unsafe_allow_html=True)
    u_in = st.text_input("أدخل الرابط:")
    if st.button("تحليل الرابط"):
        ext = tldextract.extract(u_in)
        dom = f"{ext.domain}.{ext.suffix}"
        if dom in WHITELIST: st.success(f"✅ موثوق: {dom}")
        else: st.warning(f"🔍 نطاق غير معروف: {dom} - كن حذراً.")

# 4. بلاغات المجتمع
elif menu == "👥 بلاغات المجتمع":
    st.markdown('<div class="neon-card"><h3>👥 أبلغ عن احتيال</h3></div>', unsafe_allow_html=True)
    txt = st.text_area("تفاصيل البلاغ:")
    if st.button("إرسال وتحذير"):
        if txt:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?, ?)", (txt, "عام", dt))
            conn.commit()
            st.success("تم النشر بنجاح!")
            send_telegram_msg(f"📢 بلاغ جديد: {txt[:50]}")

# 5. اتصل بنا
elif menu == "📧 اتصل بنا":
    st.markdown('<div class="neon-card"><h3>📧 تواصل معنا</h3></div>', unsafe_allow_html=True)
    n = st.text_input("الاسم:")
    m = st.text_area("الرسالة:")
    if st.button("إرسال الرسالة"):
        dt = datetime.now().strftime("%Y-%m-%d %H:%M")
        c.execute("INSERT INTO messages VALUES (?, ?, ?)", (n, m, dt))
        conn.commit()
        st.success("تم الإرسال!")
        send_telegram_msg(f"📩 رسالة من {n}: {m}")

# 6. الإدارة (نظام البطاقات)
elif menu == "🔐 الإدارة":
    st.markdown('<div class="neon-card"><h3>🔐 لوحة التحكم</h3></div>', unsafe_allow_html=True)
    pw = st.text_input("كلمة المرور:", type="password")
    if pw == "ayman7716":
        if st.button("طلب كود 2FA"):
            sc = str(random.randint(1000, 9999))
            st.session_state['sc'] = sc
            send_telegram_msg(f"🔐 كود الإدارة: {sc}")
        
        vi = st.text_input("أدخل الكود:")
        if vi and vi == st.session_state.get('sc'):
            st.success("✅ تم الدخول")
            df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
            for i, r in df.iterrows():
                st.markdown(f'<div class="neon-card"><small>{r["dt"]}</small><br><b>{r["content"]}</b></div>', unsafe_allow_html=True)
