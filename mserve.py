import os
import subprocess

import modal
from fastapi import Request

"""
  "dependencies": {
    "@duckdb/duckdb-wasm": "^1.29.0",
    "@observablehq/framework": "^1.12.0",
    "d3-dsv": "^3.0.1",
    "d3-time-format": "^4.1.0"
  },
  "devDependencies": {
    "rimraf": "^5.0.5"
  },

"""


def mount_condition(path: str):
    ignore = ["node_modules/", "dist/"]
    return not any(p in path for p in ignore)


git_url = "https://github.com/kousun12/datadash.git"
git_sha = "878de15"


img = (
    modal.Image.from_registry("node:20-bookworm", add_python="3.12")
    .apt_install("git")
    .pip_install("fastapi[standard]", "httpx")
    .run_commands(f"git clone {git_url} /app", f"cd /app && git checkout {git_sha}")
)
app = modal.App("datadash", image=img)
# vol = modal.Volume.from_name("datadash_vol", create_if_missing=True)


@app.cls(
    allow_concurrent_inputs=20,
)
class DataServer:
    @modal.build()
    def startup(self):
        os.system("cd /app/fw && yarn install && yarn build")

    @modal.enter()
    def foo(self):
        ...

    @modal.web_endpoint(label="datadash-api", method="POST")
    def update(self, request: Request):
        return {"message": "Hello World"}

    @modal.web_server(label="datadash-ui", port=3000, startup_timeout=120)
    def server(self):
        commands = [
            "echo 'Starting DataDash'",
            "cd /app/fw",
            "echo 'Starting Preview Server'",
            "yarn preview",
            "echo 'DataDash Ready'",
        ]
        env = {"OBSERVABLE_TELEMETRY_DISABLE": "true"}
        subprocess.Popen(" && ".join(commands), shell=True, env=env)


# @app.function(
#     # volumes={"/data": vol},
#     allow_concurrent_inputs=20,
#     timeout=60 * 10,
# )
