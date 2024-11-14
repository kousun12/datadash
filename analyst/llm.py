from aider.models import Model
import textwrap
from io import StringIO
import duckdb
import json
from pathlib import Path

default_cache_dir = Path("/tmp/analyst")
cache_filename = "table_summaries_cache.json"


class LLMAnalyst:
    def __init__(
        self,
        model_name="claude-3-5-sonnet-20240620",
        db_path=None,
        cache_dir=default_cache_dir,
    ):
        self.model_name = model_name
        self.db_path = db_path
        self.db = None
        self._summary_cache = {}
        cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_file = Path(cache_dir) / cache_filename
        self._load_cache()

    def _load_cache(self):
        """Load cached summaries from file if it exists"""
        if self._cache_file.exists():
            with open(self._cache_file) as f:
                cache = json.load(f)
                # Use db_path as top-level key
                self._summary_cache = cache.get(str(self.db_path) or "", {})

    def _save_cache(self):
        """Save cached summaries to file"""
        cache = {str(self.db_path): self._summary_cache}
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
        read_only_fnames = []

        return self.get_coder(
            edit_format="ask",
            fnames=fnames,
            read_only_fnames=read_only_fnames,
            **kwargs,
        )

    def get_modify_coder(self, fnames=None):
        if fnames is None:
            fnames = []
        read_only_fnames = []
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

    def table_human_summary(self, table_name: str) -> str:
        # Check in-memory cache first
        if table_name in self._summary_cache:
            return self._summary_cache[table_name]

        # Generate new summary if not cached
        stats = self.table_summary_stats(table_name)
        ac = self.get_ask_coder()
        res = ac.run(
            f"""Give a detailed summary of this table, "{table_name}". What is it for, and what what kinds of information does it include? answer in only a sentence or two. Reply with just the summary, nothing else. {stats}"""
        )

        # Cache the result both in memory and file
        self._summary_cache[table_name] = res
        self._save_cache()

        return res


if __name__ == "__main__":
    path = "/Users/robcheung/code/fred/summarize_table.py"
    db_path = "/Users/robcheung/code/fred/us_ag.db"
    analyst = LLMAnalyst(db_path=db_path)
    # res = analyst.get_ask_coder(fnames=[path]).run("what does this file do")
    for table in analyst.get_tables():
        stats = analyst.table_summary_stats(table)
        overview = analyst.table_human_summary(table)
        print(overview, stats)
        query = analyst.get_ask_coder().run(
            f"How would you visually present this table? Given your response, what sql query would you need in order to generate the data for this visualization? For the sql, put it in a code fence block.\n\n{overview}\n{stats}"
        )
        print(query)
