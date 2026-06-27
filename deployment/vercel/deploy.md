@'
# Deploying Frontend to Vercel

## One-time setup
1. vercel.com -> Add New Project -> import Orchestra-AI-voice-agents repo
2. Root Directory: client
3. Build Command: npm run build  |  Output Directory: dist  (auto-detected)
4. Environment Variables -> add:
   VITE_BACKEND_URL = https://jakharanuj-orchestra-ai-backend.hf.space

## Every deploy after that
Push to main -> Vercel auto-builds + deploys. No manual step.

## Notes
vercel.json here is a reference. If custom rewrites/headers are needed,
copy it into client/vercel.json (Vercel's project root = client/, per the
Root Directory setting above).
'@ | Set-Content -Path deployment\vercel\DEPLOY.md