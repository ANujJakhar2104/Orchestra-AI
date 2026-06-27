# OrchestraAI — Deployment Guide

Backend runs on Hugging Face Spaces (Docker SDK), frontend on Vercel.

## Architecture
Browser (Vite/TypeScript) — Vercel

│

│  WebSocket (/ws) — Pipecat RTVI Protocol

▼

FastAPI (app/main.py) — Hugging Face Spaces (Docker)

│

├─ STT: Deepgram Nova-3

├─ LLM: Groq (DeepSeek V3 / Gemini)

├─ TTS: Cartesia Sonic-3

├─ Emotion: HybridEmotionDetector (MSP-PODCAST + LLM text)

└─ Turn: SmartTurn v3 ONNX

## Backend — Hugging Face Spaces

### One-time setup
1. Create Space: huggingface.co/new-space → SDK: Docker
2. Add secrets via Space → Settings → Variables and secrets:
   - DEEPGRAM_API_KEY
   - GROQ_API_KEY
   - CARTESIA_API_KEY
   - CARTESIA_VOICE_ID
   - GOOGLE_API_KEY
   - PUBLIC_URL = https://jakharanuj-orchestra-ai-backend.hf.space
3. Ensure repo root has `Dockerfile` and `README.md` with correct frontmatter

### Deploy
```bash
./deployment/huggingface/sync-to-space.sh
# or: git push hf-space main
```

### Required root files (HF Spaces reads these from repo root only)
- `/Dockerfile` — see `deployment/docker/Dockerfile` as reference
- `/README.md` — must have `sdk: docker` and `app_port: 7860` in YAML frontmatter

## Frontend — Vercel

### One-time setup
1. vercel.com → Add New Project → import this repo
2. Root Directory: `client`
3. Build Command: `npm run build` | Output Directory: `dist`
4. Environment Variables:
   - VITE_BACKEND_URL = https://jakharanuj-orchestra-ai-backend.hf.space

### Deploy
Push to `main` → Vercel auto-builds. No manual step needed.

## Environment Variables Reference

| Variable | Used By | Description |
|----------|---------|-------------|
| DEEPGRAM_API_KEY | Backend | Speech-to-Text (Nova-3) |
| GROQ_API_KEY | Backend | LLM inference (DeepSeek V3) |
| CARTESIA_API_KEY | Backend | Text-to-Speech (Sonic-3) |
| CARTESIA_VOICE_ID | Backend | Per-persona voice IDs |
| GOOGLE_API_KEY | Backend | Gemini fallback LLM |
| PUBLIC_URL | Backend | Backend public URL for CORS |
| VITE_BACKEND_URL | Frontend | Backend WebSocket URL |

## Cost

| Component | Cost |
|-----------|------|
| HF Spaces Backend (CPU Basic, 2vCPU/16GB) | FREE |
| Vercel Frontend | FREE |
| Deepgram STT/TTS (~100 conversations/day) | ~$11/month |
| Groq/Gemini LLM | ~$3/month |
| **Total** | **~$14/month** |

## Troubleshooting

**Cold start slow (~30-60s):** Normal — MSP-PODCAST emotion model + SmartTurn ONNX loads on first boot. Healthcheck has 60s start-period.

**WebSocket fails:** Check VITE_BACKEND_URL in Vercel env vars matches live HF Space URL.

**Build fails on HF Spaces:** Check Space logs. Common cause: requirements.txt version conflicts or missing ffmpeg (already in Dockerfile).

**Permission errors (model cache):** Dockerfile creates UID 1000 user and sets HF_HOME/TORCH_HOME — ensure Dockerfile at root matches `deployment/docker/Dockerfile`.
