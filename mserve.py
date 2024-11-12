import modal

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

img = (
    modal.Image.from_registry("node:jod-bookworm", add_python="3.12")
    .apt_install("git")
    .pip_install("fastapi[standard]")
    .run_commands(
        f"yarn add --dev rimraf@^5.0.5",
        f"yarn add @duckdb/duckdb-wasm@^1.29.0 @observablehq/framework@^1.12.0 d3-dsv@^3.0.1 d3-time-format@^4.1.0",
    )
)
app = modal.App("datadash", image=img)
vol = modal.Volume.from_name("datadash_vol", create_if_missing=True)


@app.function(
    volumes={"/data": vol},
    allow_concurrent_inputs=20,
    timeout=60 * 10,
)
@modal.asgi_app(label="datadash-serve")
def server():
    import fastapi.staticfiles
    from fastapi.responses import StreamingResponse

    web_app = fastapi.FastAPI()

    @web_app.get("/stats")
    async def stats():
        ...

    @web_app.post("/step")
    async def step(prompt: str):
        ...

    # web_app.mount("/", fastapi.staticfiles.StaticFiles(directory="/assets", html=True))
    return web_app
