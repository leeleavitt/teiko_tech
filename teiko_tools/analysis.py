import pandas as pd
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt


def cell_counts_calculator(file_name: str = "cell-count.csv", file_name_out: str = "cell-counts-relative.csv"):
    """Function to convert cell count in cell-count.csv to relative frequency (in percentage) of total cell count for each sample. 
    Total cell count of each sample is the sum of cells in the five populations of that sample. 
    This return an output file in csv format with cell count and relative frequency of each population of each sample per line. 

    Args:
        file_name (str, optional): Name of the file to read in. Defaults to "cell-counts.csv".
        file_name_out (str, optional): Name of the file to write out. Defaults to "cell-counts-relative.csv".

    Returns:
        None
    
    """
    # load the cell counts
    cell_df = pd.read_csv(file_name)

    # collect column names for the cell types
    cell_name_columns = ['b_cell', "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
    # make new column for total count
    cell_df['total_count'] = cell_df.loc[:,cell_name_columns].apply(sum, axis=1)

    # calculate the relative frequency of each cell type
    cell_rf_df = cell_df.loc[:,cell_name_columns].apply(lambda x: x/cell_df['total_count']*100)
    # make a new dataframe with the sample and total count columns
    cell_rf_df = pd.concat( [cell_df[["sample", "total_count"]], cell_rf_df], axis=1)

    # melt the dataframe to get the desired format
    cell_rf_df_long = cell_rf_df.melt(id_vars=["sample", "total_count"], var_name="population", value_name="percentage")

    # make a new dataframe with the sample and total count columns with the cell counts
    columns_to_grab = ["sample", "total_count", *cell_name_columns]
    # melt the dataframe to get the desired format
    cell_df_long = cell_df[columns_to_grab].melt(id_vars=["sample", "total_count"], var_name="population", value_name="count")

    # merge the two dataframes
    cell_df_rf_long = cell_df_long.merge(cell_rf_df_long, how="left", on=["sample", "total_count", "population"])

    # save the dataframe with the relative frequency no index
    cell_df_rf_long.to_csv(file_name_out, index=False)


class CellCountsBoxPlot:
    """Class to generate a boxplot of the cell counts for each cell type.
    The boxplot will be generated using the relative frequency of each cell type.
    """

    def __init__(self, file_name="cell-counts-relative.csv", file_name_out="cell-counts-relative_boxplot.png"):
        self.file_name = file_name
        self.file_name_out = file_name_out



    def cell_type_t_tester(self, cell_type_to_calc: str = 'b_cell'):
        """Function to calculate the t-test for a given cell type.
        Args:
            cell_type_to_calc (str, optional): Name of the cell type to calculate the t-test for. Defaults to 'b_cell'.
        Returns:
            p_val (float): p-value from the t-test"""
        b_cell_group_n = self.grouped_data.get_group(('n', cell_type_to_calc))['cell_count']
        b_cell_group_y = self.grouped_data.get_group(('y', cell_type_to_calc))["cell_count"]

        t_stat, p_val = stats.ttest_ind(b_cell_group_n, b_cell_group_y)
        p_val = np.round(p_val, 4)
        return p_val


    def cell_type_treatment_box_plot(self):

        # load the data
        cell_df = pd.read_csv(self.file_name)

        # create a mask for the treatment column
        treatment_mask = cell_df["treatment"] == "tr1" 
        condition_mask = cell_df["condition"] == "melanoma"
        sample_type_mask = cell_df["sample_type"] == "PBMC"

        # create a new dataframe with the filtered data
        cell_ss_df = cell_df[treatment_mask & condition_mask & sample_type_mask]
        # drop the columns that are not needed
        cell_ss_df = cell_ss_df[['response', 'b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']]

        # we are going to use the melt function to transform the data
        cell_ss_df_melt = cell_ss_df.melt(id_vars=['response'], var_name='cell_type', value_name='cell_count')


        # now lets go with statistics to provide a p-value
        # we will use a t-test

        # collect all the cell types
        cell_types_unique = cell_ss_df_melt.cell_type.unique()

        # group the data by response and cell type
        self.grouped_data = cell_ss_df_melt.groupby(['response', 'cell_type'])

        # now generate the p value for each cell type
        x_labels = [] 
        p_vals = []
        weights = []
        for cell_type in cell_types_unique:
            p_val = self.cell_type_t_tester(cell_type)
            x_labels.append(f"{cell_type}\np={p_val}")
            p_vals.append(p_val)

            if p_val < 0.05:
                weights.append('bold')
            else:
                weights.append('normal')

        # using seaborn to plot the data
        ax = sns.boxplot(
            x="cell_type", 
            y="cell_count", 
            hue="response", 
            data=cell_ss_df_melt)

        # adding the stripplot to show the datapoints
        ax = sns.stripplot(
            ax=ax,
            x='cell_type', 
            y='cell_count', 
            hue="response", 
            data=cell_ss_df_melt, 
            dodge=True, 
            jitter=False, 
            color = "black",
            legend=False
        )

        # adding the legend and the x labels
        ax.set_xticklabels(x_labels)

        # i want the significant p values to be bolded
        for label, weight in zip(ax.get_xticklabels(), weights):
            label.set_fontweight(weight)

        # update the title
        plt.title("Cell counts for each cell type comparing response\nBolded x labels are significant (p < 0.05)")
        
        if self.file_name_out:
            plt.savefig(self.file_name_out, dpi=300)
        else:
            plt.show()


