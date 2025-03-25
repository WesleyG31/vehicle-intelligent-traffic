import streamlit as st
import os
import tempfile
#import shutil
#import base64
from glob import glob
from src.pipeline.process_video import process_video

st.set_page_config(page_title="Intelligent Traffic Analysis", layout="wide")
st.title("🚦 Intelligent Urban Traffic Analysis System")

st.markdown("Upload a traffic video and the system will detect vehicles, measure speed, read license plates, and generate a full report.")

# Subida de video
uploaded_video = st.file_uploader("📹 Upload the video (.mp4)", type=["mp4"])

if uploaded_video is not None:
    # Guardar temporalmente
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, uploaded_video.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())

    st.success("✅ Processing...")

    #output_video_path = os.path.join(temp_dir, f"analyzed_{uploaded_video.name}")


    # Pipelines
    results = process_video(video_path)

    # Show results
    st.subheader("🎥 Video Analyzed")

    st.video(results["video_analyzed"])

    st.subheader("📊 Traffic Graphs")
    image_files = glob(os.path.join(results["data_folder"], "*.png"))
    for img_path in image_files:
        filename = os.path.basename(img_path).replace("_", " ").replace(".png", "").capitalize()
        st.image(img_path, caption=filename)

    st.subheader("📄 Downloads")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with open(results["report_pdf"], "rb") as f:
            st.download_button("📥 Report PDF", f.read(), file_name="report_traffic.pdf")

    with col2:
        with open(results["violations_csv"], "rb") as f:
            st.download_button("📥 Infringement CSV", f.read(), file_name="violations.csv")

    with col3:
        with open(results["tracking_csv"], "rb") as f:
            st.download_button("📥 Tracking CSV", f.read(), file_name="tracking_data.csv")
    
    with col4:
        with open(results["video_analyzed"], "rb") as f:
            st.download_button("📥 Download video", f.read(), file_name="video_analyzed.mp4")
    st.success("✅ Analysis completed. ¡Thanks for using the app!")
