## README ------------------------------------------------------------------------------


        # ###     INITIAL SETUP    #########################################################################

        #  This is a python script used to generate graphs from specified data sets in an Excel file.
        
        #  The prerequisites for running the script are to install >= Python 3 and the following modules:
        #         pandas
        #         openpyxl
        #         matplotlib
        #         numpy
        #         configparser
        #         str2bool

        #  To do so, open a bash/terminal/command prompt and check that Python is properly installed by running
        #     "python3 --version" and
        #     "pip3 --version"
        
        #  If both these commands run successfully, then you are ready to move onto the next step.
        #  To install the modules, run the following command for each of them:
        #     "pip3 install *module name*"

        #  Note: verify that the dates in the Excel sheet are in the proper D/M/YYYY format. The data for that 
        #  row may not be imported properly if the date is not formatted correctly. If any surveys are collected
        #  over the period of multiple days, please estimate to the closest SINGLE date.    
            
            
        # ###     RUNNING THE SCRIPT    ######################################################################
        
        #  To begin running the script, place the 3 required files in the same folder - config.ini,
        #  data_to_graphv2.py, and the Excel file.
        
        #  Open a bash/terminal/command prompt and navigate to the folder containing the files (in some systems,
        #  you can right click inside the folder and select "open terminal here")
        
        #  Update the config.ini file with the desired data set. The important options are to set the spreadsheet
        #  name, the sheet name, and the start and end columns of data. ***note that names are case sensitive.
        
        #  Then you can run the following command in your bash/terminal/command prompt:
        #     "python3 data_to_graphv2.py"
            
        #  It will save the graphs to a PNG image file in a new folder labeled 'Graphs'.






## DEPENDENCIES ------------------------------------------------------------------------

# The following packages need to be installed before this script can run
# pandas
# openpyxl
# matplotlib
# numpy
# configparser
# str2bool

import pandas
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os
from configparser import ConfigParser
from str2bool import str2bool


## INITIAL CONDITIONS ------------------------------------------------------------------

config_object = ConfigParser()
config_object.read("config.ini")
# read from config file for initial conditions

spreadsheet_data = config_object["SPREADSHEET DATA"]
spreadsheet_name = spreadsheet_data["spreadsheet_name"]
sheet_name = spreadsheet_data["sheet_name"]
# specify the excel file you want to use
# choose which page of the excel sheet to analyze
# ***both names are case sensitive***

data_column_start = spreadsheet_data["data_column_start"]
data_column_end = spreadsheet_data["data_column_end"]
# choose the subset of data to analyze
# input as excel columns (e.g. "A" or "B") the start and end of the subset
# for best results, start with a data column that contains the phylum name

dates_column = spreadsheet_data["dates_column"]
# the dates column shouldn't change, but is included here just in case

species_row = int(spreadsheet_data["species_row"])

# specify which row in excel the species names are located on
# this shouldn't change


graph_config = config_object["GRAPH CONFIG"]
barWidth = float(graph_config["barWidth"])
# value between 0 and 1
# represents the thickness of the bars in the graph

figure_width_px = float(graph_config["figure_width_px"])
figure_height_px = float(graph_config["figure_height_px"])
# specify the size of each subplot in pixels

sighting_color = graph_config["sighting_color"]
no_sighting_color = graph_config["no_sighting_color"]
bar_text_color = graph_config["bar_text_color"]
# customize the color of the bar charts
# give values by name
# or by hex color code
# (see https://matplotlib.org/stable/gallery/color/named_colors.html for full list)


specialChars = '\/:*"<>|.'
# characters not allowed to be used in windows filename

## IMPORT EXCEL ------------------------------------------------------------------------

title = pandas.read_excel(spreadsheet_name, sheet_name=sheet_name, \
    usecols= data_column_start, header=0, nrows=0).columns.values[0]
# imports the phylum name of the dataset
# will not import a sensible value if the dataset does not start on 
# the same column as the name

if 'Unnamed' in title:
    title = 'Unspecified Phylum'
# fallback if the title import fails

else:
    for specialChar in specialChars:
        title = title.replace(specialChar, '')
# sanitize title text, remove characters not allowed in Windows filename

print('Imported title...')

df = pandas.read_excel(spreadsheet_name, sheet_name=sheet_name, \
    usecols=dates_column + "," + data_column_start + ":" + \
    data_column_end, header=species_row-1)
# imports the rest of the survey data

for specialChar in specialChars:
    sheet_name = sheet_name.replace(specialChar, '')
# sanitize sheet name, remove characters not allowed in Windows filename
# for use in output file

print('Imported dataset...')





## SANITIZE DATA ---------------------------------------------------------------------

good_rows = df['Date'].astype(str).str.contains('-', regex=False)
# proper datetime is in the format of YYYY-MM-DD 00:00:00
# string match to look for "-" to mark rows as the right format

bad_rows = np.invert(good_rows)
# invert array to get improper rows

rows_to_drop = np.where(bad_rows)[0]
df = df.drop(rows_to_drop)
# take index of bad rows to know which ones to drop
# drop these bad rows from the dataframe

df = df.fillna(0)
# replace empty cells with 0

df['Date'] = pandas.to_datetime(df['Date'])
# convert the date into a datetime object to make it easier to handle




## CREATE PLOTABLE ARRAYS -------------------------------------------------------------

df_count = df['Date'].groupby(df['Date'].dt.year).count()
df_perc = df.groupby(df['Date'].dt.year).mean()
df_perc_inv = 1 - df_perc # element wise subtraction
# groups the data by year and: 
# df_count       keeps track of number of observations per year
# df_perc        counts the % of times observed in that year
# df_perc_inv    also keeps track of % not observed for plotting





## FORMAT AND GENERATE PLOTS -----------------------------------------------------------

px = 1/plt.rcParams['figure.dpi']  # pixel in inches
dynamic_figure_height_px = figure_height_px*len(df_perc.columns)
# dynamically scale the height of the figure based on number of species

fig, axs = plt.subplots(ncols=1, nrows=len(df_perc.columns), sharex=False, \
    figsize=(figure_width_px*px, dynamic_figure_height_px*px))
# initialize the figure with subplots and size


fig.suptitle(t=sheet_name + ": " + title, y = 1-(10/dynamic_figure_height_px), \
    weight='bold')
fig.tight_layout()
# give the figure a title and automatic layout
# title should be 10px from the top

plt.subplots_adjust(left=0.1,
                    bottom=60/dynamic_figure_height_px, 
                    right=0.95, 
                    top=1-(60/dynamic_figure_height_px), 
                    hspace=0.4)
# specify amount of whitespace around figure fractionally (scale from 0 to 1)
# hspace = amount of vertical space between subplots
# ideal top/bottom space = 60px

for i in range(0,len(df_perc.columns)):
    axs[i].bar(x=df_perc.index, height=df_perc[df_perc.columns[i]], \
        width=barWidth, color=sighting_color)
# creates subplots in a loop, one for each species in the dataset
# plots positive sightings

    axs[i].bar(df_perc_inv.index, df_perc_inv[df_perc_inv.columns[i]], \
        bottom=df_perc[df_perc.columns[i]], width=barWidth,\
        color=no_sighting_color)
# adds no sightings to the bar graph in a different color

    axs[i].set_title(str(df_perc.columns[i]))
    axs[i].set_ylabel("% seen")
    axs[i].set_ylim([0, 1])
    axs[i].xaxis.set_major_locator(mtick.MaxNLocator(integer=True))
# add title and label to subplots
# ensure x axis labels only land on whole years

    for j in range(0, len(df_perc.index)):
        annotation = r'$\frac{' + str(int(df_count.iloc[j] * \
            df_perc[df_perc.columns[i]][df_perc.index[j]])) + '}{' + str(df_count.iloc[j]) + '}$'
        axs[i].annotate(xy=(df_perc.index[j], 0.1), \
            text=annotation, ha='center', color=bar_text_color, weight='demi', fontsize='large')
# add the number of sightings per year to the bar graph
# depends on the variable, annotate_successful_sightings

    print('Plotting ' + str(df_perc.columns[i]) + '...')

plt.figtext(x=0.5, y=10/dynamic_figure_height_px, ha='center', color='black',\
    s='***The numbers in the bar chart represent the number of successful sightings per year.')
# footnote to notify reader of how to interpret the bar chart numbers
# text should be 10px from the bottom




## SAVE PLOTS TO FILE AND DISPLAY ------------------------------------------------------

print('Saving image to file...')

if(os.path.isdir('./graphs/') == False):
    os.mkdir('./graphs/')
# check if graphs folder exists
# if not, make it

base_filename = "./graphs/" + sheet_name + " - " + title + " bar graphs"
new_filename = base_filename
extension = ".png"
# generates basic filename based on location and phylum

i = 1
while os.path.isfile(new_filename + extension) == True:
    new_filename = base_filename + " (" + str(i) + ")"
    i += 1
# checks to see if file already exists
# if so, give the new file a (larger) unique number

plt.savefig(new_filename + extension)
# writes the figure to a file

print("Image successfully saved to " + new_filename + extension)