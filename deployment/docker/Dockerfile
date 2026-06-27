# OrchestraAI Backend — Hugging Face Spaces (Docker SDK)
# Python FastAPI + Pipecat voice pipeline
# CPU-only PyTorch (~800MB vs ~2.5GB with CUDA) — fast builds, matches CPU-only config (STT/SmartTurn run on cpu anyway)

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# HF Spaces runs containers as non-root UID 1000 — create it so file
# ownership is correct, otherwise model-cache writes fail at runtime.
RUN useradd -m -u 1000 user

COPY --chown=user requirements.txt .

# CPU-only PyTorch FIRST (avoids pulling CUDA wheels — saves ~1.7GB)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

ARG CACHEBUST=1

COPY --chown=user app/ ./app/
COPY --chown=user data/ ./data/
COPY --chown=user scripts/ ./scripts/

# Writable cache dirs for model downloads (wav2vec2 emotion model, SmartTurn ONNX)
ENV HF_HOME=/app/.cache/huggingface
ENV TORCH_HOME=/app/.cache/torch
RUN mkdir -p /app/.cache && chown -R user:user /app

USER user

# HF Spaces Docker SDK requires listening on 7860
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=5 \
    CMD curl -f http://localhost:7860/health || exit 1
# 60s start-period covers emotion model + SmartTurn ONNX load on first boot

CMD ["python", "-m", "app.main"]