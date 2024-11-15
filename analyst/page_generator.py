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

    def generate_pages(self):
        for table in self.analyst.get_tables():
            chart_def = self.analyst.create_chart(table)
            print(chart_def)
            out_path = chart_def.save(in_dir=default_data_dir)
            slug = slugify(chart_def.title)
            copy_pth = observable_pages_dir / f"{slug}{out_path.suffix}"
            shutil.copy2(out_path, copy_pth)
            print(f"Generated {copy_pth}")


def slugify(title):
    slug = re.sub(r"[^\w\s-]", "", unidecode(title).lower())
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug.strip("-")


if __name__ == "__main__":
    gen = ObservablePageGenerator(db_path=base_path / "fw/src/data/us_ag.db")
    gen.generate_pages()
