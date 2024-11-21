import os
import cv2
import tifffile
import numpy as np
from PIL import Image
    
def resize_histo_png(folder_in, folder_out, name, key=2, factor=30):   
    """
    Read in an NDPI image, downsample and save as PNG.
    
    Inputs:
    - folder_in:    folder where the input NDPI image is stored
    - folder_out:   folder where to save the output PNG
    - name:         name of the input NDPI image
    - key:          resolution level at which to read the NDPI image
    - factor:       downsampling factor
    """   
        
    # Read NDPI image at chosen resolution level 
    path    = os.path.join(folder_in, name + '.ndpi')
    histo   = tifffile.imread(path, key=key)
                
    # Get original image size
    print('Original shape', histo.shape)
    [w,h,_]     = histo.shape
    histo_img   = Image.fromarray(histo)
    
    if key == 0:
        factor *= 2
    
    # Downsample image
    print('Downsampled shape', (int(h/factor), int(w/factor)))
    histo_img   = histo_img.resize((int(h/factor), int(w/factor)))
    
    # Create output folder if it does not exist
    if not os.path.exists(folder_out):
        os.mkdir(folder_out) 
        
    # Save as png
    histo_img.save(folder_out + name + '_downsampled.png')
        
    
def divide_image(folder_in, folder_out, name, key=1, size=1740):
    """
    Read in an NDPI image, divide into patches and save each patch as PNG.
    
    Inputs:
    - folder_in:    folder where the input NDPI image is stored
    - folder_out:   folder where to save the output PNGs
    - name:         name of the input NDPI image
    - key:          resolution level at which to read the NDPI image
    - size:         pixel width of the patches
    """  
     
    # Read NDPI image at chosen resolution level 
    histo   = tifffile.imread(folder_in + name + '.ndpi', key=key)
    [w,h,_] = histo.shape
    
    if key == 0:
        histo = Image.fromarray(histo)
        histo = histo.resize((int(h/2), int(w/2)))  
        histo = np.asarray(histo) 
        [w,h,_] = histo.shape

    # Count number of patches 
    count   = 0
    total   = int(w/size) * int(h/size)
    
    print('Shape:',histo.shape)
    print('Number of tiles:',total)
    
    # Create output folder if it does not exist
    if not os.path.exists(folder_out):
        os.mkdir(folder_out)   
     
    # Divide the image into patches
    for i in range(int(w/size)):
        for j in range(int(h/size)):
            # Get the relevant patch data
            img = histo[i*size:(i+1)*size, j*size:(j+1)*size, :] 
            
            # Save patch as PNG
            cv2.imwrite(folder_out + name + '_' + str(size) + '_' + str(count) + '.png', img)
            
            # Print out progress every 10 patches
            if count%10 == 0:
                print('Sub-image count: ' + str(count) + ' (' + str(count/total*100) + '%)')          
            
            count += 1
   
                
patients = {
    # 'HMU_181_MO': {'key': 2, 'slice_nums':['A2']},
    'HMU_256_DB': {'key': 0, 'slice_nums': ['A8']}
}

def main(): 
    # Choose pipeline options
    DOWNSAMPLE   = True
    MAKE_PATCHES = True
    
    # Choose input & output locations
    folder_in             = '../../backup_masramon/Histology/NDPI/'
    folder_out_downsample = './Downsampled/'    
    folder_out_patches    = './Patches/' 
    
    # Iterate over all patients
    for sid in patients:
        
        # Iterate over all slices in each patients
        for i in range(len(patients[sid]['slice_nums'])):
            name = sid + '_' + patients[sid]['slice_nums'][i]
            print(name)
            
            # Downsample image
            if DOWNSAMPLE:
                resize_histo_png(folder_in+sid+'/', folder_out_downsample, name, key=patients[sid]['key'])
            
            # Obtain patches
            if MAKE_PATCHES:
                divide_image(folder_in+sid+'/', folder_out_patches, name, key=patients[sid]['key'])   
            
main()  

