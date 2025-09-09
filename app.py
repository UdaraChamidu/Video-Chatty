import streamlit as st
import google.generativeai as genai
import os
import tempfile
import time
from pathlib import Path
import mimetypes
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
import re
import requests

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY", "")

# Page config
st.set_page_config(
    page_title="Video Master",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================
#   Video Processing Class
# ===========================
class VideoProcessor:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def upload_video(self, video_path, display_name=None):
        try:
            video_file = genai.upload_file(
                path=video_path,
                display_name=display_name or "uploaded_video"
            )
            return video_file
        except Exception as e:
            st.error(f"Error uploading video: {str(e)}")
            return None

    def wait_for_file_processing(self, video_file):
        try:
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = genai.get_file(video_file.name)
            if video_file.state.name == "FAILED":
                raise ValueError("Video processing failed")
            return video_file
        except Exception as e:
            st.error(f"Error processing video: {str(e)}")
            return None

    def chat_with_video(self, video_file, prompt):
        try:
            system_prompt = (
                "You are a helpful AI assistant that analyzes the provided video content. "
                "Always base your answers strictly on the video/transcript. "
                "Be concise, clear, user friendly and accurate. "
                "If the answer is not in the video, say you cannot find it using the video."
            )
            response = self.model.generate_content([video_file, system_prompt, prompt])
            return response.text
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return None

# ===========================
#   Helper Functions
# ===========================
def is_video_file(file):
    if file is None:
        return False
    mime_type, _ = mimetypes.guess_type(file.name)
    return mime_type and mime_type.startswith('video/')

def get_file_size_mb(file):
    return len(file.getvalue()) / (1024 * 1024)

def reset_chat():
    st.session_state.messages = []
    if 'video_file' in st.session_state:
        try:
            # If the "video_file" is an object with a name attribute (uploaded video), delete it from Gemini
            if hasattr(st.session_state.video_file, 'name'):
                genai.delete_file(st.session_state.video_file.name)
        except:
            pass
        del st.session_state.video_file
    if 'video_processor' in st.session_state:
        del st.session_state.video_processor
    if 'video_name' in st.session_state:
        del st.session_state.video_name

def display_video(video_bytes, video_name):
    st.markdown(f"### 🎬 {video_name}")
    st.video(video_bytes)

def parse_vtt_to_text(vtt_content):
    # Remove WEBVTT header and timestamps, leaving only subtitle text lines
    lines = vtt_content.splitlines()
    text_lines = []
    for line in lines:
        # skip WEBVTT header and timestamps lines like 00:00:01.000 --> 00:00:04.000
        if line.strip() == '' or line.startswith("WEBVTT") or re.match(r'\d{2}:\d{2}:\d{2}\.\d{3} -->', line):
            continue
        text_lines.append(line.strip())
    return " ".join(text_lines)

def get_youtube_captions(video_url):
    # Extract video ID
    video_id_match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", video_url)
    if not video_id_match:
        return None, "Invalid YouTube URL."
    video_id = video_id_match.group(1)

    ydl_opts = {
    'skip_download': True,
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'subtitlesformat': 'vtt',
    'quiet': True,
    'outtmpl': '%(id)s.%(ext)s',
    'cookiefile': 'cookies.txt',  # 👈 add this
}

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # subtitles and automatic_captions are dicts with language keys
            subtitles = info.get('subtitles') or {}
            automatic_captions = info.get('automatic_captions') or {}

            # Prefer manual subtitles over automatic captions
            subs = subtitles if subtitles else automatic_captions
            if 'en' not in subs:
                return None, "English subtitles not available for this video."

            subtitle_url = subs['en'][0]['url']
            resp = requests.get(subtitle_url)
            if resp.status_code != 200:
                return None, "Failed to fetch subtitles."
            transcript_text = parse_vtt_to_text(resp.text)
            if not transcript_text.strip():
                return None, "Subtitles are empty."
            return transcript_text, None
    except Exception as e:
        return None, str(e)

# ===========================
#   Session State Initialization
# ===========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "video_file" not in st.session_state:
    st.session_state.video_file = None

if "video_processor" not in st.session_state:
    st.session_state.video_processor = VideoProcessor(API_KEY) if API_KEY else None

if "video_name" not in st.session_state:
    st.session_state.video_name = None

# ===========================
#   Sidebar - Chat Controls
# ===========================
with st.sidebar:
    st.header("💬 Chat Controls")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🔄 Reset All"):
            reset_chat()
            st.rerun()

# ===========================
#   Main Interface
# ===========================
st.title("🎬 Chat with Videos")
st.markdown("Chat with your video — upload a file or provide a YouTube link.")

if not API_KEY:
    st.error("❌ API key not found in `.env` file. Please set GEMINI_API_KEY and restart.")
    st.stop()

source_type = st.radio(
    "Select video source:",
    ["Upload a video file", "YouTube video link"],
    horizontal=True
)

if source_type == "Upload a video file":
    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=["mp4", "avi", "mov", "mkv", "webm", "MP4", "M4A"],
    )
    if uploaded_file:
        if not is_video_file(uploaded_file):
            st.error("Please upload a valid video file.")
        else:
            file_size = get_file_size_mb(uploaded_file)
            st.info(f"File size: {file_size:.2f} MB")
            if file_size > 100:
                st.warning("Large files may take longer to process.")
            if st.session_state.video_file is None or st.session_state.video_name != uploaded_file.name:
                with st.spinner("Uploading and processing video..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    try:
                        video_file = st.session_state.video_processor.upload_video(tmp_path, uploaded_file.name)
                        if video_file:
                            processed_file = st.session_state.video_processor.wait_for_file_processing(video_file)
                            if processed_file:
                                st.session_state.video_file = processed_file
                                st.session_state.video_name = uploaded_file.name
                                st.success(f"✅ Video processed successfully! You can now ask questions on: **{st.session_state.video_name}**")
                                st.session_state.messages = []
                    finally:
                        os.unlink(tmp_path)
            if st.session_state.video_file:
                display_video(uploaded_file.getvalue(), uploaded_file.name)

elif source_type == "YouTube video link":
    yt_url = st.text_input("Enter YouTube URL")
    if yt_url:
        if st.session_state.video_file is None or st.session_state.video_name != yt_url:
            with st.spinner("Fetching transcript from YouTube..."):
                transcript_text, err = get_youtube_captions(yt_url)
                if err:
                    st.error(f"Error: {err}")
                else:
                    st.session_state.video_file = transcript_text
                    st.session_state.video_name = yt_url
                    st.success(f"✅ Transcript ready! You can now ask questions on: **{st.session_state.video_name}**")
                    st.session_state.messages = []
    
# ===========================
#   Chat Interface
# ===========================
if st.session_state.video_file:

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    if prompt := st.chat_input("Ask a question about your video..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            msg_placeholder = st.empty()
            with st.spinner("Analyzing video..."):
                resp = st.session_state.video_processor.chat_with_video(
                    st.session_state.video_file,
                    prompt
                )
            if resp:
                full_resp = ""
                for word in resp.split():
                    full_resp += word + " "
                    msg_placeholder.markdown(full_resp + "▌")
                    time.sleep(0.03)
                msg_placeholder.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp})
            else:
                st.error("Failed to generate response.")

# ===========================
#   Footer
# ===========================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "<p>Built ❤️ with udara, using Gemini API and Streamlit"
    "</div>",
    unsafe_allow_html=True
)
