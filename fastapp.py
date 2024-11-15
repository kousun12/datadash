from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

project_root = Path(__file__).parent

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
    todo = body_json["prompt"]

    return {"body": body_json, "todo": todo}
