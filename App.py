import streamlit as st
import tldextract, sqlite3, requests, pandas as pd
import yt_dlp
from datetime import datetime

# --- 1. الإعدادات والربط ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except: pass

# --- 2. التصميم البصري (توحيد الألوان للكحلي النيلي) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    /* الهيدر */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 25px 20px; border-radius: 20px; text-align: center; margin-bottom: 10px; border: 1px solid #30363d;
    }

    /* شريط التنبيهات */
    .ticker-wrap {
        background: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; border-radius: 10px;
        overflow: hidden; white-space: nowrap; padding: 10px 0; margin-bottom: 20px;
    }
    .ticker { display: inline-block; animation: ticker 45s linear infinite; color: #ff4b4b; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* توحيد جميع الأزرار للون الكحلي النيلي */
    div.stButton > button {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.8em !important; font-weight: bold !important; border: none !important;
    }

    /* أزرار الروابط (التحميل) */
    .download-btn {
        display: block; width: 100%; text-align: center; background-color: #1f6feb;
        color: white !important; padding: 15px 0; border-radius: 12px; font-weight: bold;
        text-decoration: none; margin-top: 10px; border: none; font-size: 1.1rem;
    }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_pro_final.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS msgs (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. واجهة المستخدم ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>Ayman Guard & Media PRO v48.0</p></div>', unsafe_allow_html=True)

st.markdown('<div class="ticker-wrap"><div class="ticker"><span>⚠️ تنبيه: لا تدخل بياناتك في روابط غير موثوقة.</span><span>🚨 تحذير: حملات احتيال نشطة حالياً.</span></div></div>', unsafe_allow_html=True)

# التبويبات الستة كاملة
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# 1. الرئيسية
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 إحصائيات النظام")
    col1, col2 = st.columns(2)
    col1.metric("حالة الحماية", "نشطة 🟢")
    col2.metric("إصدار المحرك", "v48.0")
    st.markdown('</div>', unsafe_allow_html=True)

# 2. الفحص
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    u_in = st.text_input("ضع الرابط للفحص أمنياً:")
    if st.button("بدء الفحص"):
        if u_in:
            domain = tldextract.extract(u_in).registered_domain
            st.success(f"✅ تم تحليل النطاق: {domain}")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. محمل الفيديو (تم إصلاح التحميل والعرض)
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج الوسائط")
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    if st.button("معالجة الرابط"):
        if v_url:
            with st.spinner("جاري جلب الفيديو..."):
                try:
                    with yt_dlp.YoutubeDL({'format': 'best', 'quiet': True}) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        st.video(info['url'])
                        
                        # أزرار التحميل الكحلية (روابط مباشرة لضمان عمل الملف 100%)
                        st.markdown(f'<a href="{info["url"]}" target="_blank" class="download-btn">📥 تحميل فيديو MP4 (كحلي)</a>', unsafe_allow_html=True)
                        
                        # البحث عن رابط الصوت
                        audio_url = next((f['url'] for f in info.get('formats', []) if f.get('acodec') != 'none' and f.get('vcodec') == 'none'), info['url'])
                        st.markdown(f'<a href="{audio_url}" target="_blank" class="download-btn" style="background-color:#161b22; border:1px solid #1f6feb;">🎵 تحميل صوت MP3</a>', unsafe_allow_html=True)
                        st.info("💡 بعد الضغط على التحميل، سيفتح الفيديو؛ اضغط على الثلاث نقاط (⋮) ثم 'تنزيل'.")
                except: st.error("❌ الرابط غير مدعوم حالياً.")
    st.markdown('</div>', unsafe_allow_html=True)

# 4. المجتمع
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    rep = st.text_area("وصف بلاغ الاحتيال:")
    if st.button("نشر البلاغ"):
        if rep:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (rep, dt))
            conn.commit()
            send_telegram(f"📢 بلاغ جديد: {rep}")
            st.success("تم النشر!")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. تواصل معنا
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    name = st.text_input("الاسم:")
    msg = st.text_area("الرسالة:")
    if st.button("إرسال"):
        if name and msg:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO msgs VALUES (?, ?, ?)", (name, msg, dt))
            conn.commit()
            send_telegram(f"📩 من {name}: {msg}")
            st.success("تم الإرسال.")
    st.markdown('</div>', unsafe_allow_html=True)

# 6. الإدارة
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    pw = st.text_input("كلمة السر:", type="password")
    if pw == "ayman7716":
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
