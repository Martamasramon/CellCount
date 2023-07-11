import os
import pickle 
import shutil

folder_main = './HMU_010_FH/'
folder_A2   = './HMU_010_FH/A2/'
list_main   = os.listdir(folder_main)
list_A2     = os.listdir(folder_A2)
  
# Load list of images in hard disk
with open('list.pkl','rb') as f:  
    list_saved = pickle.load(f)
  
# Move all images to main folder
for i in list_A2:
    shutil.move(folder_A2 + i, folder_main + i)
        
# Move images not in hard disk to A2 folder
for i in list_main:
    if '320' in i:
        match = [s for s in list_saved if i[18:23] in s]
        
        if len(match)>0:
            shutil.move(folder_main + i, folder_A2 + i)


