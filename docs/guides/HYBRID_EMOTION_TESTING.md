# OrchestraAI — Hybrid Emotion Detection Testing Guide

## What Was Implemented

A **hybrid emotion detection system** combining:
- **Audio emotion (70% weight)** — MSP-PODCAST wav2vec2 model (local, no API cost)
- **Text sentiment (30% weight)** — LLM-based text sentiment via Groq (llm_text_sentiment.py)
- **Mismatch detection** — identifies sarcasm, politeness masking, emotional incongruence
- **Dynamic weight adjustment** — if audio confidence low (e.g. noisy env), text weight increases

## Quick Start

### Start backend
```bash
cd D:\Orchestra-AI-voice-agents
.venv\Scripts\activate
python -m app.main
```

### Look for this in startup logs
ToneAwareProcessor HYBRID (Audio 70% + Text 30%): MSP-PODCAST, conf=0.25, buffer=1000ms, stability=2, cooldown=2.0s
✅ "HYBRID (Audio 70% + Text 30%)" = hybrid mode active
❌ "AUDIO-ONLY" = hybrid disabled (check use_hybrid_mode=True in voice_assistant.py)

---

## Reading the Logs

### Every ~1s during conversation:
🔄 HYBRID MODE: Processing audio + text (transcript: 'Hello, how are you...')

### Detailed result:
🎯 HYBRID RESULT:

Primary Emotion: frustrated (confidence: 78%)

Audio: frustrated (82%) × 70%

Text:  neutral (70%) × 30%

Mismatch: True — User masking frustration with polite language

Fused A/V/D: 0.72/0.36/0.58

**A/V/D** = Arousal / Valence / Dominance (dimensional emotion model)

---

## Test Scenarios

### Test 1: Aligned emotions
Say: *"This is really frustrating me!"*
Expected: Audio=frustrated, Text=frustrated, Mismatch=False

### Test 2: Polite masking (mismatch)
Say with annoyed tone: *"Thank you for your help"*
Expected: Audio=frustrated, Text=neutral, Mismatch=True

### Test 3: Sarcasm
Say enthusiastically: *"Oh great, another problem"*
Expected: Audio=excited, Text=frustrated, Mismatch=True

### Test 4: Low audio confidence (noisy)
Say in noisy environment: *"This isn't working!"*
Expected: weights auto-adjust to 40% audio / 60% text, Primary=frustrated

---

## Configuration

### Enable/disable hybrid mode
In `app/core/voice_assistant.py`:
```python
tone_aware_processor = ToneAwareProcessor(
    tts_service=tts_service,
    use_hybrid_mode=True,   # False = audio-only
    cooldown_seconds=2.0,
    enabled=True
)
```

### Adjust weights
In `app/services/hybrid_emotion_detector.py`:
```python
HybridEmotionDetector(
    default_audio_weight=0.7,   # 70% audio
    default_text_weight=0.3,    # 30% text
    mismatch_threshold=0.8      # higher = less sensitive to mismatch
)
```

---

## Troubleshooting

**Still seeing AUDIO-ONLY:** Set `use_hybrid_mode=True` in ToneAwareProcessor init.

**MSP-PODCAST model downloading on first run:** Normal — ~440MB, downloads to `app/.cache/` (or `HF_HOME` on HF Spaces). Subsequent starts use cached model.

**High latency on text sentiment:** Groq LLM call should be <200ms. If slow, check GROQ_API_KEY and Groq API status.

**On HF Spaces — model cache wiped on restart:** Normal for free tier ephemeral storage. Model re-downloads on cold start (~30-60s). Paid tier has persistent storage.

---

## Success Checklist

- [ ] Startup log shows "HYBRID (Audio 70% + Text 30%)"
- [ ] Logs show "🔄 HYBRID MODE" during conversation
- [ ] "🎯 HYBRID RESULT" shows both audio + text breakdown
- [ ] Mismatch detection triggers on sarcastic/masked tone
- [ ] Weights adjust automatically in noisy conditions