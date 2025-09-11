# Use an official slim Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8501

# Create app directory
WORKDIR /app

# system deps for yt_dlp, ffmpeg might be needed for some video formats
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     ffmpeg \
     build-essential \
     curl \
  && rm -rf /var/lib/apt/lists/*

# copy requirements first for caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy app code
COPY . /app
# copy cookies.txt into the container
COPY cookies.txt /app/cookies.txt

# create non-root user (optional but good practice)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the Streamlit default port
EXPOSE 8501

# Streamlit config: bind to 0.0.0.0 and disable XSRF
ENV STREAMLIT_SERVER_RUN_ON_SAVE=false
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=${PORT}

# Entrypoint to run streamlit
CMD ["sh", "-c", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"]

