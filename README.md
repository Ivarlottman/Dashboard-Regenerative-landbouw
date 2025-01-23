# Project dashboard regenerative farming
Made by Ivar Lottman
Project owner: Fenna Feenstra  
Teachers: Michiel Noback and Bart Barnard

## introduction
Introduction Regeneratieve farming project  
Regenertive farming is a method of farming aimd at restoring and improving the siol end ecosystem, preffrebly by using natural procceses to its advantige. This study focusus on the optimalisation of natural fertelizer.
For this 3 treatment fertelizers where used: Airation, grander and a combination of them. 
The goal if this project is to visualize the gras yeald data in a dashboard for both farmers and regulators aswel as researchers.

#### instalation guide
To run this dashboard you first need to instal python 3.14 or higher
After that install all of the packeges in the requirements.txt file with:

pip install [package] 

command in either windows powershel or linux commandline

##### Adding data 
To add aditional data place a tidy excel with the folowing columns: 

["Jaar", "Snede", "Behandeling", "Gewicht_T_H", "DS_ton_ha","VEM", "VCOS", "DVE", "OEB"]

for an example please look at the 2024 or 2023 clean data files. Then add the file name with extension (.xlsx) in the config txt file on a new line

##### Running Aplication
To run this Aplication type the following in the command console

cd [path/to/Dashboard-Regenerative-landbouw/Python_Scripts]

panel serve main.py

In case this doesnt work please look at the bug section of this readme

#### explanation reposetory
Logboek directory
In this directory are the exploretory data analysis, personal logfile and the hostingplan for this project.

Python_Scripts directory
in this file are the python scripts needed to run this file.

Python_Scripts/pytest
In this folder are the pytest stored for coding purposes.
it contains the test script and a test suite script.

Raw_data 
In this folder is the Raw and cleand data in excel format.

Raw_data/Codebook
In this directory are the codebooks with short explanation of the abreviations of the excel files

static directory
In this directory are the imges for this readme

static/wireframe
In this directory are the orinal wireframes designs for this aplication

#### User guide
The usage of this application is divided into 2 parts: the basic statistics and the advanced statistics
The first part the basic statistics is for the a quick overview of the effect of the treatments on a chocen production value like Gewicht_T_H or weight in tons per acre.
This way you can quicly see if your intrested treatment method differs from the standard method and if you find the diffrence intresting enough to work with.

Meaning of treatments as can be found in the codebook in Raw_data/Codebook
- A = Grander
- B = Grander+Airration
- C = Airration
- D = No treatment

Tabs the first 4 tabs are box and bar plots based on either Jaar or Snede depending on how you want to look at the data and the last tab is for advanced statistics.

![boxplot all options](/static/boxplot_all_options.PNG)

The widget selection box on the left side of the image allows you to filter the dataset based on the selected jaar, snede, treatment and production value options.

![select widget](/static/col_select.PNG)

This widget selects the type of production value you want to observe

![boxplot some options](/static/boxplot_part_options_jaar.PNG)

Subsetted example comparing years with all treatments -D on only snede 1

barplots with the same functionality

![barplot all options](/static/barplot_jaar_all_options.PNG)

![barplot some options](/static/barplot_snede_vem.PNG)

The second part advanced statistics is a panel that requires some statistical knowlige and can help detirmen if the chosen groups are statisticly diffrent from one another. For this section some knowlidge of statitics is recomended.
For a quick summery p values have to be below 0.05 to be statisticly significent. In this case either anova or kruskal is used to determing statistical significance. for anova to be valid the p values of both the shapiro-wilks test aswel as the bartet need to be significant. if atliest one of these 2 test is not significant use the kruskal wallis test and limit the data to one factor to determin significance.

![statistics tab](/static/statistics_main.PNG)
Widget bar works the same as the bar/boxplots
In the first in the top row are the basic statistics of mean and deviation to give you a first impression. The second in the top row is the shapiro wilks and bartlet test with ther P values. The third in the top row is the amount of samples. 

![meetpunten](/static/meetpunten.PNG)
Note the amount of samples has a direct effect on the statistical values so a power analys would be advised.

![statistics subtab](/static/statistic_subtab.PNG)

In the anova tab the first checkboxlist is the factors you can chose to have in anova and the second tab is the kruskal wallis test

![kruskal](/static/kruskal.PNG)

#### programmer guide
Main.py
Main module that loads in the data with utils.py function and displays it with panel_view.py function

Panel_view.py
This module contains all of the display panels

Utils.py
This function contains the data import functions aswel as the dataframe handeling and statistics for the panel view script.

##### Known bugs
###### launch cache based bug.
If the server does not display aplication after panel serve main.py its most likely this bug
To fiks it launch panel in dev mode with like this
panel serve main.py --dev --show
then open the panel view script and put a # the last line in the file cald cach_dependency_main()
save the file
then remove the # from this line and save the file again.
After this the aplication should apear on your local host webpage
###### Anova rendering bug
with multivariate anova if les then 2 factors are selected or there are less then 2 options selected from the widget box the 
multivariate will not render properly without giving you a waring to fix this have atliest 2 options selected in both the widget box and the factor box.
###### 2 box/bar plots
Becouse of an interaction between 2 of the chosen modules for this aplication panel and seaborn facit wrapping was not posible so there for was chosen to do 2 boxplots on both year and snede as a placeholder.

#### Contact
For contact please contact the hanze univeristy ILST department for references 
For orininal data gathering refrences please contact Fenna Feenstra
For coding based information contact Ivar Lottman

#### Honerary mentions
Michiel Noback for helping with visualisation choices and bugfixes  
Bart Barnard for helping with bugfixes and statistics  
Loes Oldhoff for helping with bugfixes  