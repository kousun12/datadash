from pathlib import Path
import shutil
import re
from unidecode import unidecode

from analyst.analyst_llm import LLMAnalyst
from analyst.chart_def import ChartDef
from constants import observable_pages_dir, default_data_dir, base_path


class ObservablePageGenerator:
    ...


def slugify(title):
    slug = re.sub(r"[^\w\s-]", "", unidecode(title).lower())
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug.strip("-")


if __name__ == "__main__":
    cd = ChartDef.load("f5d2eede-f6c3-4097-8d8e-9fe1bebe9067")
    print(cd.table_names)
    analyst = LLMAnalyst(chart_def=cd)
    print(analyst)
    analyst.modify_chart(instructions="remove the legend")
