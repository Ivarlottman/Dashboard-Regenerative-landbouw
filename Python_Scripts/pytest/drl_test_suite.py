"""
test enviorment becouse laptop errors
"""
import pandas as pd

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
