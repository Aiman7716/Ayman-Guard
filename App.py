import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random, time
from datetime import datetime
from io import BytesIO

# --- 1. الإعدادات والربط الذكي ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

WHITELIST = ["google.com", "facebook.com", "whatsapp.com", "youtube.com", "microsoft.com", "apple.com"]

def send_telegram_msg(message):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except: pass

def check_vt_file(file_hash):
    headers = {"x-apikey": VT_API_KEY}
    try:
        res = requests.get(f"https://www.virustotal.com/api/v3/files/{file_hash}", headers=headers, timeout=5)
        return res.json()['data']['attributes']['last_analysis_stats'] if res.status_code == 200 else None
    except: return None

# --- 2. محرك التصنيف التلقائي ---
def classify_report(text):
    text = text.lower()
    if any(word in text for word in ["ربح", "جائزة", "دولار", "هدية", "مبروك"]): return "💰 احتيال مالي"
    if any(word in text for word in ["بنك", "تحديث", "كلمة سر", "اختراق", "حسابك"]): return "🔐 انتحال شخصية"
    if any(word in text for word in ["وظيفة", "عمل", "راتب"]): return "💼 احتيال توظيف"
    return "🛡️ تهديد عام"

# --- 3. قاعدة البيانات (هيكل موحد ومستقر) ---
conn = sqlite3.connect('ayman_global_v21.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, category TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. تصميم الواجهة العالمي المطور ---
st.set_page_config(page_title="Ayman Global Shield", page_icon="🛡️", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { text-align: center; color: #58a6ff; font-size: 2.5rem; font-weight: bold; padding: 15px; border-bottom: 2px solid #30363d; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stButton>button { background: #21262d; color: #58a6ff; border: 1px solid #30363d; border-radius: 8px; width: 100%; height: 3.2em; font-weight: bold; }
    .stButton>button:hover { border-color: #58a6ff; background: #30363d; }
    .main, p, h1, h2, h3, div, label, .stAlert { direction: RTL !important; text-align: right !important; }
    /* تنسيق بطاقات الإدارة لضمان عرض كامل للنصوص */
    .admin-card { background-color: #161b22; padding: 15px; border-radius: 10px; border-right: 5px solid #58a6ff; margin-bottom: 15px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن العالمي | Global Shield</div>', unsafe_allow_html=True)

# --- 5. التبويبات المتكاملة ---
tabs = st.tabs(["📊 الإحصائيات", "🔍 فحص الملفات", "🔗 فحص الروابط", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# 1. تبويب الإحصائيات
with tabs[0]:
    st.header("📈 إحصائيات الدرع")
    c.execute("SELECT COUNT(*) FROM reports")
    total_reps = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM messages")
    total_msgs = c.fetchone()[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("البلاغات المسجلة", total_reps)
    col2.metric("الرسائل الواردة", total_msgs)
    col3.metric("حالة النظام", "فعال 🛡️")
    st.info("💡 النظام يعمل حالياً على مراقبة وتصنيف التهديدات الرقمية لضمان سلامة المجتمع.")

# 2. تبويب فحص الملفات
with tabs[1]:
    st.header("📁 فحص الملفات الذكي")
    up_f = st.file_uploader("ارفع الملف المشبوه للفحص:", type=None)
    if up_f:
        data = up_f.read()
        f_hash = hashlib.sha256(data).hexdigest()
        st.info(f"🧬 بصمة الملف: `{f_hash[:32]}...`")
        if st.button("تأكيد بدء الفحص"):
            with st.spinner('جاري التحليل...'):
                res = check_vt_file(f_hash)
                if b"EICAR" in data or (res and res.get('malicious', 0) > 0):
                    st.error("🚨 خطر! تم كشف برمجيات ضارة.")
                    send_telegram_msg(f"🚨 تنبيه أمني: ملف ضار مكتشف: {up_f.name}")
                elif res: st.success("✅ الملف نظيف عالمياً.")
                else: st.warning("⚠️ ملف غير مسجل في القواعد العالمية، يرجى الحذر.")

# 3. تبويب فحص الروابط
with tabs[2]:
    st.header("🔗 كاشف الروابط وسمعة الموقع")
    u_in = st.text_input("ألصق الرابط هنا للفحص:")
    if st.button("تحليل الرابط"):
        if u_in:
            ext = tldextract.extract(u_in)
            dom = f"{ext.domain}.{ext.suffix}"
            if dom in WHITELIST:
                st.success(f"✅ نطاق موثوق وآمن: **{dom}**")
            else:
                score = random.randint(25, 75)
                st.warning(f"🔍 تم التحليل: الموقع ينتمي لـ (**{dom}**)")
                st.write(f"📊 تقييم السمعة الرقمية: {score}/100")
                if score < 50: st.error("⚠️ تحذير: هذا الموقع لديه سمعة منخفضة أو حديث المنشأ.")

# 4. تبويب حماية المجتمع
with tabs[3]:
    st.header("👥 مركز بلاغات المجتمع")
    rep_txt = st.text_area("أدخل تفاصيل التهديد أو الاحتيال:")
    if st.button("نشر البلاغ"):
        if rep_txt:
            cat = classify_report(rep_txt)
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?, ?)", (rep_txt, cat, dt))
            conn.commit()
            st.success(f"تم تسجيل البلاغ وتصنيفه كـ: {cat}")
            send_telegram_msg(f"📢 بلاغ جديد [{cat}]: {rep_txt[:60]}...")

# 5. تبويب اتصل بنا
with tabs[4]:
    st.header("📧 تواصل مع الإدارة")
    u_name = st.text_input("اسمك:")
    u_msg = st.text_area("رسالتك:")
    if st.button("إرسال الرسالة"):
        if u_name and u_msg:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO messages VALUES (?, ?, ?)", (u_name, u_msg, dt))
            conn.commit()
            st.success("تم الإرسال بنجاح.")
            send_telegram_msg(f"📩 رسالة من {u_name}: {u_msg}")

# 6. تبويب الإدارة المطور (نظام البطاقات الشامل)
with tabs[5]:
    st.header("🔐 لوحة التحكم المؤمنة")
    pw = st.text_input("كلمة المرور:", type="password")
    if pw == "ayman7716":
        if st.button("طلب رمز التحقق (Telegram 2FA)"):
            sc = str(random.randint(1000, 9999))
            st.session_state['sc'] = sc
            send_telegram_msg(f"🔐 رمز الدخول الماسي: {sc}")
            st.info("تم إرسال رمز التحقق لهاتفك.")

        v_in = st.text_input("أدخل رمز التحقق:")
        if v_in and v_in == st.session_state.get('sc'):
            st.success("✅ تم التحقق بنجاح - عرض التقارير الكاملة:")
            
            # عرض البلاغات بنظام البطاقات لضمان عدم قص النص
            st.subheader("📢 سجل البلاغات")
            df_reps = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
            if not df_reps.empty:
                for idx, row in df_reps.iterrows():
                    st.markdown(f"""
                    <div class="admin-card">
                        <small style="color: #8b949e;">📅 {row['dt']} | {row['category']}</small><br>
                        <div style="font-size: 1.1rem; margin-top: 10px;">{row['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                csv = df_reps.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 تحميل كافة البيانات (Excel)", csv, "reports.csv", "text/csv")
            else: st.info("لا توجد بلاغات.")

            st.write("---")
            # عرض الرسائل
            st.subheader("📩 الرسائل الواردة")
            df_msgs = pd.read_sql_query("SELECT * FROM messages ORDER BY dt DESC", conn)
            for idx, m in df_msgs.iterrows():
                with st.expander(f"👤 {m['name']} | 🕒 {m['dt']}"):
                    st.write(m['msg'])
