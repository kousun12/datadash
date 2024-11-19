import pytest
import uuid
import pandas as pd
from analyst.chart_def import ChartDef


class TestChartDef:
    @pytest.fixture
    def sample_chart_def(self, tmp_path):
        """Create a sample ChartDef for testing"""
        test_id = uuid.UUID("12345678-1234-5678-1234-567812345678")
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

        return ChartDef(
            id=test_id,
            title="Test Chart",
            description="A test chart description",
            concept="Test concept markdown",
            sql="SELECT * FROM test_table",
            db_path="test.db",
            table_names=["test_table"],
            plot_js="console.log('test plot')",
            dataframe=df,
        )

    def test_save_and_load(self, tmp_path, sample_chart_def):
        """Test that saving and loading a ChartDef preserves all data"""
        # Save the chart def
        saved_path = sample_chart_def.save(tmp_path)
        assert saved_path.exists()

        # Load it back
        chart_dir = (
            tmp_path
            / "sessions"
            / sample_chart_def.table_name
            / str(sample_chart_def.id)
        )
        loaded_def = ChartDef.from_path(chart_dir)

        # Verify all fields match
        assert loaded_def.id == sample_chart_def.id
        assert loaded_def.title == sample_chart_def.title
        assert loaded_def.description == sample_chart_def.description
        assert loaded_def.concept == sample_chart_def.concept
        assert loaded_def.sql == sample_chart_def.sql
        assert loaded_def.db_path == sample_chart_def.db_path
        assert loaded_def.table_name == sample_chart_def.table_name
        assert loaded_def.plot_js == sample_chart_def.plot_js

        # DataFrame is not loaded by default when skip_df=True
        assert loaded_def.dataframe is None

    def test_save_and_load_with_dataframe(self, tmp_path, sample_chart_def):
        """Test that saving and loading with dataframe works"""
        # Save with dataframe
        saved_path = sample_chart_def.save(tmp_path, skip_df=False)
        assert saved_path.exists()

        # Load it back
        chart_dir = (
            tmp_path
            / "sessions"
            / sample_chart_def.table_name
            / str(sample_chart_def.id)
        )
        loaded_def = ChartDef.from_path(chart_dir)

        # Verify dataframe was loaded and matches
        assert loaded_def.dataframe is not None
        pd.testing.assert_frame_equal(loaded_def.dataframe, sample_chart_def.dataframe)
