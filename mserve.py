import os
import subprocess
from pathlib import Path

import modal
from fastapi import Request

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

    @modal.web_endpoint(label="datadash-api", method="POST")
    async def update(self, request: Request):
        body_json = await request.json()
        ac = self.get_ask_coder()
        print(ac)
        todo = ac.run(
            "what is one way i can improve this data visualization for cpi data. reply with just a short description of an incremental idea and nothing else"
        )
        print("todo", todo)
        mc = self.get_modify_coder()
        print(mc)
        modify = mc.run(
            f"Implement following idea. Only modify things in the second card element where the chart(s) are. Do not modify the first card where there is a text input:\n\n{todo}"
        )
        print(f"\n~~~~~~~~~CODE_EDIT~~~~~~~~~~~\n{mc.aider_edited_files}")

        return {"message": "Hello World", "body": body_json}

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

    def get_coder(self, **kwargs):
        from aider.coders import Coder
        from aider.io import InputOutput
        from aider.models import Model

        ef_suffix = ""
        if "edit_format" in kwargs:
            ef_suffix = "-" + kwargs["edit_format"]

        io = InputOutput(
            # chat_history_file=self.challenge_root
            # / f".aider.chat.history{ef_suffix}.md",
            # llm_history_file=self.challenge_root / f".aider.llm.history{ef_suffix}.md",
        )
        io.yes = False
        auto_commits = kwargs.pop("auto_commits", False)
        temp = kwargs.pop("temperature", 0.3)
        coder: Coder = Coder.create(
            # main_model=Model("claude-3-5-sonnet-20240620"),
            io=io,
            cache_prompts=True,
            stream=False,
            auto_commits=auto_commits,
            **kwargs,
        )
        # coder.repo.aider_ignore_file = self.adhoc_ignore
        coder.temperature = temp
        return coder

    def get_ask_coder(self, fnames=None, **kwargs):
        if kwargs is None:
            kwargs = {}
        if fnames is None:
            fnames = [project_root / "fw/src/index.md"]
        return self.get_coder(edit_format="ask", fnames=fnames, **kwargs)

    def get_modify_coder(self, fnames=None):
        if fnames is None:
            fnames = [project_root / "fw/src/index.md"]
        read_only_fnames = [
            # self.file_paths["notebook"],
        ]
        return self.get_coder(
            fnames=fnames, read_only_fnames=read_only_fnames, auto_commits=False
        )
