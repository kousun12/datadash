from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from analyst.analyst_llm import LLMAnalyst
from analyst.chart_def import ChartDef
from constants import sessions_dir, observable_source
import llm

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


async def judge(instruction: str):
    model = llm.get_async_model("claude-3-5-sonnet-latest")
    llm_prompt = f"user_message: {instruction}"
    response = await model.prompt(
        llm_prompt,
        system="This is Very Important. Do not respond with anything other than the word 'question' or 'command'. Your response should judge whether a user's message is a question or a command.",
    )
    return await response.text()


@fast_app.post("/")
async def root(request: Request):
    body_json = await request.json()
    prompt = body_json["message"]
    slug = body_json.get("slug")
    cd = ChartDef.load(slug)
    analyst = LLMAnalyst(chart_def=cd)

    async def message_generator():
        async def generate():
            message_type = await judge(prompt)
            print("message type", message_type)
            if message_type == "question":
                fnames_contents = ""
                fnames = [sessions_dir / slug / "plot.md"]
                for fname in fnames:
                    with open(fname) as f:
                        fnames_contents += f.read()
                model = llm.get_async_model("claude-3-5-sonnet-latest")
                response = await model.prompt(
                    f"Given the following context, answer the user query:\n\n<context>\n{fnames_contents}\n</context>\n\n<query>\n{prompt}\n</query>",
                    system="Be concise in your response, avoid going into too much detail with code.",
                )
                event = {"type": "summary", "message": await response.text()}
                yield f"data: {json.dumps(event)}\n\n"
                await request.send_push_promise("/")
            else:
                for event in analyst.modify_chart(instructions=prompt):
                    print("~~~~~~~~~~~~~~~~~~~~event~~~~~~~~~~~~~~~~~\n", event)
                    if event.get("type") == "complete":
                        loader_file.touch()
                        # Send the complete event too, just don't include the full chart data
                        yield f"data: {json.dumps({'type': 'complete'})}\n\n"
                    else:
                        yield f"data: {json.dumps(event)}\n\n"
                    await request.send_push_promise("/")

        async for chunk in generate():
            yield chunk.encode("utf-8")

    return StreamingResponse(
        message_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Transfer-Encoding": "chunked",
        },
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
