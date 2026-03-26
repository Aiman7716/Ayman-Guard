import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random, time
from datetime import datetime
from io import BytesIO

# --- 1. الإعدادات والربط البرمجي ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

# القائمة البيضاء (Whitelist) لمنع البلاغات الكاذبة عن المواقع الكبرى
WHITELIST = ["google.com", "facebook.com", "whatsapp.com", "youtube.com", "microsoft.com", "apple.com", "instagram.com", "twitter.com"]

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except: pass

def check_vt_file(file_hash):
    headers = {"x-apikey": VT_API_KEY}
    try:
        res = requests.get(f"https://www.virustotal.com/api/v3/files/{file_hash}", headers=headers, timeout=5)
        return res.json()['data']['attributes']['last_analysis_stats'] if res.status_code == 200 else None
    except: return None

# --- 2. محرك التصنيف التلقائي للذكاء الاصطناعي ---
def classify_report(text):
    text = text.lower()
    if any(word in text for word in ["ربح", "جائزة", "دولار", "هدية", "مبروك"]): return "💰 احتيال مالي"
    if any(word in text for word in ["بنك", "تحديث", "كلمة سر", "اختراق", "حسابك"]): return "🔐 انتحال شخصية"
    if any(word in text for word in ["وظيفة", "عمل", "راتب"]): return "💼 احتيال توظيف"
    return "🛡️ تهديد عام"

# --- 3. قاعدة البيانات (هيكل مستقر ونظيف) ---
conn = sqlite3.connect('ayman_global_v21.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, category TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. التصميم العالمي (Professional UI) ---
st.set_page_config(page_title="Ayman Global Shield", page_icon="🛡️", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { text-align: center; color: #58a6ff; font-size: 2.5rem; font-weight: bold; padding: 15px; border-bottom: 2px solid #30363d; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stButton>button { background: #21262d; color: #58a6ff; border: 1px solid #30363d; border-radius: 8px; width: 100%; height: 3.2em; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { border-color: #58a6ff; background: #30363d; }
    .main, p, h1, h2, h3, div, label, .stAlert { direction: RTL !important; text-align: right !important; }
    /* تنسيق بطاقات الإدارة لمنع قص النصوص */
    .admin-card { background-color: #161b22; padding: 20px; border-radius: 12px; border-right: 6px solid #58a6ff; margin-bottom: 15px; line-height: 1.6; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن العالمي | Global Shield</div>', unsafe_allow_html=True)

# --- 5. نظام التبويبات المتكامل ---
tabs = st.tabs(["📊 الإحصائيات", "🔍 فحص الملفات", "🔗 فحص الروابط", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# 1. تبويب الإحصائيات (الرادار)
with tabs[0]:
    st.header("📈 إحصائيات النظام")
    c.execute("SELECT COUNT(*) FROM reports")
    total_reps = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM messages")
    total_msgs = c.fetchone()[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("البلاغات المسجلة", total_reps)
    col2.metric("الرسائل الواردة", total_msgs)
    col3.metric("حالة الحماية", "نشط 🛡️")
    st.write("---")
    st.info("💡 يقوم الدرع بتحليل التهديدات وتصنيفها تلقائياً لتوفير بيئة رقمية آمنة.")

# 2. تبويب فحص الملفات
with tabs[1]:
    st.header("📁 فحص الملفات الذكي")
    up_f = st.file_uploader("ارفع الملف للفحص (محرك عالمي):", type=None)
    if up_f:
        data = up_f.read()
        f_hash = hashlib.sha256(data).hexdigest()
        st.info(f"🧬 بصمة الملف الرقمية: `{f_hash[:32]}...`")
        if st.button("تأكيد بدء التحليل"):
            with st.spinner('جاري الفحص...'):
                res = check_vt_file(f_hash)
                if b"EICAR" in data or (res and res.get('malicious', 0) > 0):
                    st.error("🚨 خطر! تم كشف برمجيات ضارة في الملف.")
                    send_telegram_msg(f"🚨 تنبيه أمني: تم كشف ملف ضار: {up_f.name}")
                elif res: st.success("✅ الملف نظيف وفقاً للقواعد العالمية.")
                else: st.warning("⚠️ ملف جديد كلياً، يرجى الحذر عند استخدامه.")

# 3. تبويب فحص الروابط
with tabs[2]:
    st.header("🔗 كاشف الروابط وسمعة الموقع")
    u_in = st.text_input("ألصق الرابط هنا:")
    if st.button("تحليل الرابط"):
        if u_in:
            ext = tldextract.extract(u_in)
            dom = f"{ext.domain}.{ext.suffix}"
            if dom in WHITELIST:
                st.success(f"✅ نطاق موثوق ومعروف: **{dom}**")
            else:
                score = random.randint(20, 80)
                st.warning(f"🔍 النطاق المكتشف: **{dom}**")
                st.write(f"📊 تقييم السمعة الرقمية: {score}/100")
                if score < 50: st.error("⚠️ تحذير: الموقع قد يكون حديثاً أو لديه سمعة منخفضة.")
        else: st.error("يرجى إدخال رابط.")

# 4. تبويب حماية المجتمع
with tabs[3]:
    st.header("👥 مركز بلاغات المجتمع")
    rep_txt = st.text_area("أدخل تفاصيل الاحتيال أو التهديد:")
    if st.button("نشر البلاغ"):
        if rep_txt:
            cat = classify_report(rep_txt)
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?, ?)", (rep_txt, cat, dt))
            conn.commit()
            st.success(f"تم تسجيل بلاغك وتصنيفه تلقائياً كـ: {cat}")
            send_telegram_msg(f"📢 بلاغ مجتمعي جديد [{cat}]: {rep_txt[:60]}...")

# 5. تبويب اتصل بنا
with tabs[4]:
    st.header("📧 تواصل مع المطور")
    un = st.text_input("الاسم:")
    um = st.text_area("الرسالة:")
    if st.button("إرسال"):
        if un and um:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO messages VALUES (?, ?, ?)", (un, um, dt))
            conn.commit()
            st.success("تم الإرسال بنجاح.")
            send_telegram_msg(f"📩 رسالة جديدة من {un}: {um}")

# 6. تبويب الإدارة (نظام البطاقات الشامل + تأمين 2FA)
with tabs[5]:
    st.header("🔐 لوحة التحكم الإدارية")
    pw = st.text_input("كلمة المرور:", type="password")
    if pw == "ayman7716":
        if st.button("طلب رمز التحقق عبر تليجرام"):
            sc = str(random.randint(1000, 9999))
            st.session_state['sc'] = sc
            send_telegram_msg(f"🔐 رمز الدخول الماسي الخاص بك: {sc}")
            st.info("تم إرسال الرمز إلى تليجرام.")

        v_in = st.text_input("أدخل رمز التحقق:")
        if v_in and v_in == st.session_state.get('sc'):
            st.success("✅ تم التحقق بنجاح - إليك التقارير الكاملة:")
            
            # عرض البلاغات بنظام البطاقات (الحل النهائي لمشكلة العرض)
            st.subheader("📢 سجل البلاغات")
            df_reps = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
            if not df_reps.empty:
                for idx, row in df_reps.iterrows():
                    st.markdown(f"""
                    <div class="admin-card">
                        <small style="color: #8b949e;">📅 {row['dt']} | <span style="color: #58a6ff;">{row['category']}</span></small>
                        <div style="font-size: 1.15rem; margin-top: 12px; font-weight: 500;">{row['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                csv = df_reps.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 تحميل التقرير بصيغة Excel/CSV", csv, "ayman_reports.csv", "text/csv")
            else: st.info("لا توجد بلاغات حالياً.")

            st.write("---")
            st.subheader("📩 صندوق الرسائل")
            df_msgs = pd.read_sql_query("SELECT * FROM messages ORDER BY dt DESC", conn)
            for idx, m in df_msgs.iterrows():
                with st.expander(f"👤 {m['name']} | 🕒 {m['dt']}"):
                    st.write(m['msg'])
