import os
import os.path
import shutil


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


def getfoldername(workdir):
    folder_name = input("Enter folder name: ")
    while not os.path.isdir(os.path.join(workdir, folder_name)):
        print("No such directory. Please try again\n")
        folder_name = input("Enter folder name: ")
    return folder_name


def getfilesnames(pathtofolder):
    files_dict = {}
    for folder in os.listdir(pathtofolder):
        if os.path.isdir(os.path.join(pathtofolder, folder)):
            path_to_folder_year = os.path.join(pathtofolder, folder)
            files_list = os.listdir(path_to_folder_year)
            files_dict.update({path_to_folder_year: files_list})
    return files_dict


work_dir = os.getcwd()    # Working directory
foldername = getfoldername(work_dir)    # Folder with journals
files = getfilesnames(os.path.join(work_dir, foldername))    # Dict with all journals

# how to get path to journal file in folder
for folder in files.keys():
    for file in files[folder]:
        print(os.path.join(folder, file))

targetfolder = "Mapped"
if targetfolder not in os.listdir(work_dir):
    os.mkdir(os.path.join(work_dir, targetfolder))

