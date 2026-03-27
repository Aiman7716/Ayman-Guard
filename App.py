import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. التصميم السيادي المتقدم ---
st.set_page_config(page_title="Ayman Guard Pro v14", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d; }
    /* جعل الأزرار بارزة دائماً */
    div.stButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; height: 3.8em !important; font-weight: bold !important; border: 1px solid #58a6ff !important; }
    .stTextInput > div > div > input { background-color: #161b22 !important; color: white !important; border: 1px solid #30363d !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الأمان وقواعد البيانات ---
DB_NAME = "ayman_ultra_v14.db"
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_to_telegram(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

db = init_db()

# إدارة الجلسة
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'temp_auth' not in st.session_state: st.session_state.temp_auth = None

# --- 3. الواجهة البرمجية ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن السيادي</h1><p>الإصدار v14.0 | استجابة فورية وأمان مطلق</p></div>', unsafe_allow_html=True)
tabs = st.tabs(["🔍 الفحص والمعاينة", "🎬 التحميل الذكي", "👥 حماية المجتمع", "📧 تواصل", "🔐 الإدارة"])

with tabs[0]: # الفحص والمعاينة (الأزرار ظاهرة دائماً)
    st.subheader("🔗 فحص الروابط والملفات")
    f_type = st.radio("هدف الفحص:", ["رابط موقع", "ملف محلي"], horizontal=True)
    
    if f_type == "رابط موقع":
        target_url = st.text_input("ألصق الرابط هنا:", placeholder="https://example.com")
        # الأزرار هنا خارج نطاق "if target_url" لتكون ظاهرة دائماً يا أيمن
        col1, col2 = st.columns(2)
        btn_check = col1.button("🛡️ ابدأ فحص الأمان")
        
        if btn_check:
            if target_url:
                try:
                    res = requests.get(target_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                    st.success(f"✅ الرابط نشط (كود الاستجابة: {res.status_code})")
                    send_to_telegram(f"🔍 فحص رابط: {target_url}")
                except: st.error("❌ تعذر الوصول للرابط أو أنه محمي.")
            else: st.warning("الرجاء لصق رابط أولاً.")

        # زر المعاينة المباشرة (حل مشكلة الوجه الحزين)
        if target_url:
            st.markdown(f'''
                <a href="{target_url}" target="_blank">
                    <button style="width:100%; background-color:#238636; color:white; border:none; padding:15px; border-radius:10px; cursor:pointer; font-weight:bold; margin-top:10px;">
                        👁️ عرض ومعاينة الرابط في صفحة مستقلة آمنة
                    </button>
                </a>
            ''', unsafe_allow_html=True)
    else:
        u_file = st.file_uploader("ارفع الملف للفحص:")
        if u_file and st.button("🔍 تحليل الكود"):
            st.code(u_file.getvalue().decode("latin-1", errors="replace")[:1500])

with tabs[1]: # التحميل الصامت المحسن
    v_link = st.text_input("رابط الفيديو (Facebook/YouTube):")
    btn_dl = st.button("🚀 جلب وتحميل")
    if btn_dl:
        if v_link:
            with st.spinner(" "): 
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'ayman.mp4', 'quiet': True, 'user_agent': 'Mozilla/5.0'}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_link])
                    with open("ayman.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ في الجهاز", f, "video.mp4")
                    os.remove("ayman.mp4")
                except: st.error("⚠️ الرابط قد يكون خاصاً أو محمياً.")
        else: st.warning("ألصق الرابط أولاً.")

with tabs[2]: # حماية المجتمع
    with st.form("community"):
        rep_n, rep_d = st.text_input("اسمك:"), st.text_area("وصف التهديد:")
        if st.form_submit_button("🚨 إرسال البلاغ فوراً"):
            db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?,?,?)", (rep_n, rep_d, datetime.now().strftime("%Y-%m-%d")))
            db.commit(); st.success("تم التوثيق"); send_to_telegram(f"🚨 بلاغ: {rep_d}")

with tabs[4]: # الإدارة والمصادقة (طلبك الأساسي)
    if not st.session_state.logged_in:
        st.subheader("🔐 الدخول للنظام")
        admin_pwd = st.text_input("كلمة المرور:", type="password")
        if admin_pwd == "ayman7716":
            # زر تسجيل الدخول
            if st.button("👤 تسجيل الدخول (إرسال كود تليجرام)"):
                st.session_state.temp_auth = str(random.randint(1000, 9999))
                send_to_telegram(f"🔐 كود الدخول الخاص بك يا أيمن: <b>{st.session_state.temp_auth}</b>")
                st.info("تفقد التليجرام الآن.")
            
            if st.session_state.temp_auth:
                input_code = st.text_input("أدخل كود التحقق:")
                if st.button("🔓 تأكيد"):
                    if input_code == st.session_state.temp_auth:
                        st.session_state.logged_in = True; st.rerun()
                    else: st.error("الكود غير صحيح.")
    else:
        st.subheader("⚙️ لوحة تحكم أيمن")
        if st.button("🔴 خروج آمن"): st.session_state.logged_in = False; st.rerun()
        # عرض الرسائل والبلاغات
        for r in db.execute("SELECT * FROM reports ORDER BY id DESC").fetchall(): st.warning(f"🚨 {r[1]}: {r[2]}")
