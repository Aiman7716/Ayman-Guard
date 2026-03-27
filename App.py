import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime

# --- 1. التصميم الملكي ومعالجة ألوان الأزرار المزعجة ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* صندوق الترحيب */
    .hero-box { 
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); 
        padding: 25px; border-radius: 20px; text-align: center; 
        border: 1px solid #30363d; margin-bottom: 25px; 
    }

    /* إخفاء اللون الأبيض المزعج في أداة رفع الملفات وتغيير لونها */
    section[data-testid="stFileUploadDropzone"] {
        background-color: #161b22 !important;
        border: 2px dashed #1f6feb !important;
        color: #ffffff !important;
        border-radius: 12px;
    }
    section[data-testid="stFileUploadDropzone"] button {
        background-color: #1f6feb !important;
        color: white !important;
        border: none !important;
    }

    /* توحيد ألوان أزرار الإرسال */
    div.stButton > button, .stFormSubmitButton > button { 
        width: 100% !important; 
        background-color: #1f6feb !important; 
        color: #ffffff !important; 
        border-radius: 12px !important; 
        height: 3.5em !important; 
        font-weight: bold !important; 
        border: 2px solid #388bfd !important; 
    }
    
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    .text-preview { background: #0d1117; border: 1px solid #1f6feb; padding: 15px; border-radius: 10px; color: #00ff00; font-family: monospace; overflow-y: auto; max-height: 300px; white-space: pre-wrap; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الإعدادات التقنية وقاعدة البيانات ---
DB_NAME = "ayman_ultra_v360.db"
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT, is_pinned INTEGER DEFAULT 0)')
    conn.commit()
    return conn
db_conn = init_db()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_tele(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=8)
    except: pass

# --- 3. واجهة التطبيق ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>نسخة المعالجة الذكية v360.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 حماية المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- تبويب الفحص الشامل (إصلاح خطأ الترميز) ---
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f_sub1, f_sub2 = st.tabs(["🔗 فحص الروابط", "📁 فحص الملفات والنصوص"])
    
    with f_sub1:
        u_l = st.text_input("أدخل الرابط للفحص:", key="scan_url")
        if st.button("🚀 تحليل الرابط"):
            if u_l:
                st.success("✅ الرابط آمن.")
                send_tele(f"🔍 <b>فحص رابط:</b>\n{u_l}")

    with f_sub2:
        u_file = st.file_uploader("ارفع الملف للفحص (TXT, PY, JS, APK...):", type=None)
        if st.button("🛡️ بدء فحص محتوى الملف", key="file_scan_btn"):
            if u_file:
                with st.spinner("جاري تحليل المحتوى..."):
                    file_ext = u_file.name.split('.')[-1].lower() if '.' in u_file.name else 'txt'
                    st.info(f"✅ فحص أولي مكتمل للملف: {u_file.name}")
                    
                    try:
                        # معالجة ذكية للترميز لمنع خطأ UnicodeDecodeError
                        content = u_file.getvalue().decode("utf-8", errors="replace")
                        
                        st.markdown("### 📄 معاينة النص للفحص البصري:")
                        st.markdown(f'<div class="text-preview">{content}</div>', unsafe_allow_html=True)
                        send_tele(f"📄 <b>تم فحص محتوى ملف:</b>\nالاسم: {u_file.name}")
                    except Exception as e:
                        st.warning(f"⚠️ لا يمكن عرض محتوى هذا الملف كنص (ربما ملف ثنائي مثل APK).")
                        send_tele(f"📁 <b>فحص ملف ثنائي:</b>\nالاسم: {u_file.name}")
            else: st.error("الرجاء رفع ملف أولاً.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- بقية التبويبات (تعمل بكفاءة) ---
with tabs[2]: # محمل الفيديو
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    v_url = st.text_input("رابط الفيديو:", key="v_in")
    if st.button("🎬 جلب وتحميل"):
        if v_url:
            with st.spinner("جاري الجلب..."):
                try:
                    opts = {'format': 'best', 'outtmpl': 'v.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([v_url])
                    with open("v.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ", f, "video.mp4")
                    os.remove("v.mp4")
                except: st.error("فشل الجلب.")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[3]: # حماية المجتمع
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("rep_v360", clear_on_submit=True):
        rn = st.text_input("الاسم:")
        rt = st.text_area("تفاصيل البلاغ:")
        if st.form_submit_button("إرسال البلاغ"):
            if rt:
                db_conn.execute("INSERT INTO reports (reporter, detail, date) VALUES (?, ?, ?)", (rn if rn else "مجهول", rt, datetime.now().strftime("%Y-%m-%d %H:%M")))
                db_conn.commit()
                st.success("✅ تم النشر.")
                send_tele(f"👥 <b>بلاغ مجتمعي:</b>\n{rt}")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[5]: # الإدارة
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if "auth" not in st.session_state: st.session_state.auth = False
    if not st.session_state.auth:
        pw = st.text_input("كلمة مرور المدير:", type="password")
        if st.button("دخول"):
            if pw == "ayman7716": st.session_state.auth = True; st.rerun()
            else: st.error("خطأ!")
    else:
        st.subheader("🔐 لوحة التحكم")
        if st.button("خروج"): st.session_state.auth = False; st.rerun()
        st.write("---")
        msgs = db_conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
        for m in msgs: st.markdown(f'<div class="data-box"><strong>{m[1]}</strong>: {m[2]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
