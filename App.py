import streamlit as st
import tldextract, sqlite3, requests, hashlib
from datetime import datetime

# --- 1. الإعدادات الأمنية (تأكد من بقائها) ---
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

# --- 2. قاعدة البيانات الشاملة ---
db = sqlite3.connect('aiman_ultimate.db', check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS reports (txt TEXT, dt TEXT)") # بلاغات المجتمع
db.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)") # اتصل بنا
db.commit()

# --- 3. التصميم المريح (Professional Dark Mode) ---
st.set_page_config(page_title="درع أيمن المطور", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { 
        text-align: center; color: #58a6ff; font-size: 2.5rem; 
        font-weight: bold; margin-bottom: 10px; 
    }
    .stTabs [data-baseweb="tab-list"] { 
        gap: 8px; background-color: #161b22; padding: 10px; border-radius: 12px; 
    }
    .stTabs [data-baseweb="tab"] { color: #8b949e !important; }
    .stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom: 2px solid #58a6ff !important; }
    .stButton>button { 
        background: #21262d; color: #58a6ff; border: 1px solid #30363d; 
        border-radius: 8px; width: 100%; height: 3.5em; transition: 0.3s;
    }
    .stButton>button:hover { background: #30363d; border-color: #8b949e; }
    input, textarea { 
        background-color: #010409 !important; color: #c9d1d9 !important; 
        border: 1px solid #30363d !important; border-radius: 6px !important;
    }
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
    </style>
    """, unsafe_allow_html=True)

# عرض الشعار (Logo)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    try: st.image("1774474792146.png", use_container_width=True)
    except: pass

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي</div>', unsafe_allow_html=True)

# --- 4. هيكل التبويبات الخمسة ---
tabs = st.tabs(["🔗 فحص الروابط", "🔍 فحص الملفات", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# التبويب 1: الروابط
with tabs[0]:
    st.markdown("### 🔗 كشف المواقع المشبوهة")
    url_val = st.text_input("ألصق الرابط هنا:")
    if st.button("تحليل الرابط الآن"):
        if url_val:
            ext = tldextract.extract(url_val)
            st.success(f"🔍 الموقع المكتشف: **{ext.domain}.{ext.suffix}**")
            st.info("تأكد أن هذا هو الموقع الرسمي الذي تقصده.")
        else: st.warning("الرجاء إدخال رابط.")

# التبويب 2: الملفات
with tabs[1]:
    st.markdown("### 📁 الفحص العالمي (VirusTotal)")
    up_f = st.file_uploader("ارفع الملف ليتم فحصه عبر 70 محرك حماية:", type=None)
    if up_f:
        c = up_f.read()
        h = hashlib.sha256(c).hexdigest()
        st.info(f"🧬 البصمة الرقمية: `{h[:32]}...`")
        res = check_vt_file(h)
        if b"EICAR" in c or (res and res.get('malicious', 0) > 0):
            st.error("🚨 خطر! تم اكتشاف تهديد أمني في هذا الملف.")
            send_telegram_msg(f"🚨 إنذار! تم كشف ملف ضار: {up_f.name}")
        elif res: st.success("✅ الملف نظيف وموثق عالمياً.")
        else: st.warning("⚠️ ملف فريد، تعامل معه بحذر (لم يسبق رفعه عالمياً).")

# التبويب 3: حماية المجتمع
with tabs[2]:
    st.markdown("### 👥 بلاغات المجتمع")
    txt_rep = st.text_area("ساهم في حماية غيرك، أدخل رابطاً أو رسالة احتيالية:")
    if st.button("نشر وتحذير الجميع"):
        if txt_rep:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            db.execute("INSERT INTO reports VALUES (?, ?)", (txt_rep, dt))
            db.commit()
            send_telegram_msg(f"📢 بلاغ مجتمعي جديد: {txt_rep}")
            st.success("تم النشر بنجاح.")

# التبويب 4: اتصل بنا
with tabs[3]:
    st.markdown("### 📧 تواصل مع المطور")
    u_name = st.text_input("الاسم:")
    u_msg = st.text_area("رسالتك:")
    if st.button("إرسال الرسالة"):
        if u_name and u_msg:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            db.execute("INSERT INTO messages VALUES (?, ?, ?)", (u_name, u_msg, dt))
            db.commit()
            send_telegram_msg(f"📩 رسالة من {u_name}: {u_msg}")
            st.success("شكراً لتواصلك يا بطل!")

# التبويب 5: الإدارة (الآن تعرض كل شيء)
with tabs[4]:
    st.markdown("### 🔐 لوحة التحكم الإدارية")
    pwd = st.text_input("كلمة المرور:", type="password")
    if pwd == "ayman7716":
        st.write("---")
        st.write("### 📢 بلاغات المجتمع الأخيرة")
        for r in db.execute("SELECT * FROM reports ORDER BY dt DESC LIMIT 10").fetchall():
            st.warning(f"🕒 {r[1]} | 📝 {r[0]}")
        
        st.write("---")
        st.write("### 📩 الرسائل الواردة")
        for m in db.execute("SELECT * FROM messages ORDER BY dt DESC LIMIT 10").fetchall():
            st.info(f"👤 {m[0]} ({m[2]}): \n {m[1]}")
