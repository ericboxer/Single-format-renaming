import os, re, argparse, csv

# ===============
# Global Vars
# ===============

csvFileName = "rename.csv"

# ===============
# Commandline Arguments
# ===============
parser = argparse.ArgumentParser(description="Rename files to have a leading number and a space")
parser.add_argument('-e', help="match particular file extension. Defaults to using .wav", default = "wav")
parser.add_argument('-s', help="What number to start from. Default is 1.", default = 1, type = int)
parser.add_argument('-i', help="The increment value. Deafault is 1.", default = 1, type = int)
parser.add_argument('-l', help="Location this line is used. Will not include if left empty", default = '')
parser.add_argument('-p', help = "How many 0's to pad the leading number with. Default is 3.", default = 3, type = int)
parser.add_argument('-c', help = "By default outputs to the command line only. Set true commit renaming to the directory.", action = "store_true", default = False)
parser.add_argument('-u', help = "In case of dumb.", action = "store_true", default = False)

args = vars(parser.parse_args())

# ===============
# Undo in case of Dumb
# ===============

if args['u']:
    if os.path.exists(csvFileName):

        f = open(csvFileName, mode="rb")

        csvF = csv.reader(f, delimiter = ",")

        for row in csvF:
            os.rename(row[0], row[1])
        f.close()
        os.remove(csvFileName)
    else:
        print("Renaming file doesnt exist. You're SOL.")
    exit()

# ===============
# Renaming Session Variables
# ===============

dataToCSV = []                                                                         # Holds the values to write out to the undo.

fleCount = args['s']                                                                   # Starting number to count from.

if args['l'] == '':                                                                    # Sets a location in for the filename. If blank dont place anything there.
    locationString = " "
else:
    locationString = " " + args['l'] + " "

# ===============
# Rename the Files
# ===============
for directoryFile in os.listdir('./'):                                                     # Uses the directory the script is in. TODO: update to allow to choose directory.  
    if directoryFile.endswith(args['e']):
        oldName = directoryFile
        newName = str(fleCount).zfill(args['p']) + locationString +(re.sub('^[0-9_ ]*', '', directoryFile))                                   # Remove leading numbers, spaces, and underscores and then format the name.
        print("%s renamed to %s" % (oldName, newName))
        if args['c']:                                                                  # Make the changes permanant. 
            os.rename(oldName, newName)
        dataToCSV.append("%s,%s" % (newName, oldName))
        fleCount = fleCount + args['i']

print(".::Renaming Completed::.")

# ===============
# Write a Rename File (rename.csv)
# ===============

if os.path.exists(csvFileName):
    os.remove(csvFileName)

f = open(csvFileName, "wb")
w = csv.writer(f, delimiter = ',')
w.writerows([x.split(',') for x in dataToCSV])
f.close()

print(".::Undo File Created::.")




