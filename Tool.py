import os
import os.path
import shutil
import time

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
acclist1 = ["3110201", "3110202", "3110203", "3110204", "3110205"]
acclist2 = ["3110206", "3110207", "3110211", "3110212"]
acccostlist = ["4111002", "4111003", "4111099", "4112002", "4112003", "4120301", "4120302", "4120102", "4120106",
               "4120107"]
acclist3 = ["4110105", "4110101", "4120101", "4110107"]
accCR60 = {"4350301", "4350302",
           "4350601", "4350602", "4350603", "4350604",
           "4350701", "4350702", "4350703", "4350704", "4350705", "4350706",
           "4350801", "4350802", "4350803", "4350804", "4350805",
           "4324103", "4324107", "4324108",
           "4350901",
           "4351001", "4351002", "4351003", "4351004", "4351051", "4351052", "4351053",
           "4351211", "4351212", "4351213", "4351202", "4351203", "4351204", "4351207", "4351208",
           "4351251", "4351252", "4351253",
           "4324105", "4350102", "4341101", "4341102",
           "4315101", "4311101", "4311102", "4311103", "4311104",
           "4312101", "4312102", "4312131", "4312132", "4312133", "4312104", "4312105", "4312106", "4312107",
           "4313101", "4314101", "4314102", "4314103", "4314104", "4314105", "4314106",
           "4311103", "4351101", "4351102",
           "4350521", "4350522", "4350523", "4350524", "4350525",
           "4350401", "4350402", "4350406", "4350403", "4350404", "4350405",
           "4350501", "4350503",
           "4350201", "4350202", "4350203",
           "4110102", "4110201", "4110202", "4110202", "4110203", "4110204", "4110299", "4110103", "4110104",
           "4350111", "4350112", "4350113",
           "4360101", "4360102", "4360103", "4360104", "4360105",
           "4360201", "4360202", "4360203", "4360204", "4360205",
           "4360301", "4360302", "4360303", "4360304", "4360305"
           }
# End prepeared structures
# In future, find another way to do this


# Functions
def convert(filename):
    """
    Function for convert .jlf in .txt (UTF-8) or .txt to .jlf. Target file will be a copy of source with new format
    :param filename: path to journal in .jlf or .txt format
    :return: path to journal in .txt or .jlf format
    """
    # Разделяем путь и имя файла
    (path, source_name) = os.path.split(filename)
    target_name = ''
    if source_name[-3:] == "jlf":
        target_name = source_name[:-3] + "txt"
    elif source_name[-3:] == "txt":
        target_name = source_name[:-3] + "jlf"
    new = os.path.join(path, target_name)
    shutil.copy(filename, new)
    return new


def acc3110101(sourceline):
    """
    Function for mapping lines with account 3110101
    :param sourceline: Line from journal with account 3110101
    :return: Mapped line as string
    """
    sline = sourceline
    prod_arr = ['PR_20', 'PR_67', "PR_17", "[None]"]
    PR_01020304070813 = ["PR_01", "PR_02", "PR_03"] + PR_04 + PR_07 + PR_08 + PR_13
    PR_0203070813 = ["PR_02", "PR_03"]+ PR_07 + PR_08 + PR_13
    # index of dimensions
    prod_i = 2
    acc_i = 0
    mkt_i = 4
    cost_i = 7
    if len(sline) == 13:
        prod_i = 3
        acc_i = 1
        mkt_i = 5
        cost_i = 8

    if sline[prod_i] in prod_arr:  # Line 2-8
            sline[acc_i] = "3110001"
    elif sline[prod_i] in PR_01020304070813 and sline[mkt_i] in MK_03:  # Line 9-12
            sline[acc_i] = "3110001"
    elif sline[prod_i] in PR_01020304070813 and sline[mkt_i] in MK09:  # Line 18-41
        if sline[cost_i] in ["PP_02", "PP_03", "PP_04"]:
            sline[acc_i] = "3110111"
        else:
            if sline[prod_i] == "PR_01":
                sline[acc_i] = "3110124"
            elif sline[prod_i] in PR_0203070813:
                sline[acc_i] = "3110121"
            elif sline[prod_i] in PR_04:
                sline[acc_i] = "3110122"
    elif sline[prod_i] in ["PR_15", "PR_19"]:  # Line 47, 49
        sline[acc_i] = "3110312"
        sline[prod_i] = "PR_01"
    elif sline[prod_i] == "PR_16":  # Line 48
        sline[acc_i] = "3110313"
        sline[prod_i] = "PR_02"
    elif sline[prod_i] in PR_18:  # Line 54
        sline[acc_i] = "3110402"
        sline[prod_i] = "PR_01"
    sline[cost_i] = "[None]"

    return ";".join(sline) + '\n'


def acc1conv(sourceline):
    """
    Function for mapping lines with accounts "3110201", "3110202", "3110203", "3110204", "3110205"
    :param sourceline: Line from journal with accounts "3110201", "3110202", "3110203", "3110204", "3110205"
    :return: Mapped line as string
    """
    sline = sourceline
    mkt_i = 4
    acc_i = 0
    cost_i = 7
    if len(sline) == 13:
        mkt_i = 5
        acc_i = 1
        cost_i = 8

    if sline[mkt_i] in MK_03:  # Line 13-17
        sline[acc_i] = "3110001"
    else:
        if sline[acc_i] == "3110201":
            sline[acc_i] = "3110122"
        elif sline[acc_i] == "3110204":
            sline[acc_i] = "3110125"
        else:
            sline[acc_i] = "3110124"
    sline[cost_i] = "[None]"
    return ";".join(sline) + '\n'


def acc2conv(sourceline):
    """
    Function for mapping lines with accounts "3110206", "3110207", "3110211", "3110212"
    :param sourceline: Line from journal with accounts "3110206", "3110207", "3110211", "3110212"
    :return: Mappend line as string
    """
    sline = sourceline
    acc_i = 0
    prod_i = 2
    cost_i = 7

    if len(sline) == 13:
        acc_i = 1
        prod_i = 3
        cost_i = 8

    if sline[acc_i] == "3110206":  # Line 50-52
        if sline[prod_i] in ["PR_15", "PR_19"]:
            sline[acc_i] = "3110312"
            sline[prod_i] = "PR_01"
        if sline[prod_i] == "PR_16":
            sline[acc_i] = "3110313"
            sline[prod_i] = "PR_02"
    elif sline[acc_i] == "3110207":
        if sline[prod_i] == "PR_15":
            sline[acc_i] = "3110311"
            sline[prod_i] = "PR_01"
        elif sline[prod_i] in PR_18:
            sline[acc_i] = "3110402"
            sline[prod_i] = "PR_05"
    elif sline[acc_i] == "3110211" and sline[prod_i] in PR_18:
        sline[acc_i] = "3110401"
        sline[prod_i] = "PR_01"
    elif sline[acc_i] == "3110212" and sline[prod_i] in PR_18:
        sline[acc_i] = "3110402"
        sline[prod_i] = "PR_01"
    sline[cost_i] = "[None]"
    return ";".join(sline) + '\n'


def cost(sourceline):
    sline = sourceline
    acc_i = 0
    prod_i = 2
    if len(sline) == 13:
        acc_i = 1
        prod_i = 3
    if sline[acc_i] in ["4111002", "4111003"] and sline[prod_i] in PR_18:  # Line 59-60
        sline[prod_i] = "PR_01"
    elif sline[acc_i] == "4111099" and sline[prod_i] in PR_18:  # Line 61
        sline[acc_i] = "4111003"
        sline[prod_i] = "PR_05"
    elif sline[acc_i] == "4112002" and sline[prod_i] == "PR_15":  # Line 62
        sline[prod_i] = "PR_01"
    elif sline[acc_i] == "4112003":
        if sline[prod_i] in ["PR_15", "PR_19"]:  # Line 63, 65
            sline[prod_i] = "PR_01"
        elif sline[prod_i] == "PR_16":  # Line 64
            sline[acc_i] = "4112004"
            sline[prod_i] = "PR_02"
    elif sline[acc_i] == "4120301" and sline[prod_i] in PR_18:  # Line 66
        sline[acc_i] = "4111002"
        sline[prod_i] = "PR_01"
    elif sline[acc_i] == "4120302" and sline[prod_i] in PR_18:  # Line 67
        sline[acc_i] = "4111003"
        sline[prod_i] = "PR_01"
    elif sline[acc_i] == "4120106":  # Line 69
        sline[acc_i] = "4110106"
    elif sline[acc_i] == "4120107":  # Line 70
        sline[acc_i] = "4110107"

    return ";".join(sline) + "\n"


def acc3conv(sourceline):
    sline = sourceline
    pr = PR_18 + ["PR_15", "PR_19"]
    if len(sline) == 12:  # Lines 74-87
        if sline[0] == "4120101":
            sline[0] = "4110101"
        if sline[2] in pr:
            sline[2] = "PR_01"
        elif sline[2] == "PR_16":
            sline[2] = "PR_02"
    if len(sline) == 13:
        if sline[1] == "4120101":
            sline[1] = "4110101"
        if sline[3] in pr:
            sline[3] = "PR_01"
        elif sline[3] == "PR_16":
            sline[3] = "PR_02"
    return ";".join(sline) + "\n"


def acccr60(sourceline):
    sline = sourceline
    if len(sline) == 12:
        if sline[7] == "[None]":
            sline[7] = "CC10"
    elif len(sline) == 13:
        if sline[8] == "[None]":
            sline[8] = "CC10"
    return ";".join(sline)+"\n"

# Get name Journal and check name

sourcejournal = input("Enter name for source journal - ")+".jlf"
while not os.path.isfile(sourcejournal):
    print("Not file in directory with name " + sourcejournal)
    sourcejournal = input("Enter name for source joutnal - ")+".jlf"
sourcejournal = os.path.normpath(os.getcwd() + '//' + sourcejournal)
sourceconverted = convert(sourcejournal)

# Create tagret file and log
convertName = input("Enter name for converted file - ") + '.txt'
convertPath = os.path.normpath(os.getcwd() + '//' + convertName)

convertedJournals = open(convertName, 'w', encoding="utf-8")
log = open('logs.txt', 'w', encoding="utf-8")

# Open converted into txt journal
starttime = time.time()
with open(sourceconverted, 'r') as journal:
    for line in journal:
        if line.isspace():
            convertedJournals.write(line)
        elif line.startswith("!"):
            convertedJournals.write(line)
            if line.startswith("!JOURNAL") or line.startswith("!Period"):
                log.write(line + '\n')
        else:
            splline = line.strip().split(";")  # init variable to store splited line
            if len(splline) == 12:
                acc_index = 0
            elif len(splline) == 13:
                acc_index = 1
            if splline[acc_index] == "3110101":
                line = acc3110101(splline)
            elif splline[acc_index] in acclist1:
                line = acc1conv(splline)
            elif splline[acc_index] in acclist2:
                line = acc2conv(splline)
            elif splline[acc_index] in acccostlist:
                line = cost(splline)
            elif splline[acc_index] in acclist3:
                line = acc3conv(splline)
            elif splline[acc_index] in accCR60:
                line = acccr60(splline)
            convertedJournals.write(line)  # Write line to target .txt file
convertedJournals.close()
targetJournal = convert(convertPath)
if os.path.isfile(targetJournal):
    os.remove(convertPath)
os.remove(sourceconverted)
log.close()

print("Done! Time is - {:.3f}".format(time.time() - starttime))
