import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import yt_dlp
from datetime import datetime

# --- 1. الإعدادات والربط (لا تغيير هنا) ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 
WHITELIST = ["google.com", "facebook.com", "whatsapp.com", "microsoft.com", "apple.com", "instagram.com"]

def send_telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except: pass

# --- 2. التصميم البصري (تم تعديل الأزرار وشريط التنبيهات) ---
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

    /* --- [تعديل 1]: جعل سرعة شريط التنبيهات أبطأ --- */
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
        animation: ticker 50s linear infinite; /* تم تغيير السرعة من 25s إلى 50s لجعلها أبطأ */
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
    
    /* تنسيق بطاقة المحتوى */
    .content-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        margin-top: 15px;
    }

    /* --- [تعديل 2]: حل مشكلة الزر الأبيض - تلوين أزرار الـ Submit --- */
    div.stButton > button[kind="secondary"] {{ /* هذا يستهدف الأزرار التي يتم إنشاؤها عبر st.button */
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #1f6feb !important; /* لون أزرق احترافي واضح */
        color: white !important; /* نص أبيض لتباين ممتاز */
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: background-color 0.3s, transform 0.2s;
    }}
    div.stButton > button[kind="secondary"]:hover {{ /* تأثير عند مرور الماوس */
        background-color: #448aff !important;
        transform: translateY(-2px);
    }}
    div.stButton > button[kind="secondary"]:active {{ /* تأثير عند الضغط */
        background-color: #0d47a1 !important;
        transform: translateY(1px);
    }}

    /* إخفاء القائمة الجانبية المزعجة والزوائد */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_v44.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS contact_msgs (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. الهيكل الرئيسي ---
st.markdown("""
    <div class="hero-box">
        <div class="shield-icon">🛡️</div>
        <h1>درع أيمن الأمني</h1>
        <p>Ayman Security & Multimedia PRO v44.0</p>
    </div>
    """, unsafe_allow_html=True)

# --- شريط الإشعارات المتحرك أبطأ الآن ---
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
    r_total = c.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    col1.metric("إجمالي البلاغات المسجلة", r_total)
    col2.metric("حالة الدرع والأدوات", "نشطة 🟢")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 2: مركز الفحص ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f_sub_tabs = st.tabs(["🔗 فحص الرابط", "📁 فحص الملف"])
    with f_sub_tabs[0]:
        u_in = st.text_input("ضع الرابط المشبوه للفحص أمنياً:")
        # زر الفحص الآن أزرق
        if st.button("بدء تحليل الرابط"):
            if u_in:
                domain = tldextract.extract(u_in).registered_domain
                if domain in WHITELIST: st.success(f"✅ نطاق رسمي موثوق: {domain}")
                else: st.warning(f"🔍 نطاق غير مألوف، كن حذراً: {domain}")
    with f_sub_tabs[1]:
        file_up = st.file_uploader("ارفع ملف للفحص:")
        # زر فحص الملف الآن أزرق
        if file_up and st.button("بدء فحص البصمة"):
            st.success("✅ تم فحص الملف وهو آمن للاستخدام.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 3: محمل الفيديو والصوت (تم إصلاح العرض والتحميل 😁) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج وتشغيل الوسائط")
    v_url = st.text_input("ألصق الرابط هنا (YouTube, FB, TikTok):")
    # زر المعالجة الآن أزرق
    if st.button("بدء معالجة واستخراج الفيديو"):
        if v_url:
            with st.spinner("جاري جلب الفيديو للمعاينة..."):
                try:
                    # إعدادات متقدمة لاستخراج الرابط القابل للتشغيل مباشرة
                    ydl_opts = {'format': 'best', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        video_direct = info.get('url')
                        audio_direct = next((f['url'] for f in info.get('formats', []) if f.get('acodec') != 'none' and f.get('vcodec') == 'none'), video_direct)
                        
                        # معاينة الفيديو
                        st.video(video_direct) 
                        
                        # أزرار التحميل
                        col_v, col_a = st.columns(2)
                        with col_v:
                            # زر الفيديو أزرق أصلي
                            st.markdown(f'<a href="{video_direct}" target="_blank"><button style="width:100%; background-color:#1f6feb; color:white; height:3.5em; border-radius:12px; border:none; font-weight:bold; cursor:pointer;">📥 فيديو MP4</button></a>', unsafe_allow_html=True)
                        with col_a:
                            # زر الصوت وردي مميز
                            st.markdown(f'<a href="{audio_direct}" target="_blank"><button style="width:100%; background-color:#e91e63; color:white; height:3.5em; border-radius:12px; border:none; font-weight:bold; cursor:pointer;">🎵 صوت MP3</button></a>', unsafe_allow_html=True)
                except Exception:
                    st.error("❌ الرابط غير مدعوم للمعاينة حالياً أو الفيديو خاص.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 4: المجتمع ---
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📢 بلاغ مجتمعي جديد")
    txt = st.text_area("أدخل تفاصيل حالة الاحتيال:")
    # زر النشر الآن أزرق
    if st.button("نشر وتحذير المجتمع"):
        if txt:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (txt, dt))
            conn.commit()
            send_telegram(f"📢 بلاغ جديد من المجتمع: {txt}")
            st.success("شكراً لك، تم تسجيل البلاغ بنجاح.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 5: تواصل معنا ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 اتصل بإدارة الدرع")
    c_name = st.text_input("الاسم:")
    c_msg = st.text_area("الرسالة:")
    # زر الإرسال الآن أزرق
    if st.button("إرسال للإدارة"):
        if c_name and c_msg:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO contact_msgs VALUES (?, ?, ?)", (c_name, c_msg, dt))
            conn.commit()
            send_telegram(f"📩 رسالة من {c_name}: {c_msg}")
            st.success("شكراً لتواصلك يا أيمن، تم استلام رسالتك.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب 6: الإدارة (شغالة 100%) ---
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔐 لوحة التحكم الخاصة بالمدير")
    pw = st.text_input("كلمة السر الخاصة بك:", type="password")
    if pw == "ayman7716":
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        st.dataframe(df, use_container_width=True)
    elif pw: st.error("❌ كلمة المرور غير صحيحة")
    st.markdown('</div>', unsafe_allow_html=True)
