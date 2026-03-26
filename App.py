import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random, time
from datetime import datetime
from io import BytesIO

# --- 1. الإعدادات الأمنية والمفاتيح ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

# القائمة البيضاء العالمية (Whitelist)
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
        if res.status_code == 200:
            return res.json()['data']['attributes']['last_analysis_stats']
    except: return None
    return None

# --- 2. قاعدة البيانات (هيكل احترافي) ---
conn = sqlite3.connect('ayman_shield_global.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 3. تصميم الواجهة العالمي (Professional Dark UI) ---
st.set_page_config(page_title="Ayman Security Shield", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { text-align: center; color: #58a6ff; font-size: 2.8rem; font-weight: bold; padding: 15px; border-bottom: 2px solid #30363d; margin-bottom: 25px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; gap: 10px; }
    .stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom: 2px solid #58a6ff !important; }
    .stButton>button { background: #21262d; color: #58a6ff; border: 1px solid #30363d; border-radius: 8px; font-weight: bold; height: 3.5em; transition: 0.3s; }
    .stButton>button:hover { border-color: #58a6ff; background: #30363d; }
    .main, p, h1, h2, h3, div, label, .stAlert { direction: RTL !important; text-align: right !important; }
    /* تحسين عرض الجداول والتقارير */
    .stDataFrame { border: 1px solid #30363d; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي | Ayman Security Shield</div>', unsafe_allow_html=True)

# --- 4. نظام التبويبات المتكامل ---
tabs = st.tabs(["🔍 فحص الملفات", "🔗 فحص الروابط", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# التبويب 1: فحص الملفات الذكي
with tabs[0]:
    st.header("📁 نظام الفحص العالمي للملفات")
    up_file = st.file_uploader("ارفع الملف المشبوه (سيتم تحليله عبر 70 محرك حماية):", type=None)
    if up_file:
        file_bytes = up_file.read()
        f_hash = hashlib.sha256(file_bytes).hexdigest()
        st.info(f"🧬 بصمة الملف الرقمية: `{f_hash}`")
        
        if st.button("تأكيد وفحص الملف"):
            with st.spinner('جاري التحليل العميق...'):
                res = check_vt_file(f_hash)
                # كشف محلي + عالمي
                if b"EICAR" in file_bytes or (res and res.get('malicious', 0) > 0):
                    st.error("🚨 خطر! تم اكتشاف برمجيات خبيثة.")
                    send_telegram_msg(f"🚨 تنبيه أمني: تم كشف ملف ضار!\nالاسم: {up_file.name}")
                elif res:
                    st.success("✅ الملف نظيف تماماً وفقاً للقواعد العالمية.")
                else:
                    st.warning("⚠️ الملف جديد (لم يسبق تحليله عالمياً)، يرجى توخي الحذر.")

# التبويب 2: فحص الروابط (مع القائمة البيضاء المحدثة)
with tabs[1]:
    st.header("🔗 كاشف الروابط المتقدم")
    url_input = st.text_input("ألصق الرابط المشبوه هنا:")
    if st.button("تحليل الرابط الآن"):
        if url_input:
            ext = tldextract.extract(url_input)
            domain = f"{ext.domain}.{ext.suffix}"
            if domain in WHITELIST:
                st.success(f"✅ هذا الموقع ضمن القائمة البيضاء الموثوقة: **{domain}**")
            else:
                st.warning(f"🔍 تم التحليل: الرابط ينتمي لنطاق (**{domain}**). يرجى التأكد قبل فتحه.")
        else: st.error("يرجى إدخال الرابط أولاً.")

# التبويب 3: حماية المجتمع
with tabs[2]:
    st.header("👥 قاعدة بيانات بلاغات المجتمع")
    rep_content = st.text_area("أدخل تفاصيل الاحتيال المكتشف لمساعدة الآخرين:")
    if st.button("نشر البلاغ وتحذير الجميع"):
        if rep_content:
            dt_now = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?)", (rep_content, dt_now))
            conn.commit()
            st.success("تم تسجيل البلاغ بنجاح في السجل العام.")
            send_telegram_msg(f"📢 بلاغ مجتمعي جديد: {rep_content}")

# التبويب 4: اتصل بنا
with tabs[3]:
    st.header("📧 تواصل مع المطور")
    u_name = st.text_input("اسمك:")
    u_msg = st.text_area("رسالتك أو اقتراحك:")
    if st.button("إرسال الرسالة للإدارة"):
        if u_name and u_msg:
            dt_now = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO messages VALUES (?, ?, ?)", (u_name, u_msg, dt_now))
            conn.commit()
            st.success("تم إرسال رسالتك بنجاح، شكراً لتواصلك.")
            send_telegram_msg(f"📩 رسالة من {u_name}: {u_msg}")

# التبويب 5: الإدارة (تأمين تليجرام المزدوج + التقرير الكامل)
with tabs[4]:
    st.header("🔐 لوحة التحكم الإدارية المؤمنة")
    admin_pass = st.text_input("كلمة مرور النظام:", type="password")
    
    if admin_pass == "ayman7716":
        # نظام التأمين المزدوج
        if st.button("طلب كود التحقق (Telegram 2FA)"):
            secure_code = str(random.randint(1000, 9999))
            st.session_state['secure_code'] = secure_code
            send_telegram_msg(f"🔐 رمز الدخول الخاص بك: {secure_code}")
            st.info("تم إرسال رمز التحقق إلى جوالك عبر تليجرام.")

        v_input = st.text_input("أدخل رمز التحقق المكون من 4 أرقام:")
        
        if v_input and v_input == st.session_state.get('secure_code'):
            st.success("✅ تم الدخول بنجاح! جاري استرجاع كافة البيانات...")
            
            # عرض البلاغات (كاملة وبدون قص)
            st.subheader("📢 البلاغات المجتمع المسجلة")
            df_reps = pd.read_sql_query("SELECT content AS 'البلاغ الكامل', dt AS 'التاريخ' FROM reports ORDER BY dt DESC", conn)
            if not df_reps.empty:
                st.dataframe(df_reps, use_container_width=True)
                csv = df_reps.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 تحميل التقرير الشامل (CSV/Excel)", csv, "ayman_security_report.csv", "text/csv")
            else: st.info("لا توجد بلاغات حالياً.")

            st.write("---")
            # عرض الرسائل في بطاقات منسدلة
            st.subheader("📩 صندوق الرسائل الواردة")
            df_msgs = pd.read_sql_query("SELECT * FROM messages ORDER BY dt DESC", conn).values.tolist()
            if df_msgs:
                for m in df_msgs:
                    with st.expander(f"👤 من: {m[0]} | 📅 {m[2]}"):
                        st.write(m[1])
            else: st.info("لا توجد رسائل.")
        elif v_input:
            st.error("❌ رمز التحقق خاطئ!")
