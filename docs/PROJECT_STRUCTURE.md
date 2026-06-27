# OrchestraAI — Project Structure

## Root Directory
Orchestra-AI-voice-agents/

├── app/                    # Python backend (FastAPI + Pipecat)

│   ├── core/              # Server, pipeline orchestration

│   ├── services/          # STT, TTS, LLM, emotion detection

│   ├── processors/        # Pipecat frame processors

│   └── config/            # config.yaml + loader

│

├── client/                 # TypeScript/Vite frontend

│   ├── src/               # app.ts, audio.ts, websocket.ts

│   ├── public/            # Static assets

│   └── dist/              # Production build output

│

├── data/                   # Knowledge base + persona data

│

├── deployment/             # Deployment configs & scripts

│   ├── docker/            # Dockerfile (reference) + .dockerignore

│   ├── huggingface/       # sync-to-space.sh, .env.example, DEPLOY.md

│   └── vercel/            # vercel.json (reference), DEPLOY.md

│

├── docs/                   # Documentation

│   ├── guides/            # Troubleshooting, testing guides

│   └── images/            # Architecture diagrams

│

├── scripts/                # Utility scripts (health check, monitoring)

├── .github/workflows/      # GitHub Actions CI/CD

│

├── Dockerfile              # HF Spaces root Dockerfile

├── README.md               # HF Spaces frontmatter + project overview

├── requirements.txt

└── .env.example

## Key Modules

### `/app/services/`
| File | Purpose |
|------|---------|
| `stt.py` | Deepgram Nova-3 speech-to-text |
| `tts.py` | Cartesia Sonic-3 text-to-speech |
| `conversation.py` | Groq/Gemini LLM conversation manager |
| `msp_emotion_detector.py` | MSP-PODCAST audio emotion model |
| `llm_text_sentiment.py` | LLM-based text sentiment |
| `hybrid_emotion_detector.py` | 70% audio + 30% text emotion fusion |
| `smart_turn.py` | SmartTurn v3 ONNX turn detection |

### `/app/core/`
| File | Purpose |
|------|---------|
| `server.py` | FastAPI server, WebSocket /ws endpoint |
| `voice_assistant.py` | Pipecat pipeline orchestrator, 6-persona routing |

### `/client/src/`
| File | Purpose |
|------|---------|
| `app.ts` | Main app, persona selection UI |
| `audio.ts` | Microphone capture, audio playback |
| `websocket.ts` | RTVI WebSocket protocol handler |

## Personas
Aanya · Arjun · Priya · Serena · Rohan · Zara — each with distinct voice (Cartesia voice ID), personality prompt, and language style.

## Deployment Targets
- **Backend:** Hugging Face Spaces (Docker SDK) — jakharanuj/orchestra-ai-backend
- **Frontend:** Vercel — Root dir: client/