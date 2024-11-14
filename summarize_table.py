import duckdb
import textwrap
from io import StringIO


def summarize_table(db_path, table_name, sample_rows=3, max_str_length=50):
    conn = duckdb.connect(db_path)
    output = StringIO()

    # Get column info
    columns = conn.execute(f"DESCRIBE {table_name}").fetchall()

    # Get sample data
    sample_data = conn.execute(
        f"SELECT * FROM {table_name} LIMIT {sample_rows}"
    ).fetchall()

    # Get row count
    row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    output.write(f"Table: {table_name}\n")
    output.write(f"Total rows: {row_count}\n\n")
    output.write("Columns:\n")

    for col in columns:
        col_name, col_type = col[0], col[1]
        output.write(f"  {col_name}: {col_type}\n")

    output.write("\nSample data:\n")
    for row in sample_data:
        formatted_row = []
        for value in row:
            if isinstance(value, str):
                value = textwrap.shorten(value, width=max_str_length, placeholder="...")
            formatted_row.append(str(value))
        output.write("  " + " | ".join(formatted_row) + "\n")

    conn.close()
    return output.getvalue()


if __name__ == "__main__":
    summary = summarize_table("us_ag.db", "ag_data")
    print(summary)
