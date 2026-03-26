import streamlit as st
import tldextract, sqlite3, requests, hashlib
from datetime import datetime

# --- إعدادات الحماية والتنبيهات ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

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

# --- إعداد قاعدة البيانات ---
db = sqlite3.connect('aiman_v6.db', check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS community_reports (content TEXT, date TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS admin_msgs (name TEXT, msg TEXT, date TEXT)")
db.commit()

# --- التصميم والواجهة ---
st.set_page_config(page_title="درع أيمن المتكامل", page_icon="🛡️", layout="centered")

st.markdown("""<style>
    .stApp { background-color: #0e1117; color: white; }
    .main-title { text-align: center; background: linear-gradient(90deg, #00d4ff, #0055ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.8rem; font-weight: bold; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #1a1c23; padding: 10px; border-radius: 15px; }
    .stButton>button { background: linear-gradient(45deg, #00d4ff, #0055ff); color: white; border-radius: 12px; width: 100%; font-weight: bold; border: none; }
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي</div>', unsafe_allow_html=True)

# --- نظام التبويبات الرئيسي ---
tabs = st.tabs(["🔗 فحص الروابط", "🔍 فحص الملفات", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# 1. فحص الروابط
with tabs[0]:
    st.subheader("🔗 فحص أمان الروابط")
    url_input = st.text_input("ألصق الرابط هنا للفحص:")
    if st.button("تحليل الرابط"):
        if url_input:
            ext = tldextract.extract(url_input)
            st.success(f"🔍 الموقع المكتشف: **{ext.domain}.{ext.suffix}**")
            st.warning("تنبيه: إذا كان اسم الموقع غريباً أو به أرقام بدلاً من حروف، فقد يكون احتيالياً.")
        else: st.error("يرجى إدخال رابط أولاً!")

# 2. فحص الملفات
with tabs[1]:
    st.subheader("📁 الفحص العالمي للملفات")
    up_file = st.file_uploader("ارفع الملف للفحص:")
    if up_file:
        content = up_file.read()
        f_hash = hashlib.sha256(content).hexdigest()
        st.info(f"🧬 البصمة الرقمية: `{f_hash}`")
        with st.spinner('جاري الفحص...'):
            res = check_vt_file(f_hash)
            if b"EICAR" in content or res and res.get('malicious', 0) > 0:
                st.error("🚨🚨 خطر! تم اكتشاف تهديد في هذا الملف!")
                send_telegram_msg(f"🚨 تنبيه من الدرع: تم كشف ملف ضار!\nالاسم: {up_file.name}")
            elif res: st.success("✅ الملف آمن ومسجل عالمياً.")
            else: st.warning("⚠️ الملف لم يسبق رفعه عالمياً (فريد)، تعامل معه بحذر.")

# 3. حماية المجتمع (عادت للعمل بكفاءة)
with tabs[2]:
    st.subheader("👥 بلاغات المجتمع")
    st.write("أدخل هنا أي رابط أو رسالة احتيالية وصلتك لنحذر الآخرين:")
    rep = st.text_area("تفاصيل البلاغ:")
    if st.button("نشر البلاغ الآن"):
        if rep:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            db.execute("INSERT INTO community_reports VALUES (?, ?)", (rep, now))
            db.commit()
            send_telegram_msg(f"📢 بلاغ مجتمعي جديد:\n{rep}")
            st.success("تم تسجيل بلاغك في قاعدة بيانات المجتمع.")

# 4. اتصل بنا
with tabs[3]:
    st.subheader("📧 تواصل مع المطور")
    name = st.text_input("اسمك:")
    msg = st.text_area("رسالتك:")
    if st.button("إرسال"):
        if name and msg:
            db.execute("INSERT INTO admin_msgs VALUES (?, ?, ?)", (name, msg, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            send_telegram_msg(f"📩 رسالة جديدة من {name}:\n{msg}")
            st.success("وصلت رسالتك يا بطل!")

# 5. الإدارة
with tabs[4]:
    st.subheader("🔐 لوحة تحكم أيمن")
    pwd = st.text_input("كلمة المرور:", type="password")
    if pwd == "ayman7716":
        st.write("### 📢 بلاغات المجتمع الأخيرة:")
        for r in db.execute("SELECT * FROM community_reports ORDER BY date DESC").fetchall():
            st.warning(f"🕒 {r[1]}\n📝 {r[0]}")
