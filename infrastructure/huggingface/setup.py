"""
OrchestraAI — Hugging Face Space Setup Script

Creates and configures the HF Space via huggingface_hub API.
Run once during initial setup.

Usage:
    pip install huggingface_hub
    python infrastructure/huggingface/setup.py
"""

from huggingface_hub import HfApi
import os

HF_TOKEN = os.environ.get("HF_TOKEN")  # huggingface.co/settings/tokens
SPACE_OWNER = "jakharanuj"
SPACE_NAME = "orchestra-ai-backend"

api = HfApi(token=HF_TOKEN)

def create_space():
    print(f"Creating Space: {SPACE_OWNER}/{SPACE_NAME}")
    api.create_repo(
        repo_id=f"{SPACE_OWNER}/{SPACE_NAME}",
        repo_type="space",
        space_sdk="docker",
        private=False,
        exist_ok=True,
    )
    print(f"Space URL: https://huggingface.co/spaces/{SPACE_OWNER}/{SPACE_NAME}")

def check_space_status():
    info = api.space_info(f"{SPACE_OWNER}/{SPACE_NAME}")
    print(f"Stage: {info.runtime.stage}")
    print(f"Hardware: {info.runtime.hardware}")
    print(f"URL: https://{SPACE_OWNER}-{SPACE_NAME}.hf.space")

if __name__ == "__main__":
    if not HF_TOKEN:
        print("ERROR: Set HF_TOKEN environment variable")
        print("Get token from: https://huggingface.co/settings/tokens")
        exit(1)

    create_space()
    check_space_status()
    print("\nNext steps:")
    print("1. Add secrets via Space -> Settings -> Variables and secrets")
    print("   See: infrastructure/huggingface/space-config.md")
    print("2. Push code to Space:")
    print("   ./deployment/huggingface/sync-to-space.sh")