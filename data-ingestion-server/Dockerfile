FROM python:3.11-bullseye

RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    tesseract-ocr \
    libgl1-mesa-glx \
    cmake \
    openjdk-11-jre-headless \
    git \
    curl \
    wget \
    libssl-dev \
    libffi-dev \
    ffmpeg \
    libsox-fmt-mp3 \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME if needed by sudachipy
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

WORKDIR /app

COPY requirements.txt .

# Install Rust for building sudachipy
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

#RUN python -m nltk.downloader punkt
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

COPY . .
ENV PYTHONPATH=/app/src

ENV PORT=7860

EXPOSE 7860

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
