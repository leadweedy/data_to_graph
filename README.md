# data_to_graph.py
Designed for the Center for Alaskan Coastal Studies



###     INITIAL SETUP

 This is a python script used to generate graphs from specified data sets in an Excel file.
 
 The prerequisites for running the script are to install >= Python 3 and the following modules:
 - pandas
 - openpyxl
 - matplotlib
 - numpy
 - configparser
 - str2bool

 To do so, open a bash/terminal/command prompt and check that Python is properly installed by running:
 - python3 --version
 - pip3 --version
 
 If both these commands run successfully, then you are ready to move onto the next step.
 To install the modules, run the following command for each of them:
 - pip3 install *module name*
    
    
 Note: verify that the dates in the Excel sheet are in the proper D/M/YYYY format. The data for that row may 
 not be imported properly if the date is not formatted correctly. If any surveys are collected over the period 
 of multiple days, please estimate to the closest SINGLE date.
    
    
    

    
###     RUNNING THE SCRIPT
 
 To begin running the script, place the 3 required files in the same folder:
 - config.ini
 - data_to_graph.py
 - Excel file.
 
 Open a bash/terminal/command prompt and navigate to the folder containing the files (in some systems, you can right click inside the folder and select "open terminal here")
 
 Update the config.ini file with the desired data set. The important options are to set the spreadsheet name, the sheet name, and the start and end columns of data.
 ***note that names are case sensitive.
 
 Then you can run the following command in your bash/terminal/command prompt:
 - python3 data_to_graph.py
    
 It will save the graphs to a PNG image file in a new folder labeled 'graphs'.
