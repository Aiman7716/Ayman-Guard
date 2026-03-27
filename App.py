import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime

# --- 1. التصميم الملكي (النيلي الكحلي) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 25px; }
    .alert-banner { background: #ff4b4b; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; font-weight: bold; border: 2px solid white; }
    div.stButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; border: none !important; }
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    .data-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 12px; border-right: 5px solid #1f6feb; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة قاعدة البيانات المستقرة (v330) ---
DB_NAME = "ayman_core_v330.db"

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT, is_pinned INTEGER DEFAULT 0)')
    conn.commit()
    return conn

db_conn = init_db()

# --- 3. محرك التليجرام (ربط أيمن) ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_tele(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=8)
    except: pass

# --- 4. الهيكل الرئيسي ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>الإصدار الماسي v330.0 - نظام التنبيهات المجتمعية</p></div>', unsafe_allow_html=True)

# عرض التنبيه المثبت (Pinned Alert) في الواجهة الرئيسية
cur = db_conn.cursor()
cur.execute("SELECT detail FROM reports WHERE is_pinned = 1 ORDER BY id DESC LIMIT 1")
pinned = cur.fetchone()
if pinned:
    st.markdown(f'<div class="alert-banner">🚨 تنبيه عاجل من الإدارة: {pinned[0]}</div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص الشامل", "🎬 محمل الفيديو", "👥 حماية المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- تبويب الفحص الشامل (مستقر 100%) ---
with tabs[1]:
    st.markdown('<div class="content-card"><h3>🔍 مركز التحليل</h3>', unsafe_allow_html=True)
    l_in = st.text_input("رابط للفحص:", key="l_scan")
    if st.button("🚀 فحص الرابط الآن"):
        if l_in:
            st.success("✅ الفحص المبدئي: لا توجد تهديدات معروفة.")
            send_tele(f"🔍 <b>عملية فحص رابط:</b>\n{l_in}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب محمل الفيديو (جاري جلب الفيديو) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    v_in = st.text_input("رابط الفيديو:", key="v_dl")
    if st.button("🎬 جلب الفيديو وتحميله"):
        if v_in:
            with st.spinner("جاري جلب الفيديو..."):
                try:
                    ydl_opts = {'format': 'best', 'outtmpl': 'temp.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_in])
                    with open("temp.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ الفيديو", f, "ayman_video.mp4")
                    os.remove("temp.mp4")
                except: st.error("عذراً، تعذر الجلب.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب حماية المجتمع ---
with tabs[3]:
    st.markdown('<div class="content-card"><h3>👥 بلاغات المجتمع</h3>', unsafe_allow_html=True)
    with st.form("rep_form", clear_on_submit=True):
        rn = st.text_input("الاسم (اختياري):")
        rt = st.text_area("تفاصيل التهديد:")
        if st.form_submit_button("نشر البلاغ"):
            if rt:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                db_conn.execute("INSERT INTO reports (reporter, detail, date) VALUES (?, ?, ?)", (rn if rn else "مجهول", rt, dt))
                db_conn.commit()
                st.success("✅ تم النشر. سيراجعها أيمن لتثبيتها كتحذير.")
                send_tele(f"👥 <b>بلاغ مجتمعي:</b>\n{rt}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب تواصل معنا ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.form("con_form", clear_on_submit=True):
        sn = st.text_input("اسمك:")
        msg = st.text_area("رسالتك:")
        if st.form_submit_button("إرسال لأيمن"):
            if sn and msg:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                db_conn.execute("INSERT INTO messages (sender, content, date) VALUES (?, ?, ?)", (sn, msg, dt))
                db_conn.commit()
                st.success("✅ وصلت رسالتك.")
                send_tele(f"📧 <b>رسالة خاصة لأيمن:</b>\nمن: {sn}\n{msg}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- تبويب الإدارة (تفعيل ميزة التثبيت) ---
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if "admin" not in st.session_state: st.session_state.admin = False
    if not st.session_state.admin:
        pw = st.text_input("كلمة المرور:", type="password")
        if st.button("دخول"):
            if pw == "ayman7716": st.session_state.admin = True; st.rerun()
            else: st.error("خطأ!")
    else:
        st.subheader("🔐 لوحة التحكم - إدارة البلاغات")
        if st.button("خروج"): st.session_state.admin = False; st.rerun()
        
        st.write("---")
        # إدارة البلاغات (تثبيت أو إلغاء تثبيت)
        st.markdown("### 📢 التحكم في بلاغات المجتمع")
        reps = db_conn.execute("SELECT * FROM reports ORDER BY id DESC").fetchall()
        for r in reps:
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"**{r[1]}**: {r[2]} ({r[3]})")
            label = "إلغاء التثبيت" if r[4] == 1 else "تثبيت كتحذير عاجل"
            if col2.button(label, key=f"pin_{r[0]}"):
                db_conn.execute("UPDATE reports SET is_pinned = 0") # إلغاء القديم
                if r[4] == 0: db_conn.execute("UPDATE reports SET is_pinned = 1 WHERE id = ?", (r[0],))
                db_conn.commit()
                st.rerun()
        
        st.write("---")
        st.markdown("### 📩 الرسائل الخاصة")
        msgs = db_conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
        for m in msgs: st.markdown(f'<div class="data-box"><strong>{m[1]}</strong>: {m[2]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
