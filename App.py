import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime

# --- 1. التصميم الداكن (إعدام اللون الأبيض نهائياً) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* صبغ منطقة الرفع باللون الكحلي الداكن جداً */
    section[data-testid="stFileUploadDropzone"] {
        background-color: #0d1117 !important;
        border: 2px solid #1f6feb !important;
        border-radius: 12px;
    }
    
    /* توحيد الأزرار باللون الأزرق النيلي الملكي */
    div.stButton > button, .stFormSubmitButton > button { 
        background-color: #1f6feb !important; 
        color: white !important; 
        border-radius: 10px !important;
        border: 1px solid #388bfd !important;
        font-weight: bold !important;
    }

    .info-box { background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 20px; }
    .code-view { background: #000; color: #00ff00; padding: 15px; border-radius: 10px; font-family: monospace; overflow-x: auto; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك الخلفي ---
DB_NAME = "ayman_core_final.db"
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS msgs (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, body TEXT, dt TEXT)')
    conn.commit()
    return conn

def notify_ayman(txt):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": txt, "parse_mode": "HTML"}, timeout=5)
    except: pass

db = init_db()

# --- 3. الواجهة ---
st.markdown('<div class="info-box" style="text-align:center;"><h1>🛡️ درع أيمن الأمني</h1><p>الإصدار المستقر v400.0</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🔍 الفحص الآمن", "🎬 المحمل الذكي", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويبات تعمل بمسارات معزولة لمنع الأخطاء ---

with tabs[0]: # فحص الملفات (علاج الشاشة الحمراء)
    st.write("### 📁 فحص الملفات والنصوص")
    u_file = st.file_uploader("ارفع أي ملف هنا (APK, TXT, etc):", type=None)
    if st.button("🚀 فحص الآن"):
        if u_file:
            st.success(f"تم استقبال الملف: {u_file.name}")
            # القراءة كبيانات خام (Hex) لمنع خطأ الـ Unicode نهائياً
            raw_data = u_file.getvalue()
            preview = str(raw_data[:300]) # عرض أول 300 حرف فقط كبيانات خام
            st.markdown("🔍 **معاينة البيانات الخام:**")
            st.markdown(f'<div class="code-view">{preview}</div>', unsafe_allow_html=True)
            notify_ayman(f"🔍 <b>فحص ملف:</b> {u_file.name}")
        else: st.error("يرجى رفع ملف أولاً.")

with tabs[1]: # تحميل الفيديو
    v_url = st.text_input("رابط الفيديو:")
    if st.button("🎬 جلب الفيديو"):
        if v_url:
            with st.spinner("جاري الجلب..."):
                try:
                    with yt_dlp.YoutubeDL({'format':'best','outtmpl':'ayman.mp4','quiet':True}) as ydl: ydl.download([v_url])
                    with open("ayman.mp4", "rb") as f: st.video(f.read())
                    os.remove("ayman.mp4")
                except: st.error("عذراً، الرابط غير مدعوم أو محمي.")

with tabs[2]: # تواصل معنا
    with st.form("contact", clear_on_submit=True):
        name = st.text_input("الاسم:")
        msg = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            if name and msg:
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                db.execute("INSERT INTO msgs (name, body, dt) VALUES (?, ?, ?)", (name, msg, now))
                db.commit()
                st.success("تم الإرسال بنجاح.")
                notify_ayman(f"📧 <b>رسالة من:</b> {name}\n{msg}")

with tabs[3]: # الإدارة
    pw = st.text_input("كلمة السر:", type="password")
    if pw == "ayman7716":
        st.subheader("📩 الرسائل المستلمة")
        rows = db.execute("SELECT * FROM msgs ORDER BY id DESC").fetchall()
        for r in rows:
            st.markdown(f"**من: {r[1]}** | {r[3]}\n\n{r[2]}\n---")
