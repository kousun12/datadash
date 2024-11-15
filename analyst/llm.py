import uuid
from typing import Dict, Any, Optional

from aider.models import Model
import textwrap
from io import StringIO
import duckdb
import json
import pydantic
from pathlib import Path
import re
from unidecode import unidecode
import sqlparse
from sqlparse.sql import Identifier
import shutil

base_path = Path("/Users/robcheung/code/fred")
guide_path = base_path / "plot_guide.md"
default_data_dir = Path("/tmp/analyst")
cache_filename = "analyst_cache.json"
observable_plot_version = "0.6.0"
observable_template_file = base_path / "templates/plot.j2"


def qualify_table_refs(sql, schema, table_name):
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


class ChartIdea(pydantic.BaseModel):
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


class LLMAnalyst:
    def __init__(
        self,
        model_name="claude-3-5-sonnet-20240620",
        db_path=None,
        data_dir=default_data_dir,
    ):
        self.model_name = model_name
        self.db_path = db_path
        self.db = None
        self._cache = {}
        data_dir.mkdir(parents=True, exist_ok=True)
        self._cache_file = Path(data_dir) / cache_filename
        self._load_cache()

    def _load_cache(self):
        if self._cache_file.exists():
            with open(self._cache_file) as f:
                cache = json.load(f)
                self._cache = cache.get(str(self.db_path) or "", {})

    def _save_cache(self):
        cache = {str(self.db_path): self._cache}
        with open(self._cache_file, "w") as f:
            json.dump(cache, f, indent=2)

    def connect(self):
        if self.db_path and not self.db:
            self.db = duckdb.connect(self.db_path)

    def close(self):
        if self.db:
            self.db.close()
            self.db = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def get_coder(self, **kwargs):
        from aider.coders import Coder
        from aider.io import InputOutput

        io = InputOutput()
        io.yes = False
        auto_commits = kwargs.pop("auto_commits", False)
        temp = kwargs.pop("temperature", 0.8)
        coder: Coder = Coder.create(
            main_model=Model(self.model_name),
            io=io,
            cache_prompts=True,
            stream=False,
            auto_commits=auto_commits,
            **kwargs,
        )
        # coder.repo.aider_ignore_file = self.adhoc_ignore
        coder.temperature = temp
        return coder

    def get_ask_coder(self, fnames=None, **kwargs):
        if kwargs is None:
            kwargs = {}
        if fnames is None:
            fnames = []
        read_only_fnames = [guide_path]

        return self.get_coder(
            edit_format="ask",
            fnames=fnames,
            read_only_fnames=read_only_fnames,
            **kwargs,
        )

    def get_modify_coder(self, fnames=None):
        if fnames is None:
            fnames = []
        read_only_fnames = [guide_path]
        return self.get_coder(
            fnames=fnames, read_only_fnames=read_only_fnames, auto_commits=False
        )

    def get_tables(self) -> list[str]:
        self.connect()
        tables = self.db.execute("SHOW TABLES").fetchall()
        return [table[0] for table in tables]

    def table_summary_stats(
        self, table_name, sample_rows=3, max_str_length=44, frequency_threshold=0.1
    ):
        self.connect()
        output = StringIO()
        columns = self.db.execute(f"DESCRIBE {table_name}").fetchall()

        # Get row count
        row_count = self.db.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

        output.write(f"Table: {table_name}\n")
        output.write(f"Total rows: {row_count}\n\n")
        output.write("Columns:\n")

        for col in columns:
            col_name, col_type = col[0], col[1]
            output.write(f"  {col_name}: {col_type}\n")

            escaped_col_name = f'"{col_name}"'
            # Get frequency distribution for this column
            freq_query = f"SELECT {escaped_col_name}, COUNT(*) as count FROM {table_name} GROUP BY {escaped_col_name} ORDER BY count DESC LIMIT 5"
            freq_data = self.db.execute(freq_query).fetchall()

            # Check if there are high-frequency values
            high_freq_values = [
                value
                for value, count in freq_data
                if count / row_count >= frequency_threshold
            ]

            if high_freq_values:
                formatted_values = [
                    f'"{value}" ({count / row_count:.1%})'
                    for value, count in freq_data[:3]  # Limit to top 3 for brevity
                    if count / row_count >= frequency_threshold
                ]
                formatted_values = [
                    textwrap.shorten(v, width=max_str_length, placeholder="...")
                    for v in formatted_values
                ]
                output.write(
                    f"    Sample Distributions: {', '.join(formatted_values)}\n"
                )

        # Get sample data
        sample_data = self.db.execute(
            f"SELECT * FROM {table_name} LIMIT {sample_rows}"
        ).fetchall()

        output.write("\nSample data:\n")
        for row in sample_data:
            formatted_row = []
            for value in row:
                if isinstance(value, str):
                    value = textwrap.shorten(
                        value, width=max_str_length, placeholder="..."
                    )
                formatted_row.append(str(value))
            output.write("  " + " | ".join(formatted_row) + "\n")

        return output.getvalue()

    def _get_from_cache(self, cache_type: str, key: str):
        if cache_type not in self._cache:
            self._cache[cache_type] = {}
        return self._cache[cache_type].get(key, None)

    def _set_cache(self, cache_type: str, key: str, value: str):
        if cache_type not in self._cache:
            self._cache[cache_type] = {}
        self._cache[cache_type][key] = value
        self._save_cache()

    def table_human_summary(self, table_name: str) -> str:
        cached = self._get_from_cache("human_summary", table_name)
        if cached:
            return cached

        stats = self.table_summary_stats(table_name)
        ac = self.get_ask_coder()
        res = ac.run(
            f"""Give a detailed summary of this table, "{table_name}". What is it for, and what what kinds of information does it include? answer in only a sentence or two. Reply with just the summary, nothing else. {stats}"""
        )
        self._set_cache("human_summary", table_name, res)

        return res

    def execute_sql(self, sql: str, as_df=True):
        self.connect()
        if as_df:
            return self.db.execute(sql).fetchdf()
        return self.db.execute(sql).fetchall()

    def get_chart_idea(self, table_name: str):
        id = uuid.uuid4()

        idea_dir = default_data_dir / f"ideas/{table_name}/{id}"
        idea_dir.mkdir(parents=True, exist_ok=True)

        stats = self.table_summary_stats(table_name)
        overview = self.table_human_summary(table_name)
        ac = self.get_ask_coder()
        concept = ac.run(
            f"How would you visually present this table? In considering this, think about the types of data in the table and what presentation would be most useful for a reader. Come up with just one idea and describe how it works.\n\n{overview}\n{stats}"
        )
        implementation = ac.run(
            """Respond with both the SQL and Observable Plot code required to implement this visualization. 
Respond only with a single sql code fence and a javascript code fence, nothing else. 
The javascript code fence should ONLY include a single function `plotChart` that returns a valid Observable Framework Plot. No other code or imports should be included.
For example your response should be in this form:

```sql
<Your SQL code here>
```

```javascript
function plotChart(data, {width} = {}) {
  // NB data is an Apache Arrow table
  return Plot.plot({
    width,
    ...
  });
}
```
"""
        )
        max_tries = 3

        df = None
        parsed_sql = None
        parsed_ob_plot = None
        for i in range(max_tries):
            parsed_sql = implementation.split("```sql")[1].split("```")[0].strip()
            parsed_ob_plot = (
                implementation.split("```javascript")[1].split("```")[0].strip()
            )
            try:
                df = self.execute_sql(parsed_sql)
                if df is not None:
                    break
            except Exception as e:
                message = f"Error executing SQL: {e}"
                print(message, parsed_sql)
                implementation = ac.run(
                    f"Executing that SQL produced an error: {message}. Respond with a new SQL and Plot code. Again, only respond with the new code blocks, nothing else."
                )

        if df is None or not parsed_sql or not parsed_ob_plot:
            raise ValueError("Failed to get valid SQL and Plot code")
        # save files:
        with open(idea_dir / "concept.md", "w") as f:
            f.write(concept)

        with open(idea_dir / "sql.sql", "w") as f:
            f.write(parsed_sql)

        with open(idea_dir / "plot.js", "w") as f:
            f.write(parsed_ob_plot)

        title_desc = ac.run(
            f"Give a title and description for this chart. Respond with the title on one line and the description on the next line. Do not include anything else in your response."
        )
        title, desc = [i for i in title_desc.split("\n") if i]

        with open(idea_dir / "metadata.json", "w") as f:
            json.dump({"title": title, "description": desc}, f)

        with open(idea_dir / "data.csv", "w") as f:
            df.to_csv(f, index=False)

        idea = ChartIdea(
            id=id,
            title=title,
            description=desc,
            concept=concept,
            sql=parsed_sql,
            vega_lite=None,
            plot_js=parsed_ob_plot,
            dataframe=df,
            table_name=table_name,
        )
        out_path = idea.render(
            idea_dir, db_path=self.db_path.relative_to(base_path / "fw/src").as_posix()
        )

        slug = slugify(title)
        copy_pth = base_path / f"fw/src/p/{slug}{out_path.suffix}"
        shutil.copy2(out_path, copy_pth)

        return idea


def slugify(title):
    slug = re.sub(r"[^\w\s-]", "", unidecode(title).lower())
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug.strip("-")


if __name__ == "__main__":
    # path = "/Users/robcheung/code/fred/summarize_table.py"
    # res = analyst.get_ask_coder(fnames=[path]).run("what does this file do")
    analyst = LLMAnalyst(db_path=base_path / "fw/src/data/us_ag.db")
    for table in analyst.get_tables():
        print(analyst.get_chart_idea(table))

"""
sample data
```sql
WITH ranked_commodities AS (
  SELECT Commodity, 
         SUM(CASE WHEN Attribute = 'Production' THEN "Value text" ELSE 0 END) as total_production,
         ROW_NUMBER() OVER (ORDER BY SUM(CASE WHEN Attribute = 'Production' THEN "Value text" ELSE 0 END) DESC) as rank
  FROM ag_data
  WHERE Attribute = 'Production' AND "Marketing/calendar year" >= '2010/11'
  GROUP BY Commodity
),
top_commodities AS (
  SELECT Commodity
  FROM ranked_commodities
  WHERE rank <= 5
),
filtered_data AS (
  SELECT a."Marketing/calendar year" as year, 
         a.Commodity, 
         a.Attribute, 
         a."Value text" as value
  FROM ag_data a
  JOIN top_commodities t ON a.Commodity = t.Commodity
  WHERE a.Attribute IN ('Production', 'Domestic use', 'Exports')
    AND a."Marketing/calendar year" >= '2010/11'
)
SELECT *
FROM filtered_data
ORDER BY year, Commodity, Attribute
```

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"name": "filtered_data"},
  "vconcat": [
    {
      "width": 600,
      "height": 300,
      "mark": "line",
      "encoding": {
        "x": {"field": "year", "type": "ordinal", "title": "Marketing/Calendar Year"},
        "y": {"field": "value", "type": "quantitative", "title": "Value"},
        "color": {"field": "Commodity", "type": "nominal"},
        "strokeDash": {"field": "Attribute", "type": "nominal"}
      },
      "transform": [
        {"filter": {"field": "Attribute", "equal": "Production"}}
      ]
    },
    {
      "width": 600,
      "height": 300,
      "mark": "bar",
      "encoding": {
        "x": {"field": "year", "type": "ordinal", "title": "Marketing/Calendar Year"},
        "y": {"field": "value", "type": "quantitative", "stack": "normalize", "title": "Percentage"},
        "color": {"field": "Attribute", "type": "nominal"},
        "tooltip": [
          {"field": "year", "type": "ordinal", "title": "Year"},
          {"field": "Commodity", "type": "nominal"},
          {"field": "Attribute", "type": "nominal"},
          {"field": "value", "type": "quantitative", "format": ".2f"}
        ]
      },
      "transform": [
        {"filter": {"field": "Attribute", "oneOf": ["Production", "Domestic use", "Exports"]}}
      ]
    }
  ],
  "resolve": {"scale": {"color": "independent"}},
  "config": {
    "axis": {"labelAngle": -45}
  }
}
```

"""
