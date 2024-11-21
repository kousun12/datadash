from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from analyst.analyst_llm import LLMAnalyst
from analyst.chart_def import ChartDef
from constants import base_path, default_data_dir

project_root = Path(__file__).parent

fast_app = FastAPI()

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_paths = {
    "ag_data": base_path / "fw/src/data/us_ag.db",
    "yellow_trips": base_path / "fw/src/data/yellow_trips.db",
}

loader_file = base_path / f"fw/src/d/[uuid].md.js"


@fast_app.post("/")
async def root(request: Request):
    body_json = await request.json()
    print("body json", body_json)
    prompt = body_json["message"]
    slug = body_json.get("slug")
    cd = ChartDef.load(slug)
    analyst = LLMAnalyst(chart_def=cd)
    new_chart = analyst.modify_chart(instructions=prompt)
    new_chart.save()
    loader_file.touch()

    return {"you_sent": body_json}


@fast_app.post("/update")
async def update(request: Request):
    body_json = await request.json()
    print("body json", body_json)
    plot = body_json.get("new_plot")
    slug = body_json.get("slug")
    cd = ChartDef.load(slug)
    if plot:
        with open(default_data_dir / slug / "plot.js", "w") as f:
            f.write(plot)
    cd = cd.reload()
    cd.render_main_artifact()
    loader_file.touch()

    return {"you_sent": body_json}
