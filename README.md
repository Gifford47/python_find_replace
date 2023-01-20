# Python find and/or replace script
A python script, that searches und replaces whole(!) strings with regex. You can specify a path of operation or a single file. If nothing is choosen, the current working directory is used.<br>

Please provide these arguments:<br>
-r <search_string> <replace_string> = replace string in every file in current working directory.<br>
-d <"{\'old'':\'new\',\'old2\':\'new2\'}"> = replace strings from <DICT> in every file in current working or "PATH" directory.<br>
-f <search_string> = Find string in files in current working directory.<br><br>

Optional:<br>
-p <PATH> = Define Path or file for your action. If not spcified, the current working directory will be used.<br><br>

Example:<br>
find_replace.py -r old_string new_string -p "C:\choose\dir"<br><br>

Output:<br>
Working directory:C:\Users\bratzh\Documents\PyCharm\find_replace<br>
searching...<br>
File 'C:\Users\test\Documents\find_replace\new.txt' changed 2 times!<br>
File 'C:\Users\test\Documents\find_replace\second.txt' changed 1 times!<br>
Total files changed: 2<br>
