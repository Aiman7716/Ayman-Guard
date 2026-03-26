import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
from datetime import datetime
from io import BytesIO

# --- 1. الإعدادات الأمنية (تليجرام و VirusTotal) ---
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

# --- 2. قاعدة البيانات (ضمان عدم ضياع أي جدول) ---
db = sqlite3.connect('aiman_security_v10.db', check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, date TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, date TEXT)")
db.commit()

# --- 3. التصميم المريح للعين (Dark Pro Mode) ---
st.set_page_config(page_title="درع أيمن v10", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { text-align: center; color: #58a6ff; font-size: 2.5rem; font-weight: bold; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom: 2px solid #58a6ff !important; }
    .stButton>button { 
        background: #21262d; color: #58a6ff; border: 1px solid #30363d; 
        border-radius: 8px; width: 100%; transition: 0.3s;
    }
    input, textarea { background-color: #010409 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي</div>', unsafe_allow_html=True)

# --- 4. التبويبات الخمسة (بدون أي نقص) ---
tabs = st.tabs(["🔗 فحص الروابط", "🔍 فحص الملفات", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# التبويب 1: الروابط
with tabs[0]:
    st.subheader("🔗 كاشف الروابط")
    url_in = st.text_input("ألصق الرابط للفحص:")
    if st.button("تحليل الآن"):
        if url_in:
            ext = tldextract.extract(url_in)
            st.success(f"🔍 تم التحليل: النطاق هو (**{ext.domain}.{ext.suffix}**)")
        else: st.warning("أدخل رابطاً أولاً.")

# التبويب 2: الملفات
with tabs[1]:
    st.subheader("📁 الفحص العالمي للملفات")
    up_f = st.file_uploader("ارفع الملف:", type=None)
    if up_f:
        data = up_f.read()
        f_hash = hashlib.sha256(data).hexdigest()
        st.info(f"🧬 البصمة: `{f_hash[:30]}...`")
        res = check_vt_file(f_hash)
        if b"EICAR" in data or (res and res.get('malicious', 0) > 0):
            st.error("🚨 خطر! تم اكتشاف تهديد.")
            send_telegram_msg(f"🚨 تنبيه: ملف ضار مكتشف: {up_f.name}")
        elif res: st.success("✅ الملف آمن عالمياً.")
        else: st.warning("⚠️ ملف جديد كلياً، لم يسبق رفعه.")

# التبويب 3: حماية المجتمع
with tabs[2]:
    st.subheader("👥 بلاغات المجتمع")
    rep_in = st.text_area("أدخل تفاصيل البلاغ لتحذير الآخرين:")
    if st.button("نشر البلاغ"):
        if rep_in:
            db.execute("INSERT INTO reports VALUES (?, ?)", (rep_in, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            send_telegram_msg(f"📢 بلاغ جديد: {rep_in}")
            st.success("تم النشر بنجاح.")

# التبويب 4: اتصل بنا
with tabs[3]:
    st.subheader("📧 تواصل مع المطور")
    n = st.text_input("اسمك:")
    m = st.text_area("رسالتك:")
    if st.button("إرسال"):
        if n and m:
            db.execute("INSERT INTO messages VALUES (?, ?, ?)", (n, m, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            send_telegram_msg(f"📩 رسالة من {n}: {m}")
            st.success("تم الإرسال!")

# التبويب 5: الإدارة (مع ميزة Excel)
with tabs[4]:
    st.subheader("🔐 لوحة التحكم")
    pwd = st.text_input("كلمة المرور:", type="password")
    if pwd == "ayman7716":
        # عرض وتحميل البلاغات
        st.write("### 📢 بلاغات المجتمع")
        reps = db.execute("SELECT * FROM reports ORDER BY date DESC").fetchall()
        if reps:
            df_reps = pd.DataFrame(reps, columns=["المحتوى", "التاريخ"])
            st.table(df_reps.head(5))
            
            # زر تحميل Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_reps.to_excel(writer, index=False, sheet_name='البلاغات')
            st.download_button(label="📥 تحميل البلاغات (Excel)", data=output.getvalue(), file_name="reports_aiman.xlsx")
        
        st.write("---")
        # عرض الرسائل
        st.write("### 📩 الرسائل الواردة")
        msgs = db.execute("SELECT * FROM messages ORDER BY dt DESC").fetchall()
        for msg in msgs:
            st.info(f"👤 {msg[0]} | 🕒 {msg[2]}\n\n{msg[1]}")
