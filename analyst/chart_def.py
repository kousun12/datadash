import uuid
from typing import Dict, Any, Optional

import pydantic
from pathlib import Path
import sqlparse
from sqlparse.sql import Identifier

from constants import base_path

observable_template_file = base_path / "templates/plot.j2"


class ChartDef(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)
    title: str
    description: str
    concept: str
    sql: str
    vega_lite: Optional[Dict[str, Any]] = None
    plot_js: Optional[str] = None
    dataframe: Any = None
    table_name: Optional[str] = None

    def render_vega_lite(self):
        import altair as alt
        import pandas as pd

        if self.dataframe is not None and isinstance(self.dataframe, pd.DataFrame):
            data = alt.Data(values=self.dataframe.to_dict("records"))
        else:
            data = alt.Data(values=[])

        chart = alt.Chart.from_dict(self.vega_lite)
        if "data" not in chart.to_dict():
            chart = chart.properties(data=data)

        return chart.to_html()

    def plot_observable(self, db_path) -> str:
        from jinja2 import Template

        with open(observable_template_file) as f:
            template = Template(f.read())

        context = {
            "title": self.title,
            "db_path": f"/{db_path}",
            "sql_block": qualify_table_refs(self.sql, "ds", self.table_name),
            "plot_code": self.plot_js,
            "description": self.description,
        }
        return template.render(context)

    def render(self, directory, db_path: Optional[str] = None) -> Path:
        if self.vega_lite:
            html = self.render_vega_lite()
            out = Path(directory) / "chart.html"
            with open(out, "w") as f:
                f.write(html)
            return out
        elif self.plot_js:
            md = self.plot_observable(db_path=db_path)
            out = Path(directory) / "plot.md"
            with open(out, "w") as f:
                f.write(md)
            return out
        else:
            raise ValueError("No plot data available")


def qualify_table_refs(sql, schema, table_name) -> str:
    """
    Quirk of observable is that you have to bind the tables to a schema.
    """
    parsed = sqlparse.parse(sql)[0]

    def traverse(token):
        if (
            isinstance(token, Identifier)
            and token.get_real_name().lower() == table_name.lower()
        ):
            token.tokens = [
                sqlparse.sql.Token(sqlparse.tokens.Name, f"{schema}.{table_name}")
            ]
        elif hasattr(token, "tokens"):
            for sub_token in token.tokens:
                traverse(sub_token)

    traverse(parsed)
    return str(parsed)
