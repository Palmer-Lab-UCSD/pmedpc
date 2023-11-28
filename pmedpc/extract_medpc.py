#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import os
from datetime import datetime

class MedPC: 
    def __init__(self, files: list): 
        print("INITIALIZING MEDPC DF OBJECT")
        self.files = files
        self.raw = pd.DataFrame()
        self.raw_filename = ""
        self.subjects = pd.DataFrame()
        self.subjects_filename = ""
    def getFiles(self): 
        return self.files
    def getRaw(self): 
        return self.raw
    def getSubjects(self): 
        return self.subjects
    def save_raw(self, filename): 
        self.raw.to_csv(filename, index = False)
        self.raw_filename = filename
        print("self.raw saved to " + self.raw_filename)
        return 
    def save_subjects(self, filename): 
        self.subjects.to_csv(filename, index = False)
        self.subjects_filename = filename
        print("self.subjects saved to " + self.raw_filename)
        return 
    def medpc_to_df(self): 
        print("CONVERTING MEDPC TO DF")
        files = self.files
        
        data = pd.DataFrame()
        for file in files: 
            print(file)
            with open(file, errors = "ignore") as f: 
                lines = f.readlines()

            key = ""
            value = ""
            dictionary = {}
            first = True
            array_found = False
            subject_num = 0

            for line in lines: 
                line = line.replace("\n", "")
                if ":" not in line: 
                    continue
                elif "File:" in line: 
                    continue

                elif "Start Date:" in line and first: 
                    key = line.split(":")[0]
                    # False: values should be strings
                    value = get_line(line, False)
                    dictionary[key] = value
                    first = False
                    key = ""
                    value = ""

                # if start date of next animal found, add previous animal to df
                elif "Start Date:" in line: 
                    # adding previous last variable
                    dictionary[key] = value
                    dictionary["file"] = file
                    dictionary["subject_num"] = subject_num
                    if data.shape[0] == 0: 
                        data = pd.DataFrame(columns = list(dictionary.keys()))
                    for k in dictionary.keys(): 
                        if k not in list(data.columns): 
                            data[k] = ""
                    # data = pd.concat([data, pd.DataFrame(dictionary)], ignore_index = True)
                    data = data.append(dictionary, ignore_index = True)
                    subject_num += 1

                    dictionary = {}
                    key = line.split(":")[0]
                    # False: values should be strings
                    value = get_line(line, False)
                    dictionary[key] = value
                    first = False
                    key = ""
                    value = ""

                # if line is array
                elif line[0] == " ": 
                    array_found = True
                    # True: values should be floats
                    value.extend(get_line(line, True))

                # if variable is a covariate (date, subject, etc)
                elif len(line.split(":")[0]) != 1: 
                    key = line.split(":")[0]
                    # False: values should be strings
                    value = get_line(line, False)
                    dictionary[key] = value
                    key = ""
                    value = ""

                # for first line that's not covariate
                else: 
                    # if next first line found, previous array is added
                    if array_found: 
                        dictionary[key] = value
                        key = ""
                        value = ""
                    array_found = False
                    key = line[:line.index(":")]
                    value = get_line(line, True)
                    if len(value) == 1: 
                        dictionary[key] = value[0]
                        key = ""
                        value = ""

            # adding last subject after file is closed
            if dictionary != {}: 
                dictionary["file"] = file
                dictionary["subject_num"] = subject_num
                if data.shape[0] == 0: 
                    data = pd.DataFrame(columns = list(dictionary.keys()))
                for k in dictionary.keys(): 
                    if k not in list(data.columns): 
                        data[k] = ""
                # data = pd.concat([data, pd.DataFrame(dictionary)], ignore_index = True)
                data = data.append(dictionary, ignore_index = True)

        # Fixing columns
        columns = list(data.columns)
        for c in range(len(columns)): 
            columns[c] = columns[c].lower().replace(" ", "_")
        data.columns = columns
        if "" in list(data.columns): 
            del data[""]
        
        data.index = range(data.shape[0])
        self.raw = data

# Getting list of filenames in raw data folder
def get_files(folder): 
    files = []
    queue = [folder + "/" + val for val in os.listdir(folder)]
    while len(queue) > 0: 
        file = queue.pop()
        if os.path.isfile(file): 
            files.append(file)
        else: 
            queue.extend([file + "/" + val for val in os.listdir(file)])
    return files

# Converting line into string or list of floats
def get_line(line, is_float): 
    array = []
    # If string
    if not is_float: 
        array = line[line.index(":") + 2:]
        return array
    # If list of floats
    temp = line.split(":")[-1].split(" ")
    for val in temp: 
        val = val.replace(",", ".")
        if val == "": 
            continue
        else: 
            array.append(float(val))
    return array

def get_timestamp(): 
    return str(datetime.now()).split(".")[0].replace(" ", "_").replace(":", "-")

def get_range(array, lower, upper): 
    values = []
    for val in array: 
        if val >= lower and val < upper: 
            values.append(val)
    return values
