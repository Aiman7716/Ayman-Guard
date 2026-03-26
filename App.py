import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random
from datetime import datetime
from io import BytesIO

# --- 1. الإعدادات والربط ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

WHITELIST = ["google.com", "facebook.com", "whatsapp.com", "youtube.com", "microsoft.com", "apple.com"]

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except: pass

def check_vt_file(file_hash):
    headers = {"x-apikey": VT_API_KEY}
    try:
        res = requests.get(f"https://www.virustotal.com/api/v3/files/{file_hash}", headers=headers, timeout=5)
        if res.status_code == 200:
            return res.json()['data']['attributes']['last_analysis_stats']
    except: return None
    return None

# --- 2. قاعدة البيانات (اسم جديد لضمان النظافة) ---
conn = sqlite3.connect('aiman_v17_final.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 3. تصميم الواجهة ---
st.set_page_config(page_title="درع أيمن المطور", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { text-align: center; color: #58a6ff; font-size: 2.5rem; font-weight: bold; padding: 20px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stButton>button { background: #21262d; color: #58a6ff; border: 1px solid #30363d; border-radius: 8px; width: 100%; height: 3em; }
    .main, p, h1, h2, h3, div, label, .stAlert { direction: RTL !important; text-align: right !important; }
    /* منع قص النصوص في الجداول */
    .stDataFrame div { white-space: normal !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي - النسخة المستقرة</div>', unsafe_allow_html=True)

# --- 4. التبويبات الخمسة ---
tabs = st.tabs(["🔍 فحص الملفات", "🔗 فحص الروابط", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# التبويب 1: فحص الملفات (فعال 100%)
with tabs[0]:
    st.header("📁 فحص الملفات الذكي")
    uploaded_file = st.file_uploader("ارفع الملف ليتم تحليله عالمياً ومحلياً:", type=None, key="file_uroller")
    if uploaded_file:
        file_bytes = uploaded_file.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        st.info(f"🧬 بصمة الملف الكاملة: `{file_hash}`")
        
        if st.button("بدء فحص الملف الآن"):
            with st.spinner('جاري التحليل...'):
                res = check_vt_file(file_hash)
                if b"EICAR" in file_bytes or (res and res.get('malicious', 0) > 0):
                    st.error("🚨 خطر! تم اكتشاف برمجيات ضارة في هذا الملف.")
                    send_telegram_msg(f"🚨 تنبيه: تم كشف ملف ضار!\nالاسم: {uploaded_file.name}")
                elif res:
                    st.success("✅ الملف نظيف وموثق في القواعد العالمية.")
                else:
                    st.warning("⚠️ ملف جديد كلياً، يرجى الحذر عند فتحه.")

# التبويب 2: فحص الروابط (فعال 100%)
with tabs[1]:
    st.header("🔗 كاشف الروابط المشبوهة")
    url_to_check = st.text_input("أدخل الرابط المراد فحصه:")
    if st.button("تحليل الرابط المكتوب"):
        if url_to_check:
            extracted = tldextract.extract(url_to_check)
            domain = f"{extracted.domain}.{extracted.suffix}"
            if domain in WHITELIST:
                st.success(f"✅ الموقع موثوق وآمن تماماً: **{domain}**")
            else:
                st.warning(f"🔍 تم التحليل: الموقع يتبع لنطاق (**{domain}**). تأكد من هوية المرسل.")
        else: st.error("يرجى كتابة رابط أولاً.")

# التبويب 3: حماية المجتمع
with tabs[2]:
    st.header("👥 بلاغات المجتمع")
    report_input = st.text_area("أدخل تفاصيل الاحتيال (رابط، رسالة، أو وصف):", key="rep_area")
    if st.button("نشر وتحذير الجميع"):
        if report_input:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (report_input, now))
            conn.commit()
            st.success("تم تسجيل البلاغ بنجاح في قاعدة البيانات.")
            send_telegram_msg(f"📢 بلاغ مجتمعي جديد: {report_input}")

# التبويب 4: اتصل بنا
with tabs[3]:
    st.header("📧 تواصل مع الإدارة")
    name_in = st.text_input("الاسم:")
    msg_in = st.text_area("نص الرسالة:")
    if st.button("إرسال الرسالة"):
        if name_in and msg_in:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO messages VALUES (?, ?, ?)", (name_in, msg_in, now))
            conn.commit()
            st.success("شكراً لتواصلك، تم الإرسال بنجاح.")
            send_telegram_msg(f"📩 رسالة من {name_in}: {msg_in}")

# التبويب 5: الإدارة (إصلاح عرض التقرير والرسائل)
with tabs[4]:
    st.header("🔐 لوحة التحكم")
    password = st.text_input("كلمة مرور المدير:", type="password")
    if password == "ayman7716":
        # عرض البلاغات كاملة
        st.subheader("📢 سجل البلاغات")
        all_reports = pd.read_sql_query("SELECT content AS 'البلاغ الكامل', dt AS 'تاريخ البلاغ' FROM reports ORDER BY dt DESC", conn)
        if not all_reports.empty:
            # استخدام dataframe مع تفعيل العرض الكامل
            st.dataframe(all_reports, use_container_width=True)
            
            # زر التحميل
            csv = all_reports.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل التقرير (Excel/CSV)", csv, "reports_aiman.csv", "text/csv")
        else: st.info("لا توجد بلاغات مسجلة.")

        st.write("---")
        # عرض الرسائل بوضوح
        st.subheader("📩 الرسائل الواردة")
        all_msgs = pd.read_sql_query("SELECT * FROM messages ORDER BY dt DESC", conn).values.tolist()
        if all_msgs:
            for m in all_msgs:
                with st.expander(f"👤 من: {m[0]} | 📅 {m[2]}"):
                    st.write(f"**نص الرسالة:**\n{m[1]}")
        else: st.info("لا توجد رسائل حالياً.")
