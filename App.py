import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random
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

# --- 2. الرادار المحلي (كشف الأنماط المشبوهة) ---
def local_radar_scan(content):
    # قائمة بكلمات تدل على محاولات اختراق أو أكواد خبيثة
    danger_patterns = [b"DROP TABLE", b"SELECT * FROM users", b"os.system", b"subprocess.Popen", b"eval(", b"exec("]
    found_threats = []
    for pattern in danger_patterns:
        if pattern in content:
            found_threats.append(pattern.decode())
    return found_threats

# --- 3. قاعدة البيانات ---
db = sqlite3.connect('aiman_v12_pro.db', check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, dt TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, dt TEXT)")
db.commit()

# --- 4. التصميم الاحترافي الهادئ ---
st.set_page_config(page_title="درع أيمن v12 Pro", page_icon="🛡️")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { text-align: center; color: #58a6ff; font-size: 2.5rem; font-weight: bold; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stButton>button { background: #21262d; color: #58a6ff; border: 1px solid #30363d; border-radius: 8px; width: 100%; }
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي Pro</div>', unsafe_allow_html=True)

tabs = st.tabs(["🔍 الفحص الذكي", "🔗 فحص الروابط", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# تبويب الفحص (تمت إضافة الرادار المحلي)
with tabs[0]:
    st.subheader("📁 فحص الملفات (عالمي + رادار محلي)")
    up_f = st.file_uploader("ارفع الملف للفحص:")
    if up_f:
        data = up_f.read()
        f_hash = hashlib.sha256(data).hexdigest()
        st.info(f"🧬 البصمة: `{f_hash[:30]}...`")
        
        # 1. الرادار المحلي
        local_threats = local_radar_scan(data)
        # 2. الفحص العالمي
        vt_res = check_vt_file(f_hash)
        
        if b"EICAR" in data or local_threats or (vt_res and vt_res.get('malicious', 0) > 0):
            st.error(f"🚨 تحذير: تم اكتشاف تهديد! {f' (أنماط مشبوهة: {local_threats})' if local_threats else ''}")
            send_telegram_msg(f"🚨 إنذار أمني!\nتم كشف ملف ضار: {up_f.name}\nالبصمة: {f_hash[:10]}")
        elif vt_res: st.success("✅ الملف نظيف عالمياً.")
        else: st.warning("⚠️ ملف جديد كلياً، لم يسبق رفعه.")

# تبويب الروابط
with tabs[1]:
    st.subheader("🔗 كاشف الروابط")
    url = st.text_input("ألصق الرابط:")
    if st.button("تحليل"):
        if url:
            ext = tldextract.extract(url)
            st.success(f"🔍 النطاق: **{ext.domain}.{ext.suffix}**")

# تبويب المجتمع
with tabs[2]:
    st.subheader("👥 بلاغات المجتمع")
    rep = st.text_area("تفاصيل البلاغ:")
    if st.button("نشر"):
        if rep:
            db.execute("INSERT INTO reports VALUES (?, ?)", (rep, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            st.success("تم النشر.")

# تبويب اتصل بنا
with tabs[3]:
    st.subheader("📧 اتصل بنا")
    n = st.text_input("الاسم:")
    m = st.text_area("الرسالة:")
    if st.button("إرسال"):
        if n and m:
            db.execute("INSERT INTO messages VALUES (?, ?, ?)", (n, m, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            send_telegram_msg(f"📩 رسالة من {n}: {m}")
            st.success("تم الإرسال.")

# تبويب الإدارة (التحقق بخطوتين عبر تليجرام)
with tabs[4]:
    st.subheader("🔐 لوحة التحكم المؤمنة")
    # مرحلة 1: كلمة المرور
    adm_pwd = st.text_input("كلمة المرور الإدارية:", type="password")
    
    if adm_pwd == "ayman7716":
        # زر لإرسال كود التحقق لتليجرام
        if st.button("إرسال كود التحقق إلى تليجرام"):
            v_code = str(random.randint(1000, 9999))
            st.session_state['v_code'] = v_code
            send_telegram_msg(f"🔐 كود الدخول لدرع أيمن هو: {v_code}")
            st.info("تم إرسال كود التحقق لجوالك عبر تليجرام.")
        
        # إدخال الكود
        user_code = st.text_input("أدخل الكود المرسل لتليجرام:")
        if user_code and user_code == st.session_state.get('v_code'):
            st.success("✅ تم التحقق بنجاح!")
            # عرض البيانات وتصدير Excel
            all_reps = db.execute("SELECT * FROM reports ORDER BY dt DESC").fetchall()
            if all_reps:
                df = pd.DataFrame(all_reps, columns=["البلاغ", "التاريخ"])
                st.dataframe(df)
                
                buf = BytesIO()
                with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
                    df.to_excel(wr, index=False)
                st.download_button("📥 تحميل سجل البلاغات (Excel)", buf.getvalue(), "aiman_reports.xlsx")
