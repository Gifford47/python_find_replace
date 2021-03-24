# python_find_replace
a python script, that searches und replace strings with regex

Please provide these arguments: \n"
-r <search_string> <replace_string> = replace string in every file in current working directory.
-d <"{\'alt'':\'neu\',\'alt2\':\'neu2\'}"> = replace strings from <DICT> in every file in current working directory.
-f <search_string> = Find string in files in current working directory.
Optional:\n-p <PATH> = Define Path for your action. If not spcified, the current working directory will be used.

Example:find_replace.py -r alt neu -p C:\choose\dir
