## Dependencies
Requires `python3`,`pandas` and `PySimpleGUI` to be installed

## Usage
- run `conditions_viewer.py` script
- navigate to the folder containing screens conditions files using the `Browse` button and select __any__ file from that folder and hit "Open". 
That will trigger the attempt to process __all__ `.csv` files in that folder as screens conditions files 
(please see below the instructions for where and how to download those files). The presence of unrelated `.csv` files in the folder will crash the script.
- select a screen from the dropdown menue
- select the well, and the conditions of that well will be shown in the right column of the app
- close the window when you are done

## Commercial screens conditions files
`.csv` files containing commercial screens conditions compatible for this app can be downloaded from the C6 website (https://c6.csiro.au/login.asp). 
I'd recommend to save all the files in one separate folder.
- log in as a guest 
- select Screens and Stocks -> Screens Lists from the main dropdown menue 
- select "Commercial Screens" as a Group  
- navigate to the desired screen vendor 
- click on the screen name in the table 
- Export the file opened in a new window as "CSV-ROW" (there is a link in the second to the top row of the table)

Feel free to rename the downloaded files

__NB:__ Errors are common during the processing of freshly downloaded screens conditions files. 
Please follow the instructions from the Exception messages for guidance on how to fix the problem (you'll need to open the `.csv` file in a text editor and add several commas at the end of the 6th string)
