@'
# OrchestraAI — Infrastructure Overview

Zero-cost, serverless infrastructure. No AWS, no VPS, no Kubernetes.

## Stack

| Layer | Provider | Plan | Cost |
|-------|----------|------|------|
| Backend API | Hugging Face Spaces | CPU Basic (Free) | $0/month |
| Frontend | Vercel | Hobby (Free) | $0/month |
| SSL/CDN | Included | — | $0/month |
| **Total** | | | **$0/month** |

## Why This Stack

- **HF Spaces**: 2 vCPU / 16GB RAM — enough for MSP-PODCAST + SmartTurn ONNX + FastAPI
- **Vercel**: Global CDN, auto-deploys on push, perfect for Vite/TypeScript
- **No docker-compose**: HF Spaces builds a single Dockerfile directly, no orchestration needed
- **No reverse proxy**: HF Spaces handles routing/SSL/domain itself

## Structure
infrastructure/

huggingface/    # HF Space configuration & setup

vercel/         # Vercel project configuration

## Deployment Scripts
See `deployment/huggingface/` and `deployment/vercel/` for deploy runbooks.