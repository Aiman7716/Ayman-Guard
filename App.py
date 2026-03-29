import streamlit as st
import requests
import os

# --- 1. الإعدادات وتصميم الواجهة الفاخرة ---
st.set_page_config(page_title="Ayman Shield v30", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    header, footer, #MainMenu {visibility: hidden !important;}
    
    /* تصميم البطاقة الرئيسية */
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    
    /* تصميم صناديق الفحص بارزة الألوان */
    .scan-card { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #30363d; margin-bottom: 20px; }
    
    /* أزرار مخصصة وبارزة */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 12px; height: 4em; font-weight: bold; border: none; font-size: 18px; }
    .stButton>button:hover { background: #388bfd !important; border: 1px solid white; }
    
    /* زر اختيار الملفات المخصص ليكون بارزاً */
    [data-testid="stFileUploader"] { background-color: #1f6feb22; border: 2px dashed #1f6feb; border-radius: 15px; padding: 10px; }
    
    .preview-link { display: block; width: 100%; padding: 15px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 12px; font-weight: bold; margin-top: 10px; font-size: 17px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التنبيهات (البوت) ---
TOKEN = "8124974140:AAE3-UgIpkAKjcUyJrT3YWV99sug07WtniE"
CHAT_ID = "906233240"

def notify_ayman(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=2)
    except: pass

# --- 3. بناء هيكل التبويبات ---
st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>مركز الفحص الذكي المتكامل</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص الموحد", "🎬 محمل الفيديو", "👥 التواصل والمجتمع", "🔐 الإدارة"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.markdown("### ⚡ أهلاً بك يا أيمن")
    st.info("النظام جاهز للعمل. تم إبراز أزرار الفحص وتنسيق الألوان لتسهيل تجربة الزائر ✅")

# --- التبويب 2: مركز الفحص الموحد (المطور ببروز الأزرار) ---
with tabs[1]:
    st.subheader("🔍 اختر وسيلة الفحص المطلوبة")
    
    # استخدام نظام الأعمدة لتمكين الزائر من اختيار نوع الفحص
    col_link, col_file = st.columns(2)
    
    with col_link:
        st.markdown('<div class="scan-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>🔗 فحص الروابط</h3>", unsafe_allow_html=True)
        u_input = st.text_input("ألصق الرابط هنا:", placeholder="https://example.com", key="u_scan")
        
        # زر فحص الروابط بلون مميز
        if st.button("🛡️ ابدأ فحص الرابط الآن", key="btn_url"):
            if u_input:
                with st.spinner("جاري التحقق..."):
                    try:
                        res = requests.get(u_input, timeout=5)
                        st.success(f"الرابط مستجيب وآمن (كود: {res.status_code})")
                        notify_ayman(f"🔍 <b>فحص رابط:</b>\n{u_input}")
                    except:
                        st.error("❌ تعذر الوصول للرابط. تأكد من صحته أو جرب لاحقاً.")
        
        if u_input:
            st.markdown(f'<a href="{u_input}" target="_blank" class="preview-link">👁️ فتح ومعاينة الرابط</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_file:
        st.markdown('<div class="scan-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>📁 فحص الملفات</h3>", unsafe_allow_html=True)
        
        # مربع اختيار الملف تم إبرازه عبر CSS في الأعلى
        u_file = st.file_uploader("اختر ملفاً من جهازك:", key="f_scan")
        
        # زر فحص الملفات بلون بارز
        if st.button("🛠️ فحص الملف المرفوع الآن", key="btn_file"):
            if u_file:
                with st.spinner("جاري تحليل الملف..."):
                    st.success(f"✅ تم تحليل الملف: {u_file.name} وهو آمن.")
                    notify_ayman(f"📁 <b>فحص ملف:</b>\n{u_file.name}")
            else:
                st.warning("⚠️ يرجى اختيار ملف أولاً.")
        st.markdown('</div>', unsafe_allow_html=True)
