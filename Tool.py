import json
import os, os.path
import time
import shutil
import re

# todo add function to mapping lines 59-87
# todo create mappings for accounts from CR60

# Structures in HFM
# MovProd
PR_07 = ["PR_" + str(x) for x in range(28, 67) if x not in [28, 37, 42, 46, 53, 59]]
PR_04 = ["PR_05", "PR_06"]
PR_08 = ["PR_09", "PR_10", "PR_11", "PR_12"]
PR_14 = ["PR_15", "PR_16", "PR_19"]
PR_18 = ["PR_21", "PR_22"]
PR_13 = ["PR_23", "PR_24", "PR_25", "PR_26", "PR_27"]

# MktOvr
MK09 = ['[None]', 'MK_01', 'MK_02', 'MK_13', 'MK_14', 'MK_16', 'MK_17']
MK_03 = ['MK_04', 'MK_05', 'MK_06', 'MK_07', 'MK_08']

# Accounts
acc1 = ["3110201", "3110202", "3110203", "3110204", "3110205"]
acc2 = ["3110206", "3110207", "3110211", "3110212"]


# End prepeared structures
# In future, find another way to do this

# Functions
def convert(filename):
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


def acc3110101(sourceline):
    """

    :param sourceline: Line from journal with account 3110101
    :return: Mapped line as string
    """
    sline = sourceline
    prod_arr = PR_07 + PR_08 + PR_13 + ['PR_20', 'PR_67', "PR_17", "[None]"]
    PR_01020304 = ["PR_01", "PR_02", "PR_03"] + PR_04
    if len(sline) == 12:
        if sline[2] in prod_arr:  # Line 2-8
            sline[0] = "3110001"
        elif sline[2] in PR_01020304 and sline[4] in MK_03:  # Line 9-12
            sline[0] = "3110001"
        elif sline[2] in PR_01020304 and sline[4] in MK09:  # Line 18-41
            if sline[7] in ["PP_02", "PP_03", "PP_04"]:
                sline[0] = "3110111"
            else:
                if sline[2] == "PR_01":
                    sline[0] = "3110124"
                elif sline[2] in ["PR_02", "PR_03"]:
                    sline[0] = "3110121"
                elif sline[2] in PR_04:
                    sline[0] = "3110122"
        elif sline[2] in ["PR_15", "PR_19"]:  # Line 47, 49
            sline[0] = "3110312"
            sline[2] = "PR_01"
        elif sline[2] == "PR_16":  # Line 48
            sline[0] = "3110313"
            sline[2] = "PR_02"
        elif sline[2] in PR_18:  # Line 54
            sline[0] = "3110402"
            sline[2] = "PR_01"
        sline[7] = "[None]"

    if len(sline) == 13:
        if sline[3] in prod_arr:
            sline[1] = "3110001"
        elif sline[3] in PR_01020304 and sline[5] in MK_03:  # Line 9-12
            sline[1] = "3110001"
        elif sline[3] in PR_01020304 and sline[5] in MK09:  # Line 18-41
            if sline[8] in ["PP_02", "PP_03", "PP_04"]:
                sline[1] = "3110111"
            else:
                if sline[3] == "PR_01":
                    sline[1] = "3110124"
                elif sline[3] in ["PR_02", "PR_03"]:
                    sline[1] = "3110121"
                elif sline[3] in PR_04:
                    sline[1] = "3110122"
        elif sline[3] in ["PR_15", "PR_19"]:  # Line 47, 49
            sline[1] = "3110312"
            sline[3] = "PR_01"
        elif sline[3] == "PR_16":  # Line 48
            sline[1] = "3110313"
            sline[3] = "PR_02"
        elif sline[3] in PR_18:  # Line 54
            sline[1] = "3110402"
            sline[3] = "PR_01"
        sline[8] = "[None]"

    return ";".join(sline) + '\n'


def acc1conv(sourceline):
    """

    :param sourceline: Line from journal with accounts "3110201", "3110202", "3110203", "3110204", "3110205"
    :return: Mapped line as string
    """
    sline = sourceline
    if len(sline) == 12:
        if sline[4] in MK_03:  # Line 13-17
            sline[0] = "3110001"
        else:
            if sline[0] == "3110201":
                sline[0] = "3110122"
            elif sline[0] == "3110204":
                sline[0] = "3110125"
            else:
                sline[0] = "3110124"
        sline[7] = "[None]"

    elif len(sline) == 13:
        if sline[5] in MK_03:  # Line 13-17
            sline[1] = "3110001"
        else:
            if sline[1] == "3110201":
                sline[1] = "3110122"
            elif sline[1] == "3110204":
                sline[1] = "3110125"
            else:
                sline[1] = "3110124"
        sline[8] = "[None]"

    return ";".join(sline) + '\n'


def acc2conv(sourceline):
    """

    :param sourceline: Line from journal with accounts "3110206", "3110207", "3110211", "3110212"
    :return: Mappend line as string
    """
    sline = sourceline
    if len(sline) == 12:
        if sline[0] == "3110206":  # Line 50-52
            if sline[2] in ["PR_15", "PR_19"]:
                sline[0] = "3110312"
                sline[2] = "PR_01"
            if sline[2] == "PR_16":
                sline[0] = "3110313"
                sline[2] = "PR_02"
        elif sline[0] == "3110207":
            if sline[2] == "PR_15":
                sline[0] = "3110311"
                sline[2] = "PR_01"
            elif sline[2] in PR_18:
                sline[0] = "3110402"
                sline[2] = "PR_05"
        elif sline[0] == "3110211" and sline[2] in PR_18:
            sline[0] = "3110401"
            sline[2] = "PR_01"
        elif sline[0] == "3110212" and sline[2] in PR_18:
            sline[0] = "3110402"
            sline[2] = "PR_01"
        sline[7] = "[None]"
    if len(sline) == 13:
        if sline[1] == "3110206":  # Line 50-52
            if sline[3] in ["PR_15", "PR_19"]:
                sline[1] = "3110312"
                sline[3] = "PR_01"
            if sline[3] == "PR_16":
                sline[1] = "3110313"
                sline[3] = "PR_02"
        elif sline[1] == "3110207":
            if sline[3] == "PR_15":
                sline[1] = "3110311"
                sline[3] = "PR_01"
            elif sline[3] in PR_18:
                sline[1] = "3110402"
                sline[3] = "PR_05"
        elif sline[1] == "3110211" and sline[3] in PR_18:
            sline[1] = "3110401"
            sline[3] = "PR_01"
        elif sline[1] == "3110212" and sline[3] in PR_18:
            sline[1] = "3110402"
            sline[3] = "PR_01"
        sline[8] = "[None]"
    return ";".join(sline) + '\n'


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
while not os.path.isfile(sourcejournal):
    print("Not file in directory with name " + sourcejournal)
    sourcejournal = input("Enter name for source joutnal - ")+".jlf"
"""

# Create tagret file and log
convertName = input("Enter name for converted file - ") + '.txt'
convertedJournals = open(convertName, 'w', encoding="utf-8")
log = open('logs.txt', 'w', encoding="utf-8")

# Open converted into txt journal
starttime = time.time()
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

