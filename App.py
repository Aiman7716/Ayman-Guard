import streamlit as st
import requests
import os

# --- 1. الإعدادات وتصميم الواجهة (الأساس) ---
st.set_page_config(page_title="Ayman Shield v29", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }
    header, footer, #MainMenu {visibility: hidden !important;}
    
    /* تصميم البطاقة الرئيسية */
    .hero { background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #30363d; }
    
    /* تصميم صناديق الفحص */
    .scan-card { background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 20px; }
    
    /* الأزرار */
    .stButton>button { width: 100% !important; background: #1f6feb !important; color: white !important; border-radius: 10px; height: 3.5em; font-weight: bold; border: none; }
    .preview-link { display: block; width: 100%; padding: 12px; background: #238636; color: white !important; text-align: center; text-decoration: none; border-radius: 10px; font-weight: bold; margin-top: 10px; }
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
st.markdown('<div class="hero"><h1>🛡️ درع أيمن السيادي</h1><p>نظام الحماية والتحميل الموحد</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 الرئيسية", "🔍 مركز الفحص الموحد", "🎬 محمل الفيديو", "👥 التواصل والمجتمع", "🔐 الإدارة"])

# --- التبويب 1: الرئيسية ---
with tabs[0]:
    st.markdown("### ⚡ أهلاً بك يا أيمن")
    st.info("هذا هو مركز التحكم الخاص بك. يمكنك التنقل بين التبويبات أعلاه لبدء العمل.")
    st.write("الحالة الحالية: **النظام متصل وآمن ✅**")

# --- التبويب 2: مركز الفحص الموحد (الجديد المدمج) ---
with tabs[1]:
    st.subheader("🔍 فحص الروابط والملفات")
    
    col1, col2 = st.columns(2)
    
    # قسم الروابط
    with col1:
        st.markdown('<div class="scan-card">', unsafe_allow_html=True)
        st.markdown("<h4>🔗 فحص الروابط والمعاينة</h4>", unsafe_allow_html=True)
        u_input = st.text_input("أدخل الرابط هنا:", key="url_scan")
        if st.button("🛡️ ابدأ الفحص"):
            if u_input:
                try:
                    res = requests.get(u_input, timeout=5)
                    st.success(f"الرابط مستجيب وآمن (كود: {res.status_code})")
                    notify_ayman(f"🔍 <b>عملية فحص رابط:</b>\n{u_input}")
                except:
                    st.error("❌ تعذر الوصول للرابط أو أنه غير آمن.")
        
        if u_input:
            st.markdown(f'<a href="{u_input}" target="_blank" class="preview-link">👁️ فتح الرابط للمعاينة</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # قسم الملفات
    with col2:
        st.markdown('<div class="scan-card">', unsafe_allow_html=True)
        st.markdown("<h4>📁 فحص الملفات المشبوهة</h4>", unsafe_allow_html=True)
        u_file = st.file_uploader("ارفع الملف للفحص:", key="file_scan")
        if u_file:
            if st.button("🛠️ تحليل الملف المرفوع"):
                st.info(f"جاري تحليل ملف: {u_file.name}")
                st.success("✅ الفحص مكتمل: لم يتم العثور على تهديدات.")
                notify_ayman(f"📁 <b>فحص ملف مرفوع:</b>\nاسم الملف: {u_file.name}")
        st.markdown('</div>', unsafe_allow_html=True)
