from __future__ import print_function
import numpy as np
import argparse
import cv2
import os
from PIL import Image
import tifffile

def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table    
	return cv2.LUT(image, table)

def resize_histo_png(folder_in, folder_out, sid, slices, size=600, gamma=0.5):     
    
    for i in range(len(slices)):
        # Read NDPI image
        path    = os.path.join(folder_in, sid + '_' +slices[i] + '.ndpi')
        histo   = tifffile.imread(path, key=2)
            
        # Get original image size
        print(sid, slices[i], histo.shape)
        [w,h,_]     = histo.shape
        
        # Reshape image
        histo_img   = Image.fromarray(histo)
        histo_img   = histo_img.resize((int(size/w*h), size))

        np_img      = np.array(histo_img)
        gamma_img   = adjust_gamma(np_img, gamma)

        # Save as png
        Image.fromarray(gamma_img).save(os.path.join(folder_out, sid + '_' +slices[i]) + '_gamma' +str(gamma) + '.png') 
        #histo_img.save(os.path.join(folder_out, sid + '_' +slices[i]) + '_original.png') 
       
                  
def divide_image(path_in, path_out, name, size, key=1, gamma=0.5):
    print(path_in + name + '.ndpi')
    histo   = tifffile.imread(path_in + name + '.ndpi', key=key)
    histo   = adjust_gamma(histo, gamma)
    
    [w,h,_] = histo.shape
    count   = 0
    total   = int(w/size) * int(h/size)
    print('Shape:', int(w/size), int(h/size))
    print('Number of tiles:',total)
    
    if not os.path.exists(path_out):
        os.mkdir(path_out)   
            
    for i in range(int(w/size)):
        for j in range(int(h/size)):
            img = histo[i*size:(i+1)*size, j*size:(j+1)*size, :] 
            cv2.imwrite(path_out + name + '_' + str(size) + '_' + str(count) + '.png', img)
            count += 1
            
            if count%1000 == 0:
                print('Sub-image count: ' + str(count) + ' (' + str(count/total*100) + '%)')     
                

slices = {
    'HMU_116_BC': {'gamma': 0.8, 'nums': ['A4','A5']},
    'HMU_128_RK': {'gamma': 1.3,  'nums': ['A5']},
}

def main():   
    folder_in  = './Whole images/'  
    folder_out = './Downsampled/'  
    
    for sid in slices:
        gamma = slices[sid]['gamma']
        nums  = slices[sid]['nums']
        
        resize_histo_png(folder_in, folder_out, sid, nums, gamma=gamma)
        
        for i in range(len(nums)):
            name = sid + '_' + nums[i]
            divide_image(folder_in,  'Patches/' + name + '_gamma_'+str(gamma)+'/' , name, 512, key=1, gamma=gamma) 
        
main() 