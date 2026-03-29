import streamlit as st
import os
import sqlite3
import requests
import random
from datetime import datetime

# المحاولة الآمنة لاستيراد المكتبة لمنع خطأ الانهيار
try:
    import yt_dlp
except ImportError:
    os.system('pip install yt-dlp')
    import yt_dlp

# --- 1. التصميم الجمالي السيادي المتطور ---
st.set_page_config(page_title="Ayman Guard Ultra v20", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    .hero {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 30px; border-radius: 20px; text-align: center;
        margin-bottom: 25px; border: 1px solid #30363d;
    }
    
    /* الأزرار الزرقاء الاحترافية */
    div.stButton > button {
        width: 100% !important; background: #1f6feb !important;
        color: white !important; border-radius: 12px !important; height: 3.8em !important;
        font-weight: bold !important; border: 1px solid #58a6ff !important;
    }
    
    /* زر التنزيل الأخضر */
    .stDownloadButton>button {
        background-color: #238636 !important;
        height: 4.5em !important;
        font-size: 22px !important;
        border: 2px solid #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إعدادات المحرك وقاعدة البيانات ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
DB_NAME = "ayman_guard_v20.db"

def send_bot(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text}, timeout=5)
    except: pass

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS msgs (id INTEGER PRIMARY KEY, sender TEXT, content TEXT)')
        conn.commit()

init_db()

# إدارة تسجيل الدخول
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. بناء هيكل التبويبات (بشكل آمن جداً) ---
st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي - الترا</h1><p>الإصدار المصلح v20.0</p></div>', unsafe_allow_html=True)

# تعريف التبويبات في قائمة لضمان عدم حدوث NameError
tabs_list = ["🏠 الرئيسية", "🔍 الفحص", "🎬 التحميل", "📧 تواصل", "🔐 الإدارة"]
t = st.tabs(tabs_list)

with t[0]:
    st.markdown("<h2 style='text-align:center;'>أهلاً بك يا أيمن</h2>", unsafe_allow_html=True)
    st.info("تم إصلاح أخطاء التبويبات والمكتبات المفقودة بنجاح. ✅")

with t[1]:
    st.subheader("🔍 مركز فحص الروابط")
    url_test = st.text_input("أدخل الرابط للفحص:")
    if st.button("🛡️ فحص الرابط الآن"):
        try:
            r = requests.get(url_test, timeout=5)
            st.success(f"الرابط مستجيب وحالته: {r.status_code}")
            send_bot(f"🔍 فحص رابط: {url_test}")
        except: st.error("فشل الوصول للرابط!")

with t[2]:
    st.subheader("🎬 محمل الفيديو المتطور")
    video_url = st.text_input("ألصق رابط الفيديو (فيسبوك أو غيره):")
    if st.button("🚀 بدء المعالجة"):
        if video_url:
            with st.spinner("جاري كسر حماية الرابط..."):
                try:
                    f_name = "ayman_v.mp4"
                    # مسح الملف القديم إذا وجد لضمان عدم حدوث خطأ
                    if os.path.exists(f_name): os.remove(f_name)
                    
                    opts = {'format': 'best', 'outtmpl': f_name, 'quiet': True}
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        ydl.download([video_url])
                    
                    if os.path.exists(f_name):
                        with open(f_name, "rb") as f_data:
                            st.video(video_url)
                            st.download_button(label="📥 حفظ الفيديو في جهازك", data=f_data, file_name="ayman_shield.mp4", mime="video/mp4")
                        os.remove(f_name)
                        send_bot(f"🎬 نجاح تحميل فيديو")
                except Exception as e:
                    st.error(f"حدث خطأ: تأكد من الرابط أو افتحه في متصفح خارجي. ({e})")

with t[3]:
    with st.form("contact"):
        name = st.text_input("الاسم:")
        msg = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال 📧"):
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute("INSERT INTO msgs (sender, content) VALUES (?,?)", (name, msg))
            st.success("تم الإرسال!")
            send_bot(f"📩 رسالة من {name}: {msg}")

with t[4]:
    if not st.session_state.auth:
        p = st.text_input("كلمة السر:", type="password")
        if st.button("دخول"):
            if p == "ayman7716": st.session_state.auth = True; st.rerun()
    else:
        st.subheader("⚙️ لوحة التحكم")
        if st.button("خروج"): st.session_state.auth = False; st.rerun()
        with sqlite3.connect(DB_NAME) as conn:
            data = conn.execute("SELECT * FROM msgs ORDER BY id DESC").fetchall()
            for d in data: st.info(f"من {d[1]}: {d[2]}")
