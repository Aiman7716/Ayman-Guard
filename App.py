import streamlit as st
import tldextract
import sqlite3
import random
import time
from datetime import datetime

# --- 1. تحسين مظهر التطبيق والإعدادات ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# كود التصميم الاحترافي (CSS)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; }
        .main { background: linear-gradient(180deg, #0e1117 0%, #07090c 100%); }
        .stButton>button { 
            width: 100%; border-radius: 20px; background: #00d4ff; 
            color: black; font-weight: bold; border: none; height: 3.5em;
            transition: 0.3s;
        }
        .stButton>button:hover { background: #00b8e6; transform: scale(1.02); }
        .report-card { 
            background: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; 
            border-radius: 15px; padding: 15px; margin-bottom: 10px; 
        }
        .official-btn { 
            background: #1a1c24; border: 1px solid #00d4ff; color: #00d4ff !important; 
            padding: 10px; border-radius: 12px; text-decoration: none; 
            display: block; text-align: center; margin: 5px; font-weight: bold; 
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك قاعدة البيانات (تم تغيير الاسم لحل مشكلة OperationalError) ---
def init_db():
    # تغيير اسم الملف إلى ayman_v5.db يحل مشكلة التعارض تماماً
    conn = sqlite3.connect('ayman_v5.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS reports (url TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS stats (count INTEGER)')
    c.execute('INSERT OR IGNORE INTO stats (rowid, count) SELECT 1, 250 WHERE NOT EXISTS (SELECT 1 FROM stats)')
    conn.commit()
    conn.close()

def db_action(query, val=None, fetch=True):
    conn = sqlite3.connect('ayman_v5.db')
    c = conn.cursor()
    if val: c.execute(query, val)
    else: c.execute(query)
    res = c.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return res

init_db()

# --- 3. لوحة تحكم المدير (القائمة الجانبية) ---
with st.sidebar:
    st.markdown("### 🔐 لوحة تحكم أيمن")
    admin_pw = st.text_input("كلمة المرور:", type="password")
    if admin_pw == "ayman123":
        st.success("تم تسجيل الدخول")
        if st.button("🗑️ تنظيف سجل البلاغات"):
            db_action("DELETE FROM reports", fetch=False)
            st.toast("تم مسح السجل!")
        
        new_stat = st.number_input("تعديل العداد يدوياً:", value=250)
        if st.button("⚙️ تحديث الإحصائيات"):
            db_action("UPDATE stats SET count = ?", (new_stat,), fetch=False)
            st.rerun()

# --- 4. واجهة المستخدم الرئيسية ---
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🛡️ درع أيمن الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>نظام الحماية المتقدم ضد الروابط المشبوهة</p>", unsafe_allow_html=True)

# محرك الفحص الذكي
url_input = st.text_input("🔍 الصق الرابط هنا لفحصه الآن:", placeholder="https://example.com")
if st.button("🚀 اطلق الدرع"):
    db_action("UPDATE stats SET count = count + 1", fetch=False)
    if url_input:
        with st.spinner('جاري تحليل الرابط...'):
            time.sleep(1)
            ext = tldextract.extract(url_input.lower())
            domain = f"{ext.domain}.{ext.suffix}"
            
            if domain in ['absher.sa', 'iam.gov.sa', 'google.com', 'splonline.com.sa', 'moe.gov.sa']:
                st.balloons()
                st.success(f"✅ رابط آمن: هذا موقع رسمي موثق ({domain})")
            elif ext.suffix in ['tk', 'xyz', 'ml', 'cf', 'gq']:
                st.error("🚨 خطر! تم اكتشاف نطاق وهمي يستخدم غالباً في الاحتيال.")
            else:
                st.info(f"ℹ️ نتيجة الفحص: الرابط ينتمي للنطاق ({domain}). تأكد من المصدر قبل فتحه.")
    else:
        st.warning("⚠️ يرجى إدخال الرابط أولاً.")

# قسم البلاغات
st.markdown("---")
st.subheader("📢 بلاغات المجتمع")
with st.expander("🚩 أبلغ عن رابط احتيالي جديد"):
    new_scam = st.text_input("أدخل الرابط المشبوه:")
    if st.button("تأكيد وإرسال"):
        if new_scam and "." in new_scam:
            db_action("INSERT INTO reports VALUES (?, ?)", (new_scam, datetime.now().strftime("%Y-%m-%d")), fetch=False)
            st.success("شكرًا لك! تم تسجيل البلاغ بنجاح.")
        else:
            st.error("الرابط غير صحيح.")

# عرض البلاغات بتصميم البطاقات
latest_reps = db_action("SELECT url FROM reports ORDER BY rowid DESC LIMIT 3")
for r in latest_reps:
    st.markdown(f"<div class='report-card'>⚠️ <b>تم التبليغ عن:</b> <code>{r[0]}</code></div>", unsafe_allow_html=True)

# الروابط الرسمية الموثقة
st.markdown("---")
st.markdown("<h4 style='text-align: center;'>🏛️ مراجع رسمية آمنة</h4>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown("<a href='https://absher.sa' class='official-btn'>🇸🇦 أبشر</a>", unsafe_allow_html=True)
with c2: st.markdown("<a href='https://iam.gov.sa' class='official-btn'>🔑 نفاذ</a>", unsafe_allow_html=True)
with c3: st.markdown("<a href='https://splonline.com.sa' class='official-btn'>📦 البريد</a>", unsafe_allow_html=True)

# التذييل والإحصائيات
st.markdown("---")
current_count = db_action("SELECT count FROM stats")[0][0]
st.markdown(f"<p style='text-align: center;'>📊 إجمالي العمليات: <b>{current_count}</b> | تطوير المبرمج: <b>أيمن 🦾</b></p>", unsafe_allow_html=True)
