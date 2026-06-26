# OrchestraAI

**Production-ready real-time voice AI with multi-agent personas, hybrid emotion detection, live agent transfer, and dynamic visual UI — all in 1–1.5 second end-to-end latency.**

**🔴 Live Demo:** [https://orchestra-ai-anuj.vercel.app](https://orchestra-ai-anuj.vercel.app)

---

## 📸 Screenshots

<div align="center">
  <img src="docs/images/Screenshot 2026-06-26 211913.jpg" width="85%" alt="Persona Selection - Aanya"/>
  <br/><br/>
  <img src="docs/images/Screenshot 2026-06-26 211925.jpg" width="85%" alt="Persona Selection - Priya"/>
  <br/><br/>
  <img src="docs/images/Screenshot 2026-06-26 212054.jpg" width="85%" alt="Dashboard and Emotion Analysis"/>
</div>

---

## 🚀 What Is This?

OrchestraAI is a full-stack voice conversational assistant built on the [Pipecat](https://github.com/pipecat-ai/pipecat) framework. You speak — the AI listens, understands your emotion, thinks, responds with the right voice, and optionally renders a live visual UI card — all in real time.

It supports **6 distinct AI agent personas**, each with their own voice, personality, and domain expertise. Agents are aware of each other and can **transfer mid-call** — the old agent says a connecting line, and the new agent picks up with full context of your conversation.

---

## ✨ Core Features

### 6 Expert AI Agents (Fully Interconnected)

Every agent knows every other agent and can transfer you mid-call. Voice changes instantly. The new agent receives context of what you were discussing and picks up naturally — no awkward restarts.

| Agent | Role | Specialty | Language |
|-------|------|-----------|----------|
| **Aanya** | General Assistant | Knows a bit about everything, connects you to the right person | English |
| **Arjun** | Problem Solver | Troubleshooting — tech issues, broken workflows, stuck decisions | English |
| **Priya** | Hinglish All-Rounder | Warm desi assistant — science to Bollywood, all in Hinglish | Hinglish |
| **Serena** | Business Strategist | Strategy, sales, fundraising, go-to-market, negotiation | English |
| **Rohan** | Tech Expert | Coding, AI/ML, distributed systems, cloud infra, voice AI | English |
| **Zara** | Lifestyle Coach | Health, fitness, travel, food, self-improvement, relationships | English |

**How live agent transfer works:**
1. Any agent can call `transfer_to_agent()` mid-conversation.
2. The old agent speaks a brief handoff line: *"Let me connect you with Rohan — this is his territory."*
3. The LLM system prompt swaps silently to the new agent's persona.
4. TTS voice switches in real time via `tts.set_voice(voice_id)` — no reconnect, no reload.
5. The orb color, avatar, and UI accent all update on the frontend instantly.
6. The new agent picks up with full context.

---

### 🧠 Hybrid Emotion Detection

A two-channel, weighted fusion emotion detection system that runs non-blocking in the background — adding zero latency to the voice pipeline.

* **Channel 1 (Audio):** MSP-PODCAST wav2vec2 model extracts dimensional emotions (arousal, dominance, valence) directly from voice tone.
* **Channel 2 (Text):** Google Gemini 2.0 Flash analyzes the transcription text for sentiment.
* **Fusion:** Combines both signals (70% Audio / 30% Text) to detect masked emotions (e.g., sarcasm) and dynamically shifts the AI's response tone (e.g., matching a frustrated user with a calm voice).

---

### 🎙️ Voice Pipeline

* **VAD:** Silero VAD (conf=0.92) for accurate voice detection.
* **STT:** Deepgram Nova-3 (streaming).
* **LLM:** DeepSeek V3 (`deepseek-chat`) with LLM Context Aggregator.
* **TTS:** Cartesia Sonic-3 (word timestamps + emotion control).
* **Turn Detection:** SmartTurn v3 ONNX.

---

### 📊 A2UI — Voice-Driven Visual Cards

When the LLM answers a query, it can trigger a **dynamic visual card** rendered in the frontend. Available templates include: `simple-card`, `template-grid`, `timeline`, `contact-card`, `comparison-chart`, `stats-flow-layout`, and more.

---

## 🏗️ Architecture & Deployment

The project is split into a completely decoupled frontend and backend for maximum scalability:

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
