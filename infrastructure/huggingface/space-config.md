# Hugging Face Space — Configuration Reference

## Space Details

| Field | Value |
|-------|-------|
| Owner | jakharanuj |
| Space Name | orchestra-ai-backend |
| URL | https://jakharanuj-orchestra-ai-backend.hf.space |
| SDK | Docker |
| Hardware | CPU Basic (Free) — 2 vCPU, 16GB RAM |
| Visibility | Public |

## README.md Frontmatter (required at repo root)

```yaml
---
title: OrchestraAI Voice Backend
emoji: 🎙️
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---
```

## Variables and Secrets

Add these in: Space → Settings → Variables and secrets

| Key | Type | Description |
|-----|------|-------------|
| DEEPGRAM_API_KEY | Secret | STT — Deepgram Nova-3 |
| GROQ_API_KEY | Secret | LLM — DeepSeek V3 via Groq |
| CARTESIA_API_KEY | Secret | TTS — Cartesia Sonic-3 |
| CARTESIA_VOICE_ID | Secret | Comma-separated per-persona voice IDs |
| GOOGLE_API_KEY | Secret | Gemini fallback LLM |
| PUBLIC_URL | Variable | https://jakharanuj-orchestra-ai-backend.hf.space |

## Hardware Limits (Free Tier)

| Resource | Limit |
|----------|-------|
| CPU | 2 vCPU |
| RAM | 16GB |
| Storage | 50GB ephemeral (wiped on restart) |
| Sleep | After 48h inactivity |
| Build timeout | 30 min |

## Cold Start Behavior

Free tier Spaces sleep after 48h inactivity.
Cold start time: ~30-60s (MSP-PODCAST wav2vec2 + SmartTurn ONNX loading).
Healthcheck start_period=60s in Dockerfile accounts for this.

## Persistent Storage

Free tier: ephemeral only (model cache wiped on restart).
Workaround: models re-download on each cold start from HuggingFace Hub.
HF_HOME and TORCH_HOME set to /app/.cache/ in Dockerfile.

Upgrade to paid tier for persistent /data volume.

## Build Process

HF Spaces automatically:
1. Detects Dockerfile at repo root
2. Builds image (docker build .)
3. Runs container (docker run -p 7860:7860)
4. Exposes at https://jakharanuj-orchestra-ai-backend.hf.space

No docker-compose, no manual build commands needed.