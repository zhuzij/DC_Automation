'''
module import error fixed by appending current module's os.getcwd() to sys.path, which is the top level project folder (absolute path)
'''
import os
print(f'{os.getcwd()=}')

import sys
sys.path.append(os.getcwd()) # all project file has the top level directory as its cwd??, once it's appended, I can access any subdir under it!
print(f"{sys.path=}")
from common.utils import Environment_Task_Manager

with open('config/tasks.yml', 'r') as f: # this relative path somehow doesn't rely on sys.path.append()??!
    yml = f.read()
    print(yml)