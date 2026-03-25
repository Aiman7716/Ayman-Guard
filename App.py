import streamlit as st
import tldextract
import sqlite3
import random

# 1. إعداد القاعدة والبيانات
def init_db():
    conn = sqlite3.connect('ayman_db.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS reps (id INTEGER PRIMARY KEY, url TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)')
    c.execute('INSERT OR IGNORE INTO stats VALUES (1, 250)')
    conn.commit()
    conn.close()

def db_action(query, val=None, fetch=False):
    conn = sqlite3.connect('ayman_db.db')
    c = conn.cursor()
    if val: c.execute(query, val)
    else: c.execute(query)
    res = c.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return res

init_db()

# 2. التصميم والواجهة
st.set_page_config(page_title="درع أيمن", layout="centered")
st.markdown("<h1 style='text-align:center; color:#00d4ff;'>🛡️ درع أيمن الذكي</h1>", unsafe_allow_html=True)

# 3. لوحة التحكم (السرية)
with st.sidebar:
    pw = st.text_input("قفل المدير:", type="password")
    if pw == "ayman123":
        if st.button("🗑️ مسح البيانات"):
            db_action("DELETE FROM reps")
            st.rerun()

# 4. محرك الفحص
url = st.text_input("🔍 ضع الرابط هنا:")
if st.button("🚀 افحص الآن"):
    db_action("UPDATE stats SET count = count + 1 WHERE id = 1")
    if url:
        ext = tldextract.extract(url.lower())
        dom = f"{ext.domain}.{ext.suffix}"
        if dom in ['absher.sa', 'iam.gov.sa', 'google.com']:
            st.success(f"✅ موثوق: {dom}")
        elif ext.suffix in ['tk', 'xyz', 'ml']:
            st.error("❌ رابط وهمي!")
        else:
            st.info(f"ℹ️ النطاق: {dom}")

# 5. البلاغات
st.markdown("---")
with st.expander("➕ أبلغ عن رابط"):
    r_url = st.text_input("الرابط المشبوه:")
    if st.button("📤 إرسال"):
        if r_url and tldextract.extract(r_url).domain not in ['google', 'absher']:
            db_action("INSERT INTO reps (url) VALUES (?)", (r_url,))
            st.success("تم!")

reps = db_action("SELECT url FROM reps ORDER BY id DESC LIMIT 5", fetch=True)
for r in reps:
    st.warning(f"⚠️ مشبوه: {r[0]}")

# 6. المراجع والتذييل
st.markdown("---")
st.write("🏛️ **روابط رسمية:** [أبشر](https://absher.sa) | [نفاذ](https://iam.gov.sa)")
curr_stat = db_action("SELECT count FROM stats WHERE id=1", fetch=True)[0][0]
st.write(f"📊 الفحوصات: {curr_stat} | تطوير: أيمن 🦾")
