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

# --- 2. قاعدة بيانات جديدة تماماً لتجنب خطأ الصور ---
db = sqlite3.connect('aiman_pro_final_v13.db', check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, time_stamp TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, time_stamp TEXT)")
db.commit()

# --- 3. التصميم الاحترافي الهادئ ---
st.set_page_config(page_title="درع أيمن v13 PRO", page_icon="🛡️")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { text-align: center; color: #58a6ff; font-size: 2.5rem; font-weight: bold; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stButton>button { background: #21262d; color: #58a6ff; border: 1px solid #30363d; border-radius: 8px; width: 100%; }
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي PRO</div>', unsafe_allow_html=True)

tabs = st.tabs(["🔍 الفحص الذكي", "🔗 فحص الروابط", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# التبويبات (روابط، ملفات، مجتمع، تواصل)
with tabs[2]:
    st.subheader("👥 بلاغات المجتمع")
    rep = st.text_area("تفاصيل البلاغ:")
    if st.button("نشر البلاغ"):
        if rep:
            db.execute("INSERT INTO reports VALUES (?, ?)", (rep, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            st.success("تم تسجيل البلاغ!")

with tabs[3]:
    st.subheader("📧 اتصل بنا")
    n = st.text_input("الاسم:")
    m = st.text_area("الرسالة:")
    if st.button("إرسال الرسالة"):
        if n and m:
            db.execute("INSERT INTO messages VALUES (?, ?, ?)", (n, m, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            st.success("تم الإرسال!")

# --- 4. تبويب الإدارة المصلح بالكامل ---
with tabs[4]:
    st.subheader("🔐 لوحة التحكم المؤمنة")
    adm_pwd = st.text_input("كلمة المرور الإدارية:", type="password", value="ayman7716")
    
    if adm_pwd == "ayman7716":
        # زر التحقق عبر تليجرام
        if st.button("إرسال كود التحقق إلى تليجرام"):
            v_code = str(random.randint(1000, 9999))
            st.session_state['v_code'] = v_code
            send_telegram_msg(f"🔐 كود الدخول للإدارة هو: {v_code}")
            st.info("تم إرسال الكود.")

        user_code = st.text_input("أدخل الكود المرسل لتليجرام:")
        # تم التحقق بنجاح
        if user_code and user_code == st.session_state.get('v_code'):
            st.success("✅ تم التحقق بنجاح! جاري عرض البيانات...")
            
            # عرض البلاغات المفقودة في الصورة
            st.write("---")
            st.write("### 📢 بلاغات المجتمع الأخيرة")
            reps_data = db.execute("SELECT * FROM reports ORDER BY time_stamp DESC").fetchall()
            if reps_data:
                df_reps = pd.DataFrame(reps_data, columns=["المحتوى", "التوقيت"])
                st.table(df_reps)
                
                # تصدير Excel
                buf = BytesIO()
                with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
                    df_reps.to_excel(wr, index=False)
                st.download_button("📥 تحميل سجل البلاغات (Excel)", buf.getvalue(), "reports.xlsx")
            else: st.info("لا توجد بلاغات حالياً.")

            st.write("---")
            st.write("### 📩 الرسائل الواردة")
            msgs_data = db.execute("SELECT * FROM messages ORDER BY time_stamp DESC").fetchall()
            if msgs_data:
                for msg in msgs_data:
                    st.info(f"👤 {msg[0]} | 🕒 {msg[2]}\n\n{msg[1]}")
            else: st.info("لا توجد رسائل حالياً.")
