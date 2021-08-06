#!/usr/bin/python
#!"C:\Python27\python.exe"
# -*- coding: utf-8 -*-

import os, sys, re, ast
from sys import exit

#info: sys.argv[0] is reserved for the internal filename!

#path = "C:\\Users\\risshend\\Documents\\PyCharm"
#path = os.path.dirname(__file__)		#get path of current dir of that file
path = os.getcwd()				#get path of current working dir
result_msg = "changed"

def notice_and_exit():
    print "Argument failure! Please provide these arguments: \n" \
          '-r <search_string> <replace_string> = replace string in every file in current working directory.\n' \
          '-d <"{\'alt'':\'neu\',\'alt2\':\'neu2\'}"> = replace strings from <DICT> in every file in current working directory.\n' \
          '-f <search_string> = Find string in files in current working directory.\n' \
          '\nOptional:\n-p <PATH> = Define Path for your action. If not spcified, the current working directory will be used.\n' \
          '-depth 1 = Should i search subdirs as well?. If depth is 1 (standard), the full depth is walked. If depth is 0, the current directory is listed.\n' \
          '\nExample:\nfind_replace.py -r alt neu -p C:\choose\dir\n'
    #os.system('pause')              # only for win, to read the console after finish
    exit(0)

def replace(search_str, replace_str):
    global counter
    files = get_files_list()
    for file in files:
        with open(os.path.join(path, file), 'r') as file_opened:
            filedata = file_opened.read()
            file_opened.close()
        # filedata_replaced = filedata.replace(sys.argv[1], sys.argv[2])      # replace strings (auch innerhalb woerter!!!)
        filedata_replaced = re.sub(r"\b%s\b" % search_str, replace_str, filedata)  # replace whole words only
        if filedata_replaced != filedata:
            with open(os.path.join(path, file), 'w') as file_saved:
                file_saved.write(filedata_replaced)
                file_saved.close()
            print ("File '" + os.path.join(path, file) + "' changed!")
            counter += 1

def replace_by_dict(dict):
    global counter
    flag_replaced = False
    for keys, values in dict.items():
        print ("'" + keys + "' -> '" + values + "'")
    case = raw_input("Oben genannte Ausdruecke 'alt' -> 'neu' in '" + path + "' ersetzen? (y/n): ")
    if case == "y":
        files = get_files_list()
        for file in files:
            # Read in the file and close it
            with open(os.path.join(path, file), 'r') as file_opened:
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
                    counter += 1
                    flag_replaced = True
                else:
                    # print "No File changed."
                    pass
            if flag_replaced:
                print ("File '" + os.path.join(path, file) + "' changed!")
                with open(os.path.join(path, file), 'w') as file_saved:
                    file_saved.write(filedata_replaced)
                    file_saved.close()

def find(search_str):
    global counter
    files = get_files_list()
    for file in files:
            with open(os.path.join(path, file), 'r') as file_opened:
                filedata = file_opened.read()
                file_opened.close()
            result = re.findall(r"\b%s\b" % search_str, filedata)               # "\b" = represents the backspace character
            if len(result) > 0:
                counter += 1
                print ('Found ' + str(len(result)) + "x in: '" + os.path.join(path, file))

def get_files_list():
    files_list = []

    if depth == 0:
        files_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    else:
        for root, dirs, files in os.walk(path):
            for f in files:
                files_list.append(os.path.join(root, f))

    # diese skriptdatei ignorieren
    if os.path.basename(__file__) in files_list:
        files_list.remove(os.path.basename(__file__))

    return files_list

if __name__== "__main__":
    global counter
    counter = 0
    depth = 1
    #print len(sys.argv), sys.argv

    if (len(sys.argv) <= 1):
        notice_and_exit()
    if ('-p' in sys.argv):      # index begins at [0]! element=index+1
        if (len(sys.argv) >= sys.argv.index('-p')+2):
            if (os.path.isdir(sys.argv[sys.argv.index('-p')+1])):
                path = sys.argv[sys.argv.index('-p')+1]
            else:
                notice_and_exit()
        else:
            notice_and_exit()
    if ('-depth' in sys.argv):      # index begins at [0]! element=index+1
        if (len(sys.argv) >= sys.argv.index('-depth')+2):
            if (isinstance(int(sys.argv[sys.argv.index('-depth')+1]), int)):
                depth = int(sys.argv[sys.argv.index('-depth')+1])
            else:
                notice_and_exit()
        else:
            notice_and_exit()

    print('Working directory:' + path)
    if depth == 1:
        print('Subfolders:YES')
    else:
        print('Subfolders:NO')
    print('searching...')

    # if no argument is choosen, replace a string by a new string in current script-dir:
    #if (len(sys.argv) == 3 and len(sys.argv[1]) <> 2):
        #replace(sys.argv[1], sys.argv[2])
    try:
        # replace string in every file in a path:
        if (sys.argv[1] == '-r'):
            if (len(sys.argv) < 4):
                notice_and_exit()
            replace(sys.argv[2], sys.argv[3])
        # replace a string by an new string:
        elif (sys.argv[1] == '-d'):
            if (len(sys.argv) < 3):
                notice_and_exit()
            dict = ast.literal_eval(sys.argv[2])
            replace_by_dict(dict)
        # find a string:
        elif (sys.argv[1] == '-f'):
            if (len(sys.argv) < 3):
                notice_and_exit()
            result_msg = "found"
            find(sys.argv[2])
        else:
            notice_and_exit()
    except Exception as e:
        print ('Error:')
        print (e)
    except KeyboardInterrupt:
        print ("\nUser Abort, exiting...")

    print ('Total occurences ' + result_msg + ": " + str(counter))
    #os.system('pause')              # only for win, to read the console after finish

    try:
        sys.stdout.close()
        sys.stderr.close()
    except:
        pass
