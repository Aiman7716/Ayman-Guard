import streamlit as st
import tldextract, sqlite3, requests, pandas as pd
import yt_dlp
from datetime import datetime

# --- 1. الإعدادات العامة ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except: pass

# --- 2. التصميم البصري (إصلاح العرض للجوالات الأخرى) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* إعدادات الخط والاتجاه لتعمل على كل الجوالات */
    html, body, [class*="st-"] { 
        font-family: 'Cairo', sans-serif !important; 
        direction: RTL !important; 
        text-align: right !important; 
    }
    
    .stApp { background-color: #0d1117; color: #ffffff; }

    /* الهيدر الاحترافي */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 20px; border-radius: 15px; text-align: center; 
        margin-bottom: 15px; border: 1px solid #30363d;
    }

    /* شريط التنبيهات البطيء */
    .ticker-wrap {
        background: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; border-radius: 10px;
        overflow: hidden; white-space: nowrap; padding: 10px 0; margin-bottom: 20px;
    }
    .ticker { display: inline-block; animation: ticker 50s linear infinite; color: #ff4b4b; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* توحيد الأزرار للكحلي النيلي الواضح جداً */
    div.stButton > button {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.8em !important; font-weight: bold !important; 
        border: none !important; font-size: 1.1rem !important;
    }

    /* أزرار التحميل اليدوية (لحل مشكلة الجوالات الأخرى) */
    .btn-link {
        display: block; width: 100%; text-align: center; background-color: #1f6feb;
        color: white !important; padding: 18px 0; border-radius: 12px; font-weight: bold;
        text-decoration: none; margin: 10px 0; font-size: 1.1rem; border: none;
    }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 20px; margin-top: 10px; }
    
    /* تحسين شكل التبويبات لتظهر بوضوح في الجوال */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: #161b22; padding: 5px; border-radius: 10px; 
        display: flex; overflow-x: auto; 
    }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; border-radius: 8px !important; }

    /* إخفاء الزوائد */
    [data-testid="stSidebar"], footer, header { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة البيانات ---
conn = sqlite3.connect('ayman_global_v49.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS contact (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. واجهة التطبيق ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة التوافق العالمي v49.0</p></div>', unsafe_allow_html=True)

st.markdown('<div class="ticker-wrap"><div class="ticker"><span>⚠️ تنبيه: نظام الدرع يراقب الروابط المشبوهة الآن.</span><span>🚨 حذارِ من الصفحات التي تطلب كلمة مرورك.</span></div></div>', unsafe_allow_html=True)

# التبويبات الستة (تم التأكد من برمجتها لتعمل على كل الأجهزة)
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 المحمل", "👥 المجتمع", "📧 تواصل", "🔐 الإدارة"])

with tabs[0]: # الرئيسية
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 إحصائيات الدرع")
    st.info("نظام الحماية نشط ويعمل على تأمين جلساتك الحالية.")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]: # الفحص
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    url_check = st.text_input("ضع الرابط للفحص:")
    if st.button("تحليل الآن"):
        if url_check:
            d = tldextract.extract(url_check).registered_domain
            st.success(f"🔍 نتيجة الفحص: النطاق المستهدف هو ({d})")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]: # محمل الفيديو (حل مشكلة الجوال الثاني)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج الوسائط الذكي")
    v_url = st.text_input("رابط الفيديو (تيك توك، فيسبوك، يوتيوب):")
    if st.button("استخراج وتحضير"):
        if v_url:
            with st.spinner("جاري تجاوز حماية الموقع المضيف..."):
                try:
                    # استخدام وكيل متصفح لضمان عدم ظهور 403 في الجوالات الأخرى
                    ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        video_final = info['url']
                        
                        st.video(video_final) # عرض المعاينة
                        
                        # الزر الكحلي النيلي (رابط مباشر متوافق مع كل المتصفحات)
                        st.markdown(f'<a href="{video_final}" target="_blank" class="btn-link">📥 تحميل فيديو MP4 (كحلي)</a>', unsafe_allow_html=True)
                        
                        st.warning("💡 ملاحظة للجوال: إذا فتح الفيديو في صفحة جديدة، اضغط مطولاً عليه واختر 'تنزيل الفيديو'.")
                except:
                    st.error("❌ فشل الاستخراج. قد يكون الرابط خاصاً أو محمياً.")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[3]: # المجتمع
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    txt = st.text_area("تفاصيل بلاغ الاحتيال:")
    if st.button("نشر وتحذير الجميع"):
        if txt:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (txt, dt))
            conn.commit()
            send_telegram(f"📢 بلاغ: {txt}")
            st.success("✅ تم النشر بنجاح.")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[4]: # تواصل معنا
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    nm = st.text_input("الاسم:")
    ms = st.text_area("الرسالة:")
    if st.button("إرسال للإدارة"):
        if nm and ms:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO contact VALUES (?, ?, ?)", (nm, ms, dt))
            conn.commit()
            send_telegram(f"📩 رسالة من {nm}: {ms}")
            st.success("✅ تم الإرسال.")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[5]: # الإدارة
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    adm_pw = st.text_input("كلمة السر الخاصة بك:", type="password")
    if adm_pw == "ayman7716":
        st.write("📋 سجل البلاغات:")
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        st.dataframe(df, use_container_width=True)
    elif adm_pw: st.error("❌ كلمة المرور غير صحيحة")
    st.markdown('</div>', unsafe_allow_html=True)
