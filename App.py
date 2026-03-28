import streamlit as st
import yt_dlp
import os
import base64
import requests

# دالة لتحويل الملف لرابط تحميل مباشر (حل مشكلة الصلاحيات)
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}" class="preview-link" style="background:#238636; text-decoration:none; display:block; text-align:center; padding:15px; border-radius:10px; color:white; font-weight:bold;">📥 اضغط هنا لحفظ الفيديو فوراً</a>'
    return href

# --- داخل تبويب التحميل ---
with tabs[2]:
    st.subheader("🎬 محمل الفيديو الذكي")
    v_url = st.text_input("ألصق رابط الفيديو هنا:", key="final_dl")
    if st.button("🚀 معالجة التحميل الآن"):
        if v_url:
            with st.spinner("جاري التحميل والمعالجة..."):
                try:
                    # إعدادات ثابتة لمنع بياض الشاشة
                    ydl_opts = {'format': 'best', 'outtmpl': 'ayman_video.mp4', 'quiet': True, 'noplaylist': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_url])
                    
                    if os.path.exists("ayman_video.mp4"):
                        st.video("ayman_video.mp4") # عرض الفيديو للمعاينة
                        # استخدام الرابط المباشر بدلاً من زر st.download_button العادي
                        st.markdown(get_binary_file_downloader_html("ayman_video.mp4", "Video"), unsafe_allow_html=True)
                        os.remove("ayman_video.mp4")
                        st.success("تم التجهيز بنجاح!")
                except Exception as e:
                    st.error(f"حدث خطأ: تأكد من الرابط أو جرب لاحقاً.")
