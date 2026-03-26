import streamlit as st
import tldextract, sqlite3, requests, hashlib, pandas as pd
from datetime import datetime
from io import BytesIO

# --- 1. الإعدادات الأمنية والمفاتيح ---
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

# --- 2. قاعدة البيانات الشاملة ---
db = sqlite3.connect('aiman_security_final.db', check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS reports (content TEXT, date TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, msg TEXT, date TEXT)")
db.commit()

# --- 3. التصميم المريح للعين (Deep Dark Mode) ---
st.set_page_config(page_title="درع أيمن الاحترافي", page_icon="🛡️")

st.markdown("""
    <style>
    /* ألوان هادئة ومريحة للعين */
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-title { text-align: center; color: #58a6ff; font-size: 2.3rem; font-weight: bold; margin-bottom: 20px; }
    
    /* تنسيق التبويبات كما في صورك */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 5px; background-color: #161b22; padding: 10px; border-radius: 12px; direction: RTL; 
    }
    .stTabs [aria-selected="true"] { 
        color: #58a6ff !important; border-bottom: 2px solid #58a6ff !important; 
    }

    /* الأزرار والحقول */
    .stButton>button { 
        background: #21262d; color: #58a6ff; border: 1px solid #30363d; 
        border-radius: 8px; width: 100%; transition: 0.3s; font-weight: bold;
    }
    input, textarea { 
        background-color: #010409 !important; color: #c9d1d9 !important; 
        border: 1px solid #30363d !important; border-radius: 6px !important;
    }
    
    /* توحيد المحاذاة للعربية */
    .main, p, h1, h2, h3, div, label { direction: RTL !important; text-align: right !important; }
    .stAlert { direction: RTL !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ درع أيمن الاحترافي</div>', unsafe_allow_html=True)

# --- 4. التبويبات المستوحاة من صورك ---
tabs = st.tabs(["🔍 فحص ذكي المطور", "🔗 فحص الروابط", "👥 حماية المجتمع", "📧 اتصل بنا", "🔐 الإدارة"])

# التبويب 1: الفحص الذكي (عالمي + محلي) كما في الصورة
with tabs[0]:
    st.subheader("📁 فحص الملفات (عالمي + محلي)")
    up_f = st.file_uploader("ارفع الملف للفحص الشامل:", type=None)
    if up_f:
        file_bytes = up_f.read()
        f_hash = hashlib.sha256(file_bytes).hexdigest()
        
        # عرض البصمة كما في الصورة
        st.info(f"🧬 **بصمة الملف الرقمية:**\n`{f_hash}`")
        
        with st.spinner('جاري التحليل...'):
            vt_res = check_vt_file(f_hash)
            # الكشف المحلي لكود EICAR
            is_local_threat = b"EICAR-STANDARD-ANTIVIRUS-TEST-FILE" in file_bytes
            
            if is_local_threat or (vt_res and vt_res.get('malicious', 0) > 0):
                st.error("🚨 **تحذير أمني:** تم اكتشاف تهديد في هذا الملف!")
                send_telegram_msg(f"🚨 تنبيه من الدرع: ملف ضار مكتشف!\nالاسم: {up_f.name}\nالبصمة: {f_hash[:15]}...")
            elif vt_res:
                st.success("✅ الملف نظيف ومسجل في القواعد العالمية.")
            else:
                # الرسالة التي ظهرت في صورك
                st.warning("⚠️ الملف لم يسبق رفعه عالمياً (فريد)، تعامل معه بحذر.")

# التبويب 2: فحص الروابط
with tabs[1]:
    st.subheader("🔗 كاشف الروابط المشبوهة")
    url_input = st.text_input("ألصق الرابط هنا:")
    if st.button("تحليل الرابط"):
        if url_input:
            ext = tldextract.extract(url_input)
            st.success(f"🔍 الموقع المكتشف: **{ext.domain}.{ext.suffix}**")
        else: st.warning("يرجى إدخال الرابط.")

# التبويب 3: حماية المجتمع
with tabs[2]:
    st.subheader("👥 بلاغات المجتمع")
    rep_text = st.text_area("أدخل تفاصيل الاحتيال المنشور:")
    if st.button("نشر وتحذير المجتمع"):
        if rep_text:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            db.execute("INSERT INTO reports VALUES (?, ?)", (rep_text, now))
            db.commit()
            send_telegram_msg(f"📢 بلاغ مجتمعي جديد: {rep_text}")
            st.success("تم تسجيل البلاغ بنجاح.")

# التبويب 4: اتصل بنا
with tabs[3]:
    st.subheader("📧 تواصل مباشر مع أيمن")
    user_n = st.text_input("الاسم:")
    user_m = st.text_area("رسالتك:")
    if st.button("إرسال"):
        if user_n and user_m:
            db.execute("INSERT INTO messages VALUES (?, ?, ?)", (user_n, user_m, datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.commit()
            send_telegram_msg(f"📩 رسالة من {user_n}: {user_m}")
            st.success("تم الإرسال!")

# التبويب 5: الإدارة (كما في الصورة)
with tabs[4]:
    st.subheader("🔐 لوحة التحكم الإدارية")
    # كلمة المرور التي تظهر في صورتك
    admin_pass = st.text_input("كلمة المرور:", type="password", value="ayman7716") 
    
    if admin_pass == "ayman7716":
        st.write("### 📢 بلاغات المجتمع الأخيرة")
        all_reps = db.execute("SELECT * FROM reports ORDER BY date DESC").fetchall()
        if all_reps:
            df_reps = pd.DataFrame(all_reps, columns=["البلاغ", "التاريخ"])
            st.dataframe(df_reps, use_container_width=True)
            
            # ميزة تصدير Excel الاحترافية
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_reps.to_excel(writer, index=False, sheet_name='البلاغات')
            st.download_button(label="📥 تحميل سجل البلاغات (Excel)", data=output.getvalue(), file_name="Ayman_Security_Reports.xlsx")
        
        st.write("---")
        st.write("### 📩 الرسائل الواردة")
        for m in db.execute("SELECT * FROM messages ORDER BY dt DESC").fetchall():
            st.info(f"👤 {m[0]} | 🕒 {m[2]}\n\n{m[1]}")
