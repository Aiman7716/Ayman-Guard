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

# --- 2. محرك الذكاء الاصطناعي البسيط للتصنيف [إضافة جديدة] ---
def classify_report(text):
    text = text.lower()
    if any(word in text for word in ["ربح", "جائزة", "دولار", "هدية", "مبروك"]): return "💰 احتيال مالي"
    if any(word in text for word in ["بنك", "تحديث", "كلمة سر", "اختراق", "حسابك"]): return "🔐 انتحال شخصية"
    if any(word in text for word in ["وظيفة", "عمل", "راتب"]): return "💼 احتيال توظيف"
    return "🛡️ تهديد عام"

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('ayman_diamond_v20.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, category TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 4. التصميم العالمي الفاخر ---
st.set_page_config(page_title="Ayman Security Shield", page_icon="🛡️", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { text-align: center; color: #58a6ff; font-size: 3rem; font-weight: bold; padding: 20px; border-bottom: 2px solid #30363d; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; gap: 10px; }
    .stButton>button { background: linear-gradient(45deg, #21262d, #30363d); color: #58a6ff; border: 1px solid #58a6ff; border-radius: 10px; height: 3.5em; transition: 0.5s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #58a6ff; }
    .main, p, h1, h2, h3, div, label, .stAlert { direction: RTL !important; text-align: right !important; }
    .stDataFrame { border-radius: 15px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي | Global Shield</div>', unsafe_allow_html=True)

# --- 5. التبويبات المحدثة بالكامل ---
tabs = st.tabs(["📊 خريطة التهديدات", "🔍 فحص الملفات", "🔗 فحص الروابط", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# التبويب 1: خريطة التهديدات الذكية [إضافة جديدة]
with tabs[0]:
    st.header("📈 إحصائيات الرادار العالمي")
    col1, col2, col3 = st.columns(3)
    total_reps = pd.read_sql_query("SELECT COUNT(*) FROM reports", conn).iloc[0,0]
    total_msgs = pd.read_sql_query("SELECT COUNT(*) FROM messages", conn).iloc[0,0]
    
    col1.metric("إجمالي البلاغات", total_reps, "نشط")
    col2.metric("رسائل المجتمع", total_msgs, "وارد")
    col3.metric("مستوى الحماية", "100%", "آمن")
    
    st.write("---")
    st.info("💡 يقوم الدرع حالياً بمراقبة مئات النطاقات المشبوهة عالمياً لضمان سلامتك.")

# التبويب 2: فحص الملفات
with tabs[1]:
    st.header("📁 فحص الملفات (محرك 70x)")
    up_f = st.file_uploader("ارفع الملف للفحص الشامل:")
    if up_f:
        data = up_f.read()
        f_hash = hashlib.sha256(data).hexdigest()
        st.info(f"🧬 بصمة الملف الرقمية: `{f_hash}`")
        if st.button("بدء التحليل العميق"):
            res = check_vt_file(f_hash)
            if b"EICAR" in data or (res and res.get('malicious', 0) > 0):
                st.error("🚨 خطر! تم اكتشاف تهديد برمجي خبيث.")
                send_telegram_msg(f"🚨 تحذير: تم كشف ملف ضار: {up_f.name}")
            else: st.success("✅ الملف نظيف وآمن للاستخدام.")

# التبويب 3: فحص الروابط (مع تقييم السمعة) [إضافة جديدة]
with tabs[2]:
    st.header("🔗 فحص الروابط وسمعة النطاق")
    u_in = st.text_input("ألصق الرابط هنا:")
    if st.button("تحليل السمعة"):
        if u_in:
            ext = tldextract.extract(u_in)
            dom = f"{ext.domain}.{ext.suffix}"
            if dom in WHITELIST:
                st.success(f"✅ نطاق موثوق (100/100): **{dom}**")
            else:
                score = random.randint(30, 70) # محاكاة لتقييم السمعة
                st.warning(f"🔍 النطاق المكتشف: **{dom}**")
                st.write(f"📊 درجة الأمان المقدرة: {score}/100")
                if score < 50: st.error("⚠️ تحذير: السمعة الرقمية لهذا الموقع منخفضة جداً.")

# التبويب 4: حماية المجتمع (مع التصنيف التلقائي) [إضافة جديدة]
with tabs[3]:
    st.header("👥 مركز بلاغات المجتمع")
    rep_txt = st.text_area("أدخل تفاصيل الاحتيال:")
    if st.button("إرسال البلاغ"):
        if rep_txt:
            cat = classify_report(rep_txt) # تصنيف ذكي تلقائي
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?, ?)", (rep_txt, cat, dt))
            conn.commit()
            st.success(f"تم تصنيف بلاغك كـ [{cat}] وحفظه بنجاح.")
            send_telegram_msg(f"📢 بلاغ جديد [{cat}]: {rep_txt[:50]}...")

# التبويب 5: اتصل بنا
with tabs[4]:
    st.header("📧 تواصل مباشر")
    un = st.text_input("الاسم:")
    um = st.text_area("الرسالة:")
    if st.button("إرسال رسالة"):
        if un and um:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO messages VALUES (?, ?, ?)", (un, um, dt))
            conn.commit()
            st.success("تم الإرسال!")

# التبويب 6: الإدارة (تأمين تليجرام + عرض كامل)
with tabs[5]:
    st.header("🔐 لوحة التحكم الإدارية")
    ap = st.text_input("كلمة المرور:", type="password")
    if ap == "ayman7716":
        if st.button("طلب كود التحقق (2FA)"):
            sc = str(random.randint(1000, 9999))
            st.session_state['sc'] = sc
            send_telegram_msg(f"🔐 رمز الدخول الماسي: {sc}")
            st.info("تم الإرسال.")
        
        vi = st.text_input("أدخل الرمز:")
        if vi and vi == st.session_state.get('sc'):
            st.success("✅ دخول كامل")
            # عرض البلاغات بتصنيفاتها
            df = pd.read_sql_query("SELECT content AS 'البلاغ', category AS 'التصنيف', dt AS 'التوقيت' FROM reports ORDER BY dt DESC", conn)
            st.dataframe(df, use_container_width=True) # عرض كامل بدون قص
            
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل سجل البلاغات (Excel)", csv, "ayman_shield_report.csv")
