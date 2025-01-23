"""
Main script
Author: Ivar Lottman
Date: 22-1-2025
Version: 1.0
This is the main script for
the dashboard regenertive farming dashboard aplication

Commandline CD to /Python_Scripts then insert the following command
[panel][serve][main.py]
"""
from utils import import_data
from panel_view import tabs
import panel as pn


def main():
    """
    This is the main function of the dashboard.
    The data is imported with the import data function from utils and
    is past onto the Tabs function from panel_view to display the data
    Param: None
    Return: served Bokeh server
    """
    merged_dataframe = import_data()
    # served function
    tabs(merged_dataframe)


if __name__ == "__main__":
    main()
