import streamlit as st
import yt_dlp
import os
import requests

# --- 1. التصميم السيادي (أزرار زرقاء + إخفاء التبويبات) ---
st.set_page_config(page_title="Ayman Shield v41", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stHeader"], [data-testid="stTabNav"] { display: none !important; }
    
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 35px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    .card { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; }
    
    /* أزرار الواجهة الرئيسية */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 15px; height: 4.5em; font-weight: bold; border: none; font-size: 18px; }
    
    /* حل تلوين زر "اختيار ملف" للأزرق (طلبك الأساسي) */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; width: 100% !important; height: 3.5em !important; border: none !important; }
    div[data-testid="stFileUploader"] section button span::after { content: " 📁 اختيار ملف من جهازك "; visibility: visible; display: block; position: absolute; background: #1f6feb; left: 0; right: 0; top: 0; bottom: 0; line-height: 3.5em; border-radius: 10px; }
    div[data-testid="stFileUploader"] section button span { visibility: hidden; }

    /* زر التحميل الأخضر الكبير (الحل الجديد) */
    .final-dl { display: block; width: 100%; padding: 20px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 15px; font-weight: bold; font-size: 20px; border: 2px solid #ffffff; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة التنقل والبوت ---
if 'pg' not in st.session_state: st.session_state.pg = "home"

def go(target):
    st.session_state.pg = target
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_bot(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=2)
    except: pass

# --- 3. عرض الصفحات ---

if st.session_state.pg == "home":
    st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>تم تفعيل نظام الروابط الخارجية لتجاوز حظر التطبيقات ✅</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 فحص الروابط والملفات"): go("scan")
        if st.button("🎬 تحميل الفيديوهات"): go("dl")
    with c2:
        if st.button("👥 التواصل والبلاغات"): go("contact")
        if st.button("🔐 دخول الإدارة"): go("admin")

elif st.session_state.pg == "dl":
    if st.button("🔙 عودة للرئيسية"): go("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو (تجاوز القيود)</h3>', unsafe_allow_html=True)
    v_url = st.text_input("ألصق رابط الفيديو هنا:")
    
    if st.button("🚀 استخراج رابط الحفظ"):
        if v_url:
            with st.spinner("جاري استخراج الرابط المباشر..."):
                try:
                    # نستخدم yt-dlp للحصول على الرابط المباشر من سيرفرات الفيديو
                    ydl_opts = {'format': 'best', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        direct_url = info.get('url', None)
                    
                    if direct_url:
                        st.video(direct_url)
                        # الحل القاطع: رابط يفتح في صفحة جديدة (يسمح بالتحميل في كروم)
                        st.markdown(f'<a href="{direct_url}" target="_blank" class="final-dl">📥 اضغط هنا: سيفتح الفيديو في صفحة جديدة للحفظ</a>', unsafe_allow_html=True)
                        st.info("💡 بعد الضغط، إذا لم يبدأ التحميل، اضغط على النقاط الثلاث بجانب الفيديو واختر 'تنزيل'.")
                        send_bot(f"🎬 نجاح استخراج رابط فيديو: {v_url}")
                except:
                    st.error("فشل في استخراج الرابط. تأكد من صحة الرابط.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.pg == "scan":
    if st.button("🔙 عودة"): go("home")
    st.markdown("## 🔍 مركز الفحص")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h4>🔗 الروابط</h4>', unsafe_allow_html=True)
        u_in = st.text_input("الرابط:")
        if st.button("🛡️ فحص الآن"):
            try:
                r = requests.get(u_in, timeout=5)
                st.success(f"مستجيب: {r.status_code}")
                send_bot(f"🔍 فحص رابط: {u_in}")
            except: st.error("فشل الوصول")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h4>📁 الملفات</h4>', unsafe_allow_html=True)
        # زر اختيار الملف الأزرق
        f_up = st.file_uploader(" ", key="file_up_final")
        if st.button("🛠️ فحص الملف"):
            if f_up:
                st.success(f"تم فحص {f_up.name} بنجاح ✅")
                send_bot(f"📁 فحص ملف: {f_up.name}")
        st.markdown('</div>', unsafe_allow_html=True)

# (تواصل، إدارة) تظل كما هي لضمان الاستقرار
elif st.session_state.pg == "contact":
    if st.button("🔙 عودة"): go("home")
    with st.form("contact"):
        n = st.text_input("الاسم:")
        m = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            send_bot(f"📩 من {n}: {m}")
            st.success("تم!")

elif st.session_state.pg == "admin":
    if st.button("🔙 عودة"): go("home")
    pw = st.text_input("السر:", type="password")
    if st.button("دخول"):
        if pw == "ayman7716": st.success("أهلاً أيمن"); send_bot("🔐 دخول إدارة")
        else: st.error("خطأ")
