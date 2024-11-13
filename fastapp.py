from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# project_root = Path("/app")
project_root = Path(__file__).parent


def get_coder(**kwargs):
    from aider.coders import Coder
    from aider.io import InputOutput
    from aider.models import Model

    ef_suffix = ""
    if "edit_format" in kwargs:
        ef_suffix = "-" + kwargs["edit_format"]

    io = InputOutput()
    io.yes = False
    auto_commits = kwargs.pop("auto_commits", False)
    temp = kwargs.pop("temperature", 0.8)
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


def get_ask_coder(fnames=None, **kwargs):
    if kwargs is None:
        kwargs = {}
    if fnames is None:
        fnames = [project_root / "fw/src/index.md"]
    read_only_fnames = []
    for example in examples:
        read_only_fnames.append(project_root / f"fw/src/examples/{example}.md")

    return get_coder(
        edit_format="ask", fnames=fnames, read_only_fnames=read_only_fnames, **kwargs
    )


examples = [
    "cpi",
    "dams",
    "electricity",
    "hotels",
    "mortgages",
    "package_dl",
    "polling",
    "taxis",
]


def get_modify_coder(fnames=None):
    if fnames is None:
        fnames = [project_root / "fw/src/index.md"]

    read_only_fnames = []
    for example in examples:
        read_only_fnames.append(project_root / f"fw/src/examples/{example}.md")
    return get_coder(
        fnames=fnames, read_only_fnames=read_only_fnames, auto_commits=False
    )


fast_app = FastAPI()

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@fast_app.post("/")
async def root(request: Request):
    body_json = await request.json()
    ac = get_ask_coder()
    print(ac)
    todo = ac.run(
        "what is one idea for digging into this data more deeply? It can be an idea to improve a chart, add a new chart, a new metric, a new filter, or a new way to visualize the data. reply with just a short description of the idea and nothing else."
    )
    print("todo", todo)
    mc = get_modify_coder()
    print(mc)
    modify = mc.run(
        f"Implement following idea.\nOnly modify things in the second card element where the chart(s) are. Do not modify the first card where there is a text input. Follow the patterns set by the examples and NOT what you know about Observable Notebook, this is Observable Framework:\n\n{todo}"
    )
    print(f"\n~~~~~~~~~CODE_EDIT~~~~~~~~~~~\n{mc.aider_edited_files}")

    return {"body": body_json, "modify": modify, "todo": todo}
