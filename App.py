import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
from datetime import datetime
from io import BytesIO

# --- 1. الإعدادات الأمنية ---
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

# --- 2. قاعدة البيانات (إصلاح خطأ الأسماء) ---
db = sqlite3.connect('aiman_final_fix.db', check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, date_fixed TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, date_fixed TEXT)")
db.commit()

# --- 3. التصميم المريح للعين (Dark Slate Blue) ---
st.set_page_config(page_title="درع أيمن v11", page_icon="🛡️")

st.markdown("""
    <style>
    /* خلفية داكنة مريحة جداً */
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { text-align: center; color: #58a6ff; font-size: 2.2rem; font-weight: bold; margin-bottom: 25px; }
    
    /* تنسيق التبويبات */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 5px; background-color: #161b22; padding: 10px; border-radius: 12px; 
    }
    .stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom: 2px solid #58a6ff !important; }

    /* أزرار وحقول داكنة مريحة */
    .stButton>button { 
        background: #21262d; color: #58a6ff; border: 1px solid #30363d; 
        border-radius: 8px; width: 100%; transition: 0.3s;
    }
    input, textarea { background-color: #010409 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي</div>', unsafe_allow_html=True)

# --- 4. التبويبات الشاملة ---
tabs = st.tabs(["🔍 الفحص الذكي", "🔗 فحص الروابط", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# التبويب 1: الفحص الذكي (المحدث)
with tabs[0]:
    st.subheader("📁 فحص الملفات (عالمي + محلي)")
    up_f = st.file_uploader("ارفع الملف للفحص الشامل:", type=None)
    if up_f:
        file_data = up_f.read()
        f_hash = hashlib.sha256(file_data).hexdigest()
        st.info(f"🧬 **البصمة:** `{f_hash}`") # كما في صورتك
        res = check_vt_file(f_hash)
        if b"EICAR" in file_data or (res and res.get('malicious', 0) > 0):
            st.error("🚨 تهديد أمني مكتشف!")
        elif res: st.success("✅ الملف آمن.")
        else: st.warning("⚠️ الملف فريد ولم يرفع عالمياً من قبل.")

# التبويب 2: فحص الروابط
with tabs[1]:
    st.subheader("🔗 كاشف الروابط")
    url_v = st.text_input("ألصق الرابط هنا للفحص:")
    if st.button("تحليل الرابط"):
        if url_v:
            ext = tldextract.extract(url_v)
            st.success(f"🔍 الموقع المكتشف هو: **{ext.domain}.{ext.suffix}**")

# التبويب 3: حماية المجتمع
with tabs[2]:
    st.subheader("👥 بلاغات المجتمع")
    rep_txt = st.text_area("أدخل تفاصيل الاحتيال:")
    if st.button("نشر وتحذير المجتمع"):
        if rep_txt:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            db.execute("INSERT INTO reports VALUES (?, ?)", (rep_txt, now))
            db.commit()
            send_telegram_msg(f"📢 بلاغ جديد: {rep_txt}")
            st.success("تم تسجيل بلاغك بنجاح.")

# التبويب 4: اتصل بنا
with tabs[3]:
    st.subheader("📧 تواصل مع المطور")
    un = st.text_input("الاسم:")
    um = st.text_area("رسالتك:")
    if st.button("إرسال"):
        if un and um:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            db.execute("INSERT INTO messages VALUES (?, ?, ?)", (un, um, now))
            db.commit()
            send_telegram_msg(f"📩 رسالة من {un}: {um}")
            st.success("وصلت رسالتك يا بطل!")

# التبويب 5: الإدارة (إصلاح الخطأ وإضافة Excel)
with tabs[4]:
    st.subheader("🔐 لوحة التحكم الإدارية")
    # كلمة المرور كما في صورتك
    pw = st.text_input("كلمة المرور:", type="password", value="ayman7716")
    if pw == "ayman7716":
        # عرض وتحميل البلاغات
        st.write("### 📢 بلاغات المجتمع")
        reps = db.execute("SELECT * FROM reports ORDER BY date_fixed DESC").fetchall()
        if reps:
            df = pd.DataFrame(reps, columns=["البلاغ", "التاريخ"])
            st.dataframe(df, use_container_width=True)
            
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            st.download_button("📥 تحميل سجل البلاغات (Excel)", output.getvalue(), "reports.xlsx")
        
        st.write("---")
        st.write("### 📩 الرسائل الواردة")
        msgs = db.execute("SELECT * FROM messages ORDER BY date_fixed DESC").fetchall()
        for m in msgs:
            st.info(f"👤 {m[0]} | 🕒 {m[2]}\n\n{m[1]}")
