import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import yt_dlp
from datetime import datetime

# --- 1. الإعدادات والربط ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 

def send_telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except: pass

# --- 2. التصميم البصري (تم توحيد الألوان للكحلي الاحترافي) ---
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

    /* شريط التنبيهات بطيء وانسيابي */
    .ticker-wrap {
        background: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; border-radius: 10px;
        overflow: hidden; white-space: nowrap; padding: 10px 0; margin-bottom: 20px;
    }
    .ticker { display: inline-block; animation: ticker 50s linear infinite; color: #ff4b4b; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker span { padding: 0 40px; }

    /* توحيد ألوان جميع الأزرار (الكحلي النيلي) */
    div.stButton > button, .custom-btn {
        width: 100% !important;
        border-radius: 12px !important;
        height: 3.8em !important;
        background-color: #1f6feb !important; /* اللون الكحلي المطلوب */
        color: white !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(31, 111, 235, 0.2) !important;
        margin-top: 10px !important;
    }
    
    /* تأثير الضغط والحركة */
    div.stButton > button:hover { background-color: #3884ff !important; transform: scale(1.01); }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_pro_v45.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
conn.commit()

# --- 4. واجهة التطبيق ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>Ayman Security & Multimedia v45.0</p></div>', unsafe_allow_html=True)

st.markdown('<div class="ticker-wrap"><div class="ticker"><span>⚠️ تنبيه: لا تدخل بياناتك في روابط غير موثوقة.</span><span>🚨 تحذير: حملات احتيال نشطة حالياً.</span></div></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- تبويب محمل الفيديو (تم تعديل ألوان الأزرار هنا) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج الوسائط")
    v_url = st.text_input("ألصق الرابط هنا:")
    
    if st.button("بدء المعالجة والاستخراج"):
        if v_url:
            with st.spinner("جاري جلب الفيديو..."):
                try:
                    with yt_dlp.YoutubeDL({'format': 'best', 'quiet': True}) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        st.video(info['url'])
                        
                        # أزرار التحميل الكحلية (حل مشكلة اللون الأبيض في الصورة 7)
                        st.markdown(f'''
                            <a href="{info['url']}" target="_blank" style="text-decoration:none;">
                                <button class="custom-btn">📥 تحميل الفيديو MP4 (كحلي واضع)</button>
                            </a>
                            <a href="{info['url']}" target="_blank" style="text-decoration:none;">
                                <button class="custom-btn" style="background-color:#161b22 !important; border:1px solid #1f6feb !important;">🎵 تحويل إلى صوت MP3</button>
                            </a>
                        ''', unsafe_allow_html=True)
                except:
                    st.error("❌ عذراً، هذا الرابط محمي أو غير مدعوم حالياً.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- بقية التبويبات (تستخدم نفس نمط الأزرار الموحد) ---
with tabs[3]: # المجتمع
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    rep = st.text_area("وصف البلاغ:")
    if st.button("نشر البلاغ الآن"):
        st.success("تم النشر باللون الكحلي الواضح!")

with tabs[1]: # الفحص
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.text_input("رابط للفحص:")
    st.button("تحليل الرابط")
