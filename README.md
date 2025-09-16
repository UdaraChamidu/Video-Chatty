# 🎬 Video Chatty - Chat with Videos

Video chatty is a Streamlit-based AI app that lets you **chat interactively with videos**.  
You can upload a local video file or provide a YouTube link, and the app extracts video content (via transcripts or direct processing) to answer your questions using **Google Gemini’s generative AI**.

[![Open in Browser](https://img.shields.io/badge/Open%20in%20Browser-🌐-blueviolet?style=for-the-badge)](http://3.91.52.125)

---

## 🚀 Features

- **Upload Local Videos:** Upload `.mp4` and other video formats, processed with Gemini Video API.
- **YouTube Transcript Fetching:** Provide a YouTube URL, and the app automatically fetches English subtitles (captions) using `yt-dlp`.
- **Interactive Chat:** Ask questions about the video content or transcript, powered by Gemini’s generative model.
- **Chat History:** Maintain an interactive chat session with previous messages.
- **Dockerized Deployment:** Packaged into a Docker container for easy portability.
- **AWS Hosting:** Deployed using AWS EC2 for scalable cloud hosting.
- **GitHub Actions CI/CD:** Automatic deployment to EC2 via GitHub Actions on each push to `main`.

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
- [AWS EC2](https://aws.amazon.com/ec2/) — Cloud hosting for scalable application deployment
- [GitHub Actions](https://github.com/features/actions) — CI/CD automation

---

## ⚙️ Setup and Usage

### 🔹 Local Development

```bash
git clone https://github.com/UdaraChamidu/video-chatty.git
cd video-chatty
pip install -r requirements.txt
streamlit run app.py
```

### 🔹 Deployment on AWS EC2 with Docker & GitHub Actions CI/CD

1. **Prepare EC2 Instance:**
   - Launch an Ubuntu EC2 instance.
   - SSH in: `ssh -i <your-key.pem> ubuntu@<your-ec2-ip>`
   - Install Docker:
     ```bash
     sudo apt update
     sudo apt install -y docker.io
     sudo usermod -aG docker $USER
     ```
     Log out and log back in to activate the Docker group.

2. **Configure GitHub Actions:**
   - Workflow file: `.github/workflows/deploy.yml`
   - On each push to `main`, GitHub Actions will:
     - Build the Docker image
     - Copy the image to EC2
     - SSH into EC2 and run the container

3. **Add GitHub Secrets:**
   - `EC2_HOST`: Your EC2 public IP (e.g., `3.91.52.125`)
   - `EC2_SSH_KEY`: Contents of your EC2 private key

4. **Access the App:**
   - Open `http://<your-ec2-ip>` in your browser (default port 80).

#### Example: Manually Start the App on EC2

If you need to manually run the app on EC2:
```bash
docker run -d --name video-chatty-app -p 80:8501 video-chatty-app
```
- Visit: `http://<your-ec2-ip>` in your browser

---

## 📚 Future Plans

- Download Chat as PDF — Export full chat history as a formatted PDF.
- Sinhala Translation — Localized experience by translating responses to Sinhala.
- Nginx/Load Balancer Setup — Custom domain + HTTPS support.
