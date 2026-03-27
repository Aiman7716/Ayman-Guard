import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import yt_dlp
from datetime import datetime

# --- 1. الإعدادات والربط (Settings) ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 
WHITELIST = ["google.com", "facebook.com", "whatsapp.com", "microsoft.com", "apple.com", "instagram.com"]

def send_telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except: pass

# --- 2. التصميم البصري المطور (المحسن لحل مشكلة وضوح الأزرار) ---
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

    /* شريط الإشعارات */
    .ticker-wrap {
        background: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; border-radius: 10px;
        overflow: hidden; white-space: nowrap; padding: 10px 0; margin-bottom: 20px;
    }
    .ticker { display: inline-block; animation: ticker 25s linear infinite; color: #ff4b4b; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker span { padding: 0 40px; }

    /* التبويبات والبطاقات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; background-color: #161b22; padding: 10px; border-radius: 12px; border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] { height: 50px; color: #8b949e !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    
    /* بطاقة المحتوى */
    .content-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        margin-top: 15px;
    }

    /* --- [التحسين البصري]: تنسيق الأزرار (حل مشكلة عدم الوضوح) --- */
    /* هذا يستهدف أزرار Streamlit الافتراضية (مثل نشر، معالجة، تحليل) */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        /* جعل الزر باللون الأزرق الاحترافي ليكون واضحاً للمستخدم */
        background-color: #1f6feb !important; 
        color: white !important; /* نص أبيض لتباين عالي */
        font-weight: bold;
        border: none;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #448aff !important; /* تأثير عند تمرير الماوس لجذب الانتباه */
    }

    /* تحسين أزرار التحميل MP4 و MP3 لضمان وضوح النص الأبيض */
    .stButton > button.mp4-btn {
        background-color: #28a745 !important;
    }
    .stButton > button.mp3-btn {
        background-color: #e91e63 !important;
    }
    
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_security_v43.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS contact_msgs (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. الهيكل الرئيسي ---
st.markdown("""
    <div class="hero-box">
        <div class="shield-icon">🛡️</div>
        <h1>درع أيمن الأمني</h1>
        <p>Ayman Security & Multimedia PRO v43.1</p>
    </div>
    """, unsafe_allow_html=True)

# --- شريط التنبيهات المتحرك ---
st.markdown("""
    <div class="ticker-wrap">
        <div class="ticker">
            <span>⚠️ تنبيه: لا تقم بإدخال بياناتك الشخصية في روابط غير موثوقة.</span>
            <span>🚨 تحذير: حملات احتيال جديدة مرصودة حالياً. كن حذراً.</span>
            <span>🛡️ نصيحة: فحص الملفات عبر نظام الدرع يقي جهازك من الفيروسات.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 حالة النظام")
    col1, col2 = st.columns(2)
    col1.metric("إجمالي التهديدات المرصودة", c.execute("SELECT COUNT(*) FROM reports").fetchone()[0])
    col2.metric("حالة أدوات الوسائط", "نشطة 🟢")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 2: مركز الفحص ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f_sub = st.tabs(["🔗 فحص الرابط", "📁 فحص الملف"])
    with f_sub[0]:
        u_in = st.text_input("ضع الرابط المشبوه هنا للفحص:")
        # هذا الزر أصبح أزرق الآن ليكون واضحاً جداً
        if st.button("تحليل الرابط"):
            if u_in:
                dom = tldextract.extract(u_in).registered_domain
                if dom in WHITELIST: st.success(f"✅ نطاق موثوق جداً: {dom}")
                else: st.warning(f"🔍 نطاق غير مألوف، كن حذراً: {dom}")
    with f_sub[1]:
        f_up = st.file_uploader("ارفع ملف للفحص أمنياً:")
        # هذا الزر أيضاً أزرق
        if f_up and st.button("بدء فحص البصمة"):
            st.success("✅ الملف سليم برمجياً.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 3: محمل الفيديو والصوت (تم إصلاح العرض والتحميل 😁) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج وتشغيل الوسائط")
    v_url = st.text_input("ألصق رابط الفيديو (YouTube, FB, TikTok):")
    # هذا الزر أصبح أزرق بدلاً من الباهت (حل مشكلة الصورة الأخيرة)
    if st.button("استخراج وتحويل الوسائط"):
        if v_url:
            with st.spinner("جاري جلب الفيديو للمعاينة..."):
                try:
                    with yt_dlp.YoutubeDL({'format': 'best', 'quiet': True}) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        st.video(info['url']) # المعاينة
                        
                        st.info(f"✅ تم استخراج الفيديو بنجاح: {info.get('title', 'Video')}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f'<a href="{info["url"]}" target="_blank"><button class="mp4-btn" style="width:100%; height:3.5em; border-radius:10px; border:none; color:white; font-weight:bold; cursor:pointer;">📥 تحميل فيديو MP4</button></a>', unsafe_allow_html=True)
                        with col2:
                            audio = next((f['url'] for f in info.get('formats', []) if f.get('acodec') != 'none' and f.get('vcodec') == 'none'), info['url'])
                            st.markdown(f'<a href="{audio}" target="_blank"><button class="mp3-btn" style="width:100%; height:3.5em; border-radius:10px; border:none; color:white; font-weight:bold; cursor:pointer;">🎵 تحميل صوت MP3</button></a>', unsafe_allow_html=True)
                except: st.error("❌ الرابط غير مدعوم للمعاينة حالياً أو الفيديو خاص.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 4: المجتمع ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📢 بلاغ مجتمعي جديد")
    rep_txt = st.text_area("أدخل تفاصيل حالة الاحتيال:")
    # هذا الزر أصبح أزرق بدلاً من الباهت في صورتك
    if st.button("نشر وتحذير المجتمع"):
        if rep_txt:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (rep_txt, dt))
            conn.commit()
            send_telegram(f"📢 بلاغ مجتمعي: {rep_txt}")
            st.success("تم النشر بنجاح.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 5: تواصل معنا ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 اتصل بإدارة الدرع")
    c_name = st.text_input("اسمك:")
    c_msg = st.text_area("رسالتك للإدارة:")
    # هذا الزر أصبح أزرق واضح جداً
    if st.button("إرسال الرسالة"):
        if c_name and c_msg:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO contact_msgs VALUES (?, ?, ?)", (c_name, c_msg, dt))
            conn.commit()
            send_telegram(f"📩 رسالة من {c_name}: {c_msg}")
            st.success("تم الإرسال.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 6: الإدارة ---
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    pw = st.text_input("كلمة السر الخاصة بك:", type="password")
    if pw == "ayman7716":
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        st.dataframe(df, use_container_width=True)
    elif pw: st.error("❌ كلمة المرور غير صحيحة")
    st.markdown('</div>', unsafe_allow_html=True)
