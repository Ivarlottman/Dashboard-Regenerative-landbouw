"""
panel_view
Author: Ivar Lottman
Date: 22-1-2025
Version: 1.0
This script is for generating the diffrent panels for the aplication
The main function of this script is done in the tabs function wich combines
all of the plots and statistics.
"""
import panel as pn
import seaborn as sns
import matplotlib as plt
import pandas as pd
from scipy import stats
from utils import subset_frame
from utils import make_aov_model
from utils import make_anova_table
from utils import make_basic_stat_frame
from utils import make_basic_join
# weird dependency explaind in last function of this script
from utils import import_data

def tabs(dataframe):
    """
    This function takes the dataframe generated from ultis.py and
    makes a final servable panel.
    The widgedts in the widget box are in global scope becouse all of
    the functions utilize it for subsetting.

    Param:dataframe
    return:servable panel tabs
    """
    # global scope widgets
    # values
    col_select_widget = pn.widgets.Select(name="colomn selectie", options=["Gewicht_T_H", "DS_ton_ha","VEM", "VCOS", "DVE", "OEB"],value="Gewicht_T_H")
    snede_select_widget = pn.widgets.CheckBoxGroup(name="snede_selection", options=[1,2,3,4], value=[1,2,3,4])
    jaar_select_widget = pn.widgets.CheckBoxGroup(name="year_selection", options=[2023, 2024], value=[2023,2024])
    behandeling_select_widget = pn.widgets.CheckBoxGroup(name="Behandeling_select", options=["A", "B", "C", "D"], value=["A","B","C","D"])
    # box widget
    widget_box = pn.WidgetBox("# Selectie", col_select_widget, "Snede", snede_select_widget,
        "Jaar", jaar_select_widget, "Behandeling", behandeling_select_widget)

    # Boxplot x axis snede
    interactive_boxplot = pn.bind(boxplot_panel, dataframe, col_select_widget, snede_select_widget, jaar_select_widget, behandeling_select_widget)
    boxplot_snede = pn.Row(widget_box, interactive_boxplot, name="Boxplot Snede")
    # Boxplot x axis jaar
    interactive_jaar_box = pn.bind(boxplot_jaarpanel, dataframe, col_select_widget, snede_select_widget, jaar_select_widget, behandeling_select_widget)
    boxplot_jaar = pn.Row(widget_box, interactive_jaar_box, name="Boxplot Jaar")
    # Barplot x axis snede
    interactive_snede_barplot = pn.bind(barplot_snede_panel, dataframe, col_select_widget, snede_select_widget, jaar_select_widget, behandeling_select_widget)
    barplot_snede = pn.Row(widget_box, interactive_snede_barplot, name="Barplot Snede")
    # Barplot x axis jaar
    interactive_jaar_barplot = pn.bind(barplot_jaar_panel, dataframe, col_select_widget, snede_select_widget, jaar_select_widget, behandeling_select_widget)
    barplot_jaar = pn.Row(widget_box, interactive_jaar_barplot, name="Barplot Jaar")
    # statistics tab
    # panels
    basic_statistic_panel = pn.bind(basic_stat_panel, dataframe, col_select_widget, snede_select_widget, jaar_select_widget, behandeling_select_widget)
    anova_req_panel = pn.bind(calc_anova_requirments, dataframe, col_select_widget, snede_select_widget, jaar_select_widget, behandeling_select_widget)
    anova_pane = pn.Row(pn.bind(anova_panel, dataframe, col_select_widget, snede_select_widget, jaar_select_widget, behandeling_select_widget), name="ANOVA")
    kruskal_pane = pn.pane.Markdown(pn.bind(get_kruskal_value, dataframe, col_select_widget, snede_select_widget, jaar_select_widget, behandeling_select_widget), name="Kruskal")
    tab_stat = pn.Tabs(anova_pane, kruskal_pane)
    # sample size string
    sample_text_pane = pn.pane.Markdown(pn.bind(get_sample_size, dataframe, col_select_widget, snede_select_widget, jaar_select_widget, behandeling_select_widget))
    # combining the subpanels
    basic_stats_row = pn.Row(basic_statistic_panel, anova_req_panel, sample_text_pane)
    stats_column = pn.Column(basic_stats_row, tab_stat)
    final_stat_panel = pn.Row(widget_box, stats_column, name="Statistics")

    main_tab = pn.Tabs(boxplot_snede, boxplot_jaar, barplot_jaar, barplot_snede, final_stat_panel).servable()
    return


def boxplot_panel(dataframe, col_select, snede, jaar, behandeling):
    """
    This function makes a boxplot based on the subsetted data provided.
    Future warning: the seaborn plot is forced into a matplotlib fig
    object to make it compatibel with panel. this could couse problems
    in the future
    param: dataframe[pandas dataframe]
    param: col_select[string with colum name with numerical values]
    param: snede[list of ints]
    param: jaar[list of ints]
    param: behandeling[list of 1 caracter strings]
    return: matplotlib pane with seaborn plot
    """
    # turn of plotimg so that it does not stack imgs
    plt.pyplot.ioff()

    # subset frame
    subframe = subset_frame(dataframe, col_select, snede, jaar, behandeling)

    # Make matplotlib fig object so it can be parsed with seaborn to panel
    fig, ax = plt.pyplot.subplots()
    boxplot = sns.boxplot(x=subframe["Snede"], y=subframe[col_select],
        hue=subframe["Behandeling"], palette=["#606C38", "#283618", "#DDA15E", "#BC6C25",])

    sns.move_legend(boxplot, "upper right")
    # boxplot.set_title("test")
    boxplot_panel = pn.pane.Matplotlib(fig)

    # plt.pyplot.ion()
    return boxplot_panel


def boxplot_jaarpanel(dataframe, col_select, snede, jaar, behandeling):
    """
    This function makes a boxplot based on the subsetted data provided.
    Future warning: the seaborn plot is forced into a matplotlib fig
    object to make it compatibel with panel. this could couse problems
    in the future
    param: dataframe[pandas dataframe]
    param: col_select[string with colum name with numerical values]
    param: snede[list of ints]
    param: jaar[list of ints]
    param: behandeling[list of 1 caracter strings]
    return: matplotlib pane with seaborn plot
    """
    # turn of plotimg so that it does not stack imgs
    plt.pyplot.ioff()

    # subset frame
    subframe = subset_frame(dataframe, col_select, snede, jaar, behandeling)

    # Make matplotlib fig object so it can be parsed with seaborn to panel
    fig, ax = plt.pyplot.subplots()
    boxplot = sns.boxplot(x=subframe["Jaar"], y=subframe[col_select], hue=subframe["Behandeling"] ,palette=["#606C38","#283618","#DDA15E","#BC6C25",])
    sns.move_legend(boxplot, "upper right")
    # boxplot.set_title("test")
    boxplot_panel = pn.pane.Matplotlib(fig)

    # plt.pyplot.ion()
    return boxplot_panel


def barplot_snede_panel(dataframe, col_select, snede, jaar, behandeling):
    """
    This function makes a barplot based on the subsetted data provided.
    Future warning: the seaborn plot is forced into a matplotlib fig
    object to make it compatibel with panel. this could couse problems
    in the future
    param: dataframe[pandas dataframe]
    param: col_select[string with colum name with numerical values]
    param: snede[list of ints]
    param: jaar[list of ints]
    param: behandeling[list of 1 caracter strings]
    return: matplotlib pane with seaborn plot
    """
    # turn of plotimg so that it does not stack imgs
    plt.pyplot.ioff()

    # subset frame
    subframe = subset_frame(dataframe, col_select, snede, jaar, behandeling)

    # Make matplotlib fig object so it can be parsed with seaborn to panel
    fig, ax = plt.pyplot.subplots()
    boxplot = sns.barplot(x=subframe["Snede"], y=subframe[col_select], hue=subframe["Behandeling"] ,palette=["#606C38","#283618","#DDA15E","#BC6C25",])
    sns.move_legend(boxplot, "upper right")
    # boxplot.set_title("test")
    boxplot_panel = pn.pane.Matplotlib(fig)

    # plt.pyplot.ion()
    return boxplot_panel


def barplot_jaar_panel(dataframe, col_select, snede, jaar, behandeling):
    """
    This function makes a barplot based on the subsetted data provided.
    Future warning: the seaborn plot is forced into a matplotlib fig
    object to make it compatibel with panel. this could couse problems
    in the future
    param: dataframe[pandas dataframe]
    param: col_select[string with colum name with numerical values]
    param: snede[list of ints]
    param: jaar[list of ints]
    param: behandeling[list of 1 caracter strings]
    return: matplotlib pane with seaborn plot
    """
    # turn of plotimg so that it does not stack imgs
    plt.pyplot.ioff()

    # subset frame
    subframe = subset_frame(dataframe, col_select, snede, jaar, behandeling)

    # Make matplotlib fig object so it can be parsed with seaborn to panel
    fig, ax = plt.pyplot.subplots()
    boxplot = sns.barplot(x=subframe["Jaar"], y=subframe[col_select], hue=subframe["Behandeling"] ,palette=["#606C38","#283618","#DDA15E","#BC6C25",])
    sns.move_legend(boxplot, "upper right")
    # boxplot.set_title("test")
    boxplot_panel = pn.pane.Matplotlib(fig)

    # plt.pyplot.ion()
    return boxplot_panel


def basic_stat_panel(dataframe, col_select, snede, jaar, behandeling):
    """
    This function makes a pandas dataframe of the basic statistics
    (mean and dev) to be displayed based on the subsetted dataframe

    param: dataframe[pandas dataframe]
    param: col_select[string with colum name with numerical values]
    param: snede[list of ints]
    param: jaar[list of ints]
    param: behandeling[list of 1 caracter strings]
    return: Pandas dataframe with basic statistics
    """
    subframe = subset_frame(dataframe, col_select, snede, jaar, behandeling)

    basic_statframe_list = []

    for treatment in subframe["Behandeling"].unique():
        treatmentframe = subset_frame(subframe, col_select, snede, jaar, [treatment])
        basic_frame = make_basic_stat_frame(treatmentframe, treatment)
        basic_statframe_list.append(basic_frame)

    joind_frame = make_basic_join(basic_statframe_list)
    return joind_frame


def calc_anova_requirments(dataframe, col_select, snede, jaar, behandeling):
    """
    This function makes a dataframe with the p-values calculated from
    shapiro-wilks for normality and bartlet for homogenity.
    The shapiro test is on the whole numeric column of the subset
    and bartlett is subsetted per selected treatment.

    param: dataframe[pandas dataframe]
    param: col_select[string with colum name with numerical values]
    param: snede[list of ints]
    param: jaar[list of ints]
    param: behandeling[list of 1 caracter strings]
    return: pandas dataframe with p values of shapiro-wilk and bartlet
    """
    subframe = subset_frame(dataframe, col_select, snede, jaar, behandeling)
    shapiro_result = stats.shapiro(subframe[col_select])

    barlet_list = []
    for treatment in subframe["Behandeling"].unique():
        treatment_frame = subset_frame(dataframe, col_select, snede, jaar, [treatment])
        barlet_list.append(treatment_frame[col_select])

    bartlett_result = stats.bartlett(*barlet_list)
    anova_req_dict = {"P waarde" : [shapiro_result[1], bartlett_result[1]]}
    anova_req_dataframe = pd.DataFrame(anova_req_dict, ["Shapiro-Wilks", "Bartlett"])

    return anova_req_dataframe


def get_sample_size(dataframe, col_select, snede, jaar, behandeling):
    """
    This function makes an f string with the sample size of the subsetted
    data.
    param: dataframe[pandas dataframe]
    param: col_select[string with colum name with numerical values]
    param: snede[list of ints]
    param: jaar[list of ints]
    param: behandeling[list of 1 caracter strings]
    return: f string with variable sample size number
    """
    subframe = subset_frame(dataframe, col_select, snede, jaar, behandeling)
    sample_size = len(subframe[col_select])
    return f"Hoeveelheid meetpunten {sample_size}"


def anova_panel(dataframe, col_select, snede, jaar, behandeling):
    """
    This function makes the anova subpanel based on the subsetted data

    param: dataframe[pandas dataframe]
    param: col_select[string with colum name with numerical values]
    param: snede[list of ints]
    param: jaar[list of ints]
    param: behandeling[list of 1 caracter strings]
    returns: anova results [pandas dataframe]
    """
    subframe = subset_frame(dataframe, col_select, snede, jaar, behandeling)
    # local widget uniqe to aov
    factor_select_widget = pn.widgets.CheckBoxGroup(name="Factor list", options=["Behandeling", "Snede", "Jaar"], value=["Behandeling", "Snede", "Jaar"])

    aov_modal = pn.bind(make_aov_model, subframe, col_select, factor_select_widget)
    aov_frame = pn.bind(make_anova_table, aov_modal)
    return pn.Row(factor_select_widget, aov_frame)


def get_kruskal_value(dataframe, col_select, snede, jaar, behandeling):
    """
    This function calculates the kruskal wallis value and returns it as an f string
    param: dataframe[pandas dataframe]
    param: col_select[string with colum name with numerical values]
    param: snede[list of ints]
    param: jaar[list of ints]
    param: behandeling[list of 1 caracter strings]
    return: f string with the kruskal wallis p value
    """
    subframe = subset_frame(dataframe, col_select, snede, jaar, behandeling)
    dataset = set(dataframe["Behandeling"])

    kruskal_list = []
    for treatment in subframe["Behandeling"].unique():
        treatment_frame = subset_frame(dataframe, col_select, snede, jaar, [treatment])
        kruskal_list.append(treatment_frame[col_select])

    kruskal_result = stats.kruskal(*kruskal_list)

    return f"Kruskal Wallis P waarde {kruskal_result[1]}"


def cach_dependency_main():
    """
    this function and its call is the same as main.py but for
    probebel caching reasons/glitches it depends on
    this script/function to properly make servebel panel.
    if script does not work launch main.py with --dev and
    comment this function, save and uncomment this function.
    """
    x = import_data()
    tabs(x)
    return

cach_dependency_main()
