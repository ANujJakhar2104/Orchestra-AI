@'
# Deploying Backend to Hugging Face Spaces

## One-time setup
1. Space already created: jakharanuj/orchestra-ai-backend (Docker SDK)
2. Secrets added via Space -> Settings -> "Variables and secrets" (see .env.example)

## Every deploy after that
    ./deployment/huggingface/sync-to-space.sh
or manually:
    git push hf-space main

## Required files at repo ROOT (HF Spaces only reads these from root, not from deployment/)
- /Dockerfile
- /README.md  (must have `sdk: docker` + `app_port: 7860` in the YAML frontmatter)

## Notes
- Free tier: 2 vCPU / 16GB RAM, sleeps after 48h inactivity (cold start ~30-60s on next request)
- /health endpoint, 60s start-period covers emotion model load on boot
'@ | Set-Content -Path deployment\huggingface\DEPLOY.md