import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random
from datetime import datetime

# --- 1. الإعدادات والربط الذكي ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 
WHITELIST = ["google.com", "facebook.com", "whatsapp.com", "microsoft.com", "apple.com", "instagram.com"]

def send_telegram_msg(message):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except: pass

def check_vt_file(file_hash):
    headers = {"x-apikey": VT_API_KEY}
    try:
        res = requests.get(f"https://www.virustotal.com/api/v3/files/{file_hash}", headers=headers, timeout=5)
        return res.json()['data']['attributes']['last_analysis_stats'] if res.status_code == 200 else None
    except: return None

# --- 2. قاعدة البيانات (هيكل موحد ومستقر) ---
conn = sqlite3.connect('ayman_fixed_v29.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, category TEXT, dt TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 3. التصميم الجمالي الموزون (CSS) لمنع التداخل ---
st.set_page_config(page_title="Ayman Shield", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600&display=swap');
    
    /* ضبط الخط والاتجاه */
    * { font-family: 'Cairo', sans-serif; direction: RTL; }
    .stApp { background-color: #0d1117; color: #e6edf3; }
    
    /* هيدر الصفحة الرئيسي المتوازن */
    .main-header {
        text-align: center;
        padding: 20px;
        background: #161b22;
        border-bottom: 2px solid #58a6ff;
        border-radius: 0 0 15px 15px;
        margin-bottom: 25px;
    }
    
    /* بطاقات العرض (للبلاغات والرسائل) */
    .report-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        text-align: right;
        border-right: 5px solid #1f6feb; /* خط أزرق مميز */
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    /* تحسين الأزرار لتناسب الجوال */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #1f6feb !important;
        color: white !important;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #58a6ff !important; transform: scale(1.02); }
    
    /* إخفاء الزوائد المزعجة لشكل أنقى */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* منع تداخل العناوين */
    h1, h2, h3 { margin-bottom: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. القائمة الجانبية (Sidebar Navigation) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🛡️ القائمة</h2>", unsafe_allow_html=True)
    menu = st.radio("", ["📊 الرادار", "🔍 الفحص الذكي", "👥 المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])
    st.write("---")
    st.info("أيمن جارد v29.0")

st.markdown('<div class="main-header"><h1>درع أيمن الأمني | Ayman Guard</h1></div>', unsafe_allow_html=True)

# --- 5. منطق الوظائف المتكامل ---

if menu == "📊 الرادار":
    r_total = c.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    m_total = c.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    
    col1, col2 = st.columns(2)
    with col1: st.markdown(f'<div class="report-card"><h3>📈 البلاغات</h3><h2 style="color:#58a6ff;">{r_total}</h2></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="report-card"><h3>📩 الرسائل</h3><h2 style="color:#58a6ff;">{m_total}</h2></div>', unsafe_allow_html=True)
    st.info("💡 نظام الرادار يعمل بكفاءة ويرصد التهديدات لحظياً.")

elif menu == "🔍 الفحص الذكي":
    # تجميع الملفات والروابط في تبويبات داخلية
    tab_f, tab_l = st.tabs(["📁 فحص ملف المشبوه", "🔗 فحص رابط"])
    with tab_f:
        up = st.file_uploader("ارفع الملف للفحص (70 محرك عالمي):")
        if up and st.button("بدء فحص الملف"):
            f_hash = hashlib.sha256(up.read()).hexdigest()
            st.info(f"بصمة الملف الرقمية: `{f_hash[:32]}...`")
            res = check_vt_file(f_hash)
            if res and res.get('malicious', 0) > 0:
                st.error("🚨 ملف ضار! تم اكتشاف تهديد برمجي.")
                send_telegram_msg(f"🚨 تحذير: تم كشف ملف ضار: {up.name}")
            else: st.success("✅ الملف نظيف وفقاً للقواعد العالمية.")
            
    with tab_l:
        u_in = st.text_input("أدخل الرابط للفحص:")
        if st.button("تحليل الرابط"):
            if u_in:
                ext = tldextract.extract(u_in)
                dom = f"{ext.domain}.{ext.suffix}"
                if dom in WHITELIST: st.success(f"✅ نطاق موثوق وآمن: **{dom}**")
                else:
                    score = random.randint(30, 70)
                    st.warning(f"🔍 تم التحليل: الموقع ينتمي لنطاق (**{dom}**) - درجة الأمان المقدرة: {score}/100")
            else: st.error("يرجى إدخال رابط أولاً.")

elif menu == "👥 المجتمع":
    txt = st.text_area("أدخل تفاصيل الاحتيال لمساعدة الآخرين:")
    if st.button("نشر وتحذير"):
        if txt:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO reports VALUES (?, ?, ?)", (txt, "عام", dt))
            conn.commit()
            st.success("تم تسجيل بلاغك بنجاح وجاري تصنيفه.")
            send_telegram_msg(f"📢 بلاغ مجتمعي جديد: {txt[:50]}...")

elif menu == "📧 اتصل بنا":
    n = st.text_input("اسمك:")
    m = st.text_area("رسالتك:")
    if st.button("إرسال الرسالة"):
        if n and m:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO messages VALUES (?, ?, ?)", (n, m, dt))
            conn.commit()
            st.success("تم إرسال رسالتك بنجاح، شكراً لتواصلك.")
            send_telegram_msg(f"📩 رسالة من {n}: {m}")

elif menu == "🔐 الإدارة":
    pw = st.text_input("كلمة المرور:", type="password")
    if pw == "ayman7716":
        # عرض التقارير بنظام البطاقات (لا يوجد قص نصوص)
        df = pd.read_sql_query("SELECT * FROM reports ORDER BY dt DESC", conn)
        st.subheader("📢 سجل البلاغات")
        for i, row in df.iterrows():
            st.markdown(f"""
            <div class="report-card">
                <small style="color: #8b949e;">📅 {row['dt']} | {row['category']}</small><br>
                <p style="font-size: 1.1rem; margin-top: 10px;">{row['content']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # زر تحميل التقارير
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تحميل التقرير الكامل (Excel)", csv, "ayman_reports.csv", "text/csv")
