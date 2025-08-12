# 🎬 Video Master - Chat with Videos

Video Master is a Streamlit-based AI app that lets you **chat interactively with videos**.  
You can upload a local video file or provide a YouTube link, and the app extracts video content (via transcripts or direct processing) to answer your questions using Google Gemini’s generative AI.

---

## 🚀 Features

- **Upload Local Videos:** Upload `.mp4` videos, which are processed with Gemini Video API.
- **YouTube Transcript Fetching:** Provide a YouTube URL, and the app automatically fetches English subtitles (captions) using `yt-dlp`.
- **Interactive Chat:** Ask questions about the video content or transcript, powered by Gemini’s generative model.
- **Chat History:** Maintain an interactive chat session with previous messages.

---

<img width="1307" height="691" alt="image" src="https://github.com/user-attachments/assets/fc2d94e2-c598-44d2-ab2b-0db1a121c11c" />

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io/) — Web app framework for Python
- [Google Gemini API](https://ai.google.com/gemini) — Generative AI for video understanding and chat
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) — To extract YouTube subtitles without downloading videos
- [Python-dotenv](https://pypi.org/project/python-dotenv/) — To manage environment variables securely
- [Requests](https://requests.readthedocs.io/en/latest/) — To fetch subtitle files

---

## ⚙️ Setup and Usage

```bash
git clone https://github.com/UdaraChamidu/video-master.git
cd video-master
pip install -r requirements.txt
streamlit run app.py

```

## 📚 Future Plans

- Download Chat as PDF: Add functionality to download the full chat history as a nicely formatted PDF document.

- Sinhala Translation: Implement chat translation features to convert chat content and responses into Sinhala language for localized user experience.

