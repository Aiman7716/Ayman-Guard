import streamlit as st
import tldextract
import re
import random

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="درع أيمن الرقمي", page_icon="🛡️", layout="centered")

# 2. تصميم الواجهة (الأسود الملكي مع لمسات الأمان)
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; font-family: 'Arial'; text-shadow: 2px 2px #000; }
    .stButton>button {
        width: 100%;
        background-color: #00d4ff;
        color: #000;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px;
        border: none;
        box-shadow: 0px 4px 10px rgba(0, 212, 255, 0.3);
    }
    .stButton>button:hover { background-color: #ff4b4b; color: white; }
    .stTextInput>div>div>input {
        background-color: #1a1c24;
        color: white;
        border: 2px solid #00d4ff;
        border-radius: 12px;
        text-align: center;
    }
    .tips-box {
        background-color: #1a1c24;
        padding: 15px;
        border-radius: 10px;
        border-right: 5px solid #00d4ff;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 3. العنوان والشعار
st.markdown("<h1>🛡️ درع أيمن <br> لصيد الروابط الوهمية</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;
