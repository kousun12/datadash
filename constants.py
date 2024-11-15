import os
from pathlib import Path

default_model = "claude-3-5-sonnet-20240620"
base_path = Path(os.getenv("PROJECT_PATH_ABS", "/Users/robcheung/code/fred"))
default_data_dir = Path("/tmp/analyst")
observable_pages_dir = base_path / "fw/src/p"
