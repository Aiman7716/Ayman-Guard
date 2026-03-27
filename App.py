import streamlit as st
import requests
import sqlite3
from datetime import datetime

# --- 1. التصميم البصري (كحلي نيلي فخم) ---
st.set_page_config(page_title="Ayman Guard Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: RTL; text-align: right; }
    .stApp { background-color: #0d1117; color: #ffffff; }

    .hero-box {
        background: linear-gradient(135deg, #1f6feb 0%, #111d2e 100%);
        padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #30363d; margin-bottom: 20px;
    }

    /* أزرار كحلية واضحة جداً (حل مشكلة الأزرار البيضاء) */
    div.stButton > button, .final-dl-btn {
        width: 100% !important; background-color: #1f6feb !important; color: white !important;
        border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; 
        border: none !important; display: flex; align-items: center; justify-content: center;
        text-decoration: none; font-size: 1.1rem !important; cursor: pointer; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #388bfd !important; }

    .content-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-top: 15px; }
    
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 12px; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات ---
conn = sqlite3.connect('ayman_db_v80.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS contact (name TEXT, msg TEXT, dt TEXT)")
conn.commit()

# --- 3. الواجهة الرئيسية ---
st.markdown('<div class="hero-box"><h1>🛡️ درع أيمن الأمني</h1><p>Ayman Security Ultimate v80.0</p></div>', unsafe_allow_html=True)

# استعادة التبويبات الستة كاملة
tabs = st.tabs(["🏠 الرئيسية", "🔍 الفحص", "🎬 محمل الفيديو", "👥 المجتمع", "📧 تواصل معنا", "🔐 الإدارة"])

# --- التبويب: محمل الفيديو (الحل المستقر) ---
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🎬 استخراج الوسائط الذكي")
    v_url = st.text_input("ألصق الرابط هنا (TikTok, FB, YT):")
    
    if st.button("🚀 تحليل واستخراج الفيديو"):
        if v_url:
            with st.spinner("جاري جلب الرابط الآمن..."):
                try:
                    # استخدام محرك بديل (Cobalt) أو TikWM API لضمان تجاوز الحظر 403
                    api_bridge = f"https://api.tikwm.com/api/?url={v_url}"
                    res = requests.get(api_bridge, timeout=10).json()
                    
                    if res.get("code") == 0:
                        v_data = res.get("data")
                        v_link = v_data.get("play")
                        
                        st.success("✅ تم العثور على الفيديو بنجاح!")
                        
                        # معاينة الفيديو (إذا كان السيرفر يسمح)
                        st.video(v_link)
                        
                        # الحل الجذري: زر "رابط مباشر" يفتح في صفحة جديدة للتحميل الفوري
                        st.markdown(f'''
                            <a href="{v_link}" target="_blank" class="final-dl-btn">
                                📥 اضغط هنا لبدء التحميل الفوري (MP4)
                            </a>
                        ''', unsafe_allow_html=True)
                        st.info("💡 ملاحظة للجوال: إذا لم يبدأ التحميل تلقائياً، اضغط مطولاً على الزر واختر 'Download Linked File'.")
                    else:
                        st.error("❌ عذراً، هذا الرابط محمي بواسطة المنصة الأصلية.")
                except:
                    st.error("🚨 خطأ في الاتصال بالمضيف، يرجى المحاولة بعد قليل.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب: تواصل معنا ---
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📧 تواصل مع أيمن")
    nm = st.text_input("اسمك:")
    ms = st.text_area("رسالتك:")
    if st.button("إرسال البيانات"):
        if nm and ms:
            c.execute("INSERT INTO contact VALUES (?, ?, ?)", (nm, ms, datetime.now().strftime("%H:%M")))
            conn.commit()
            st.success("✅ تم الإرسال بنجاح.")
    st.markdown('</div>', unsafe_allow_html=True)

# بقية الأقسام لضمان توازن الواجهة
with tabs[0]: st.info("النظام نشط ومستقر حالياً.")
with tabs[1]: st.text_input("رابط لفحصه:"); st.button("فحص")
with tabs[3]: st.text_area("بلاغ احتيال:"); st.button("نشر")
with tabs[5]: 
    if st.text_input("كلمة السر:", type="password") == "ayman7716":
        st.write("سجلات النظام.")
