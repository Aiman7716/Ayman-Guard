with tabs[1]: # تبويب الفحص والمعاينة المطور
    sub_mode = st.radio("اختر العملية:", ["تحليل ومعاينة الروابط 🔗", "فحص ملف 📁"], horizontal=True)
    
    if sub_mode == "تحليل ومعاينة الروابط 🔗":
        p_url = st.text_input("ألصق الرابط هنا للفحص والعرض:")
        col1, col2 = st.columns(2)
        
        with col1:
            btn_preview = st.button("👁️ عرض محتوى الصفحة")
        with col2:
            btn_check = st.button("🛡️ فحص أمان الرابط")

        if p_url:
            # الجزء الخاص بالمعاينة (الذي طلبته)
            if btn_preview:
                with st.spinner("جاري جلب معاينة الصفحة..."):
                    data = get_site_preview(p_url)
                    if data:
                        st.markdown(f"""
                        <div style="background: #1c2128; border: 1px solid #1f6feb; padding: 15px; border-radius: 12px;">
                            <h4 style="color: #58a6ff;">🌐 {data['title']}</h4>
                            <p style="color: #8b949e;">{data['desc']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("تعذر عرض الصفحة. قد يكون الموقع محجوباً.")

            # الجزء الخاص بنتيجة الفحص (سليم أم لا)
            if btn_check:
                with st.spinner("جاري تحليل الرابط..."):
                    try:
                        response = requests.get(p_url, timeout=5)
                        if response.status_code == 200:
                            if p_url.startswith("https"):
                                st.success("✅ الرابط سليم: الموقع مشفر (SSL) واستجابته طبيعية.")
                            else:
                                st.warning("⚠️ الرابط يعمل ولكنه غير مشفر (HTTP): قد يكون غير آمن لنقل البيانات الحساسة.")
                        else:
                            st.error(f"❌ الرابط مشبوه: الموقع أعاد رمز خطأ ({response.status_code})")
                    except:
                        st.error("❌ الرابط غير سليم: تعذر الاتصال بالموقع أو الرابط وهمي.")
                    
                    send_to_telegram(f"🔍 فحص رابط: {p_url}")

    else: # فحص الملفات
        u_file = st.file_uploader("ارفع الملف للفحص البصري:", type=None)
        if st.button("🛡️ بدء فحص الملف"):
            if u_file:
                raw_data = u_file.getvalue()
                try:
                    content = raw_data.decode("utf-8")
                except:
                    content = raw_data.decode("latin-1", errors="replace")
                
                st.info(f"📄 فحص ملف: {u_file.name}")
                st.code(content[:2000], language="text")
                st.success("✅ تم فحص هيكل الملف بصرياً بنجاح.")
                send_to_telegram(f"📁 فحص ملف: {u_file.name}")
