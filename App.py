import streamlit as st
import tldextract

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="درع أيمن الرقمي", page_icon="🛡️", layout="centered")

# 2. تصميم الواجهة (الأسود الملكي والألوان الاحترافية)
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; font-family: 'Arial'; }
    .stButton>button {
        width: 100%;
        background-color: #00d4ff;
        color: #000;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 10px;
    }
    .stTextInput>div>div>input {
        background-color: #1a1c24;
        color: white;
        border: 1px solid #00d4ff;
        border-radius: 10px;
        text-align: center;
    }
    .stAlert { border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# 3. العنوان والشعار
st.markdown("<h1>🛡️ درع أيمن <br> لحماية الروابط</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>أداة ذكية لفحص الروابط وحمايتك من الاحتيال الرقمي</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. إدارة العداد (Session State)
if 'counter' not in st.session_state:
    st.session_state.counter = 150

# 5. خانة المدخلات
url_input
