from pathlib import Path
import shutil
import re
from unidecode import unidecode

from analyst.llm import LLMAnalyst
from constants import observable_pages_dir, default_data_dir, base_path


class ObservablePageGenerator:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.analyst = LLMAnalyst(db_path=db_path)

    def write_page(self, chart_def, out_path, slug_override=None):
        slug = slug_override or slugify(chart_def.title)
        copy_pth = observable_pages_dir / f"{slug}{out_path.suffix}"
        shutil.copy2(out_path, copy_pth)
        print(f"Generated {copy_pth}")

    def generate_pages(self, slug_override=None):
        for table in self.analyst.get_tables():
            chart_def = self.analyst.create_chart(table)
            out_path = chart_def.save(in_dir=default_data_dir)
            self.write_page(chart_def, out_path, slug_override)

    def modify_page(self, instructions: str, at_dir: Path, slug_override=None):
        new_chart = self.analyst.modify_chart(instructions, at_dir)
        out_path = new_chart.save(in_dir=default_data_dir)
        self.write_page(new_chart, out_path, slug_override=slug_override)


def slugify(title):
    slug = re.sub(r"[^\w\s-]", "", unidecode(title).lower())
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug.strip("-")


if __name__ == "__main__":
    sha = "eac2414a-e382-43b4-befc-d8efe18813fc"
    gen = ObservablePageGenerator(db_path=base_path / "fw/src/data/us_ag.db")
    slug_override = "us-agriculture"
    # gen.generate_pages(slug_override=slug_override)
    instruct = "for some reason the tooltip is showing on the wrong y value"
    at_dir = base_path / f"chart_defs/sessions/ag_data/{sha}"
    gen.modify_page(instruct, at_dir, slug_override=slug_override)
