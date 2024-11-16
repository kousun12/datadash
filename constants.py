import os
from pathlib import Path

project_root = Path(__file__).parent
default_model = "claude-3-5-sonnet-20240620"
base_path = Path(os.getenv("PROJECT_PATH", project_root))
default_data_dir = base_path / "chart_defs"
observable_pages_dir = base_path / "fw/src/p"
observable_template_file = base_path / "templates/plot.j2"
