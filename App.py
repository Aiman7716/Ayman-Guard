# --- تبويب التحميل الصامت (المطور) ---
with tabs[2]:
    st.subheader("🎬 مركز تحميل الوسائط")
    v_url = st.text_input("ألصق رابط الفيديو هنا:", key="vid_input")
    if st.button("🚀 بدء المعالجة والتحميل"):
        if v_url:
            with st.spinner("جاري كسر حماية الرابط وسحب البيانات..."): 
                try:
                    # نستخدم اسم فريد لكل عملية لمنع التعارض
                    temp_vid = f"vid_{random.randint(1000,9999)}.mp4"
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': temp_vid,
                        'quiet': True,
                        'no_warnings': True
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
                        ydl.download([v_url])
                    
                    # التأكد من اكتمال وجود الملف قبل العرض
                    if os.path.exists(temp_vid):
                        with open(temp_vid, "rb") as f:
                            vid_bytes = f.read()
                            st.video(vid_bytes)
                            st.download_button(
                                label="📥 حفظ الفيديو في جهازك الآن", 
                                data=vid_bytes, 
                                file_name="Ayman_Guard_Video.mp4",
                                mime="video/mp4"
                            )
                        os.remove(temp_vid) # تنظيف السيرفر
                        send_to_telegram(f"🎬 نجاح عملية تحميل فيديو جديد بنجاح ✅")
                    else:
                        st.error("❌ حدث خطأ في استخراج الملف، جرب رابطاً آخر.")
                except Exception as e: 
                    st.error(f"❌ فشل المحرك: {e}")
