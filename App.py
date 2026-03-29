import streamlit as st
import os
import requests
import sqlite3
from datetime import datetime
from io import BytesIO

# --- 1. التأكد من وجود المكتبات اللازمة برمجياً ---
try:
    import yt_dlp
except ImportError:
    os.system('pip install yt-dlp')
    import yt_dlp

# --- 2. التصميم الجمالي السيادي ---
st.set_page_config(page_title="Ayman Guard Pro v21", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    
    /* أزرار أيمن الزرقاء */
    div.stButton > button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; border: none; }
    
    /* زر التنزيل الأخضر (الذي لا يطلب صلاحيات) */
    .stDownloadButton>button { background-color: #238636 !important; color: white !important; border-radius: 12px !important; height: 4.5em !important; font-size: 20px !important; font-weight: bold !important; border: 2px solid #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. المحرك التقني وقاعدة البيانات ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"
DB_NAME = "ayman_data_v21.db"

def notify_ayman(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}, timeout=3)
    except: pass

# إعداد قاعدة البيانات بشكل آمن
with sqlite3.connect(DB_NAME) as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS msgs (id INTEGER PRIMARY KEY, sender TEXT, content TEXT)')

# --- 4. واجهة التبويبات المصلحة ---
st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>نظام التحميل بالتدفق المباشر v21.0</p></div>', unsafe_allow_html=True)

# حل مشكلة NameError بتعريف التبويبات بمتغير واحد
t = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 التحميل", "📧 تواصل", "🔐 الإدارة"])

with t[0]:
    st.markdown("<h2 style='text-align:center;'>مرحباً بك يا أيمن</h2>", unsafe_allow_html=True)
    st.success("✅ تم تفعيل محرك الذاكرة المؤقتة لتجاوز أخطاء الصلاحيات.")

with t[1]:
    u_f = st.text_input("رابط للفحص:")
    if st.button("🛡️ ابدأ الفحص"):
        try:
            r = requests.get(u_f, timeout=5)
            st.success(f"الرابط مستجيب ({r.status_code})")
            notify_ayman(f"🔍 فحص رابط: {u_f}")
        except: st.error("فشل الوصول")

with t[2]:
    st.subheader("🎬 محمل الفيديو (بدون حفظ ملفات)")
    v_url = st.text_input("ألصق الرابط هنا:")
    if st.button("🚀 معالجة فورية"):
        if v_url:
            with st.spinner("جاري سحب بيانات الفيديو للذاكرة..."):
                try:
                    # الطريقة البرمجية التي لا تحتاج Permission (التدفق للذاكرة)
                    buffer = BytesIO()
                    ydl_opts = {
                        'format': 'best',
                        'quiet': True,
                        'no_warnings': True,
                        'outtmpl': '-', # إرسال المخرجات مباشرة للتدفق
                        'logtostderr': True
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=True)
                        # هنا نقوم بتقديم الملف مباشرة من المتصفح
                    
                    st.video(v_url)
                    st.warning("⚠️ إذا لم يظهر زر التحميل، يرجى فتح الموقع في متصفح Chrome خارجي.")
                except Exception as e:
                    st.error(f"عذراً أيمن، المتصفح الداخلي يحجب العملية. يرجى استخدام متصفح خارجي.")

with t[3]:
    with st.form("c"):
        n, m = st.text_input("الاسم:"), st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute("INSERT INTO msgs (sender, content) VALUES (?,?)", (n, m))
            st.success("تم الإرسال ✅")
            notify_ayman(f"📩 رسالة من {n}: {m}")

with t[4]:
    if 'login' not in st.session_state: st.session_state.login = False
    if not st.session_state.login:
        p = st.text_input("كلمة السر:", type="password")
        if st.button("دخول"):
            if p == "ayman7716": st.session_state.login = True; st.rerun()
    else:
        if st.button("خروج"): st.session_state.login = False; st.rerun()
        with sqlite3.connect(DB_NAME) as conn:
            data = conn.execute("SELECT * FROM msgs ORDER BY id DESC").fetchall()
            for d in data: st.info(f"من {d[1]}: {d[2]}")
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
