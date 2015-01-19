__author__ = 'aperritano'

import csv
import os
import shutil
import thread
import threading

from sys import argv
from pprint import pprint
from PIL import Image
from PIL.ExifTags import TAGS

script, file_path = argv
no_folder = "other"
csv_path = "/Users/aperritano/Pictures/sorted/2015/"

file_names = next(os.walk(file_path))[2]

allDicts = {}

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

def copy_file(file_path, file_name, folder_name):
    src =  file_path + "/" + file_name
    dst = file_path + "/" + folder_name + "/"
    shutil.copy(src, dst)

def group_into_folders():

      for file_name in file_names:
        base_name = file_name[0:-4]

        if " " in base_name:
            folder_name = base_name.split()[1]

            make_sure_path_exists(file_path + "/" + folder_name)
            copy_file(file_path, file_name, folder_name)
            # print "found folder" + folder_name

        else:

            make_sure_path_exists(file_path + "/" + no_folder)
            copy_file(file_path, file_name, no_folder)
            # print "found no folder"

def add_to_dict(folder_name, base_name):
    has_dict = allDicts.has_key(folder_name)
    if has_dict:
        folder_list = allDicts[folder_name]
        folder_list.append(base_name)
        #print allDicts
    else:
        new_folder_list = [base_name]
        allDicts[folder_name] = new_folder_list
        #print allDicts

    sorted(allDicts)

def dir_contents(path):

    root_dir = path.split("/")[-1]

    for dirName, subdirList, fileList in os.walk(path):

        d_name = dirName.split("/")[-1]

        if root_dir != d_name:
            print "Found directory dir: " + d_name

            for file_name in fileList:
                if file_name != ".DS_Store":

                    tags = get_exif(dirName + "/" + file_name)

                    add_to_dict(d_name, tags["DateTimeOriginal"])

                    #print "\t" + file_name
    path = file_path +"/" + "output.csv"
    csv_writer(allDicts, path)





def get_exif(file_name):
    ret = {}
    print "EXIF " + file_name
    i = Image.open(file_name)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret


def csv_writer(data, path):

    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow( ('Index', 'Timestamp') )

        for line in data:
            for key in allDicts:
                list_values = allDicts[key]
                for value in list_values:
                    print key + " " + value
                    writer.writerow( (key, value) )



if __name__ == '__main__':

    group_into_folders()

    dir_contents(file_path)
    # Create two threads as follows
    # try:
    #     thread.Thread( dir_contents(file_path), ("Thread-1", 1, ) )
    #
    # except:
    #     print "Error: unable to start thread"
    # while 1:
    #     pass



    pprint(allDicts)

    csv_path = csv_path + "output.csv"

    csv_writer(allDicts, csv_path)


# print os.listdir(filepath)

