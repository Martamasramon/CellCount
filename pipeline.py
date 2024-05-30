import os
import cv2
import tifffile
import numpy as np
from PIL import Image
    
def resize_histo_png(folder_in, folder_out, sid, slices, size=600, key=2, factor=100, tif=False):      
        
    for i in range(len(slices)):
        # Read NDPI image
        path    = os.path.join(folder_in, sid + '_' +slices[i] + '.ndpi')
        histo   = tifffile.imread(path, key=key)
                    
        # Get original image size
        print(sid, slices[i], histo.shape)
        [w,h,_]     = histo.shape
        histo_img   = Image.fromarray(histo)
        
        # Reshape image
        # histo_img   = histo_img.resize((int(size/w*h), size))
        # print(int(size/w*h), size)
        
        # 2x2mm patches for manju
        print(int(h/factor), int(w/factor))
        histo_img   = histo_img.resize((int(h/factor), int(w/factor)))
        
        if tif:
            # Save as tif
            tifffile.imsave(os.path.join(folder_out, sid + '_' +slices[i]) + '_high_res.tif', np.array(histo_img))
        else:
            # Save as png
            histo_img.save(os.path.join(folder_out, sid + '_' +slices[i]) + '_high_res.png')
        
    
def divide_image(path_in, path_out, name, size=512, key=1):
    print(name)
    histo   = tifffile.imread(path_in + name + '.ndpi', key=key)
    
    print('Shape:',histo.shape)
    [w,h,_] = histo.shape
    
    count   = 0
    total   = int(w/size) * int(h/size)
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

def divide_image_reshape(path_in, path_out, name, size=512, key=1):
    print(name)
    size_big = size*2
    histo    = tifffile.imread(path_in + name + '.ndpi', key=key)
    
    print('Shape:',histo.shape)
    [w,h,_] = histo.shape
    
    count   = 0
    total   = int(w/size_big) * int(h/size_big)
    print('Number of tiles:',total)
    
    if not os.path.exists(path_out):
        os.mkdir(path_out)   
     
          
    for i in range(int(w/size_big)):
        for j in range(int(h/size_big)):
            img = histo[i*size_big:(i+1)*size_big, j*size_big:(j+1)*size_big, :] 
            img = Image.fromarray(img)
            img = img.resize((size, size))
            img.save(path_out + name + '_' + str(size) + '_' + str(count) + '.png')
            count += 1
            
            if count%1000 == 0:
                print('Sub-image count: ' + str(count) + ' (' + str(count/total*100) + '%)')   
                
slices = {
    #'HMU_033_JS': {'key': 2, 'nums': ['A3']},
    #'HMU_038_JC': {'key': 2, 'nums': ['A2']},
    #'HMU_056_JH': {'key': 2, 'nums': ['A5']},
    #'HMU_063_RS': {'key': 2, 'nums': ['A2']},
    #'HMU_065_RH': {'key': 2, 'nums': ['A4']},
    #'HMU_066_JF': {'key': 2, 'nums': ['A2']},
    #'HMU_067_MS': {'key': 2, 'nums': ['A3']},
    #'HMU_068_PB': {'key': 1, 'nums': ['A3']},
    #'HMU_069_NS': {'key': 2, 'nums': ['A4']}
    #'HMU_076_RV': {'key': 2, 'nums': ['A4']},
    #'HMU_077_MW': {'key': 2, 'nums': ['A3']},
    #'HMU_082_PS': {'key': 2, 'nums':['A3']}
    #'HMU_084_AJ': {'key': 1, 'nums': ['A2']}, #,'A3']},
    #'HMU_087_FM': {'key': 1, 'nums': ['A3']},
    #'HMU_094_RB': {'key': 1, 'nums': ['A1','A3']},
    #'HMU_099_DL': {'key': 1, 'nums': ['A4','A7']},
    #'HMU_113_MT': {'key': 1, 'nums': ['A2']}, 
    #'HMU_121_CN': {'key': 1, 'nums': ['A1']}
    #'HMU_176_IJ': {'key': 2, 'nums': ['A3']}, 
    #'HMU_180_KF': {'key':2, 'nums':['A3','A4','A5']},
    #'HMU_198_JL': {'key': 0, 'nums': ['A2']},
    #'HMU_201_MB': {'key': 2, 'nums': ['A3']} ,
    'HMU_227_KT': {'key': 1, 'nums': ['A3']},
    'HMU_235_CC': {'key': 1, 'nums': ['A7']},
    'HMU_256_DB': {'key': 1, 'nums': ['A8']}
    # 'HMU_242_JD': {'key': 0, 'nums': ['A5']}, # too dark...?
    # 'HMU_245_DC': {'key': 0, 'nums': ['A7']},
    # 'HMU_256_DB': {'key': 0, 'nums': ['A6']},
    # 'HMU_258_JK': {'key': 0, 'nums': ['A6']},
    # 'HMU_265_JM': {'key': 0, 'nums': ['A7']}
}

def main(): 
    # Choose pipeline options
    RESIZE       = False
    MAKE_PATCHES = True
    
    folder_in  = './Whole images/'  
    folder_out = './Downsampled/'  
    
    for sid in slices:
        if RESIZE:
            resize_histo_png(folder_in, folder_out, sid, slices[sid]['nums'],factor=30,key=slices[sid]['key'])
            # for manju, size =30
        
        if MAKE_PATCHES:
            for i in range(len(slices[sid]['nums'])):
                name = sid + '_' + slices[sid]['nums'][i]
                divide_image(folder_in,  'Patches/' + name + '/' , name, size=1740, key=slices[sid]['key'])   
                #for manju, size=4406
            
main()  