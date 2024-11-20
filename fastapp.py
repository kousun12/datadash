from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from analyst.page_generator import ObservablePageGenerator
from constants import base_path

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


@fast_app.post("/")
async def root(request: Request):
    body_json = await request.json()
    print("body json", body_json)
    prompt = body_json["message"]
    slug = body_json.get("slug")
    table_name = body_json.get("tableName", "ag_data")
    at_dir = base_path / f"chart_defs/sessions/{table_name}/{slug}"
    db_path = db_paths[table_name]
    pg = ObservablePageGenerator(db_path=db_path)
    pg.modify_page(prompt, at_dir=at_dir)
    # touch the file: fw/src/d/[tableName]/[uuid].md.js to trigger observable to rebuild
    (base_path / f"fw/src/d/[tableName]/[uuid].md.js").touch()

    return {"you_sent": body_json}
