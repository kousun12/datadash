import tempfile

import llm
from aider.models import Model
import textwrap
from io import StringIO
import duckdb
import json
from pathlib import Path

from analyst import prompts
from analyst.chart_def import ChartDef
from constants import (
    base_path,
    default_data_dir,
    default_model,
    observable_template_file,
    sessions_dir,
)

guide_path = base_path / "plot_guide.md"
cache_filename = "analyst_cache.json"
observable_plot_version = "0.6.0"


def ask(prompt: str, system=None):
    model = llm.get_model("claude-3-5-sonnet-latest")
    response = model.prompt(prompt, system=system)
    return response.text()


class LLMAnalyst:
    @classmethod
    def create(cls, db_path, model_name=default_model):
        db_path = Path(db_path)
        cd = ChartDef(
            title="",
            description="",
            concept="",
            sql="",
            db_path=Path(db_path),
            table_names=[],
        )
        cd.save()
        return cls(chart_def=cd, model_name=model_name)

    def __init__(
        self,
        chart_def,
        model_name=default_model,
    ):
        self.chart_def: ChartDef = chart_def
        self.model_name = model_name
        self.db = None
        self._cache = {}
        default_data_dir.mkdir(parents=True, exist_ok=True)
        self._cache_file = Path(default_data_dir) / cache_filename
        self._load_cache()
        self.tmp_ignore_path = None

    def _load_cache(self):
        if self._cache_file.exists():
            with open(self._cache_file) as f:
                self._cache = json.load(f)

    def _save_cache(self):
        with open(self._cache_file, "w") as f:
            json.dump(self._cache, f, indent=2)

    def connect(self):
        if self.chart_def.db_path and not self.db:
            self.db = duckdb.connect(self.chart_def.db_path)

    def close(self):
        if self.db:
            self.db.close()
            self.db = None
        if self.tmp_ignore_path:
            Path(self.tmp_ignore_path).unlink()

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
        temp = kwargs.pop("temperature", 0.6)
        coder: Coder = Coder.create(
            main_model=Model(self.model_name),
            io=io,
            cache_prompts=True,
            stream=False,
            auto_commits=auto_commits,
            verbose=True,
            suggest_shell_commands=False,
            **kwargs,
        )

        # coder.repo.aider_ignore_file = base_path / ".aiderignore-template"
        coder.repo.aider_ignore_file = Path(
            self._make_tmp_aiderignore(self.chart_def.id)
        )
        print(coder.get_all_relative_files())
        print(coder.get_repo_map())

        coder.temperature = temp
        return coder

    def _make_tmp_aiderignore(self, session_id: str):
        ignore_template = base_path / ".aiderignore-modify"
        with open(ignore_template, "r") as tf:
            template_content = tf.read()

        with tempfile.NamedTemporaryFile(
            mode="w+", delete=False, suffix=".aiderignore"
        ) as tmp_file:
            tmp_file.write(template_content)
            tmp_file.write("\n")
            relative_sessions = sessions_dir.relative_to(base_path).as_posix()
            include_session = f"!{relative_sessions}/{session_id}/\n"
            print("~~~~~INCLUDE", include_session, tmp_file.name)
            tmp_file.write(include_session)

        self.tmp_ignore_path = tmp_file.name
        return self.tmp_ignore_path

    def get_ask_coder(self, fnames=None, read_only_fnames=None, **kwargs):
        if kwargs is None:
            kwargs = {}
        if fnames is None:
            fnames = []

        if read_only_fnames is None:
            read_only_fnames = [observable_template_file, guide_path]

        return self.get_coder(
            edit_format="ask",
            fnames=fnames,
            read_only_fnames=read_only_fnames,
            **kwargs,
        )

    def get_modify_coder(self, auto_commits=False):
        base_dir = sessions_dir / self.chart_def.id
        fnames = [base_dir / f for f in ChartDef.mutable_file_names()]
        read_only_fnames = [base_dir / f for f in ChartDef.readonly_file_names()]

        if fnames is None:
            fnames = []
        req_readonly = [observable_template_file, guide_path]
        read_only_fnames.extend(req_readonly)

        return self.get_coder(
            fnames=fnames, read_only_fnames=read_only_fnames, auto_commits=auto_commits
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
        res = ask(
            f"""Give a detailed summary of this table, "{table_name}". What is it for, and what what kinds of information does it include? answer in only a sentence or two. Reply with just the summary, nothing else. {stats}"""
        )
        self._set_cache("human_summary", table_name, res)

        return res

    def execute_sql(self, sql: str, as_df=True):
        self.connect()
        if as_df:
            return self.db.execute(sql).fetchdf()
        return self.db.execute(sql).fetchall()

    def create_chart(self):
        overview = ""
        table_names = self.get_tables()
        for table in table_names:
            overview += self.table_summary_stats(table)
            overview += "\n"
            overview += self.table_human_summary(table)
            overview += "\n"
        ac = self.get_ask_coder(auto_commits=True)
        concept = ac.run(
            f"{overview}\n\nHow would you visually present data from this data source? In considering this, think about the types of data in the table and what presentation would be most useful for a reader. Come up with just one idea and describe how it works."
        )
        implementation = ac.run(prompts.generate_chart)
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

        title_desc = ac.run(
            f"Give a title and description for this chart. Respond with the title on one line and the description on the next line. Do not include anything else in your response."
        )
        title, desc = [i for i in title_desc.split("\n") if i]

        overrides = dict(
            title=title,
            description=desc,
            concept=concept,
            sql=parsed_sql,
            table_names=table_names,
            dataframe=df,
            plot_js=parsed_ob_plot,
        )
        self.chart_def = ChartDef(**{**self.chart_def.dict(), **overrides})
        self.chart_def.save()
        return self.chart_def

    def modify_chart(self, instructions: str):
        import time

        modifier = self.get_modify_coder(auto_commits=True)

        # First yield the start event
        yield {"type": "start", "message": "Starting update..."}
        time.sleep(0.1)  # Small delay to ensure events are processed separately

        # Run the modification
        modifier.run(
            f"""
Given these instructions, update the plot.js and/or query.sql code if necessary. Sometimes you may need to update concept.md or metadata.yaml as well. 
The SQL flavor is DuckDB. 
The javascript code should ALWAYS include a function `plotChart` that returns a valid Observable Plot; do not change this signature. `displayError` will be available to you as per `plot.j2`. Do not include any new imports.
Remember that `data` is an Apache Arrow table, so you cannot use normal array functions or indexing. this is extremely important. Never use data.map for example or index data with an array index bracket.s
            
Instructions: {instructions}"""
        )

        # Yield the commit message if available
        if modifier.last_aider_commit_message:
            yield {"type": "commit", "message": modifier.last_aider_commit_message}

        # Get a summary of changes
        summary = modifier.run(
            "Now just give me a concise summary of what was just changed. Respond with just the summary, nothing else."
        )

        yield {"type": "summary", "message": summary}

        # Reload and render the chart
        self.chart_def = self.chart_def.reload()
        self.chart_def.render_main_artifact()
        self.chart_def.save()

        # Finally yield the completed chart
        yield {"type": "complete", "chart": self.chart_def}


if __name__ == "__main__":
    _cd = ChartDef.load("f5d2eede-f6c3-4097-8d8e-9fe1bebe9067")
    print(_cd.db_path)
    _cd.save()
    _cd = _cd.reload()
    print(_cd.db_path)
    # analyst = LLMAnalyst(chart_def=_cd)
    # print(_cd.sql)
    # _df = analyst.execute_sql(_cd.sql)
    # print(_df)
