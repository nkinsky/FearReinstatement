# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:42:45 2018

@author: William Mau
"""

# Import libraries
from os import chdir, environ
from csv import DictReader
from pickle import dump


# Grab computer name to identify proper session directory location
comp_name = environ['COMPUTERNAME']
if comp_name == 'NATLAPTOP':
    master_directory = 'C:\Eraser\SessionDirectories'
elif comp_name == 'NORVAL' or comp_name == 'CAS-2CUMM202-02':
    master_directory = 'E:\Eraser\SessionDirectories'
# print(master_directory)


def make_session_list(csv_directory=master_directory):

    """
    
    Make a list of recording sessions by reading from an editable CSV found in 
    csv_directory.
    
    """

    # Go to the directory containing the CSV file.
    chdir(csv_directory)

    # Define "structure array". Not going to bother to learn how to preallocate
    # yet; this should only ever be a few entries long per project.
    session_directories = []
    with open('SessionDirectories.csv', 'r') as file:
        reader = DictReader(file)

        # Consolidate entries.
        for entry in reader:
            session_directories.append({"Animal": entry['Animal'],
                                        "Date": entry['Date'],
                                        "Location": entry['Location'],
                                        "Session": entry['Session'],
                                        "Notes": entry['Notes']})

    # Save.
    with open('SessionDirectories.pkl', 'wb') as output:
        dump(session_directories, output)

    return session_directories

if __name__ == '__main__':
    make_session_list('U:\Fear conditioning project_Mosaic2\SessionDirectories')
