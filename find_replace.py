#!/usr/bin/python
#!"C:\Python27\python.exe"
# -*- coding: utf-8 -*-

import os, sys, re, ast
from sys import exit

#info: sys.argv[0] is reserved for the internal filename!

#path = os.path.dirname(__file__)               #get path of current dir of that file
path = os.getcwd()                              #get path of current working dir
result_msg = "changed"

def notice():
    print "Argument failure! Please provide these arguments: \n" \
          '-r <search_string> <replace_string> = replace string in every file in current working directory.\n' \
          '-d <"{\'alt'':\'neu\',\'alt2\':\'neu2\'}"> = replace strings from <DICT> in every file in current working directory.\n' \
          '-f <search_string> = Find string in files in current working directory.\n' \
          'Optional:\n-p <PATH> = Define Path for your action. If not spcified, the current working directory will be used.\n' \
          'Example:\nfind_replace.py -r alt neu -p C:\choose\dir\n'
    #os.system('pause')              # only for win, to read the console after finish
    exit(0)
def replace(search_str, replace_str):
    global file_counter
    # print sys.argv[1], sys.argv[2]
    if (os.path.isfile(path)):
        with open(path, 'r') as file_opened:
            filedata = file_opened.read()
            file_opened.close()
        occ = re.findall(r"\b%s\b" % search_str, filedata)  # "\b" = represents the backspace character
        filedata_replaced = re.sub(r"\b%s\b" % search_str, replace_str, filedata)  # replace whole words only
        if filedata_replaced != filedata:
            with open(path, 'w') as file_saved:
                file_saved.write(filedata_replaced)
                file_saved.close()
            print "File '" + path + "' changed " + str(len(occ)) + " times!"
            file_counter += 1
        return

    for root, dirs, files in os.walk(path):
        # diese skriptdatei ignorieren
        if os.path.basename(__file__) in files:
            files.remove(os.path.basename(__file__))
        for file in files:
            with open(os.path.join(root, file), 'r') as file_opened:
                filedata = file_opened.read()
                file_opened.close()
            # filedata_replaced = filedata.replace(sys.argv[1], sys.argv[2])      # replace strings (auch innerhalb woerter!!!)
            occ = re.findall(r"\b%s\b" % search_str, filedata)                   # find occcurences
            filedata_replaced = re.sub(r"\b%s\b" % search_str, replace_str, filedata)  # replace whole words only
            if filedata_replaced != filedata:
                with open(os.path.join(root, file), 'w') as file_saved:
                    file_saved.write(filedata_replaced)
                    file_saved.close()
                print "File '" + os.path.join(root, file) + "' changed " + str(len(occ)) +" times!"
                file_counter += 1

def replace_by_dict(dict):
    global file_counter
    flag_replaced = False

    if (os.path.isfile(path)):
        print "\nReplacing by dict allows only a directory path not a file path!\n"
        notice()

    for keys, values in dict.items():
        print "'" + keys + "' -> '" + values + "'"
    case = raw_input("Oben genannte Ausdruecke 'alt' -> 'neu' in '" + path + "' ersetzen? (y/n): ")
    if case == "y":
        for root, dirs, files in os.walk(path):
            # diese skriptdatei ignorieren
            if os.path.basename(__file__) in files:
                files.remove(os.path.basename(__file__))
            for file in files:
                # print(os.path.join(root, file))
                # print os.path.basename(__file__)

                # Read in the file and close it
                with open(os.path.join(root, file), 'r') as file_opened:
                    filedata = file_opened.read()
                    file_opened.close()
                # Replace the target string
                # filedata_replaced = filedata.replace(dict["alt"], dict["neu"])   # statically replace items
                for key, value in dict.iteritems():
                    # print key, value
                    # filedata_replaced = filedata.replace(str(key), str(value))      # replace strings (auch innerhalb woerter!!!)
                    filedata_replaced = re.sub(r"\b%s\b" % str(key), str(value), filedata)  # replace whole words only
                    # Write the file out again and close it
                    if filedata_replaced != filedata:
                        filedata = filedata_replaced
                        file_counter += 1
                        flag_replaced = True
                    else:
                        # print "No File changed."
                        pass
                if flag_replaced:
                    print "File '" + os.path.join(root, file) + "' changed!"
                    with open(os.path.join(root, file), 'w') as file_saved:
                        file_saved.write(filedata_replaced)
                        file_saved.close()

def find(search_str):
    global file_counter
    if (os.path.isfile(path)):
        with open(path, 'r') as file_opened:
            filedata = file_opened.read()
            file_opened.close()
        occ = re.findall(r"\b%s\b" % search_str, filedata)  # "\b" = represents the backspace character
        if len(occ) > 0:
            file_counter += 1
            print "Found " + str(len(occ)) + "x in: '" + path
        return

    for root, dirs, files in os.walk(path):
        # diese skriptdatei ignorieren
        if os.path.basename(__file__) in files:
            files.remove(os.path.basename(__file__))
        for file in files:
            with open(os.path.join(root, file), 'r') as file_opened:
                filedata = file_opened.read()
                file_opened.close()
            occ = re.findall(r"\b%s\b" % search_str, filedata)               # "\b" = represents the backspace character
            if len(occ) > 0:
                file_counter += 1
                print "Found " + str(len(occ)) + "x in: '" + os.path.join(root, file)

if __name__== "__main__":
    global file_counter
    file_counter = 0

    if (len(sys.argv) <= 1):
        notice()
    elif ('-p' in sys.argv):      # index begins at [0]! element=index+1
        if (len(sys.argv) >= sys.argv.index('-p')+2):
            if (os.path.isdir(sys.argv[sys.argv.index('-p')+1])):
                path = sys.argv[sys.argv.index('-p')+1]
            else:
                path = sys.argv[sys.argv.index('-p') + 1]
                #notice()
        else:
            notice()

    if (os.path.isfile(path)):
        print "Working file:" + path
    else:
        print "Working directory:" + path

    # print len(sys.argv), sys.argv
    print "searching..."

    # if no argument is choosen, replace a string by a new string in current script-dir:
    #if (len(sys.argv) == 3 and len(sys.argv[1]) <> 2):
        #replace(sys.argv[1], sys.argv[2])
    try:
        # replace string in every file in a path:
        if (sys.argv[1] == '-r'):
            if (len(sys.argv) < 4):
                notice()
            replace(sys.argv[2], sys.argv[3])
        # replace a string by an new string:
        elif (sys.argv[1] == '-d'):
            if (len(sys.argv) < 3):
                notice()
            dict = ast.literal_eval(sys.argv[2])
            replace_by_dict(dict)
        # find a string:
        elif (sys.argv[1] == '-f'):
            if (len(sys.argv) < 3):
                notice()
            result_msg = "found"
            find(sys.argv[2])
        else:
            notice()
    except Exception as e:
        print "Error:"
        print e
    except KeyboardInterrupt:
        print ("\nUser Abort, exiting...")

    print "Total files " + result_msg + ": " + str(file_counter)
    #os.system('pause')              # only for win, to read the console after finish

    try:
        sys.stdout.close()
        sys.stderr.close()
    except:
        pass
