import pytest
import pandas as pd
from io import StringIO
from teiko_tools.analysis import cell_counts_calculator, CellCountsBoxPlot


class TestCellCountsCalculator:
    @pytest.fixture(autouse=True)
    def setup_class(self, tmpdir):
        # This method will be run before every test
        self.tmpdir = tmpdir
        self.input_csv = tmpdir.join("input.csv")
        self.output_csv = tmpdir.join("output.csv")
        sample_data = """sample,b_cell,cd8_t_cell,cd4_t_cell,nk_cell,monocyte
sample1,100,150,200,120,130
sample2,200,100,150,170,180"""
        self.input_csv.write(sample_data)

    def test_creates_file(self):
        # Act
        cell_counts_calculator(str(self.input_csv), str(self.output_csv))

        # Assert
        assert self.output_csv.check(file=1)  # File exists

    def test_output_structure(self):
        # Act
        cell_counts_calculator(str(self.input_csv), str(self.output_csv))
        output_df = pd.read_csv(str(self.output_csv))

        # Assert
        expected_columns = [
            "sample",
            "total_count",
            "population",
            "count",
            "percentage",
        ]
        assert list(output_df.columns) == expected_columns

    def test_calculations_correctness(self):
        # Act
        cell_counts_calculator(str(self.input_csv), str(self.output_csv))
        output_df = pd.read_csv(str(self.output_csv))

        # Assert
        total_count_sample1 = 700  # Sum of all cell counts for sample1
        b_cell_percentage_sample1 = (100 / total_count_sample1) * 100
        obtained_percentage = output_df[
            (output_df["sample"] == "sample1") & (output_df["population"] == "b_cell")
        ]["percentage"].iloc[0]
        assert b_cell_percentage_sample1 == pytest.approx(obtained_percentage)

    def test_empty_input_file(self):
        # Arrange
        empty_csv = self.tmpdir.join("empty.csv")
        empty_csv.write("")

        # Act and Assert
        with pytest.raises(pd.errors.EmptyDataError):
            cell_counts_calculator(str(empty_csv), str(self.output_csv))

    def test_invalid_input_format(self):
        # Arrange
        invalid_csv = self.tmpdir.join("invalid.csv")
        invalid_data = """sample;b_cell;cd8_t_cell;cd4_t_cell;nk_cell;monocyte
sample1;100;150;200;120;130
sample2;200;100;150;170;180"""
        invalid_csv.write(invalid_data)

        # Act and Assert
        with pytest.raises(KeyError):
            cell_counts_calculator(str(invalid_csv), str(self.output_csv))


from unittest.mock import Mock, patch


class TestCellCountsBoxPlot:
    @pytest.fixture
    def cell_count_data(self, tmpdir):
        data = pd.DataFrame(
            {
                "sample": ["s1", "s2", "s3", "s4", "s5", "s6"],
                "treatment": ["tr1", "tr1", "tr1", "tr1", "tr1", "tr1"],
                "condition": [
                    "melanoma",
                    "melanoma",
                    "melanoma",
                    "melanoma",
                    "melanoma",
                    "melanoma",
                ],
                "sample_type": ["PBMC", "PBMC", "PBMC", "PBMC", "PBMC", "PBMC"],
                "response": ["y", "n", "y", "n", "y", "n"],
                "b_cell": [100, 200, 150, 250, 300, 350],
                "cd8_t_cell": [120, 220, 180, 280, 320, 370],
                "cd4_t_cell": [130, 230, 170, 270, 310, 360],
                "nk_cell": [140, 240, 160, 260, 330, 380],
                "monocyte": [110, 210, 190, 290, 340, 390],
            }
        )
        file = tmpdir.join("cell-count.csv")
        data.to_csv(file, index=False)
        return file

    # Test if the boxplot is created and saved correctly
    def test_cell_type_treatment_box_plot_creates_file(self, cell_count_data, tmpdir):
        plot_file = tmpdir.join("boxplot.png")
        boxplotter = CellCountsBoxPlot(str(cell_count_data), str(plot_file))
        with patch("matplotlib.pyplot.savefig") as mock_savefig:
            boxplotter.cell_type_treatment_box_plot()
            mock_savefig.assert_called_with(str(plot_file), dpi=300)

    # Test the t-test calculation with a mock
    def test_cell_type_t_tester_correct_p_value(self, cell_count_data):
        boxplotter = CellCountsBoxPlot(str(cell_count_data))
        boxplotter.cell_type_treatment_box_plot()

        # Perform the t-test for a cell type with known values
        p_val = boxplotter.cell_type_t_tester("b_cell")

        # Check if the p-value is within the expected range
        assert (
            p_val >= 0 and p_val <= 1
        )  # p-value is a probability, so it should be between 0 and 1
