import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
import random
from datetime import datetime

# --- 1. الإعدادات الأمنية والمواقع الموثوقة ---
TELEGRAM_TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240" 
VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce" 

# القائمة البيضاء لمنع البلاغات الكاذبة
WHITELIST = ["google.com", "youtube.com", "facebook.com", "whatsapp.com", "microsoft.com", "apple.com", "instagram.com"]

def send_telegram_msg(message):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except: pass

# --- 2. قاعدة البيانات (هيكل مصلح تماماً) ---
# ملاحظة: تم تغيير اسم الملف لضمان إنشاء جداول نظيفة بدون أخطاء سابقة
db = sqlite3.connect('aiman_final_ultra.db', check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, report_date TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, msg_date TEXT)")
db.commit()

# --- 3. تصميم الواجهة (محاذاة وألوان مريحة) ---
st.set_page_config(page_title="درع أيمن v16", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { text-align: center; color: #58a6ff; font-size: 2.2rem; font-weight: bold; padding: 10px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 5px; border-radius: 10px; direction: RTL; }
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
    /* تحسين عرض الجداول على الجوال */
    div[data-testimonial="true"] { direction: RTL !important; }
    .stDataFrame { width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي</div>', unsafe_allow_html=True)

tabs = st.tabs(["🔍 فحص ذكي", "🔗 فحص الروابط", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# قسم البلاغات (إدخال البيانات)
with tabs[2]:
    st.subheader("👥 بلاغات المجتمع")
    rep_text = st.text_area("أدخل تفاصيل الرابط أو الملف الاحتيالي:")
    if st.button("نشر وتحذير المجتمع"):
        if rep_text:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            db.execute("INSERT INTO reports VALUES (?, ?)", (rep_text, current_time))
            db.commit()
            st.success(f"تم تسجيل البلاغ في {current_time}")

# قسم الإدارة (المعدل لإظهار المعلومات كاملة)
with tabs[4]:
    st.subheader("🔐 لوحة التحكم الإدارية")
    # كلمة المرور كما في صورتك
    pwd = st.text_input("كلمة المرور:", type="password", value="ayman7716")
    
    if pwd == "ayman7716":
        if st.button("إرسال كود التحقق (Telegram)"):
            v_code = str(random.randint(1000, 9999))
            st.session_state['auth_code'] = v_code
            send_telegram_msg(f"🔐 كود الدخول الخاص بك: {v_code}")
            st.info("تم إرسال الكود.")

        user_v = st.text_input("أدخل كود التحقق:")
        if user_v and user_v == st.session_state.get('auth_code'):
            st.success("✅ تم التحقق بنجاح!")
            
            # --- عرض البلاغات بشكل كامل [إصلاح مشكلة الصورة 1000566704.jpg] ---
            st.write("### 📢 سجل البلاغات الكامل")
            reps_query = db.execute("SELECT content as 'المحتوى', report_date as 'التاريخ' FROM reports ORDER BY report_date DESC").fetchall()
            
            if reps_query:
                df = pd.DataFrame(reps_query, columns=["المحتوى", "التاريخ"])
                # استخدام dataframe مع توسيع العرض ليظهر التاريخ كاملاً
                st.dataframe(df, use_container_width=True)
                
                # ميزة التحميل (CSV تعمل كـ Excel وتظهر كل البيانات)
                csv_data = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 تحميل التقرير الكامل (Excel/CSV)", csv_data, "aiman_reports.csv", "text/csv")
            else:
                st.info("لا توجد بلاغات مسجلة.")

            # عرض الرسائل
            st.write("---")
            st.write("### 📩 صندوق الرسائل")
            msgs = db.execute("SELECT * FROM messages ORDER BY msg_date DESC").fetchall()
            for m in msgs:
                st.warning(f"👤 **المرسل:** {m[0]} | 🕒 **التاريخ:** {m[2]}\n\n**الرسالة:** {m[1]}")
