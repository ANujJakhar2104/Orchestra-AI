Saari files padh li. Analysis:

CLEANUP_SUMMARY.md — purana (Nester, src/ directory, Deepgram TTS, Gemini LLM) → rewrite
DEPLOYMENT_FIX.md — completely irrelevant (Resemble AI, Lightsail, GHCR) → rewrite with HF Spaces issues
DEPLOYMENT_TROUBLESHOOTING.md — Nester/Lightsail/Caddy specific → rewrite for HF Spaces
HYBRID_EMOTION_TESTING.md — actually useful content! Sirf project name + BERT model change karni hai (current project uses LLM text sentiment, not BERT) → light update

Sab ek saath de raha hoon:

1) docs\guides\CLEANUP_SUMMARY.md:
powershell@'
# OrchestraAI — Project Cleanup Summary

**Date:** June 2026
**Status:** Complete

## What Was Removed

### Legacy AWS/Lightsail Deployment Files
- `deployment/aws/` — CloudFormation template, EC2/ECS task definitions, deploy scripts
- `deployment/scripts/` — lightsail-deploy.sh, lightsail-deploy-https.sh
- `deployment/docker/` Caddyfiles (Caddyfile, Caddyfile.graviton, Caddyfile.prod)
- `deployment/docker/` docker-compose variants (ghcr, graviton, https, prod)
- `deployment/docker/a2ui-chatbot-service.code-workspace` — stale workspace file

### Legacy Docs (Nester/AWS era)
- `docs/DEPLOYMENT_STRATEGY.md` — AWS ECS Fargate guide (irrelevant)
- `docs/PROJECT_DOCUMENTATION.md` — Nester bot documentation

### Why Removed
Project migrated from AWS Lightsail/ECS to Hugging Face Spaces (Docker) + Vercel.
No docker-compose orchestration needed — HF Spaces builds a single Dockerfile directly.
No Caddyfile needed — HF Spaces handles routing/SSL/domain itself.

## What Was Added

### New Deployment Structure
- `deployment/huggingface/sync-to-space.sh` — git push to HF Space remote
- `deployment/huggingface/.env.example` — HF Secrets template
- `deployment/huggingface/DEPLOY.md` — deployment runbook
- `deployment/vercel/vercel.json` — Vercel config reference
- `deployment/vercel/DEPLOY.md` — Vercel setup guide

### Updated Docs
- `docs/DEPLOYMENT.md` — rewritten for HF Spaces + Vercel
- `docs/PROJECT_STRUCTURE.md` — reflects current OrchestraAI structure
- `docs/GITHUB_SETUP.md` — HF Spaces git remote + GitHub Actions
- `docs/RESTRUCTURING_SUMMARY.md` — migration history

## Current Active Structure
app/                    # FastAPI + Pipecat backend

client/                 # Vite/TypeScript frontend

deployment/

docker/              # Dockerfile reference

huggingface/         # HF Spaces deploy scripts

vercel/              # Vercel config reference

docs/                   # Updated documentation

## What Was NOT Changed
- `app/` — all backend code unchanged
- `client/` — frontend unchanged
- `requirements.txt` — unchanged
- `.env.example` — updated with current API keys
'@ | Set-Content -Path docs\guides\CLEANUP_SUMMARY.md
2) docs\guides\DEPLOYMENT_FIX.md:
powershell@'
# OrchestraAI — Common Deployment Fixes

## Issue 1: HF Space Build Fails

### Symptoms
Space shows "Build failed" in HF Spaces logs.

### Common Causes & Fixes

**Missing Dockerfile at repo root:**
HF Spaces only reads Dockerfile from the root of the Space repo — not from subfolders.
```bash
# Verify Dockerfile exists at root
dir D:\Orchestra-AI-voice-agents\Dockerfile
```
If missing, copy from reference:
```powershell
Copy-Item deployment\docker\Dockerfile .\Dockerfile
```

**requirements.txt version conflict:**
Check Space build logs for pip install errors. Fix version pins in requirements.txt, then:
```bash
git add requirements.txt
git commit -m "fix: resolve requirements conflict"
git push hf-space main
```

**README.md missing frontmatter:**
HF Spaces requires this exact YAML at top of README.md:
```yaml
---
sdk: docker
app_port: 7860
---
```

---

## Issue 2: Backend Cold Start (~30-60s)

### Symptoms
First request after Space wakes up is very slow or times out.

### Reason
MSP-PODCAST wav2vec2 emotion model + SmartTurn ONNX both load on first boot.
This is expected — Dockerfile has 60s healthcheck start-period for this reason.

### Fix
Nothing to fix — this is normal. Free tier HF Spaces sleep after 48h inactivity.
For production use, upgrade to paid tier (persistent/always-on).

---

## Issue 3: WebSocket Connection Fails on Frontend

### Symptoms
Browser console: `WebSocket connection to 'wss://...' failed`

### Fix
Check VITE_BACKEND_URL in Vercel project settings:
- Go to vercel.com → Project → Settings → Environment Variables
- Should be exactly: `https://jakharanuj-orchestra-ai-backend.hf.space`
- No trailing slash, no /ws suffix (frontend appends /ws itself)

Redeploy Vercel after changing env var (env changes require redeploy).

---

## Issue 4: Permission Error on Model Cache (HF Spaces)

### Symptoms
Space logs show: `PermissionError: [Errno 13] Permission denied: '/root/.cache/...'`

### Reason
HF Spaces runs containers as UID 1000, not root. Root-owned cache dirs fail.

### Fix
Ensure Dockerfile has:
```dockerfile
RUN useradd -m -u 1000 user
ENV HF_HOME=/app/.cache/huggingface
ENV TORCH_HOME=/app/.cache/torch
RUN mkdir -p /app/.cache && chown -R user:user /app
USER user
```
Push updated Dockerfile to trigger rebuild.

---

## Issue 5: Missing API Keys (Space shows 500 errors)

### Symptoms
Space is running but API calls fail with 500/401 errors.

### Fix
Add missing secrets via: HF Space → Settings → Variables and secrets

Required secrets:
| Key | Description |
|-----|-------------|
| DEEPGRAM_API_KEY | STT (Deepgram Nova-3) |
| GROQ_API_KEY | LLM (DeepSeek V3) |
| CARTESIA_API_KEY | TTS (Sonic-3) |
| CARTESIA_VOICE_ID | Per-persona voice IDs |
| GOOGLE_API_KEY | Gemini fallback LLM |
| PUBLIC_URL | https://jakharanuj-orchestra-ai-backend.hf.space |

After adding secrets, restart the Space (Factory reboot in Space settings).

---

## Health Check

```bash
curl https://jakharanuj-orchestra-ai-backend.hf.space/health
# Expected: {"status": "healthy"}

curl https://jakharanuj-orchestra-ai-backend.hf.space/docs
# Expected: FastAPI Swagger UI
```