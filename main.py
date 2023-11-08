from teiko_tools.analysis import cell_counts_calculator, CellCountsBoxPlot

# create the file for problem 1
cell_counts_calculator(file_name="cell-count.csv", file_name_out="cell-counts-relative.csv")

# create the boxplot for problem 2
ccbp = CellCountsBoxPlot(file_name="cell-count.csv", file_name_out = "cell-counts-relative_boxplot.png")
ccbp.cell_type_treatment_box_plot()