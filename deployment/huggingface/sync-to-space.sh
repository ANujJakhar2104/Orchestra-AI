@'
#!/bin/bash
# Push local main branch to the Hugging Face Space git remote.
# Run this whenever you want to deploy backend changes.
set -e

SPACE_REMOTE="hf-space"
SPACE_URL="https://huggingface.co/spaces/jakharanuj/orchestra-ai-backend"

if ! git remote | grep -q "^${SPACE_REMOTE}$"; then
  echo "Adding remote '${SPACE_REMOTE}' -> ${SPACE_URL}"
  git remote add ${SPACE_REMOTE} ${SPACE_URL}
fi

echo "Pushing main -> ${SPACE_REMOTE}..."
git push ${SPACE_REMOTE} main

echo "Done. Check build logs at: ${SPACE_URL}"
'@ | Set-Content -Path deployment\huggingface\sync-to-space.sh -NoNewline