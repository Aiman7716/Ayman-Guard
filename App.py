import streamlit as st
import tldextract
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="درع أيمن الذكي", page_icon="🛡️", layout="centered")

# --- 2. CSS احترافي يمنع التداخل ولا يعطل الوظائف ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] { 
            font-family: 'Cairo', sans-serif !important; 
            direction: rtl !important; 
            text-align: right !important; 
        }
        .main-header { color: #00d4ff; text-align: center; font-size: 2.5rem; font-weight: bold; }
        div.stButton > button:first-child { 
            background-color: #ff4b4b !important; color: white !important; 
            border-radius: 12px !important; width: 100% !important; height: 3.5em !important; font-weight: bold !important; 
        }
        /* إخفاء نصوص التداخل فقط دون تعطيل الأزرار */
        symbol, .st-emotion-cache-1kyx60p { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. قاعدة البيانات الموثوقة ---
OFFICIAL_SUFFIXES = ['.gov.sa', '.edu.sa']
TRUSTED_DOMAINS = ['absher.sa', 'iam.gov.sa', 'splonline.com.sa', 'saudipost.sa', 'moj.gov.sa']

# --- 4. الواجهة الرئيسية ---
st.markdown('<div class="main-header">🛡️ درع أيمن الذكي</div>', unsafe_allow_html=True)

# حقل الفحص الأساسي
url_to_check = st.text_input("🔍 ضع الرابط هنا للفحص (حكومي، جامعة، أو جهة رسمية) :", placeholder="https://example.gov.sa", key="main_scanner")

if st.button("🚀 افحص وصِد الرابط الآن", key="btn_check"):
    if url_to_check:
        url_lower = url_to_check.lower().strip()
        ext = tldextract.extract(url_lower)
        domain_only = f"{ext.domain}.{ext.suffix}"
        
        with st.spinner('جاري التحقق من الموثوقية...'):
            time.sleep(1)
            # أولاً: التحقق من الانتهاء بـ .gov.sa أو .edu.sa
            is_official_suffix = any(url_lower.endswith(s) for s in OFFICIAL_SUFFIXES)
            # ثانياً: التحقق من القائمة الموثوقة
            is_trusted_domain = domain_only in TRUSTED_DOMAINS
            
            if is_official_suffix or is_trusted_domain:
                st.balloons()
                st.success(f"✅ هذا رابط رسمي موثوق (جهة حكومية أو تعليمية): {domain_only}")
            elif ext.suffix in ['tk', 'xyz', 'ml', 'cf', 'gq']:
                st.error("🚨 تحذير: هذا النطاق مشبوه جداً وغير آمن!")
            else:
                st.warning(f"⚠️ الرابط ({domain_only}) غير مسجل في القوائم الرسمية المباشرة.")
    else:
        st.error("⚠️ يرجى إدخال الرابط أولاً.")

st.divider()

# --- 5. ساحة البلاغات (مع منع التبليغ عن الروابط الرسمية) ---
st.subheader("📢 ساحة بلاغات المجتمع")
report_url = st.text_input("أدخل الرابط المحتال للتبليغ عنه :", key="scam_report")

if st.button("إرسال البلاغ", key="btn_report"):
    if report_url:
        rep_lower = report_url.lower().strip()
        rep_ext = tldextract.extract(rep_lower)
        rep_domain = f"{rep_ext.domain}.{rep_ext.suffix}"
        
        # حماية: منع التبليغ عن الجهات الرسمية
        if any(rep_lower.endswith(s) for s in OFFICIAL_SUFFIXES) or rep_domain in TRUSTED_DOMAINS:
            st.error("❌ خطأ: لا يمكنك التبليغ عن رابط رسمي أو حكومي موثوق!")
        else:
            st.success("✅ تم استلام بلاغك بنجاح لمراجعته من قبل المهندس أيمن.")
    else:
        st.warning("⚠️ أدخل الرابط الذي تريد التبليغ عنه.")

st.markdown("<p style='text-align:center; color:#888;'>📊 تطوير المهندس: أيمن 🦾</p>", unsafe_allow_html=True)
