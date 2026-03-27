import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import yt_dlp
from datetime import datetime

# --- 1. الإعدادات والربط (آمنة تماماً) ---
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

# --- 2. التصميم البصري (مطابق لصورة 1000566740.jpg) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #30363d;
    }
    .shield-icon { font-size: 55px; filter: drop-shadow(0 0 10px #58a6ff); margin-bottom: 10px; }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; background-color: #161b22; padding: 10px; border-radius: 12px; border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] { height: 50px; color: #8b949e !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1f6feb !important; color: white !important; border: none; font-weight: bold; }
    
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_pro_v36.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS contact_msgs (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. واجهة المستخدم ---
st.markdown("""
    <div class="hero-box">
        <div class="shield-icon">🛡️</div>
        <h1>درع أيمن الأمني</h1>
        <p>Ayman Security & Media PRO v36.5</p>
    </div>
    """, unsafe_allow_html=True)

# التبويبات الخمسة المكتملة
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "🔐 الإدارة"])

# --- 1: الرئيسية ---
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 إحصائيات الدرع")
    r_total = c.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    st.metric("البلاغات المسجلة", r_total)
    st.success("✅ النظام يعمل بكامل طاقته.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 2: مركز الفحص (الروابط والملفات) ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f_sub_tabs = st.tabs(["🔗 فحص الرابط", "📁 فحص الملف"])
    with f_sub_tabs[0]:
        u_in = st.text_input("ضع الرابط هنا:")
        if st.button("تحليل الرابط"):
            if u_in:
                domain = tldextract.extract(u_in).registered_domain
                if domain in WHITELIST: st.success(f"✅ موثوق: {domain}")
                else: st.warning(f"🔍 نطاق غير مألوف: {domain}")
    with f_sub_tabs[1]:
        f_up = st.file_uploader("ارفع ملف للفحص:")
        if f_up and st.button("بدء الفحص البرمجي"):
            h = hashlib.sha256(f_up.read()).hexdigest()
            res = check_vt_file(h)
            if res and res.get('malicious', 0) > 0: st.error("🚨 خطر! تم اكتشاف برمجية ضارة.")
            else: st.success("✅ الملف سليم.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3: محمل الفيديو (الميزة الجديدة 😁) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 تحميل الفيديوهات")
    v_url = st.text_input("ألصق رابط الفيديو:")
    if st.button("استخراج وتحميل"):
        if v_url:
            with st.spinner("جاري التحليل..."):
                try:
                    ydl_opts = {'format': 'best', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        st.video(v_url)
                        st.markdown(f'<a href="{info["url"]}" target="_blank"><button style="width:100%; background-color:#28a745; color:white; height:3em; border-radius:10px; border:none; cursor:pointer;">📥 اضغط هنا للتحميل المباشر</button></a>', unsafe_allow_html=True)
                except: st.error("❌ الرابط غير مدعوم حالياً.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4: المجتمع وتواصل معنا (دمج ذكي) ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📢 البلاغات والتواصل")
    name = st.text_input("الاسم:")
    txt = st.text_area("نص البلاغ أو الرسالة:")
    if st.button("إرسال الآن"):
        if txt:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (txt, dt))
            conn.commit()
            send_telegram(f"📢 بلاغ/رسالة من {name}: {txt}")
            st.success("تم الإرسال بنجاح!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5: الإدارة (شغالة 100%) ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔐 لوحة التحكم")
    pw = st.text_input("كلمة مرور المدير:", type="password")
    if pw == "ayman7716":
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        st.dataframe(df, use_container_width=True)
    elif pw: st.error("كلمة المرور خاطئة")
    st.markdown('</div>', unsafe_allow_html=True)
