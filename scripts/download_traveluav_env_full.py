import os
from huggingface_hub import snapshot_download

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HOME"] = "/root/autodl-tmp/hf_home"
os.environ["HF_HUB_CACHE"] = "/root/autodl-tmp/hf_home/hub"

local_dir = "/root/autodl-tmp/TravelUAV_envs"

path = snapshot_download(
    repo_id="wangxiangyu0814/TravelUAV_env",
    repo_type="dataset",
    local_dir=local_dir,
    resume_download=True,
)

print("Downloaded to:", path)
print("Local dir:", local_dir)
