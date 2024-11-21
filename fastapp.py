from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from analyst.analyst_llm import LLMAnalyst
from analyst.chart_def import ChartDef
from constants import base_path, default_data_dir, sessions_dir, observable_source

project_root = Path(__file__).parent

fast_app = FastAPI()

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

loader_file = observable_source / "d/[uuid].md.js"


from fastapi.responses import StreamingResponse
import json


@fast_app.post("/")
async def root(request: Request):
    body_json = await request.json()
    prompt = body_json["message"]
    slug = body_json.get("slug")
    cd = ChartDef.load(slug)
    analyst = LLMAnalyst(chart_def=cd)

    async def event_generator():
        async def generate():
            for event in analyst.modify_chart(instructions=prompt):
                print("~~~~~~~~~~~~~~~~~~~~event~~~~~~~~~~~~~~~~~\n", event)
                if event.get("type") == "complete":
                    loader_file.touch()
                    # Send the complete event too, just don't include the full chart data
                    yield f"data: {json.dumps({'type': 'complete'})}\n\n"
                else:
                    yield f"data: {json.dumps(event)}\n\n"
                await request.send_push_promise('/')

        async for chunk in generate():
            yield chunk.encode('utf-8')

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Transfer-Encoding": "chunked"
        }
    )


@fast_app.post("/update")
async def update(request: Request):
    body_json = await request.json()
    print("body json", body_json)
    plot = body_json.get("new_plot")
    slug = body_json.get("slug")
    cd = ChartDef.load(slug)
    if plot:
        with open(sessions_dir / slug / "plot.js", "w") as f:
            f.write(plot)
    cd = cd.reload()
    cd.render_main_artifact()
    loader_file.touch()

    return {"you_sent": body_json}
