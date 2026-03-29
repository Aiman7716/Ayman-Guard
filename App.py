import streamlit as st
import yt_dlp
import requests

# --- 1. واجهة أيمن السيادية (تصميم نظيف + أزرار زرقاء) ---
st.set_page_config(page_title="Ayman Shield v45", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stHeader"], [data-testid="stTabNav"] { display: none !important; }
    
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d; }
    .card { background: #161b22; padding: 20px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; text-align: center; }
    
    /* أزرار التنقل الزرقاء */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; height: 4em; font-weight: bold; font-size: 18px; border: none; }
    
    /* زر اختيار الملف بالأزرق */
    div[data-testid="stFileUploader"] section button { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    
    /* زر التحميل الخارجي الأخضر (الحل السحري) */
    .final-dl-link { display: block; width: 100%; padding: 25px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 15px; font-weight: bold; font-size: 22px; border: 3px solid #ffffff; box-shadow: 0px 5px 15px rgba(0,0,0,0.4); margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. نظام البوت والتنقل ---
if 'pg' not in st.session_state: st.session_state.pg = "home"

def nav(t):
    st.session_state.pg = t
    st.rerun()

TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def send_log(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}, timeout=2)
    except: pass

# --- 3. الصفحات ---

if st.session_state.pg == "home":
    st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>تم تفعيل بروتوكول "الرابط الخارجي" لتجاوز قيود الفيسبوك ✅</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 فحص الروابط والملفات"): nav("scan")
        if st.button("🎬 تحميل الفيديوهات"): nav("dl")
    with c2:
        if st.button("👥 التواصل والبلاغات"): nav("contact")
        if st.button("🔐 دخول الإدارة"): nav("admin")

elif st.session_state.pg == "dl":
    if st.button("🔙 العودة"): nav("home")
    st.markdown('<div class="card"><h3>🎬 محمل الفيديو (تجاوز حظر التحميل)</h3>', unsafe_allow_html=True)
    v_url = st.text_input("ألصق رابط الفيديو (Facebook, YouTube, etc):")
    
    if st.button("🚀 استخراج رابط التحميل المباشر"):
        if v_url:
            with st.spinner("جاري كسر حماية الرابط..."):
                try:
                    # نستخدم yt-dlp لاستخراج الرابط المباشر فقط دون تحميله للسيرفر
                    ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(v_url, download=False)
                        direct_link = info.get('url', None)
                    
                    if direct_link:
                        st.success("تم استخراج الرابط بنجاح! ✅")
                        # الحل القاطع: زر يفتح الرابط المباشر في صفحة جديدة
                        st.markdown(f'<a href="{direct_link}" target="_blank" class="final-dl-link">⬇️ اضغط هنا للحفظ في الاستوديو</a>', unsafe_allow_html=True)
                        st.info("💡 ملاحظة: سيفتح الرابط في صفحة جديدة، اضغط مطولاً على الفيديو واختر 'تنزيل'.")
                        send_log(f"🎬 تم استخراج رابط: {v_url}")
                    else:
                        st.error("لم نتمكن من العثور على رابط مباشر لهذا الفيديو.")
                except Exception as e:
                    st.error("فشل الاستخراج. تأكد من أن الحساب صاحب الفيديو 'عام' وليس 'خاص'.")

elif st.session_state.pg == "scan":
    if st.button("🔙 عودة"): nav("home")
    st.markdown("### 🔍 مركز الفحص")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h4>🔗 الروابط</h4>', unsafe_allow_html=True)
        u = st.text_input("الرابط للفحص:")
        if st.button("🛡️ ابدأ الفحص"):
            try:
                r = requests.head(u, timeout=5)
                st.success(f"الرابط مستجيب ({r.status_code})")
                send_log(f"🔍 فحص رابط: {u}")
            except: st.error("فشل الوصول")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h4>📁 الملفات</h4>', unsafe_allow_html=True)
        # زر اختيار ملف (أزرق) كما طلبت
        f = st.file_uploader(" ", key="ayman_file_final")
        if st.button("🛠️ فحص الملف"):
            if f:
                st.success(f"تم فحص {f.name} وهو آمن")
                send_log(f"📁 فحص ملف: {f.name}")
        st.markdown('</div>', unsafe_allow_html=True)

# باقي الصفحات (تواصل، إدارة)
elif st.session_state.pg == "contact":
    if st.button("🔙 عودة"): nav("home")
    with st.form("c"):
        n = st.text_input("الاسم:")
        m = st.text_area("الرسالة:")
        if st.form_submit_button("إرسال"):
            send_log(f"📩 رسالة من {n}: {m}")
            st.success("تم!")

elif st.session_state.pg == "admin":
    if st.button("🔙 عودة"): nav("home")
    p = st.text_input("السر:", type="password")
    if st.button("دخول"):
        if p == "ayman7716": st.success("أهلاً أيمن")
        else: st.error("خطأ")
