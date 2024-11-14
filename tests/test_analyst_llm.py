import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from analyst.llm import LLMAnalyst, ChartIdea


class TestLLMAnalyst(unittest.TestCase):
    def setUp(self):
        self.db_path = ":memory:"
        self.analyst = LLMAnalyst(db_path=self.db_path)

    def test_init(self):
        self.assertEqual(self.analyst.model_name, "claude-3-5-sonnet-20240620")
        self.assertEqual(self.analyst.db_path, ":memory:")
        self.assertIsNone(self.analyst.db)

    @patch("duckdb.connect")
    def test_connect(self, mock_connect):
        self.analyst.connect()
        mock_connect.assert_called_once_with(self.db_path)

    @patch("duckdb.connect")
    def test_context_manager(self, mock_connect):
        mock_db = MagicMock()
        mock_connect.return_value = mock_db

        with self.analyst as a:
            self.assertIsNotNone(a.db)

        mock_db.close.assert_called_once()

    @patch("duckdb.connect")
    def test_get_tables(self, mock_connect):
        mock_db = MagicMock()
        mock_db.execute.return_value.fetchall.return_value = [("table1",), ("table2",)]
        mock_connect.return_value = mock_db

        tables = self.analyst.get_tables()
        self.assertEqual(tables, ["table1", "table2"])

    @patch("duckdb.connect")
    def test_table_summary_stats(self, mock_connect):
        mock_db = MagicMock()
        mock_db.execute.side_effect = [
            MagicMock(fetchall=lambda: [("col1", "INT"), ("col2", "TEXT")]),
            MagicMock(fetchone=lambda: (100,)),
            MagicMock(fetchall=lambda: [("value1", 50), ("value2", 30)]),
            MagicMock(fetchall=lambda: [("value1", 50), ("value2", 30)]),
            MagicMock(fetchall=lambda: [(1, "a"), (2, "b"), (3, "c")]),
        ]
        mock_connect.return_value = mock_db

        summary = self.analyst.table_summary_stats("test_table")
        self.assertIn("Table: test_table", summary)
        self.assertIn("Total rows: 100", summary)
        self.assertIn("col1: INT", summary)
        self.assertIn("col2: TEXT", summary)

    @patch("analyst.llm.LLMAnalyst.get_ask_coder")
    @patch("analyst.llm.LLMAnalyst.table_summary_stats")
    def test_table_human_summary(self, mock_stats, mock_get_coder):
        mock_stats.return_value = "Mock stats"
        mock_coder = MagicMock()
        mock_coder.run.return_value = "Human summary"
        mock_get_coder.return_value = mock_coder

        summary = self.analyst.table_human_summary("test_table")
        self.assertEqual(summary, "Human summary")

    @patch("duckdb.connect")
    def test_execute_sql(self, mock_connect):
        mock_db = MagicMock()
        mock_db.execute.return_value.fetchdf.return_value = pd.DataFrame(
            {"a": [1, 2, 3]}
        )
        mock_connect.return_value = mock_db

        df = self.analyst.execute_sql("SELECT * FROM test")
        pd.testing.assert_frame_equal(df, pd.DataFrame({"a": [1, 2, 3]}))

    @patch("analyst.llm.LLMAnalyst.get_ask_coder")
    @patch("analyst.llm.LLMAnalyst.table_summary_stats")
    @patch("analyst.llm.LLMAnalyst.table_human_summary")
    @patch("analyst.llm.LLMAnalyst.execute_sql")
    def test_get_chart_idea(
        self, mock_execute, mock_human_summary, mock_stats, mock_get_coder
    ):
        mock_stats.return_value = "Mock stats"
        mock_human_summary.return_value = "Human summary"
        mock_coder = MagicMock()
        mock_coder.run.side_effect = [
            "Chart concept",
            '```sql\nSELECT * FROM test\n```\n```json\n{"mark": "bar"}\n```',
        ]
        mock_get_coder.return_value = mock_coder
        mock_execute.return_value = pd.DataFrame({"a": [1, 2, 3]})

        chart_idea = self.analyst.get_chart_idea("test_table")
        self.assertIsInstance(chart_idea, ChartIdea)
        self.assertEqual(chart_idea.sql, "SELECT * FROM test")
        self.assertEqual(chart_idea.vega_lite, {"mark": "bar"})
        pd.testing.assert_frame_equal(
            chart_idea.dataframe, pd.DataFrame({"a": [1, 2, 3]})
        )


if __name__ == "__main__":
    unittest.main()
