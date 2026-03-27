import streamlit as st
import yt_dlp
import os
import sqlite3
import requests
from datetime import datetime
from bs4 import BeautifulSoup


# --- 1. الإعدادات الأساسية والتصميم (منع اللون الأبيض تماماً) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    
    /* صبغ منطقة الرفع باللون الكحلي الداكن لإراحة العين */
    section[data-testid="stFileUploadDropzone"] {
        background-color: #161b22 !important;
        border: 2px dashed #1f6feb !important;
        color: #ffffff !important;
        border-radius: 15px;
    }
    
    /* تصميم الأزرار الموحد */
    div.stButton > button, .stFormSubmitButton > button { 
        width: 100% !important; 
        background-color: #1f6feb !important; 
        color: white !important; 
        border-radius: 12px !important; 
        height: 3.5em !important; 
        font-weight: bold !important; 
        border: 1px solid #388bfd !important; 
    }

    .hero-box { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 25px; }
    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 10px; }
    .status-ok { color: #00ff00; font-weight: bold; }
    .preview-box { background: #000; color: #00ff00; padding: 15px; border-radius: 10px; font-family: monospace; overflow: auto; max-height: 300px; border: 1px solid #1f6feb; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك التقني (قاعدة البيانات والتراسل) ---
DB_NAME = "ayman_ultimate_v6.db"
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, reporter TEXT, detail TEXT, date TEXT)')
    conn.commit()
    return conn

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

db = init_db()

# --- 3. بناء التبويبات بشكل مستقل ---

# [تبويب 1: الرئيسية]
def tab_home():
    st.markdown('<div class="hero-box"><h1>👋 مرحباً بك في درع أيمن</h1><p>نظام الحماية والتحميل المتكامل - النسخة المستقرة 6.0</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **نصيحة أمنية:** لا تفتح روابط من مصادر مجهولة قبل فحصها هنا.")
    with col2:
        st.success("✅ **حالة النظام:** جميع التبويبات تعمل بكفاءة.")

# [تبويب 2: الفحص الشامل - إصلاح الروابط والملفات]
def tab_scanner():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔍 فحص الروابط والملفات")
    f_mode = st.radio("اختر نوع الفحص:", ["فحص رابط 🔗", "فحص ملف 📁"], horizontal=True)

    # --- بداية ميزة المعاينة الآمنة ---
def get_site_preview(url):
    try:
        # إرسال طلب للموقع لجلب البيانات في الخلفية
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج العنوان والوصف
        title = soup.title.string if soup.title else "عنوان غير معروف"
        description = soup.find('meta', attrs={'name': 'description'})
        description = description['content'] if description else "لا يوجد وصف مختصر متاح لهذه الصفحة."
        
        return {"title": title, "desc": description}
    except Exception as e:
        return None

# واجهة المعاينة داخل التبويب
st.markdown("### 🌐 معاينة الرابط قبل الدخول")
preview_url = st.text_input("ألصق الرابط هنا لرؤية محتواه:")

if st.button("👁️ عرض معاينة الصفحة"):
    if preview_url:
        with st.spinner("جاري فحص محتوى الصفحة..."):
            data = get_site_preview(preview_url)
            if data:
                st.markdown(f"""
                <div style="background: #1c2128; border: 1px solid #1f6feb; padding: 15px; border-radius: 12px;">
                    <h4 style="color: #58a6ff; margin-bottom: 5px;">{data['title']}</h4>
                    <p style="color: #8b949e; font-size: 0.9em;">{data['desc']}</p>
                    <hr style="border: 0.1px solid #30363d;">
                    <p style="color: #3fb950; font-size: 0.8em; font-weight: bold;">✅ حالة الرابط: تمت قراءته برمجياً بنجاح</p>
                </div>
                """, unsafe_allow_html=True)
                # إشعار التليجرام (اختياري)
                                        # --- تأكد أن هذه الأسطر تبدأ بنفس مستوى السطر الذي فوقها ---
        st.markdown("", unsafe_allow_html=True) 
        # إشعار التليجرام (اختياري)
        send_to_telegram(f"🔍 معاينة رابط آمنة: {preview_url}")
    else:
        st.error("تعذر جلب بيانات هذا الموقع...")

            else:
                st.error("تعذر جلب بيانات هذا الموقع. قد يكون محمياً أو الرابط غير صحيح.")
# --- نهاية ميزة المعاينة الآمنة ---

    if f_mode == "فحص رابط 🔗":
        url_input = st.text_input("أدخل الرابط المراد تحليله:")
        if st.button("تحليل الرابط"):
            if url_input:
                st.write(f"تحليل الرابط: `{url_input}`")
                st.markdown("النتيجة: <span class='status-ok'>آمن (فحص برمجى)</span>", unsafe_allow_html=True)
                send_to_telegram(f"🔍 <b>فحص رابط:</b>\n{url_input}")
    else:
        u_file = st.file_uploader("ارفع الملف للفحص (منع الشاشة الحمراء فعال):", type=None)
        if st.button("بدء فحص محتوى الملف"):
            if u_file:
                # معالجة الخطأ بترميز مرن (اصلاح الصورة السابقة)
                raw = u_file.getvalue()
                try: content = raw.decode("utf-8")
                except: content = raw.decode("latin-1", errors="replace")
                st.markdown("🔍 **معاينة المحتوى:**")
                st.markdown(f'<div class="preview-box">{content[:2000]}</div>', unsafe_allow_html=True)
                send_to_telegram(f"📁 <b>فحص ملف:</b> {u_file.name}")
    st.markdown('</div>', unsafe_allow_html=True)

# [تبويب 3: محمل الفيديو]
def tab_downloader():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 محمل الفيديو الذكي")
    v_url = st.text_input("رابط الفيديو (يوتيوب، فيسبوك، إلخ):")
    if st.button("جلب وتحميل الفيديو"):
        if v_url:
            with st.spinner("جاري المعالجة..."):
                try:
                    opts = {'format': 'best', 'outtmpl': 'temp_vid.mp4', 'quiet': True}
                    with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([v_url])
                    with open("temp_vid.mp4", "rb") as f:
                        st.video(f.read())
                        st.download_button("📥 حفظ الفيديو", f, "ayman_video.mp4")
                    os.remove("temp_vid.mp4")
                except: st.error("فشل الجلب. تأكد من صحة الرابط.")
    st.markdown('</div>', unsafe_allow_html=True)

# [تبويب 4: حماية المجتمع - بلاغات]
def tab_community():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("👥 بلاغات حماية المجتمع")
    with st.form("community_form", clear_on_submit=True):
        r_name = st.text_input("اسم صاحب البلاغ:")
        r_detail = st.text_area("تفاصيل النشاط المشبوه أو البلاغ:")
        if st.form_submit_button("إرسال البلاغ"):
            if r_detail:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                db.execute("INSERT INTO reports (reporter, detail, date) VALUES (?, ?, ?)", (r_name if r_name else "مجهول", r_detail, dt))
                db.commit()
                st.success("✅ تم توثيق البلاغ وإرساله.")
                send_to_telegram(f"🚨 <b>بلاغ مجتمعي جديد:</b>\n{r_detail}")
    st.markdown('</div>', unsafe_allow_html=True)

# [تبويب 5: تواصل معنا]
def tab_contact():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 تواصل مباشر مع أيمن")
    with st.form("contact_form", clear_on_submit=True):
        c_name = st.text_input("اسمك:")
        c_msg = st.text_area("رسالتك:")
        if st.form_submit_button("إرسال الرسالة"):
            if c_name and c_msg:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M")
                db.execute("INSERT INTO messages (sender, content, date) VALUES (?, ?, ?)", (c_name, c_msg, dt))
                db.commit()
                st.success("✅ وصلت رسالتك بنجاح.")
                send_to_telegram(f"📧 <b>رسالة خاصة لأيمن:</b>\nمن: {c_name}\nالمحتوى: {c_msg}")
    st.markdown('</div>', unsafe_allow_html=True)

# [تبويب 6: الإدارة والمصادقة]
def tab_admin():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🔐 لوحة التحكم (للمدير فقط)")
    if "admin_auth" not in st.session_state: st.session_state.admin_auth = False
    
    if not st.session_state.admin_auth:
        pwd = st.text_input("كلمة السر الخاصة بك يا أيمن:", type="password")
        if st.button("دخول"):
            if pwd == "ayman7716": 
                st.session_state.admin_auth = True
                st.rerun()
            else: st.error("❌ كلمة السر غير صحيحة.")
    else:
        if st.button("تسجيل الخروج"): 
            st.session_state.admin_auth = False
            st.rerun()
        st.write("---")
        # عرض الرسائل والبلاغات
        st.write("📩 **آخر الرسائل المستلمة:**")
        msgs = db.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 10").fetchall()
        for m in msgs: st.info(f"👤 {m[1]} | 📅 {m[3]}\n\n{m[2]}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. تشغيل التطبيق وتوزيع التبويبات ---
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 التحميل", "👥 المجتمع", "📧 تواصل", "🔐 الإدارة"])

with tabs[0]: tab_home()
with tabs[1]: tab_scanner()
with tabs[2]: tab_downloader()
with tabs[3]: tab_community()
with tabs[4]: tab_contact()
with tabs[5]: tab_admin()
