#!/usr/bin/python3
# File name   : autorun.py
# Description : Control Motors 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12

import os
import sys

def search(path,name):
    for root, dirs, files in os.walk(path):
        if name in dirs or name in files:
            flag = 1
            root = str(root)
            dirs = str(dirs)
            return os.path.join(root, dirs)
    return -1

def replace_num(file,initial,new_num):  
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)

path_get = str(search('//home/pi/','server.py'))
path_get=path_get[:-2]

try:
	os.system('sudo rm //home/pi/startup.sh')
except:
	pass

try:
	os.system('sudo touch //home/pi/startup.sh')
	with open("//home/pi/startup.sh",'w') as file_to_write:
		file_to_write.write("#!/bin/sh\nsudo python3 %sserver.py"%path_get)
except:
	pass

os.system('sudo chmod 777 //home/pi/startup.sh')
