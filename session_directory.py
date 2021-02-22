# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 09:23:20 2018

@author: William Mau
"""

from os import path, chdir, environ
from pickle import load
from csv import DictReader
from pickle import dump
from helper_functions import find_dict_index as fd
import numpy as np
import re
from pathlib import Path

# Grab computer name to identify proper session directory location
comp_name = environ['COMPUTERNAME']
if comp_name == 'NATLAPTOP':
    master_directory = 'C:\Eraser\SessionDirectories'
elif comp_name == 'NORVAL' or comp_name == 'CAS-2CUMM202-02' or comp_name == 'RKC-HAS-WD-0005':
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
                                        "Location": Path(entry['Location']),
                                        "Session": entry['Session'],
                                        "Notes": entry['Notes']})

    # Save.
    with open('SessionDirectories.pkl', 'wb') as output:
        dump(session_directories, output)

    return session_directories


def load_session_list(dir_use=master_directory):

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


def find_mouse_directory(mouse, list_dir=master_directory):
    session_list = load_session_list(list_dir)

    # Seems really inefficient but functional for now. Searches the directory containing that
    # mouse's data folders.
    mouse_not_found = True
    while mouse_not_found:
        for session in session_list:
            if session["Animal"] == mouse:
                mouse_directory = path.split(session["Location"])[0]
                mouse_not_found = False
                break
        # Break out of while loop once you've made it through all the sessions
        mouse_not_found = False
        mouse_directory = None

    return mouse_directory


def find_session_directory(mouse, date, sesh, list_dir=master_directory):
    session_list = load_session_list(list_dir)

    session_directory = None
    for session in session_list:
        if session["Animal"] == mouse and session["Date"] == date and \
                session["Session"] == str(sesh):
            session_directory = session["Location"]
            break

    return session_directory


def find_eraser_directory(mouse, arena, exp_day, list_dir=master_directory):
    """
        Pulls the working directory for Eraser mice based on mouse name, arena type, and exposure day

        :param

        :return
            session_directory: working directory for mouse/arena/exposure day
        """
    session_list = load_session_list(list_dir)

    # Construct regular expression to grab proper day
    import re
    daystr = ' +' + str(exp_day)
    dayreg = re.compile(daystr)

    # Loop through all sessions and check if mouse, arena, and exp_day all match
    session_directory = None  # Spit out None if no match is found
    for session in session_list:
        if session["Animal"] == mouse and session["Notes"].find(arena) != -1 and \
                dayreg.search(session["Notes"]) is not None:

            session_directory = session["Location"]
            break

    return session_directory


def find_eraser_session(mouse, arena, exp_day, list_dir=master_directory):
    """
        Pulls the session info for Eraser mice based on mouse name, arena type, and exposure day

        :param

        :return
            session_use: all session info for mouse/arena/exposure day
        """
    assert isinstance(exp_day, int), "exp_day is not of type int"
    session_list = load_session_list(list_dir)

    # Construct regular expression to grab proper day
    import re
    daystr = ' +' + str(exp_day)
    dayreg = re.compile(daystr)

    # Loop through all sessions and check if mouse, arena, and exp_day all match
    session_use = None  # Spit out None if no match is found
    for session in session_list:
        if session["Animal"] == mouse and session["Notes"].find(arena) != -1 and \
                dayreg.search(session["Notes"]) is not None:

            session_use = session
            break

    return session_use


def find_mouse_sessions(mouse):
    session_list = load_session_list()

    filtered = filter(lambda sessions: sessions["Animal"] == mouse,
                      session_list)
    sessions = list(filtered)

    idx = np.asarray(fd(session_list, "Animal", mouse))

    return idx, sessions


def fix_slash_date(date_use):
    """
    Sends dates in m/d/yyyy format to mm_dd_yyyy format
    :param date_use: date in m/d/yyyy format (day an month can be 1-2 digits, year must be 4)
    :return: u_date: date string in mm_dd_yyyy format
    """

    datereg = re.compile('/')  # regular expression to find all front slashes
    slashmatch = datereg.finditer(date_use)  # Match all slashes, spit out iterator
    slash1 = next(slashmatch)  # Get first iteration
    mo = str.zfill(date_use[0:slash1.regs[0][0]], 2)  # find month num and fill in leading zero
    slash2 = next(slashmatch)
    day = str.zfill(date_use[slash1.regs[0][1]:slash2.regs[0][0]], 2)
    year = date_use[slash2.regs[0][1]:]
    u_date = mo + '_' + day + '_' + year

    return u_date


if __name__ == '__main__':
    find_eraser_directory('ANI1test', 'Open', '1 hour')
    pass

