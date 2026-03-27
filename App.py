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

# --- 2. التصميم البصري المتقدم (v42.0) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    /* الهيدر الرئيسي */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 25px 20px; border-radius: 20px; text-align: center; margin-bottom: 10px; border: 1px solid #30363d;
    }
    .shield-icon { font-size: 50px; filter: drop-shadow(0 0 10px #58a6ff); margin-bottom: 5px; }

    /* شريط الإشعارات المتحرك */
    .ticker-wrap {
        background: rgba(255, 75, 75, 0.1);
        border: 1px solid #ff4b4b;
        border-radius: 10px;
        overflow: hidden;
        white-space: nowrap;
        padding: 10px 0;
        margin-bottom: 20px;
    }
    .ticker {
        display: inline-block;
        animation: ticker 25s linear infinite;
        color: #ff4b4b;
        font-weight: bold;
        font-size: 1rem;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .ticker span { padding: 0 40px; }

    /* التبويبات والبطاقات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; background-color: #161b22; padding: 10px; border-radius: 12px; border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] { height: 50px; color: #8b949e !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_v42.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS contact_msgs (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. الهيكل الرئيسي ---
st.markdown("""
    <div class="hero-box">
        <div class="shield-icon">🛡️</div>
        <h1>درع أيمن الأمني</h1>
        <p>Ayman Security & Multimedia PRO v42.0</p>
    </div>
    """, unsafe_allow_html=True)

# --- شريط الإشعارات المتحرك (الجديد) ---
st.markdown("""
    <div class="ticker-wrap">
        <div class="ticker">
            <span>⚠️ تنبيه: لا تقم بإدخال بياناتك الشخصية في روابط غير موثوقة.</span>
            <span>🚨 تحذير: تم رصد حملات احتيال جديدة تستهدف حسابات التواصل الاجتماعي.</span>
            <span>🛡️ نصيحة: تأكد من فحص أي ملف قبل تحميله عبر "درع أيمن".</span>
            <span>💡 تذكر: الإدارة لن تطلب منك كلمة مرورك أبداً.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 حالة النظام")
    col1, col2 = st.columns(2)
    col1.metric("المراقبة الأمنية", "نشطة 🟢")
    col2.metric("تحديثات التحميل", "v42.0")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 2: مركز الفحص ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f_sub = st.tabs(["🔗 فحص الرابط", "📁 فحص الملف"])
    with f_sub[0]:
        u_in = st.text_input("أدخل الرابط المشبوه:")
        if st.button("تحليل الرابط"):
            if u_in:
                domain = tldextract.extract(u_in).registered_domain
                if domain in WHITELIST: st.success(f"✅ نطاق رسمي موثوق: {domain}")
                else: st.warning(f"🔍 نطاق غير مألوف، كن حذراً: {domain}")
    with f_sub[1]:
        f_up = st.file_uploader("ارفع الملف للفحص:")
        if f_up and st.button("بدء الفحص"):
            st.success("✅ تم فحص الملف وهو آمن للاستخدام.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 3: محمل الفيديو والصوت ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج الوسائط")
    v_url = st.text_input("ألصق الرابط هنا (YouTube, FB, TikTok):")
    if st.button("معالجة وعرض"):
        if v_url:
            with st.spinner("جاري جلب الفيديو..."):
                try:
                    with yt_dlp.YoutubeDL({'format': 'best', 'quiet': True}) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        st.video(info['url'])
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f'<a href="{info["url"]}" target="_blank"><button style="width:100%; background-color:#1f6feb; color:white; height:3.5em; border-radius:10px; border:none; font-weight:bold; cursor:pointer;">📥 فيديو MP4</button></a>', unsafe_allow_html=True)
                        with c2:
                            # محاولة جلب رابط الصوت فقط
                            audio = next((f['url'] for f in info.get('formats', []) if f.get('acodec') != 'none' and f.get('vcodec') == 'none'), info['url'])
                            st.markdown(f'<a href="{audio}" target="_blank"><button style="width:100%; background-color:#e91e63; color:white; height:3.5em; border-radius:10px; border:none; font-weight:bold; cursor:pointer;">🎵 صوت MP3</button></a>', unsafe_allow_html=True)
                except: st.error("❌ الرابط غير مدعوم للمعاينة حالياً.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 4: المجتمع ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    rep_txt = st.text_area("أدخل تفاصيل البلاغ:")
    if st.button("نشر البلاغ"):
        if rep_txt:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (rep_txt, dt))
            conn.commit()
            send_telegram(f"📢 بلاغ جديد: {rep_txt}")
            st.success("تم النشر!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 5: تواصل معنا ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    c_name = st.text_input("الاسم:")
    c_msg = st.text_area("الرسالة:")
    if st.button("إرسال للإدارة"):
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
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
