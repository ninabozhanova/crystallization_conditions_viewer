#!/usr/bin/env python3

import os
import re
import pandas as pd
import PySimpleGUI as sg

def main():
    ### Variables
    font_style = 'Courier 12 bold'
    
    ### Helper functions
    # Uploading crystallization conditions info from all .csv files in the selected folder
    # and save them in the "screen_library" dictionary 
    def download_screen_info(dir_path, screen_names):
        for screen_name in screen_names:
            try:
                df = pd.read_csv("%s/%s.csv" %(dir_path, screen_name), skiprows = [i for i in range(5) ])
                variable_columns = list(df.columns[2:])
                screen_library[screen_name] = {}
                for i, row in df.iterrows():
                    well_name = row["Well"]
                    screen_library[screen_name][well_name] = {}
                    for column_id in range(int(len(variable_columns)/4.0)):
                        column_name = variable_columns[4 * column_id].strip()
                        if pd.isnull(row[column_name]) == False :
                            screen_library[screen_name][well_name][row[variable_columns[4 * column_id + 2]].strip()] = [
                                row[variable_columns[4 * column_id ]], row[variable_columns[4 * column_id + 1]].strip()]
                            ### pH information, you might decide to handle it differently later!!!
                            if pd.isnull(row[variable_columns[4 * column_id + 3]]) == False :
                                screen_library[screen_name][well_name][row[variable_columns[4 * column_id + 2]].strip()].append(row[variable_columns[4 * column_id + 3]].strip())

            except Exception as e:
                try:
                    error_type = str(e).split(":")[0].strip()
                    error_message = str(e).split(":")[1].strip()
                    # Trying to catch a very common problem and tell how to fix it
                    # An example of the error message that we are looking for:
                    # "pandas.errors.ParserError: Error tokenizing data. C error: Expected 19 fields in line 15, saw 22"
                    if error_type == "Error tokenizing data. C error":
                        numbers_from_error_message = [int(s) for s in re.findall(r'\b\d+\b', error_message)]
                        to_add = numbers_from_error_message[2] - numbers_from_error_message[0]
                        raise Exception("Please open the '%s.csv' file in a text editor and add %s commas to the end of the 6th line to fix the problem" %(screen_name, str(to_add))) from None
                    # Something else is wrong:
                    else:
                        raise Exception("Something is wrong with the '%s.csv' file: %s" %(screen_name, str(e))) from None
                except:
                    raise Exception("Something is wrong with the '%s.csv' file: %s" %(screen_name, str(e))) from None
    
    # Get crystallization conditions of the specific well 
    def get_conditions(name, well):
        out = ""
        condition = screen_library[name][well]
        for compound in condition.keys():
            info_string = str(condition[compound][0]) + " " + condition[compound][1] + " " + compound
            if len(condition[compound]) > 2:
                info_string += ", " + condition[compound][2]
            out += (info_string + "\n")
        return out
    
    ### Window layout in 2 columns
    # Left column
    select_column = [
        [
            sg.Text("Select Folder", font = font_style),
        ],
        [
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FileBrowse(),
        ],
        [
            sg.Text("Select Screen name:"),
        ],   
        [
            sg.Combo(
                values = [], key="-ScreenName-", font = font_style, size=(25, 1), enable_events=True,
            )
        ],
        [
            sg.Text(""),
        ],
    ]
    
    wells = []
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    numbers = [str(x) for x in range(1, 13)]
    for letter in letters:
        for number in numbers:
            wells.append(letter + number)
    
    # Add well buttons
    well_counter = 0      
    for row in range(8):
        select_column.append([])
        for column in range(12):
            select_column[-1].append(sg.Button(wells[well_counter], key = wells[well_counter], size=(3, 1)))
            well_counter += 1
    
    # Right column
    output_column = [
        [sg.Text("Please select any file from a folder containing all screens", font = font_style, key = "-HEADER-")],
        [sg.Text("")],
        [sg.Text(size=(50, 10), key="-OUT-", font = font_style)],
    ]
    
    
    # Full layout
    layout = [
        [
            sg.Column(select_column),
            sg.VSeperator(),
            sg.Column(output_column),
        ]
    ]
    
    ### Create the window
    window = sg.Window("Crystallization Conditions Viewer", layout, margins=(50, 50))
    
    ### The Event loop
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # the user chose a file from a folder -> create a library of all crystallization screens in that folder
        if event == "-FOLDER-":
            screen_library = {}
            file = values["-FOLDER-"]
            dir_path = os.path.dirname(file)
            file_list = os.listdir(dir_path)
            screen_names = []
            for file_name in file_list:
                if file_name[-3:] == "csv":
                    screen_names.append(file_name[:-4])
            download_screen_info(dir_path, screen_names)
            screen_names.sort()
            # Update values in the dropdown menue
            window["-ScreenName-"].update(values = screen_names)
            # Update instructions on the right panel 
            window["-HEADER-"].update("Please select Screen name, Well name, and Well number")
    
        # the user selected Screen name -> update instructions on the right panel        
        if event == "-ScreenName-":
            window["-HEADER-"].update("Please select a well to see the conditions")
            window["-OUT-"].update("")
        
        # the user selects a well -> show conditions of the selected well
        if event in wells:
            if values["-ScreenName-"] != '':
                screen = values["-ScreenName-"]
                window["-OUT-"].update(get_conditions(screen, event))
                window["-HEADER-"].update("%s, %s well conditions:" %(screen, event))
    
            
    window.close()

if __name__ == '__main__':
    main() 
