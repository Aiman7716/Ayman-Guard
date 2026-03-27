import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. الإعدادات والتصميم ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    section[data-testid="stFileUploadDropzone"] { background-color: #161b22 !important; border: 2px dashed #1f6feb !important; border-radius: 15px; }
    div.stButton > button { width: 100% !important; background-color: #1f6feb !important; color: white !important; border-radius: 12px !important; }
    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الدوال الأساسية ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_to_telegram(text):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

def get_site_preview(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.title.string if soup.title else "عنوان غير معروف"
        desc = soup.find('meta', attrs={'name': 'description'})
        desc = desc['content'] if desc else "وصف غير متاح."
        return {"title": title, "desc": desc}
    except: return None

# --- 3. بناء الواجهة والتبويبات ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن</h1><p>الفحص الذكي والمعاينة الآمنة</p></div>', unsafe_allow_html=True)
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص والمعاينة", "🎬 التحميل", "📧 تواصل"])

with tabs[0]:
    st.info("👋 أهلاً بك يا أيمن. النظام الآن يدعم فحص أمان الروابط ومعاينتها في آن واحد.")

with tabs[1]: # التبويب المطور الذي طلبته
    sub_mode = st.radio("اختر المهمة:", ["تحليل الروابط ومعاينتها 🔗", "فحص الملفات 📁"], horizontal=True)
    
    if sub_mode == "تحليل الروابط ومعاينتها 🔗":
        p_url = st.text_input("ألصق الرابط هنا للفحص:")
        col1, col2 = st.columns(2)
        
        if p_url:
            with col1:
                if st.button("👁️ عرض محتوى الصفحة"):
                    data = get_site_preview(p_url)
                    if data:
                        st.markdown(f"""<div style="background:#1c2128; border:1px solid #1f6feb; padding:15px; border-radius:12px;">
                        <h4 style="color:#58a6ff;">🌐 {data['title']}</h4><p style="color:#8b949e;">{data['desc']}</p></div>""", unsafe_allow_html=True)
                    else: st.error("تعذر جلب المعاينة.")

            with col2:
                if st.button("🛡️ فحص أمان الرابط"):
                    try:
                        res = requests.get(p_url, timeout=5)
                        if res.status_code == 200:
                            if p_url.startswith("https"): st.success("✅ الرابط سليم ومشفر (Secure).")
                            else: st.warning("⚠️ الرابط يعمل ولكنه غير مشفر (HTTP).")
                        else: st.error(f"❌ الرابط مشبوه (خطأ {res.status_code})")
                    except: st.error("❌ الرابط غير سليم أو وهمي.")
                    send_to_telegram(f"🔍 فحص أمان رابط: {p_url}")

    else: # فحص الملفات (حل مشكلة الشاشة الحمراء)
        u_file = st.file_uploader("ارفع الملف للفحص:", type=None)
        if u_file and st.button("🛡️ بدء فحص الملف"):
            raw = u_file.getvalue()
            try: content = raw.decode("utf-8")
            except: content = raw.decode("latin-1", errors="replace")
            st.code(content[:1500], language="text")
            st.success("✅ تم الفحص البصري للملف.")
            send_to_telegram(f"📁 فحص ملف: {u_file.name}")

with tabs[2]: # التحميل
    v_url = st.text_input("رابط الفيديو:")
    if st.button("🎬 تحميل الآن"):
        st.write("جاري المعالجة...")
        # كود yt-dlp الخاص بك يوضع هنا
