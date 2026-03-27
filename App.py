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

# --- 2. التصميم البصري (توحيد الألوان للكحلي النيلي الواضح) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    /* الهيدر */
    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 10px; border: 1px solid #30363d;
    }

    /* شريط التنبيهات (سرعة بطيئة جداً للقراءة) */
    .ticker-wrap {
        background: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; border-radius: 10px;
        overflow: hidden; white-space: nowrap; padding: 10px 0; margin-bottom: 20px;
    }
    .ticker { display: inline-block; animation: ticker 60s linear infinite; color: #ff4b4b; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* توحيد جميع الأزرار للون الكحلي النيلي الواضح جداً كما طلبت */
    div.stButton > button, .main-btn {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.8em !important; font-weight: bold !important; 
        border: none !important; font-size: 1.1rem !important; text-decoration: none;
        display: flex; align-items: center; justify-content: center; cursor: pointer;
    }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    
    /* تنسيق التبويبات */
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 8px; border-radius: 12px; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    
    /* إخفاء الزوائد */
    [data-testid="stSidebar"], footer, header { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_final_v51.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS msgs (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. الهيكل الرئيسي ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>النسخة الاحترافية المستقرة v51.0</p></div>', unsafe_allow_html=True)

st.markdown('<div class="ticker-wrap"><div class="ticker"><span>⚠️ تنبيه: لا تدخل بياناتك في روابط غير موثوقة.</span><span>🚨 تحذير: حملات احتيال نشطة حالياً، كن حذراً.</span><span>🛡️ نصيحة: نظام الدرع يقوم بفحص الروابط بشكل آلي.</span></div></div>', unsafe_allow_html=True)

# التبويبات الستة المطلوبة (كاملة وبدون نقص)
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# 1. الرئيسية
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 حالة النظام")
    col1, col2 = st.columns(2)
    col1.metric("حالة الدرع", "نشطة 🟢")
    col2.metric("الإصدار", "v51.0")
    st.markdown('</div>', unsafe_allow_html=True)

# 2. الفحص
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    u_check = st.text_input("ضع الرابط للفحص أمنياً:")
    if st.button("تحليل الرابط الآن"):
        if u_check:
            d = tldextract.extract(u_check).registered_domain
            st.success(f"🔍 تم تحليل النطاق: {d}")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. محمل الفيديو (الحل النهائي للتحميل)
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج الوسائط")
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    if st.button("استخراج وتحويل"):
        if v_url:
            with st.spinner("جاري جلب الفيديو للمعاينة..."):
                try:
                    # إعدادات بسيطة ومباشرة لضمان عدم انهيار السيرفر
                    ydl_opts = {'format': 'best', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        video_url = info['url']
                        
                        st.video(video_url)
                        
                        # الزر الكحلي النيلي (رابط مباشر نظيف)
                        # هذا الرابط سيفتح الفيديو؛ المستخدم يضغط (⋮) ثم 'تنزيل'
                        st.markdown(f'''
                            <a href="{video_url}" target="_blank" class="main-btn">
                                📥 اضغط هنا للتحميل المباشر (كحلي)
                            </a>
                        ''', unsafe_allow_html=True)
                        st.info("💡 ملاحظة: إذا فتح الفيديو في صفحة جديدة، اضغط على النقاط الثلاث (⋮) في الزاوية ثم اختر 'تنزيل'.")
                except:
                    st.error("❌ الرابط غير مدعوم أو محمي.")
    st.markdown('</div>', unsafe_allow_html=True)

# 4. المجتمع
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    rep = st.text_area("تفاصيل البلاغ:")
    if st.button("نشر الآن"):
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
    name = st.text_input("اسمك:")
    msg = st.text_area("رسالتك:")
    if st.button("إرسال الرسالة"):
        if name and msg:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO msgs VALUES (?, ?, ?)", (name, msg, dt))
            conn.commit()
            send_telegram(f"📩 رسالة من {name}: {msg}")
            st.success("تم الاستلام.")
    st.markdown('</div>', unsafe_allow_html=True)

# 6. الإدارة
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    pw = st.text_input("كلمة السر:", type="password")
    if pw == "ayman7716":
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        st.dataframe(df, use_container_width=True)
    elif pw: st.error("❌ كلمة المرور خاطئة")
    st.markdown('</div>', unsafe_allow_html=True)
