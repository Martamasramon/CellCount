import os
import pickle 
import shutil
import numpy as np

folder_main = './HMU_010_FH/'
folder_A2   = './HMU_010_FH/A2/'
list_main   = np.sort(os.listdir(folder_main))
list_A2     = os.listdir(folder_A2)
  
# Load list of images in hard disk
with open('list.pkl','rb') as f:  
    list_saved = pickle.load(f)
  
"""# Move all images to main folder
for i in list_A2:
    shutil.move(folder_A2 + i, folder_main + i)"""
 
for i in list_main:
    if '320' in i:   
        match = [s for s in list_saved if i[18:23] in s]  
           
        if len(match) == 0:
            os.remove(folder_main + i)
           
for i in list_A2:
    match = [s for s in list_saved if i[18:23] in s]  
        
    if len(match) == 0:
        os.remove(folder_A2 + i)

    
"""# Move images not in hard disk to A2 folder
for i in list_main:
    if '320' in i:
        match = [s for s in list_saved if i[18:23] in s]
        
        if len(match)>0:
            shutil.move(folder_main + i, folder_A2 + i)"""


import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2hed, hed2rgb

def separate_img(img, display=False):
    # Separate the stains from the img image
    img_hed = rgb2hed(img)

    # Create an RGB image for each of the stains
    null = np.zeros_like(img_hed[:, :, 0])
    img_h = hed2rgb(np.stack((img_hed[:, :, 0], null, null), axis=-1))
    img_e = hed2rgb(np.stack((null, img_hed[:, :, 1], null), axis=-1))
    img_d = hed2rgb(np.stack((null, null, img_hed[:, :, 2]), axis=-1))

    if display:
        fig, axes = plt.subplots(2, 2, figsize=(7, 6), sharex=True, sharey=True)
        ax = axes.ravel()

        ax[0].imshow(img)
        ax[0].set_title("Original image")

        ax[1].imshow(img_h)
        ax[1].set_title("Hematoxylin")

        ax[2].imshow(img_e)
        ax[2].set_title("Eosin")  # Note that there is no Eosin stain in this image

        ax[3].imshow(img_d)
        ax[3].set_title("DAB")

        for a in ax.ravel():
            a.axis('off')

        fig.tight_layout()
        
    return img_h