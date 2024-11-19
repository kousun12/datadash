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
    # gen = ObservablePageGenerator(db_path=base_path / "fw/src/data/us_ag.db")
    gen = ObservablePageGenerator(db_path=base_path / "fw/src/data/yellow_trips.db")

    def new_chart(override=None):
        gen.generate_pages(slug_override=override)

    def update_chart(sha, instruct, override=None):
        at_dir = base_path / f"chart_defs/sessions/yellow_trips/{sha}"
        gen.modify_page(instruct, at_dir, slug_override=override)

    # at_dir = default_data_dir / "sessions/ag_data/4beb2033-a621-469d-822d-f53c17d5f4fe"
    # cd = ChartDef.from_path(at_dir)
    # print(gen.analyst)
    # cd_after = cd.save(in_dir=default_data_dir)
    # print(cd_after)
    # update_chart(
    #     sha="4beb2033-a621-469d-822d-f53c17d5f4fe",
    #     instruct="i don't see anything other than a few colors in the top right for the legend and a whole bunch of overlapping text in the top right. chart area is blank",
    #     override="us-agriculture",
    # )

    new_chart(override="nyc-trips")
    update_chart(
        sha="36ac5569-935b-43fe-810c-1f97baefb380",
        instruct="Error: d.getHours is not a function",
        override="nyc-trips",
    )
