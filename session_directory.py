# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 09:23:20 2018

@author: William Mau
"""

from os import path, chdir
from pickle import load
from csv import DictReader
from pickle import dump

master_directory = 'E:\Eraser\SessionDirectories'

def make_session_list(csv_directory):
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

def load_session_list(master_directory_custom):
    if master_directory_custom == None:
        dir_use = master_directory
    else:
        dir_use = master_directory_custom

    file = path.join(dir_use, 'SessionDirectories.pkl')
    session_list = load(open(file, 'rb'))

    return session_list

def check_session(session_index):
    """
    Displays all the details of that session as recorded in the CSV file.

    :param
        session_index: number corresponding to a session.
    :return
        Printed session information.
    """
    session_list = load_session_list()

    print("Mouse: " + session_list[session_index]["Animal"])
    print("Date: " + session_list[session_index]["Date"])
    print("Session # that day: " + session_list[session_index]["Session"])
    print("Location: " + session_list[session_index]["Location"])
    print("Notes: " + session_list[session_index]["Notes"])

def find_mouse_directory(mouse):
    session_list = load_session_list()

    # Seems really inefficient but functional for now. Searches the directory containing that
    # mouse's data folders.
    mouse_not_found = True
    while mouse_not_found:
        for session in session_list:
            if session["Animal"] == mouse:
                mouse_directory = path.split(session["Location"])[0]
                mouse_not_found = False
                break

    return mouse_directory


def find_session_directory(mouse,date,sesh):
    session_list = load_session_list()

    sesh_not_found = True
    while sesh_not_found:
        for session in session_list:
            if session["Animal"] == mouse and session["Date"] == date and \
                    session["Session"] == sesh:
                session_directory = session["Location"]
                sesh_not_found = False
                break

    return session_directory

