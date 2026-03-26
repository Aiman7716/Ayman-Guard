import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random, time
from datetime import datetime

# --- 1. الإعدادات والربط (تأكد من صحة التوكين) ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 
WHITELIST = ["google.com", "facebook.com", "whatsapp.com", "microsoft.com", "apple.com", "instagram.com"]

def send_telegram_msg(message):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except: pass

def check_vt_file(file_hash):
    headers = {"x-apikey": VT_API_KEY}
    try:
        res = requests.get(f"https://www.virustotal.com/api/v3/files/{file_hash}", headers=headers, timeout=5)
        return res.json()['data']['attributes']['last_analysis_stats'] if res.status_code == 200 else None
    except: return None

# --- 2. قاعدة البيانات ---
conn = sqlite3.connect('ayman_pro_shield.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, category TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 3. التصميم السيبراني المطور (CSS) ---
st.set_page_config(page_title="Ayman Shield Pro", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #05070a; color: #e6edf3; }
    
    /* تنسيق البطاقات لمنع تداخل النصوص */
    .neon-card {
        background: #0d1117; border: 1px solid #30363d;
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        border-right: 5px solid #1f6feb;
    }
    
    /* تحسين الأزرار */
    .stButton>button {
        background: linear-gradient(90deg, #1f6feb, #58a6ff) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important; font-weight: bold !important;
        height: 3.5rem !important; width: 100%; transition: 0.3s;
    }
    
    /* إخفاء الزوائد */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* تنسيق خاص للجوال */
    @media (max-width: 600px) {
        .stMarkdown h1 { font-size: 1.5rem !important; }
        .neon-card { padding: 15px; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🛡️ التحكم</h2>", unsafe_allow_html=True)
    menu = st.radio("", ["📊 الرادار", "🔍 فحص الملفات", "🔗 فحص الروابط", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])
    st.write("---")
    st.markdown(f"<p style='text-align:center; color:#8b949e;'>أيمن جارد v25.0</p>", unsafe_allow_html=True)

st.markdown(f'<h1 style="text-align:center; color:#58a6ff;">🛡️ درع أيمن الاحترافي</h1>', unsafe_allow_html=True)

# --- 5. منطق الوظائف ---

if menu == "📊 الرادار":
    col1, col2 = st.columns(2)
    with col1:
        r_count = c.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
        st.markdown(f'<div class="neon-card"><h3>📈 البلاغات</h3><h2 style="color:#58a6ff;">{r_count}</h2></div>', unsafe_allow_html=True)
    with col2:
        m_count = c.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        st.markdown(f'<div class="neon-card"><h3>📩 الرسائل</h3><h2 style="color:#58a6ff;">{m_count}</h2></div>', unsafe_allow_html=True)

elif menu == "🔍 فحص الملفات":
    st.markdown('<div class="neon-card"><h3>📁 تحليل الملفات الذكي</h3></div>', unsafe_allow_html=True)
    up = st.file_uploader("اختر ملفاً لفحصه:")
    if up:
        data = up.read()
        f_hash = hashlib.sha256(data).hexdigest()
        st.info(f"بصمة الملف الرقمية: `{f_hash[:32]}...`")
        if st.button("بدء التحليل"):
            res = check_vt_file(f_hash)
            if res and res.get('malicious', 0) > 0:
                st.error("🚨 تحذير: تم اكتشاف برمجيات ضارة!")
                send_telegram_msg(f"🚨 ملف ضار: {up.name}")
            else: st.success("✅ الملف يبدو آمناً.")

elif menu == "🔗 فحص الروابط":
    st.markdown('<div class="neon-card"><h3>🔗 كاشف الروابط المشبوهة</h3></div>', unsafe_allow_html=True)
    url = st.text_input("ألصق الرابط هنا:")
    if st.button("فحص الرابط"):
        ext = tldextract.extract(url)
        dom = f"{ext.domain}.{ext.suffix}"
        if dom in WHITELIST: st.success(f"✅ نطاق موثوق: {dom}")
        else: st.warning(f"🔍 نطاق غير معروف: {dom} - يرجى توخي الحذر.")

elif menu == "👥 المجتمع":
    st.markdown('<div class="neon-card"><h3>👥 مركز بلاغات المجتمع</h3></div>', unsafe_allow_html=True)
    rep = st.text_area("أدخل تفاصيل التهديد أو الاحتيال:")
    if st.button("نشر البلاغ"):
        if rep:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?, ?)", (rep, "عام", dt))
            conn.commit()
            st.success("تم تسجيل بلاغك بنجاح!")
            send_telegram_msg(f"📢 بلاغ مجتمعي جديد: {rep[:60]}...")

elif menu == "🔐 الإدارة":
    st.markdown('<div class="neon-card"><h3>🔐 لوحة التحكم المؤمنة</h3></div>', unsafe_allow_html=True)
    pw = st.text_input("كلمة مرور النظام:", type="password")
    if pw == "ayman7716":
        if st.button("إرسال رمز 2FA"):
            sc = str(random.randint(1000, 9999))
            st.session_state['sc'] = sc
            send_telegram_msg(f"🔐 رمز دخول الإدارة: {sc}")
            st.info("تم إرسال الرمز إلى تليجرام.")
        
        v_code = st.text_input("أدخل الرمز المستلم:")
        if v_code and v_code == st.session_state.get('sc'):
            st.success("✅ تم التحقق")
            df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
            for i, r in df.iterrows():
                st.markdown(f'<div class="neon-card"><small>{r["dt"]}</small><br><b>{r["content"]}</b></div>', unsafe_allow_html=True)
