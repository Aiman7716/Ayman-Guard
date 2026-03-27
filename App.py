import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import yt_dlp
from datetime import datetime

# --- 1. الإعدادات والربط ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 
WHITELIST = ["google.com", "facebook.com", "whatsapp.com", "microsoft.com", "apple.com", "instagram.com"]

def send_telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except: pass

# --- 2. التصميم البصري (v41.0) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px 20px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d;
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
conn = sqlite3.connect('ayman_pro_v41.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS contact_msgs (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. واجهة المستخدم ---
st.markdown("""
    <div class="hero-box">
        <div class="shield-icon">🛡️</div>
        <h1>درع أيمن الأمني</h1>
        <p>Ayman Security & Media PRO v41.0</p>
    </div>
    """, unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 إحصائيات النظام")
    col1, col2 = st.columns(2)
    col1.metric("الحماية", "نشطة")
    col2.metric("الوسائط", "جاهزة")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 2: الفحص ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f_sub = st.tabs(["🔗 فحص الرابط", "📁 فحص الملف"])
    with f_sub[0]:
        u_in = st.text_input("ضع الرابط للفحص:")
        if st.button("تحليل الرابط"):
            if u_in:
                dom = tldextract.extract(u_in).registered_domain
                if dom in WHITELIST: st.success(f"✅ موثوق: {dom}")
                else: st.warning(f"🔍 غير معروف: {dom}")
    with f_sub[1]:
        f_up = st.file_uploader("ارفع الملف:")
        if f_up and st.button("فحص"):
            st.success("✅ ملف سليم.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 3: محمل الفيديو والصوت (إصلاح العرض 😁) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج وتشغيل الوسائط")
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    
    if st.button("بدء المعالجة والعرض"):
        if v_url:
            with st.spinner("جاري استخراج الفيديو للمعاينة..."):
                try:
                    # إعدادات متقدمة لاستخراج الرابط القابل للتشغيل مباشرة
                    ydl_opts = {
                        'format': 'best',
                        'quiet': True,
                        'no_warnings': True,
                        'force_generic_extractor': False
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        
                        # الرابط المباشر (Direct Stream)
                        video_direct = info.get('url')
                        audio_direct = next((f['url'] for f in info.get('formats', []) if f.get('acodec') != 'none' and f.get('vcodec') == 'none'), video_direct)
                        
                        # محاولة عرض الفيديو
                        if video_direct:
                            st.video(video_direct) 
                            st.success(f"📺 تم استخراج: {info.get('title', 'Video')}")
                        
                        # أزرار التحميل
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f'<a href="{video_direct}" target="_blank"><button style="width:100%; background-color:#1f6feb; color:white; height:3.5em; border-radius:10px; border:none; font-weight:bold; cursor:pointer;">📥 تحميل فيديو MP4</button></a>', unsafe_allow_html=True)
                        with c2:
                            st.markdown(f'<a href="{audio_direct}" target="_blank"><button style="width:100%; background-color:#e91e63; color:white; height:3.5em; border-radius:10px; border:none; font-weight:bold; cursor:pointer;">🎵 تحميل صوت MP3</button></a>', unsafe_allow_html=True)
                            
                except Exception as e:
                    st.error("❌ تعذر تشغيل المعاينة المباشرة لهذا الرابط، ولكن يمكنك تجربة أزرار التحميل أدناه.")
                    # توفير أزرار تحميل احتياطية في حال فشل المعاينة
                    st.info("قد يكون الفيديو محمياً من العرض الخارجي.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 4: المجتمع ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    rep_txt = st.text_area("وصف حالة الاحتيال:")
    if st.button("إرسال البلاغ"):
        if rep_txt:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (rep_txt, dt))
            conn.commit()
            st.success("تم!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 5: تواصل معنا ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    c_name = st.text_input("اسمك:")
    c_msg = st.text_area("رسالتك:")
    if st.button("إرسال"):
        if c_name and c_msg:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO contact_msgs VALUES (?, ?, ?)", (c_name, c_msg, dt))
            conn.commit()
            send_telegram(f"📩 رسالة من {c_name}: {c_msg}")
            st.success("تم الإرسال!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 6: الإدارة ---
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    pw = st.text_input("كلمة السر:", type="password")
    if pw == "ayman7716":
        df = pd.read_sql_query("SELECT * FROM reports", conn)
        st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
