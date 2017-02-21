import json
import os, os.path
import time
import shutil
import re

starttime = time.time()
# Structures in HFM
# MovProd
PR_07 = ["PR_"+str(x) for x in range(28, 67) if x not in [28, 37, 42, 46, 53, 59]]
PR_04 = ["PR_05", "PR_06"]
PR_08 = ["PR_09", "PR_10", "PR_11", "PR_12"]
PR_14 = ["PR_15", "PR_16", "PR_19"]
PR_18 = ["PR_21", "PR_22"]
PR_13 = ["PR_23", "PR_24", "PR_25", "PR_26", "PR_27"]

# MktOvr
MK_09 = ['[None]', 'MK_01', 'MK_02', 'MK_13', 'MK_14', 'MK_16', 'MK_17']
MK_03 = ['MK_04', 'MK_05', 'MK_06', 'MK_07', 'MK_08']

# Accounts
acc1 = ["3110201", "3110202", "3110203", "3110204", "3110205"]
acc2 = ["3110206", "3110207", "3110211", "3110212"]

# End prepeared structures
# In future, find another way to do this

# Functions
def convert (filename):
    """
    Function for convert .jlf in .txt (UTF-8)
    :param filename: path to journal in .jlf format
    :return: path to journal in .txt format
    """
    # Разделяем путь и имя файла
    (path, jlf_name) = os.path.split(filename)
    txt_name = jlf_name[:-3] + "txt"
    new = os.path.join(path, txt_name)
    shutil.copy(filename, new)
    return new


def acc3110101(sline):
    sline = ";".join(sline)
    return "{0}  CONVERTED by acc3110101+\n".format(sline)


def acc1conv(sline):
    sline = ";".join(sline)
    return "{0}  CONVERTED by acc1conv+\n".format(sline)


def acc2conv(sline):
    sline = ";".join(sline)
    return "{0}  CONVERTED by acc2conv+\n".format(sline)

# Read easy accounts
"""
with open("Mapping.json", "r", encoding="utf-8") as file:
    alldict = json.load(file)
    mappings = alldict["Mappings"]
"""
# Get name Journal and check name
"""
sourcejournal = input("Enter name for source journal - ")+".jlf"
sourcejournal = os.path.normpath(os.getcwd()+'//'+sourcejournal)
print (sourcejournal)
while not os.path.isfile(sourcejournal):
    print("Not file in directory with name " + sourcejournal)
    sourcejournal = input("Enter name for source joutnal - ")+".jlf"
"""

# Create tagret file and log
convertName = input("Enter name for converted file - ")+'.txt'
convertedJournals = open(convertName, 'w', encoding="utf-8")
log = open('logs.txt', 'w', encoding="utf-8")

# Open converted into txt journal
with open("GRSHFM_Journal.txt", 'r', encoding="utf-8") as journal:
    for line in journal:
        if line.isspace():
            convertedJournals.write(line)
        elif line.startswith("!"):
            convertedJournals.write(line)
            if line.startswith("!JOURNAL") or line.startswith("!Period"):
                log.write(line + '\n')
        else:
            splline = line.strip().split(";")  # init variable to store splited line
            if splline[0].isdigit():
                if splline[0] == "3110101":
                    line = acc3110101(splline)
                elif splline[0] in acc1:
                    line = acc1conv(splline)
                elif splline[0] in acc2:
                    line = acc2conv(splline)
            elif not splline[0].isdigit():
                if splline[1] == "3110101":
                    line = acc3110101(splline)
                elif splline[1] in acc1:
                    line = acc1conv(splline)
                elif splline[1] in acc2:
                    line = acc2conv(splline)
            convertedJournals.write(line)
convertedJournals.close()
log.close()

print("Done! Time is - {:.3f}".format(time.time() - starttime))




