# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 09:23:20 2018

@author: William Mau
"""

from os import path
from pickle import load

master_directory = 'E:\Eraser\SessionDirectories'

def load_session_list(master_directory_custom):
    if master_directory_custom == None:
        dir_use = master_directory
    else:
        dir_use = master_directory_custom

    file = path.join(dir_use, 'SessionDirectories.pkl')
    session_list = load(open(file, 'rb'))

    return session_list
