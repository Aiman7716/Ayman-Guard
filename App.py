import streamlit as st
import tldextract
import sqlite3
import os
import requests
import hashlib
from datetime import datetime

# --- إعدادات الحماية والتنبيهات ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, json=payload, timeout=5)
    except: pass

def check_virustotal(file_content):
    file_hash = hashlib.sha256(file_content).hexdigest()
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": VT_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['data']['attributes']['last_analysis_stats']
    except: return None
    return None

# --- التصميم السيبراني (نفس الروح في صورتك الأخيرة) ---
st.set_page_config(page_title="درع أيمن الاحترافي", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .main-title {
        text-align: center;
        background: linear-gradient(90deg, #00d4ff, #0055ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: bold;
        text-shadow: 2px 2px 15px rgba(0, 212, 255, 0.4);
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #1a1c23; padding: 10px; border-radius: 15px; direction: RTL; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-size: 14px; }
    .stButton>button { background: linear-gradient(45deg, #00d4ff, #0055ff); color: white; border-radius: 12px; font-weight: bold; width: 100%; height: 3.5em; border: none; }
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
    input, textarea { background-color: #161b22 !important; color: white !important; direction: RTL !important; }
    </style>
    """, unsafe_allow_html=True)

# العنوان كما في صورتك
st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي</div>', unsafe_allow_html=True)

# التبويبات (أضفنا فحص الروابط كأول خيار)
tabs = st.tabs(["🔗 فحص الروابط", "🔍 فحص ملف (AI)", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# --- 1. تبويب فحص الروابط (العائد) ---
with tabs[0]:
    st.subheader("🔗 فحص الروابط والمواقع")
    url_to_check = st.text_input("ألصق الرابط المشبوه هنا:")
    if st.button("تحليل الرابط الآن"):
        if url_to_check:
            info = tldextract.extract(url_to_check)
            st.success(f"✅ تم تحليل الرابط.\n\nالموقع الأساسي: **{info.domain}.{info.suffix}**")
            st.info("نصيحة: تأكد دائماً أن اسم الموقع (Domain) هو الموقع الرسمي الذي تقصده وليس حروفا مشابهة.")
        else:
            st.warning("يرجى إدخال رابط أولاً.")

# --- 2. تبويب فحص الملفات (VirusTotal) ---
with tabs[1]:
    st.subheader("📁 فحص الملفات عبر قاعدة بيانات عالمية")
    up_file = st.file_uploader("ارفع الملف للفحص (70 محرك حماية):", type=None)
    if up_file:
        with st.spinner('جاري التحليل السيبراني...'):
            content = up_file.read()
            res = check_virustotal(content)
            if res:
                mal = res.get('malicious', 0)
                if mal > 0:
                    st.error(f"🚨 تحذير: تم اكتشاف {mal} تهديد!")
                    send_telegram_msg(f"🚨 ملف خطير! {up_file.name} | تهديدات: {mal}")
                else:
                    st.success("✅ الملف نظيف تماماً.")
            else:
                st.info("لم يسبق فحص هذا الملف عالمياً، سيتم التعامل معه كملف جديد.")

# [باقي التبويبات: حماية المجتمع، اتصل بنا، الإدارة تظل كما هي في كودك السابق]
with tabs[2]:
    st.subheader("👥 بلاغات المجتمع")
    rep = st.text_area("أدخل تفاصيل الاحتيال:")
    if st.button("نشر البلاغ"):
        send_telegram_msg(f"📢 بلاغ جديد: {rep}")
        st.success("شكراً لك.")

with tabs[3]:
    st.subheader("📧 تواصل معنا")
    n = st.text_input("الاسم:")
    m = st.text_area("الرسالة:")
    if st.button("إرسال"):
        send_telegram_msg(f"📩 رسالة من {n}: {m}")
        st.success("تم الإرسال.")

with tabs[4]:
    pwd = st.text_input("كلمة المرور:", type="password")
    if pwd == "ayman7716":
        st.write("أهلاً بك يا مهندس أيمن في لوحة التحكم.")
