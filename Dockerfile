FROM python:3.11-slim

WORKDIR /app 

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libavcodec-extra \
    libsndfile1-dev \
    espeak-ng \
    gcc \
    g++ \
    make \
    python3-dev \
    libxext6 \
    libxrender-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY docker-requirements.txt .

RUN pip install --no-cache-dir torch==2.7.1+cpu torchaudio==2.7.1+cpu --index-url https://download.pytorch.org/whl/cpu

RUN mkdir -p src artifacts pipelines utils templates config static

COPY artifacts/audio artifacts/audio
COPY src/ src/
COPY pipelines/ pipelines/
COPY utils/ utils/
COPY templates/ templates/
COPY config/ config/
COPY static/ static/
COPY app.py .

RUN touch src/__init__.py
RUN touch pipelines/__init__.py
RUN touch utils/__init__.py
RUN touch config/__init__.py
RUN touch static/__init__.py

# Verify static files are copied correctly
RUN ls -la static/css/ static/js/
RUN cat static/css/style.css | head -5
RUN cat static/js/script.js | head -5

COPY setup.py .
RUN pip install --no-cache-dir -e .
RUN pip cache purge

RUN chmod -R 755 /app/static

RUN python src/download_pretrained_model.py -y

EXPOSE 5000

CMD ["python", "app.py"]