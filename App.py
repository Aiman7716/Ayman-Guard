import streamlit as st
import tldextract, sqlite3, os, requests, hashlib
from datetime import datetime

VT_API_KEY = "Ab38a92fadf6868867f8376d7ff1fd93f06f94608d76fbf93a5735ef09deadce"

def check_virustotal(file_hash):
    headers = {"x-apikey": VT_API_KEY}
    try:
        response = requests.get(f"https://www.virustotal.com/api/v3/files/{file_hash}", headers=headers)
        if response.status_code == 200: return response.json()['data']['attributes']['last_analysis_stats']
    except: return None
    return None

st.set_page_config(page_title="درع أيمن v5.5", page_icon="🛡️")

# تصميم نيون احترافي
st.markdown("""<style> .stApp { background-color: #0e1117; color: white; } .main-title { text-align: center; color: #00d4ff; font-weight: bold; font-size: 2.5rem; } </style>""", unsafe_allow_html=True)
st.markdown('<div class="main-title">🛡️ درع أيمن: الفحص العميق</div>', unsafe_allow_html=True)

up_file = st.file_uploader("ارفع الملف لاختبار البصمة الرقمية:", type=None)

if up_file:
    content = up_file.read()
    # حساب البصمة (SHA-256)
    file_hash = hashlib.sha256(content).hexdigest()
    
    st.info(f"🧬 بصمة الملف الرقمية: \n`{file_hash}`")
    
    with st.spinner('جاري مطابقة البصمة عالمياً...'):
        res = check_virustotal(file_hash)
        
        if res and res.get('malicious', 0) > 0:
            st.error(f"🚨🚨 إنذار: هذا الملف معروف عالمياً كتهديد! (العدد: {res['malicious']})")
        elif res:
            st.success("✅ البصمة مطابقة لملف آمن ومعروف عالمياً.")
        else:
            st.warning("⚠️ هذه البصمة 'فريدة' ولم يسبق لأحد في العالم رفع هذا الملف بدقة.")
            
            # اختبار محلي إضافي
            if b"EICAR" in content:
                st.error("💡 ملاحظة: الكود يحتوي على كلمة EICAR لكن بصمته غير مطابقة للأصل (ربما بسبب تنسيق الملف).")
