FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Copy requirements and setup files
COPY requirements.txt .
COPY setup.py .
COPY src/ src/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY --chown=user:user . .
RUN mkdir -p /app/logs && chown -R user:user /app

USER user

# Expose port (Hugging Face default: 7860)
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"]
