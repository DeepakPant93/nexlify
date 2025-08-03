FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    tesseract-ocr \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Add this to make relative imports work
ENV PYTHONPATH=/app/src

# Copy and install requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Expose and run app
EXPOSE 7860
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]