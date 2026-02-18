import streamlit as st
import yt_dlp
import os
import io

# إعدادات واجهة الموقع
st.set_page_config(page_title="Video Downloader Pro", page_icon="📥", layout="centered")

# تصميم الهيدر
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📥 محمل الفيديوهات الذكي")
st.subheader("قم بتحميل الفيديوهات بأعلى دقة (4K) أو كملفات صوتية")

# إدخال الرابط
url = st.text_input("ألصق رابط الفيديو هنا (يوتيوب، تيك توك، إنستغرام):", placeholder="https://...")

# خيارات التحميل
col1, col2 = st.columns(2)
with col1:
    download_type = st.selectbox("نوع الملف:", ["فيديو (أعلى دقة 4K)", "ملف صوتي (MP3)"])

# دالة التحميل
def download_process(link, is_audio):
    try:
        # إعدادات الذاكرة المؤقتة (لأن الموقع يحمل الملف ثم يرسله للمتصفح)
        ydl_opts = {
            'format': 'bestaudio/best' if is_audio else 'bestvideo+bestaudio/best',
            'outtmpl': 'temp_file.%(ext)s',
            'quiet': True,
            'noplaylist': True,
        }
        
        if is_audio:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info)
            if is_audio: filename = filename.rsplit('.', 1)[0] + '.mp3'
            
            with open(filename, "rb") as f:
                data = f.read()
            
            # حذف الملف المؤقت من السيرفر بعد القراءة
            os.remove(filename)
            return data, filename

    except Exception as e:
        st.error(f"حدث خطأ: {str(e)}")
        return None, None

# زر التحميل
if st.button("تحميل واستخراج الملف"):
    if url:
        with st.spinner("جاري معالجة الفيديو... قد يستغرق الأمر ثواني للدقات العالية"):
            is_audio = True if "صوتي" in download_type else False
            file_data, file_name = download_process(url, is_audio)
            
            if file_data:
                st.success("✅ تم التجهيز بنجاح!")
                st.download_button(
                    label="اضغط هنا لحفظ الملف على جهازك",
                    data=file_data,
                    file_name=file_name,
                    mime="video/mp4" if not is_audio else "audio/mpeg"
                )
    else:
        st.warning("يرجى وضع رابط أولاً!")

st.markdown("---")
st.caption("ملاحظة: السرعة تعتمد على حجم الفيديو الأصلي وسرعة الإنترنت لديك.")