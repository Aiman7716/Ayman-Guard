import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random, time
from datetime import datetime
from io import BytesIO

# --- 1. الإعدادات الأمنية ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

# قائمة المواقع الموثوقة (البيضاء) لمنع البلاغات الكاذبة
WHITELIST = ["google.com", "facebook.com", "youtube.com", "whatsapp.com", "microsoft.com", "apple.com", "instagram.com", "twitter.com", "amazon.com", "gmail.com"]

def send_telegram_msg(message):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except: pass

def check_vt_file(file_hash):
    headers = {"x-apikey": VT_API_KEY}
    try:
        res = requests.get(f"https://www.virustotal.com/api/v3/files/{file_hash}", headers=headers, timeout=5)
        if res.status_code == 200: return res.json()['data']['attributes']['last_analysis_stats']
    except: return None
    return None

# --- 2. قاعدة البيانات (هيكل مستقر) ---
db = sqlite3.connect('aiman_v15_final.db', check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, time_stamp TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, time_stamp TEXT)")
db.commit()

# --- 3. التصميم المريح للعين ---
st.set_page_config(page_title="درع أيمن v15", page_icon="🛡️")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { text-align: center; color: #58a6ff; font-size: 2.5rem; font-weight: bold; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stButton>button { background: #21262d; color: #58a6ff; border: 1px solid #30363d; border-radius: 8px; width: 100%; transition: 0.3s; }
    .stButton>button:hover { border-color: #58a6ff; }
    input, textarea { background-color: #010409 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; border-radius: 6px !important; }
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي</div>', unsafe_allow_html=True)

tabs = st.tabs(["🔍 الفحص الذكي", "🔗 فحص الروابط", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# الفحص الذكي (ملفات)
with tabs[0]:
    st.subheader("📁 فحص الملفات المطور")
    up_file = st.file_uploader("ارفع الملف للفحص الشامل:", type=None)
    if up_file:
        file_bytes = up_file.read()
        f_hash = hashlib.sha256(file_bytes).hexdigest()
        st.info(f"🧬 بصمة الملف: `{f_hash[:32]}...`")
        
        with st.spinner('جاري الفحص الدقيق...'):
            res = check_vt_file(f_hash)
            # فحص محلي (EICAR) وفحص عالمي
            if b"EICAR-STANDARD-ANTIVIRUS-TEST-FILE" in file_bytes or (res and res.get('malicious', 0) > 0):
                st.error("🚨 خطر! تم اكتشاف برمجيات ضارة.")
                send_telegram_msg(f"🚨 تنبيه: ملف ضار مكتشف!\nالاسم: {up_file.name}")
            elif res: st.success("✅ الملف نظيف وموثق عالمياً.")
            else: st.warning("⚠️ ملف جديد كلياً، لم يسبق رفعه للمختبرات العالمية.")

# فحص الروابط (مع القائمة البيضاء)
with tabs[1]:
    st.subheader("🔗 كاشف الروابط")
    url_input = st.text_input("ألصق الرابط هنا:")
    if st.button("بدء تحليل الرابط"):
        if url_input:
            ext = tldextract.extract(url_input)
            domain_full = f"{ext.domain}.{ext.suffix}"
            
            if domain_full in WHITELIST:
                st.success(f"✅ هذا الموقع موثوق وآمن: **{domain_full}**")
            else:
                st.warning(f"🔍 تم التحليل: الموقع هو (**{domain_full}**). يرجى الحذر إذا لم تكن تعرف هذا الموقع.")
        else: st.error("يرجى إدخال رابط.")

# حماية المجتمع
with tabs[2]:
    st.subheader("👥 بلاغات المجتمع")
    rep_txt = st.text_area("أدخل تفاصيل الاحتيال المنشور:")
    if st.button("نشر البلاغ"):
        if rep_txt:
            db.execute("INSERT INTO reports VALUES (?, ?)", (rep_txt, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            st.success("تم تسجيل بلاغك بنجاح.")

# اتصل بنا
with tabs[3]:
    st.subheader("📧 اتصل بالمطور")
    n = st.text_input("اسمك:")
    m = st.text_area("رسالتك:")
    if st.button("إرسال الآن"):
        if n and m:
            db.execute("INSERT INTO messages VALUES (?, ?, ?)", (n, m, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            send_telegram_msg(f"📩 رسالة جديدة من {n}: {m}")
            st.success("تم الإرسال!")

# الإدارة (المصلحة بالكامل)
with tabs[4]:
    st.subheader("🔐 لوحة التحكم")
    pw = st.text_input("كلمة المرور:", type="password", value="ayman7716")
    if pw == "ayman7716":
        if st.button("إرسال كود تليجرام"):
            code = str(random.randint(1000, 9999))
            st.session_state['v_code'] = code
            send_telegram_msg(f"🔐 كود الدخول هو: {code}")
            st.info("تم إرسال الكود.")

        user_v = st.text_input("كود التحقق:")
        if user_v and user_v == st.session_state.get('v_code'):
            st.success("✅ دخول آمن")
            
            # عرض البلاغات
            st.write("### 📢 البلاغات")
            reps = db.execute("SELECT * FROM reports ORDER BY time_stamp DESC").fetchall()
            if reps:
                df = pd.DataFrame(reps, columns=["المحتوى", "التاريخ"])
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 تحميل التقرير (CSV/Excel)", csv, "reports.csv", "text/csv")
            
            # عرض الرسائل
            st.write("---")
            st.write("### 📩 الرسائل")
            msgs = db.execute("SELECT * FROM messages ORDER BY time_stamp DESC").fetchall()
            for msg in msgs:
                st.info(f"👤 {msg[0]} | 🕒 {msg[2]}\n\n{msg[1]}")
