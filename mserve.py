import os
import subprocess
from pathlib import Path

import modal
from fastapp import fast_app

git_url = "https://github.com/kousun12/datadash.git"
git_sha = "256b29b"


img = (
    modal.Image.from_registry("node:20-bookworm", add_python="3.12")
    .apt_install("git")
    .pip_install("fastapi[standard]", "httpx")
    .run_commands(f"git clone {git_url} /app", "cd /app/fw && yarn install")
    .pip_install("aider-chat==0.62.1", "pydantic==2.9.2", "fastapi==0.115.5")
    .run_commands(
        "git config --global user.name 'rob' && git config --global user.email 'kousun12@gmail.com'"
    )
)
# vol = modal.Volume.from_name("datadash_vol", create_if_missing=True)
app = modal.App("datadash", image=img)
project_root = Path("/app")


@app.cls(allow_concurrent_inputs=20, secrets=[modal.Secret.from_name("openai-secret")])
class DataServer:
    @modal.build()
    def startup(self):
        os.system(f"cd /app/fw && git pull")

    @modal.enter()
    def on_warmup(self):
        os.chdir("/app/fw")

    @modal.asgi_app(label="datadash-api")
    def update(self):
        return fast_app

    @modal.web_server(label="datadash-ui", port=3000, startup_timeout=120)
    def server(self):
        commands = [
            # "echo 'Starting DataDash'",
            # "cd /app/fw",
            "echo 'Starting Preview Server'",
            "yarn preview",
            "echo 'DataDash Ready'",
        ]
        env = {"OBSERVABLE_TELEMETRY_DISABLE": "true"}
        subprocess.Popen(" && ".join(commands), shell=True, env=env)
