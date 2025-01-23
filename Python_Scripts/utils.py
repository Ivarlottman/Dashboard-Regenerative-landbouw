"""
Utility script
Author: Ivar Lottman
Date: 22-1-2025
Version: 1.0
In this script are the extra utility's needed for making the dataframe
and statistical preperation and data manipulation for the panel script.
"""
import os
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols


def config_reader(path):
    """
    This function reads all the file names in the
    config file
    param: None
    Return file_list[list with strings]
    """
    file_list = []
    fail_list = []
    if type(path) != str:
        return ValueError

    with open(path, "r") as file:
        for line in file:
            newline = line.strip()
            if ".xlsx" in newline:
                file_list.append(newline)
            else:
                fail_list.append(newline)

        if len(fail_list) != 0:
            print("list of failed files to read", fail_list)
    return file_list


def read_files(file_list):
    """
    This function reads all of the files in the file list
    with pandas read excel using openpyx submodule.

    param file_list [list with strings]
    return frame list [list with panda dataframes]
    """
    frame_list = []
    for file in file_list:
        dataframe = pd.read_excel(os.path.join("..", "Raw_data", file))
        filterd_frame = dataframe.loc[:, ["Jaar", "Snede", "Behandeling", "Gewicht_T_H", "DS_ton_ha","VEM", "VCOS", "DVE", "OEB"]]
        frame_list.append(filterd_frame)

    return frame_list


def merge_frames(dataframe_list):
    """
    This function merges all of the panda dataframes
    into one dataframe
    param:dataframe list[list with dataframes]
    return:merged dataframe[one pandas dataframe]
    """
    if type(dataframe_list) != list:
        return ValueError

    for item in dataframe_list:
        if type(item) != pd.core.frame.DataFrame:
            return ValueError

    merged_dataframe = dataframe_list[0].merge(*dataframe_list[1:], "outer")
    return merged_dataframe


def import_data():
    """
    This function uses the config reader function, read_file and 
    merge frames function to get the merged dataframe needed
    for the aplication
    param: None
    return: merged pandas dataframe
    """
    config_path = os.path.join("..", "config.txt")
    config_list = config_reader(config_path)
    frame_list = read_files(config_list)
    merged_dataframe = merge_frames(frame_list)

    return merged_dataframe


def subset_frame(merged_frame, column_selection, snede_list=[1,2,3,4], jaar_list=[2023,2024], behandeling_list=["A","B","C","D"]):
    """
    This function makes a subset pandas dataframe
    based on the selected variables given to it.
    param: dataframe[pandas dataframe]
    param: col_select[string with colum name with numerical values]
    param: snede[list of ints]
    param: jaar[list of ints]
    param: behandeling[list of 1 caracter strings]
    return: subsetted_frame[pandas dataframe]
    """
    # uses the .isin funcction of pandas
    row_select_frame = merged_frame[merged_frame["Snede"].isin(snede_list) &
    merged_frame["Jaar"].isin(jaar_list) &
    merged_frame["Behandeling"].isin(behandeling_list)]
    subsetted_frame = row_select_frame.loc[:,["Snede", "Jaar", "Behandeling", column_selection]]
    return subsetted_frame


def make_basic_stat_frame(input_frame, behandeling_code):
    """
    This function makes a 1 colum 2 row dataframe with mean and dev
    based on the input frame.
    param:input_frame[pandas dataframe]
    param behandeling_code[1 caracter string]
    """
    # mean and diviation
    mean = input_frame.loc[:,[False,False,False,True]].mean()
    dev = input_frame.loc[:,[False,False,False,True]].std()
    # make dict for dataframe
    data_dict = {behandeling_code : [mean.iloc[0], dev.iloc[0]]}

    # makes dataframe with mean and std as rownames
    return_frame = pd.DataFrame(data_dict, ["mean", "std"])

    return return_frame


def make_basic_join(frame_list):
    """
    This function joins dataframes
    param:frame list[list of dataframes]
    return:newframe[joined pandas dataframe]
    """
    # join function based the amount of imput frames
    newframe = frame_list[0].join(frame_list[1:])
    return newframe


def make_aov_model(dataframe, numeric_colunm, factor_list):
    """
    Makes an aov modal using statsmodels with a dataframe
    as input
    the input for the model is a string based on:
    [numeric colum] [~ as function of][C[factor]+[C[factor]]]
    that can be fitted into the anova function
    param: dataframe[pandas dataframe]
    param: numeric_colunm[string of the selected numeric column]
    param: factor list[list with factor strings]
    return anova ols.fit() model
    """

    if len(factor_list) == 2:
        factor_1 = "C("+factor_list[0]+")"
        factor_2 = "C("+factor_list[1]+")"

        anova_string = numeric_colunm + " ~ " + factor_1 + " + " + factor_2 + " + " + factor_1+":"+factor_2

        anova_model = ols(anova_string, dataframe).fit()
    if len(factor_list) == 3:
        factor_1 = "C("+factor_list[0]+")"
        factor_2 = "C("+factor_list[1]+")"
        factor_3 = "C("+factor_list[2]+")"
        anova_string = numeric_colunm + " ~ " + factor_1 + " + " + factor_2 + " + " + factor_3 + " + " + factor_1+":" + \
            factor_2 + " + " + factor_1+":"+factor_3 + " + " + factor_2+":"+factor_3 + " + " + factor_1+":"+factor_2+":"+factor_3
        anova_model = ols(anova_string, dataframe).fit()

    return anova_model


def make_anova_table(model):
    """
    This function makes a aov results pandas dataframe

    param:model[sm.ols.aov model]
    return: data_model [pandas dataframe with aov results]
    """
    data_model = sm.stats.anova_lm(model, typ=2)
    return data_model
