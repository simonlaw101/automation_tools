import os
import re
import shutil

'''
(1) Specify source and destination root path
(2) Change setting (Optional):
    -To add filter, add regular expression in filter_, e.g. filter_ = ['*.java','*.properties']
    -To exclude file, set include_mode = False
    -To rename file if file exists in destination, set replace_mode = False
    -To ignore folder structure when copying file, set ignore_folder_struct = True
'''

#Source root path
src_root = r'C:\Users\simonlaw\Desktop\source'

#Destination root path
dst_root = r'C:\Users\simonlaw\Desktop\dst'

#Setting
filter_ = []
include_mode = True
replace_mode = True
ignore_folder_struct = False

def match_re(pattern, string):
    pattern = '^'+pattern.replace('.','\.').replace('*','.*')+'$'
    return re.match(pattern, string, re.I)!=None

def check_file(filename):
    global include_mode
    global filter_
    if len(filter_)==0:
        return True
    copy = not(include_mode)
    for pattern in filter_:
        if match_re(pattern, filename):
            copy = include_mode
            break
    return copy
    
def copy_file(path, filename):
    src_path = src_root+"\\"+path if path != src_root else src_root
    dst_path = dst_root+"\\"+path if path != src_root and not(ignore_folder_struct) else dst_root
    if check_file(filename):
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        name, extension = os.path.splitext(filename)
        dst_filename = filename
        if not(replace_mode) and os.path.exists(dst_path+"\\"+filename):
            i = 2
            while True:
                new_name = name+' ('+str(i)+')'+extension
                if not os.path.exists(dst_path+"\\"+new_name):
                    dst_filename = new_name
                    break
                i+=1
        shutil.copyfile(src_path+"\\"+filename, dst_path+"\\"+dst_filename)
        print(dst_path+"\\"+dst_filename)   #debug msg
        
def loop_file(path, dir_list):
    cur_path = src_root+"\\"+path if path != src_root else src_root    
    for dir in dir_list:
        if os.path.isdir(cur_path+"\\"+dir):
            src_list = os.listdir(cur_path+"\\"+dir)
            src_path = path+"\\"+dir if path != src_root else dir
            loop_file(src_path, src_list.copy())
        else:
            copy_file(path, dir)

print("\n\nFile(s) replaced at:\n") #debug msg
loop_file(src_root, os.listdir(src_root))