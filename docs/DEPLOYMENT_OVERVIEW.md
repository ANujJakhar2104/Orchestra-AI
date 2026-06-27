# OrchestraAI - Deployment Overview

> A guide to our production-ready, decoupled deployment architecture: Vercel for Frontend and Hugging Face Spaces for Backend.

---

## 🏗️ Architecture Philosophy
Unlike a monolithic AWS setup, we have moved to a **decoupled architecture** to ensure maximum scalability, zero-cost infrastructure, and better performance for real-time voice AI.

### Infrastructure Layers

| Layer | Technology | Why We Chose It |
|-------|------------|-----------------|
| **Frontend UI** | Vercel | Global CDN, optimized for Vite, seamless GitHub CI/CD |
| **Backend API** | Hugging Face Spaces | 16GB RAM for ML models, Docker-native, zero-cost |
| **Transport** | WebSockets (RTVI) | Real-time bi-directional audio/event streaming |

---

## 🚀 Deployment Workflow

### 1. Backend: Hugging Face Spaces
We deploy our FastAPI backend as a Docker container on Hugging Face Spaces to handle heavy AI models (MSP-PODCAST, LightRAG).

- **SDK:** Docker
- **Hardware:** CPU Basic (Free tier)
- **Deployment:** Automatic sync from GitHub repository.
- **Environment:** 
    - `PUBLIC_URL`: `https://[your-space-name].hf.space`
    - API keys are managed via "Variables and Secrets".

### 2. Frontend: Vercel
Our TypeScript/Vite frontend is hosted on Vercel for sub-millisecond global delivery.

- **Root Directory:** `client/`
- **Build Command:** `npm run build`
- **Environment Variables:**
    - `VITE_BACKEND_URL`: `https://[your-space-name].hf.space`

---

## 💰 Economic Analysis

### Monthly Infrastructure Cost

| Component | Cost |
|-----------|------|
| Hugging Face Spaces (Backend) | **FREE** |
| Vercel Frontend Hosting | **FREE** |
| SSL Certificates | **FREE** |
| **Total Infrastructure** | **$0/month** |

### Estimated API Costs (Moderate Usage: ~100 conversations/day)

| Service | Estimated Monthly Cost |
|---------|------------------------|
| Deepgram STT/TTS | ~$11.00 |
| DeepSeek / Gemini | ~$3.00 |
| **Total API** | **~$14/month** |

**Savings:** 100% savings on infrastructure compared to traditional VPS/AWS setups.

---

## 📊 Deployment Architecture

```text
Browser (TypeScript/Vite - Hosted on Vercel)
    │
    │  WebSocket (/ws) — Pipecat RTVI Protocol
    │
FastAPI (app/main.py) — Hosted on Hugging Face Spaces (Docker)
    │
    ├─ Pipecat Pipeline (per session)
    │   ├─ STT: Deepgram Nova-3
    │   ├─ LLM: DeepSeek V3
    │   ├─ TTS: Cartesia Sonic-3
    │   ├─ Emotion: HybridEmotionDetector (Audio + Text)
    │   └─ Turn: SmartTurn v3 ONNX
    │
    └─ Session Management (Live agent transfer, Context memory)