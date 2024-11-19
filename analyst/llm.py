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
)

guide_path = base_path / "plot_guide.md"
cache_filename = "analyst_cache.json"
observable_plot_version = "0.6.0"


class LLMAnalyst:
    def __init__(
        self,
        model_name=default_model,
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
        temp = kwargs.pop("temperature", 0.6)
        coder: Coder = Coder.create(
            main_model=Model(self.model_name),
            io=io,
            cache_prompts=True,
            stream=False,
            auto_commits=auto_commits,
            verbose=True,
            **kwargs,
        )
        coder.repo.aider_ignore_file = base_path / ".aiderignore-modify"
        print(coder.get_all_relative_files())
        print(coder.get_repo_map())

        coder.temperature = temp
        return coder

    def get_ask_coder(self, fnames=None, read_only_fnames=None, **kwargs):
        if kwargs is None:
            kwargs = {}
        if fnames is None:
            fnames = []

        req_readonly = [observable_template_file, guide_path]
        if read_only_fnames:
            read_only_fnames.extend(req_readonly)
        else:
            read_only_fnames = req_readonly

        return self.get_coder(
            edit_format="ask",
            fnames=fnames,
            read_only_fnames=read_only_fnames,
            **kwargs,
        )

    def get_modify_coder(self, fnames=None, read_only_fnames=None, auto_commits=False):
        if fnames is None:
            fnames = []
        req_readonly = [observable_template_file, guide_path]
        if read_only_fnames:
            read_only_fnames.extend(req_readonly)
        else:
            read_only_fnames = req_readonly

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

    def create_chart(self, table_name: str):
        stats = self.table_summary_stats(table_name)
        overview = self.table_human_summary(table_name)
        ac = self.get_ask_coder()
        concept = ac.run(
            f"How would you visually present this table? In considering this, think about the types of data in the table and what presentation would be most useful for a reader. Come up with just one idea and describe how it works.\n\n{overview}\n{stats}"
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

        return ChartDef(
            title=title,
            description=desc,
            concept=concept,
            sql=parsed_sql,
            table_name=table_name,
            db_path=self.db_path.relative_to(base_path / "fw/src").as_posix(),
            dataframe=df,
            plot_js=parsed_ob_plot,
        )

    def modify_chart(self, instructions: str, at_dir: Path):
        ChartDef.from_path(at_dir)
        fnames = [at_dir / f for f in ChartDef.mutable_file_names()]
        readonly_fnames = [at_dir / f for f in ChartDef.readonly_file_names()]
        modifier = self.get_modify_coder(
            fnames=fnames, read_only_fnames=readonly_fnames, auto_commits=True
        )
        modifier.run(
            f"""
Given these instructions, update the plot.js and/or query.sql code if necessary. Sometimes you may need to update concept.md or metadata.yaml as well. 
The SQL flavor is DuckDB. 
The javascript code should ALWAYS include a function `plotChart` that returns a valid Observable Plot; do not change this signature. `displayError` will be available to you as per `plot.j2`. Do not include any new imports.
Remember that `data` is an Apache Arrow table, so you cannot use normal array functions or indexing. this is extremely important. Never use data.map for example or index data with an array index bracket.s
            
Instructions: {instructions}"""
        )
        reloaded = ChartDef.from_path(at_dir)
        reloaded.render_main_artifact(at_dir)
        return reloaded


if __name__ == "__main__":
    db_path = base_path / "fw/src/data/us_ag.db"
    analyst = LLMAnalyst(db_path=db_path)
    at_dir = default_data_dir / "sessions/ag_data/4beb2033-a621-469d-822d-f53c17d5f4fe"
    cd = ChartDef.from_path(at_dir)
    print(cd.sql)
    df = analyst.execute_sql(cd.sql)
    print(df)
