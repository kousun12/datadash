import json

import yaml
import uuid
import pandas as pd
from typing import Dict, Any, Optional

import pydantic
from pathlib import Path
import sqlparse
from sqlparse.sql import Identifier

from constants import (
    base_path,
    observable_template_file,
    sessions_dir,
    observable_source,
)


class ChartDef(pydantic.BaseModel):
    class FileTypes:
        METADATA = "metadata.yaml"
        CONCEPT = "concept.md"
        SQL = "query.sql"
        PLOT_JS = "plot.js"
        DATA = "data.csv"
        VEGA_CHART = "chart.html"
        OBSERVABLE_PLOT = "plot.md"

    id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    concept: str
    sql: str
    db_path: Path
    table_names: list[str]
    plot_js: Optional[str] = None
    dataframe: Any = None
    vega_lite: Optional[Dict[str, Any]] = None

    @classmethod
    def load(cls, id):
        return cls.from_path(sessions_dir / id)

    @classmethod
    def from_path(cls, path: Path) -> "ChartDef":
        path = Path(path)
        with open(path / cls.FileTypes.METADATA) as f:
            metadata = yaml.safe_load(f)
        with open(path / cls.FileTypes.CONCEPT) as f:
            concept = f.read()
        with open(path / cls.FileTypes.SQL) as f:
            sql = f.read()
        plot_js = None
        if (path / cls.FileTypes.PLOT_JS).exists():
            with open(path / cls.FileTypes.PLOT_JS) as f:
                plot_js = f.read()
        dataframe = None
        if (path / cls.FileTypes.DATA).exists():
            dataframe = pd.read_csv(path / cls.FileTypes.DATA)
        id = metadata.get("id") if metadata.get("id") else str(uuid.uuid4())

        db_path = base_path / Path(metadata["db_path"])

        return cls(
            id=id,
            title=metadata["title"],
            description=metadata["description"],
            concept=concept,
            sql=sql,
            db_path=db_path,
            table_names=metadata.get("table_names", [metadata.get("table_name")]),
            plot_js=plot_js,
            dataframe=dataframe,
        )

    @classmethod
    def mutable_file_names(cls):
        return [
            cls.FileTypes.METADATA,
            cls.FileTypes.CONCEPT,
            cls.FileTypes.SQL,
            cls.FileTypes.PLOT_JS,
        ]

    @classmethod
    def readonly_file_names(cls):
        return []

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

    def plot_observable(self) -> str:
        from jinja2 import Template

        with open(observable_template_file) as f:
            template = Template(f.read())

        relative_path = self.db_path.relative_to(observable_source).as_posix()
        context = {
            "title": self.title,
            "db_path": f"/{relative_path}",
            "sql_block": qualify_table_refs(self.sql, "ds", self.table_names),
            "plot_code": self.plot_js,
            "plot_code_str": json.dumps(self.plot_js),
            "description": self.description,
        }
        return template.render(context)

    def render_main_artifact(self) -> Path:
        dest_dir = sessions_dir / self.id
        if self.vega_lite:
            html = self.render_vega_lite()
            out = Path(dest_dir) / self.FileTypes.VEGA_CHART
            with open(out, "w") as f:
                f.write(html)
            return out
        elif self.plot_js:
            md = self.plot_observable()
            out = Path(dest_dir) / self.FileTypes.OBSERVABLE_PLOT
            with open(out, "w") as f:
                f.write(md)
            return out
        else:
            print("No plot to render")

    def save(self, skip_df=True) -> Path:
        dest_dir = sessions_dir / self.id
        dest_dir.mkdir(parents=True, exist_ok=True)
        with open(dest_dir / self.FileTypes.CONCEPT, "w") as f:
            f.write(self.concept)
        with open(dest_dir / self.FileTypes.SQL, "w") as f:
            f.write(self.sql)
        if self.plot_js:
            with open(dest_dir / self.FileTypes.PLOT_JS, "w") as f:
                f.write(self.plot_js)
        with open(dest_dir / self.FileTypes.METADATA, "w") as f:
            relative_db_path = self.db_path.relative_to(base_path).as_posix()
            yaml.dump(
                {
                    "title": self.title,
                    "description": self.description,
                    "db_path": relative_db_path,
                    "table_names": self.table_names,
                    "id": str(self.id),
                },
                f,
                sort_keys=False,
            )
        if self.dataframe is not None and not skip_df:
            with open(dest_dir / self.FileTypes.DATA, "w") as f:
                self.dataframe.to_csv(f, index=False)

        artifact_path = self.render_main_artifact()
        self.add_to_git()

        return artifact_path

    def reload(self):
        return ChartDef.from_path(sessions_dir / self.id)

    def add_to_git(self):
        import subprocess
        import os

        dest_dir = sessions_dir / self.id
        dest_posix = dest_dir.relative_to(base_path).as_posix()

        if not os.path.exists(dest_dir):
            return  # File doesn't exist, so we can't add it

        try:
            subprocess.run(
                ["git", "ls-files", "--error-unmatch", dest_posix],
                check=True,
                cwd=base_path,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return
        except subprocess.CalledProcessError:
            pass

        try:
            subprocess.run(["git", "add", dest_posix], check=True, cwd=base_path)
        except subprocess.CalledProcessError as e:
            print(f"Failed to add file to Git: {e}")


def _qualify_ref_for_table(sql, schema, table_name) -> str:
    """
    Quirk of observable is that you have to bind the tables to a schema.
    """
    parsed = sqlparse.parse(sql)[0]

    def traverse(token):
        if isinstance(token, Identifier):
            # Check if this identifier is our target table
            if token.get_real_name().lower() == table_name.lower():
                # Get the original tokens to preserve any alias
                original_tokens = token.tokens
                # Find and modify just the table name part
                for i, t in enumerate(original_tokens):
                    if t.value.lower() == table_name.lower():
                        original_tokens[i] = sqlparse.sql.Token(
                            sqlparse.tokens.Name, f"{schema}.{table_name}"
                        )
                        break
                token.tokens = original_tokens
        # Handle raw tokens that might be table references
        elif (
            token.ttype == sqlparse.tokens.Name
            and token.value.lower() == table_name.lower()
        ):
            token.value = f"{schema}.{table_name}"

        # Recursively process child tokens
        if hasattr(token, "tokens"):
            for sub_token in token.tokens:
                traverse(sub_token)

    traverse(parsed)
    return str(parsed)


def qualify_table_refs(sql, schema, table_names) -> str:
    for table_name in table_names:
        sql = _qualify_ref_for_table(sql, schema, table_name)
    return sql
