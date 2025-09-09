# 🎬 Video Master - Chat with Videos

Video Master is a Streamlit-based AI app that lets you **chat interactively with videos**.  
You can upload a local video file or provide a YouTube link, and the app extracts video content (via transcripts or direct processing) to answer your questions using **Google Gemini’s generative AI**.

---

[![Try App](https://img.shields.io/badge/Try%20App-Click%20Here-brightgreen?style=for-the-badge&logo=streamlit)](http://13.216.1.128:8501)

---

## 🚀 Features

- **Upload Local Videos:** Upload `.mp4` and other video formats, processed with Gemini Video API.
- **YouTube Transcript Fetching:** Provide a YouTube URL, and the app automatically fetches English subtitles (captions) using `yt-dlp`.
- **Interactive Chat:** Ask questions about the video content or transcript, powered by Gemini’s generative model.
- **Chat History:** Maintain an interactive chat session with previous messages.
- **Dockerized Deployment:** Packaged into a Docker container for easy portability.
- **AWS Hosting:** Deployed using AWS (ECS/EC2) for scalable cloud hosting.

---

<img width="1307" height="691" alt="screenshot" src="https://github.com/user-attachments/assets/fc2d94e2-c598-44d2-ab2b-0db1a121c11c" />

---

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io/) — Web app framework for Python
- [Google Gemini API](https://ai.google.com/gemini) — Generative AI for video understanding and chat
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) — Extract YouTube subtitles without downloading full videos
- [Python-dotenv](https://pypi.org/project/python-dotenv/) — Manage environment variables securely
- [Requests](https://requests.readthedocs.io/en/latest/) — Fetch subtitle files
- [Docker](https://www.docker.com/) — Containerization for consistent deployment
- [AWS ECS/EC2](https://aws.amazon.com/ecs/) — Cloud hosting for scalable application deployment

---

## ⚙️ Setup and Usage

### 🔹 Local Development
```bash
git clone https://github.com/UdaraChamidu/video-master.git
cd video-master
pip install -r requirements.txt
streamlit run app.py
```

## 📚 Future Plans

- Download Chat as PDF — Export full chat history as a formatted PDF.
- Sinhala Translation — Localized experience by translating responses to Sinhala.
- Nginx/Load Balancer Setup — Custom domain + HTTPS support.

