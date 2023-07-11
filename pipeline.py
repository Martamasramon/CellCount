import os
import cv2
import tifffile
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
    
    
def divide_image(path_in, path_out, name, size, divide=True):
    
    histo   = tifffile.imread(path_in + name + '.ndpi', key=2)
    [w,h,_] = histo.shape
    print(histo.shape)
    count   = 14760
    total   = int(w/size) * int(h/size)
    print(total)
    
    if divide:
        for i in range(90,121):#int(w/size)
            for j in range(int(h/size)):
                img = histo[i*size:(i+1)*size, j*size:(j+1)*size, :] 
                cv2.imwrite(path_out + name + '_' + str(size) + '_' + str(count) + '.png', img)
                #img = separate_img(img)*255
                count += 1
                
                if count%1000 == 0:
                    print('Sub-image count: ' + str(count) + ' (' + str(count/total*100) + '%)')
                    
                    
            
  
slices = {
    'HMU_010_FH': ['A2']    #['A2','A3','A5','A6']
    }
  
def main():        
    for sid in slices:
        for i in range(len(slices[sid])):
            name = sid + '_' + slices[sid][i]
            divide_image(sid+'/',  sid + '/' , name, 320, True) 
            
main() 