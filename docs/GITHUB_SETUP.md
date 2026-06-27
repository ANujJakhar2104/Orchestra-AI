# OrchestraAI — GitHub & CI/CD Setup

## Security: Never commit .env

`.env` is in `.gitignore`. Use `.env.example` as template.
For HF Spaces: add secrets via Space → Settings → Variables and secrets.
For Vercel: add env vars via Vercel project settings.

## Repository Setup

```bash
git init
git add .
git commit -m "Initial commit: OrchestraAI Voice Agents"
git remote add origin https://github.com/jakharanuj/Orchestra-AI-voice-agents.git
git push -u origin main
```

## Add HF Spaces Remote

```bash
git remote add hf-space https://huggingface.co/spaces/jakharanuj/orchestra-ai-backend
git push hf-space main
```

After this, use `deployment/huggingface/sync-to-space.sh` for deploys.

## GitHub Actions (auto-deploy to Vercel)

Vercel auto-deploys on push to main via GitHub integration — no workflow file needed.

For HF Spaces auto-sync, add `.github/workflows/deploy-hf.yml`:

```yaml
name: Deploy to HF Spaces
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Push to HF Spaces
        run: |
          git remote add hf-space https://jakharanuj:${{ secrets.HF_TOKEN }}@huggingface.co/spaces/jakharanuj/orchestra-ai-backend
          git push hf-space main --force
```

Add `HF_TOKEN` in GitHub repo → Settings → Secrets and variables → Actions.

## Files in Git

| File | In Git? | Reason |
|------|---------|--------|
| `.env` | ❌ NO | Contains API keys |
| `.env.example` | ✅ YES | Template (no real keys) |
| `Dockerfile` | ✅ YES | HF Spaces build config |
| `README.md` | ✅ YES | HF Spaces frontmatter |
| `requirements.txt` | ✅ YES | Python deps |
| `client/` | ✅ YES | Frontend source |
| `app/` | ✅ YES | Backend source |