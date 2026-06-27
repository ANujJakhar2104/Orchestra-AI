# Vercel — Project Configuration Reference

## Project Settings

| Field | Value |
|-------|-------|
| Project Name | orchestra-ai-frontend |
| Framework | Vite |
| Root Directory | client |
| Build Command | npm run build |
| Output Directory | dist |
| Install Command | npm install |

## Environment Variables

Add in: Vercel Dashboard → Project → Settings → Environment Variables

| Key | Value | Environment |
|-----|-------|-------------|
| VITE_BACKEND_URL | https://jakharanuj-orchestra-ai-backend.hf.space | Production |
| VITE_BACKEND_URL | http://localhost:7860 | Development |

## Auto-Deploy Setup

1. Connect GitHub repo in Vercel dashboard
2. Every push to `main` → auto build + deploy
3. PRs get preview deployments automatically

## Custom Domain (Optional)

Vercel Dashboard → Project → Settings → Domains → Add domain
Free SSL included automatically.

## Build Specs (Free Hobby Plan)

| Resource | Limit |
|----------|-------|
| Bandwidth | 100GB/month |
| Build time | 45 min max |
| Deployments | Unlimited |
| Serverless functions | 100GB-hours/month |

## Local Vercel CLI (Optional)

```bash
npm i -g vercel
cd client
vercel dev        # local with Vercel env vars
vercel --prod     # manual deploy to production
```

## Troubleshooting

**Build fails:** Run `npm run build` locally first — must pass before pushing.
**Env vars not working:** VITE_ prefix required for client-side vars. Redeploy after changing.
**SPA routing broken:** vercel.json rewrites rule handles this (all routes → index.html).