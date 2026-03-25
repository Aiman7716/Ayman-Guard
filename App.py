import streamlit as st
import tldextract
import time
import smtplib
from email.mime.text import MIMEText

# --- 1. إعدادات البريد الإلكتروني (تنبيهات أيمن) ---
def send_email_notification(reported_url):
    sender_email = "ayman.shield.alerts@gmail.com" # بريد مخصص للارسال
    receiver_email = "ayman@example.com" # ضع بريدك الشخصي هنا يا أيمن
    password = "your-app-password" # كلمة مرور التطبيقات من جوجل

    msg = MIMEText(f"تنبيه جديد يا أيمن!\n\nقام أحد المستخدمين بالتبليغ عن رابط مشبوه: {reported_url}")
    msg['Subject'] = '🚩 بلاغ جديد في درع أيمن'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except:
        return False

# --- 2. التنسيق البصري الصافي (منع keyboard_ar) ---
st.set_page_config(page_title="درع أيمن الذكي", layout="centered")
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
        .st-emotion-cache-1kyx60p, .st-emotion-cache-k77z8q, symbol, svg, i, [data-testid="stIcon"] { display: none !important; }
        .main-title { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        div.stButton > button { background-color: #ff4b4b !important; color: white !important; border-radius: 12px !important; width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

if 'blacklist' not in st.session_state: st.session_state.blacklist = {}

# --- 3. الواجهة وساحة البلاغات ---
st.markdown('<div class="main-title">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# (جزء الفحص يبقى كما هو في النسخ السابقة لضمان السرعة)

st.divider()
st.subheader("📢 ساحة بلاغات المجتمع")
r_url = st.text_input("رابط المحتال للتبليغ الفوري :", key="v40_report")

if st.button("🚩 إرسال البلاغ وتنبيه الإدارة"):
    if r_url:
        ext = tldextract.extract(r_url)
        d_name = f"{ext.domain}.{ext.suffix}"
        st.session_state.blacklist[d_name] = True
        
        # محاولة إرسال التنبيه للبريد
        with st.spinner('جاري إرسال البلاغ للمهندس أيمن...'):
            success = send_email_notification(r_url)
            if success:
                st.success(f"✅ تم البلاغ وإرسال تنبيه لبريد أيمن بنجاح.")
            else:
                st.info(f"✅ تم تسجيل البلاغ محلياً (التنبيه البريدي يحتاج ضبط الإعدادات).")
    else:
        st.warning("⚠️ أدخل الرابط أولاً.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
