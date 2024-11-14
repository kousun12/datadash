import os
import tempfile

import pandas as pd
import duckdb


def xls_to_csv(xl_path, csv_path):
    df = pd.read_excel(xl_path)
    df.to_csv(csv_path, index=False)


def csv_to_duckdb(csv_path, db_path, table_name):
    con = duckdb.connect(db_path)
    con.execute(
        f"""
        CREATE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{csv_path}')
    """
    )
    con.close()


import argparse


def main():
    parser = argparse.ArgumentParser(description="Convert XLS to DuckDB")
    parser.add_argument("xls_path", help="Path to the input XLS file")
    parser.add_argument("db_path", help="Path for the DuckDB database")
    parser.add_argument(
        "--table_name", default="data", help="Name of the table in DuckDB"
    )

    args = parser.parse_args()

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_csv:
        temp_csv_path = temp_csv.name

    try:
        xls_to_csv(args.xls_path, temp_csv_path)
        csv_to_duckdb(temp_csv_path, args.db_path, args.table_name)
    finally:
        os.unlink(temp_csv_path)


if __name__ == "__main__":
    main()
