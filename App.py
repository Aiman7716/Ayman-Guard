import streamlit as st
import tldextract, sqlite3, requests, hashlib
from datetime import datetime

# --- إعدادات الحماية ---
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

# --- قاعدة البيانات ---
db = sqlite3.connect('aiman_final_v7.db', check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS community (txt TEXT, dt TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS contact (name TEXT, msg TEXT, dt TEXT)")
db.commit()

# --- التصميم ---
st.set_page_config(page_title="درع أيمن المتكامل", page_icon="🛡️")
st.markdown("""<style>
    .stApp { background-color: #0e1117; color: white; }
    .main-title { text-align: center; color: #00d4ff; font-size: 2.8rem; font-weight: bold; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #1a1c23; padding: 10px; border-radius: 15px; }
    .stButton>button { background: linear-gradient(45deg, #00d4ff, #0055ff); color: white; border-radius: 12px; width: 100%; border: none; font-weight: bold; }
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# --- توزيع التبويبات ---
tabs = st.tabs(["🔗 فحص الروابط", "🔍 فحص الملفات", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# 1. فحص الروابط (تم تفعيله بالكامل)
with tabs[0]:
    st.subheader("🔗 كاشف الروابط المزيفة")
    link_in = st.text_input("ألصق الرابط المشبوه هنا:")
    if st.button("بدء الفحص"):
        if link_in:
            ext = tldextract.extract(link_in)
            st.success(f"🔍 تم التحليل: أنت تزور موقع (**{ext.domain}.{ext.suffix}**)")
            st.info("نصيحة أيمن: المواقع الأصلية تنتهي غالباً بـ .com أو .net وتكون أسماؤها واضحة.")
        else: st.warning("يرجى إدخال رابط.")

# 2. فحص الملفات
with tabs[1]:
    st.subheader("📁 الفحص العالمي للملفات")
    up = st.file_uploader("ارفع الملف للفحص:")
    if up:
        bytes_data = up.read()
        h = hashlib.sha256(bytes_data).hexdigest()
        st.info(f"🧬 البصمة الرقمية: `{h}`")
        res = check_vt_file(h)
        if b"EICAR" in bytes_data or (res and res.get('malicious', 0) > 0):
            st.error("🚨 خطر! ملف ضار مكتشف.")
            send_telegram_msg(f"🚨 تنبيه من الدرع: تم كشف ملف مشبوه باسم: {up.name}")
        elif res: st.success("✅ الملف نظيف وموثوق عالمياً.")
        else: st.warning("⚠️ ملف فريد، لم يسبق رفعه عالمياً.")

# 3. حماية المجتمع (عادت للظهور)
with tabs[2]:
    st.subheader("👥 بلاغات مجتمع أيمن")
    r_txt = st.text_area("أدخل تفاصيل الاحتيال أو الرابط المزعج:")
    if st.button("نشر البلاغ"):
        if r_txt:
            db.execute("INSERT INTO community VALUES (?, ?)", (r_txt, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            send_telegram_msg(f"📢 بلاغ مجتمعي: {r_txt}")
            st.success("تم النشر بنجاح!")

# 4. اتصل بنا
with tabs[3]:
    st.subheader("📧 تواصل مع الإدارة")
    n = st.text_input("اسمك:")
    m = st.text_area("رسالتك:")
    if st.button("إرسال الآن"):
        if n and m:
            db.execute("INSERT INTO contact VALUES (?, ?, ?)", (n, m, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            send_telegram_msg(f"📩 رسالة من {n}: {m}")
            st.success("تم الإرسال!")

# 5. الإدارة
with tabs[4]:
    st.subheader("🔐 لوحة تحكم أيمن")
    p = st.text_input("كلمة المرور:", type="password")
    if p == "ayman7716":
        st.write("### 📝 أحدث البلاغات:")
        for row in db.execute("SELECT * FROM community ORDER BY dt DESC").fetchall():
            st.warning(f"{row[1]}: {row[0]}")
