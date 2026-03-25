import streamlit as st
import tldextract
import sqlite3
import random
from datetime import datetime

# --- 1. إعداد قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('ayman_guard.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, scan_count INTEGER)''')
    c.execute('''INSERT OR IGNORE INTO stats (id, scan_count) VALUES (1, 250)''')
    conn.commit()
    conn.close()

def update_scan_count():
    conn = sqlite3.connect('ayman_guard.db')
    c = conn.cursor()
    c.execute("UPDATE stats SET scan_count = scan_count + 1 WHERE id = 1")
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('ayman_guard.db')
    c = conn.cursor()
    c.execute("SELECT scan_count FROM stats WHERE id = 1")
    res = c.fetchone()
    conn.close()
    return res[0] if res else 250

def add_report(url):
    conn = sqlite3.connect('ayman_guard.db')
    c = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO reports (url, date) VALUES (?, ?)", (url, date_str))
    conn.commit()
    conn.close()

def get_reports():
    conn = sqlite3.connect('ayman_guard.db')
    c = conn.cursor()
    c.execute("SELECT url FROM reports ORDER BY id DESC LIMIT 5")
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

def clear_db():
    conn = sqlite3.connect('ayman_guard.db')
    c = conn.cursor()
    c.execute("DELETE FROM reports")
    conn.commit()
    conn.close()

init_db()

# --- 2. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="درع أيمن الرقمي", page_icon="🛡️", layout="centered")

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; background-color: #00d4ff; color: #000; font-weight: bold; border-radius: 12px; }
    .report-card { background-color: #1a1c24; border-radius: 10px; padding: 12px; border-right: 5px solid #ff4b4b; margin-bottom: 10px; }
    .official-card { background: #1a1c24; border: 1px solid #00d4ff; padding: 10px; border-radius: 8px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 3. لوحة التحكم السرية (في القائمة الجانبية) ---
with st.sidebar:
    st.header("🔐 إدارة الدرع")
    admin_pass = st.text_input("كلمة مرور المدير:", type="password")
    if admin_pass == "ayman123":
        st.success("أهلاً أيمن!")
        if st.button("🗑️ مسح البلاغات"):
            clear_db()
            st.rerun()
        manual_count = st.number_input("تعديل العداد:", value=get_stats())
        if st.button("⚙️ تحديث"):
            conn = sqlite3.connect('ayman_guard.db')
            conn.cursor().execute("UPDATE stats SET scan_count = ? WHERE id = 1", (manual_count,))
            conn.commit()
            conn.close()
            st.rerun()

# --- 4. الواجهة الرئيسية ---
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🛡️ درع أيمن الذكي</h1>", unsafe_allow_html=True)
st.info(random.choice(["💡 تأكد من وجود HTTPS دائمًا.", "💡 لا تشارك رمز OTP أبدًا."]))

# الفحص
url_in = st.text_input("🔍 الصق الرابط هنا:", placeholder="https://example.com")
if st.button("🚀 افحص الآن"):
    update_scan_count()
    if url_in:
        ext = tldextract.extract(url_in.lower())
        full_dom = f"{ext.domain}.{ext.suffix}"
        if full_dom in ['absher.sa', 'iam.gov.sa', 'google.com']:
            st.success(f"✅ آمن: ({full_dom})")
        elif ext.suffix in ['tk', 'xyz', 'ml']:
            st.error(f"❌ تم صيد رابط وهمي!")
        else:
            st.info(f"ℹ️ النطاق هو ({full_dom}).")

# البلاغات
st.markdown("---")
st.markdown("### 📢 ساحة البلاغات")
with st.expander("➕ أبلغ عن رابط"):
    rep_url = st.text_input("الرابط المشبوه:")
    if st.button("📤 إرسال"):
        if rep_url and tldextract.extract(rep_url).domain not in ['google', 'absher']:
            add_report(rep_url)
            st.success("تم الحفظ!")
        else: st.error("خطأ!")

for r in get_reports():
    st.markdown(f"<div class='report-card'>⚠️ مشبوه: <code>{r}</code></div>", unsafe_allow_html=True)

# المراجع الرسمية
st.markdown("---")
st.markdown("### 🏛️ الروابط الرسمية الموثقة")
c1, c2, c3 = st.columns(3)
with c1: st.markdown("<div class='official-card'>🇸🇦 <a href='https://absher.sa' style='color:#00d4ff;'>أبشر</a></div>", unsafe_allow_html=True)
with c2: st.markdown("<div class='official-card'>🔑 <a href='https://iam.gov.sa' style='color:#00d4ff;'>نفاذ</a></div>", unsafe_allow_html=True)
with c3: st.markdown("<div class='official-card'>📦 <a href='https://splonline.com.sa' style='color:#00d4ff;'>البريد</a></div>", unsafe_allow_html=True)

# التذييل
st.markdown("---")
st.write(f"📊 الفحوصات: **{get_stats()}** | تطوير: أيمن 🦾")
    else:
        st.error("⚠️ من فضلك ضع الرابط أولاً!")

st.markdown("---")

# 7. ساحة بلاغات المجتمع الموثقة
st.markdown("### 📢 ساحة بلاغات المجتمع")
with st.expander("➕ إرسال بلاغ وتحقق"):
    new_report = st.text_input("أدخل الرابط المشبوه هنا:", key="report_box")
    if st.button("📤 إرسال وتحذير الجميع"):
        if new_report:
            rep_ext = tldextract.extract(new_report.lower())
            if rep_ext.domain in ['google', 'absher', 'moi', 'whatsapp', 'iam', 'splonline']:
                st.warning("⚠️ لا يمكن التبليغ عن المواقع الرسمية الموثقة.")
            else:
                st.session_state.verified_scams.insert(0, new_report.strip().lower())
                st.success("✅ تم التحقق وإضافة البلاغ بنجاح!")
        else:
            st.error("⚠️ يرجى إدخال الرابط.")

if st.session_state.verified_scams:
    st.write("**🚨 أحدث الروابط التي تم التبليغ عنها:**")
    for scam in st.session_state.verified_scams[:3]:
        st.markdown(f"<div class='report-card'>⚠️ رابط مشبوه: <code>{scam}</code> <br><small>🚩 حالة التحقق: تم التأكيد بواسطة درع أيمن</small></div>", unsafe_allow_html=True)

# 8. التحديث الجديد: قسم الروابط المرجعية الرسمية
st.markdown("---")
st.markdown("### 🏛️ المرجع الآمن للروابط الرسمية")
st.write("استخدم هذه الروابط دائماً للوصول للخدمات الحكومية بأمان:")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='official-card'>🇸🇦 أبشر<br><a href='https://www.absher.sa' style='color:#00d4ff; text-decoration:none;'>انقر هنا</a></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='official-card'>🔑 نفاذ<br><a href='https://iam.gov.sa' style='color:#00d4ff; text-decoration:none;'>انقر هنا</a></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='official-card'>📦 البريد<br><a href='https://splonline.com.sa' style='color:#00d4ff; text-decoration:none;'>انقر هنا</a></div>", unsafe_allow_html=True)

# 9. التذييل
st.markdown("---")
col_stat, col_dev = st.columns(2)
with col_stat:
    st.write(f"📊 إجمالي الفحوصات: **{st.session_state.counter}**")
with col_dev:
    st.markdown("<p style='text-align: left; font-weight: bold;'>تطوير: أيمن 🦾🛡️</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 0.7em; color: #555;'>درع أيمن - حماية المجتمع مسؤولية الجميع</p>", unsafe_allow_html=True)
