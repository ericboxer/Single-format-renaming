# ===============
# File Prep for Storage v 1.0
# Copyright Eric Boxer, 2016
# eric@ericboxer.net
# http://ericboxer.net
# ===============


# ===============
# Usage
# ===============

# This script is designed to batch rename a directory of files. The files will have a leading number follwoed by a space. 
# An optional bit of text may be added between the nubmer and the space before the file name.
# if the file already has a leading number it will be removed.
# The renaming can be undone if a mistake is made.
# Run python fileprep.py -h for help in the command line. 


# ===============
# imports
# ===============

import os, re, argparse, csv


# ===============
# Global Vars
# ===============

csvFileName = "rename.csv"                                                                                  # Rename file.


# ===============
# Commandline Arguments
# ===============

parser = argparse.ArgumentParser(description="Rename files to have a leading number with an optional text insert.")
parser.add_argument('-f', help = "The folder with files to rename.", default = "")
parser.add_argument('-e', help="match particular file extension. Defaults to using .wav", default = "wav")
parser.add_argument('-s', help="What number to start from. Default is 1.", default = 1, type = int)
parser.add_argument('-i', help="The increment value. Deafault is 1.", default = 1, type = int)
parser.add_argument('-l', help="Location this line is used. Will not include if left empty", default = '')
parser.add_argument('-p', help = "How many 0's to pad the leading number with. Default is 3.", default = 3, type = int)
parser.add_argument('-c', help = "By default outputs to the command line only. Set true commit renaming to the directory.", action = "store_true", default = False)
parser.add_argument('-u', help = "In case of dumb.", action = "store_true", default = False)

args = vars(parser.parse_args())


folderToUse = os.path.join(os.path.curdir,args['f'])                                                        # Directory of the files being modified
renameCSVPath = os.path.join(folderToUse,csvFileName)                                                       # Path to the rename file.


# ===============
# Undo in case of Dumb
# ===============

if args['u']:
    if os.path.exists(renameCSVPath):

        f = open(renameCSVPath, mode="rb")

        csvF = csv.reader(f, delimiter = ",")

        for row in csvF:
            os.rename(os.path.join(folderToUse, row[0]),os.path.join(folderToUse, row[1]))
            print("%s renamed back to %s." % (row[0], row[1]))
        f.close()
        print(".::All Files Renamed::.")
        os.remove(renameCSVPath)
        print(".::Undo File Removed For Your Safety::.")
    else:
        print(".::Renaming file doesnt exist. You're SOL::.")
    exit()


# ===============
# Renaming Session Variables
# ===============

dataToCSV = []                                                                                              # Holds the values to write out to the undo.

fleCount = args['s']                                                                                        # Starting number to count from.

if args['l'] == '':                                                                                         # Sets a location in for the filename. If blank dont place anything there.
    locationString = " "
else:
    locationString = " " + args['l'] + " "


# ===============
# Rename the Files
# ===============

for directoryFile in os.listdir(folderToUse):                                                               # Uses the directory the script is in. TODO: update to allow to choose directory.  
    if directoryFile.endswith(args['e']):
        oldName = directoryFile
        newName = str(fleCount).zfill(args['p']) + locationString +(re.sub('^[0-9_ ]*', '', directoryFile)) # Remove leading numbers, spaces, and underscores and then format the name.
        print("%s is now %s" % (oldName, newName))
        if args['c']:                                                                                       # Make the changes permanant. 
            os.rename(os.path.join(folderToUse,oldName), os.path.join(folderToUse, newName))
        dataToCSV.append("%s,%s" % (newName, oldName))
        fleCount = fleCount + args['i']

print(".::Renaming Completed::.")


# ===============
# Write a Rename File
# ===============

if os.path.exists(renameCSVPath):                                                                           # If the rename file already exists delete it
    os.remove(renameCSVPath)

f = open(renameCSVPath, "wb")                                                                               # Create the new rename file
w = csv.writer(f, delimiter = ',')
w.writerows([x.split(',') for x in dataToCSV])
f.close()

print(".::Undo File Created::.")

exit()
