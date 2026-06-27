# OrchestraAI — Deployment Troubleshooting

## Backend (Hugging Face Spaces)

### Space stuck on "Building"
- HF free tier builds can take 5-15 min (CPU-only torch install is ~800MB)
- Check build logs in Space → Logs tab
- If stuck >20 min: Factory reboot from Space settings

### Space builds but immediately crashes
Check logs for:
1. Missing env var → add to Space secrets, reboot
2. Port mismatch → ensure app listens on 7860 (check app/config/config.yaml: fastapi_port: 7860)
3. OOM → free tier has 16GB RAM; MSP-PODCAST + SmartTurn together use ~2-3GB, should be fine

### Logs (HF Spaces)
View real-time logs: Space page → Logs tab
Or via API:
```bash
# If you have HF CLI installed
huggingface-cli repo info jakharanuj/orchestra-ai-backend --repo-type space
```

### Manual redeploy
```bash
# Force rebuild by pushing (even empty commit works)
git commit --allow-empty -m "trigger rebuild"
git push hf-space main
```

---

## Frontend (Vercel)

### Build fails
Check Vercel deployment logs. Common causes:
- TypeScript errors → fix locally, `npm run build` must pass before pushing
- Wrong root directory → ensure Vercel project Root Directory = `client`

### Page loads but voice doesn't work
1. Open browser DevTools → Console tab
2. Look for WebSocket errors
3. Check VITE_BACKEND_URL in Vercel env vars (no trailing slash)
4. Check if HF Space is awake (visit the Space URL directly first)

### Environment variables not updating
Vercel env var changes require a redeploy:
Vercel Dashboard → Deployments → Redeploy (latest)

---

## Local Development

### Run backend locally
```bash
cd D:\Orchestra-AI-voice-agents
.venv\Scripts\activate
python -m app.main
# Runs on http://localhost:7860
```

### Run frontend locally
```bash
cd client
npm install
npm run dev
# Runs on http://localhost:5173
# Set VITE_BACKEND_URL=http://localhost:7860 in client/.env.local
```

### Test health endpoint
```bash
curl http://localhost:7860/health
curl http://localhost:7860/docs
```

### Check persona routes
```bash
curl http://localhost:7860/personas
# Should list: Aanya, Arjun, Priya, Serena, Rohan, Zara
```

---

## Startup Timing (Expected)

| Environment | Cold Start Time | Reason |
|-------------|-----------------|--------|
| Local (good CPU) | 5-10s | Fast disk, warm pip cache |
| HF Spaces (first boot) | 30-60s | MSP-PODCAST model + SmartTurn ONNX loading |
| HF Spaces (warm) | 2-5s | Models already in memory |

Healthcheck `start_period: 60s` in Dockerfile accounts for this — do not reduce it.

---

## Persona / WebSocket Issues

### Persona not switching
- Check Space logs for transfer errors
- Verify all 6 persona configs exist in app/config/config.yaml
- Each persona needs its own CARTESIA_VOICE_ID

### Audio cuts out mid-conversation
- Usually Deepgram WebSocket timeout (long silence)
- Check DEEPGRAM_API_KEY is valid and not rate-limited

### High latency (>3s TTFB)
Normal pipeline latency breakdown:
- STT (Deepgram): ~200-400ms
- LLM (Groq): ~400-800ms
- TTS (Cartesia): ~200-400ms
- Total expected: ~1-2s

If >3s: check Groq API status at status.groq.com