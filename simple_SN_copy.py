import os
import tifffile
import math
import numpy as np
from skimage import color
import cv2
from PIL import Image

def check_hsv(folder_in, sid, s, key=2):      
        
    # Read NDPI image
    path    = os.path.join(folder_in, sid + '_' + s + '.ndpi')
    histo   = tifffile.imread(path, key=key)
        
    # Get original image size
    [w,h,_] = histo.shape
    histo   = cv2.resize(histo, (int(h/10), int(w/10)), interpolation=cv2.INTER_CUBIC)
    
    # Convert the image to HSV color space
    image_hsv = color.rgb2hsv(histo)

    contrast        = np.std(image_hsv[:,:,2])
    brightness      = np.mean(image_hsv[:,:,2])
    saturation_mean = np.mean(image_hsv[:,:,1])
    saturation_std  = np.std(image_hsv[:,:,1])
    
    return contrast, brightness, saturation_mean, saturation_std
    
def scale_mean_std(array, target_mean, target_std, current_mean=None, current_std=None):
    if (current_mean is None) or (current_std is None):
        print(array.shape)
        size = array.shape
        current_mean = np.mean(array)
        current_std  = np.std(array)

    scaled_array = (array - current_mean) * (target_std / current_std) + target_mean
    
    return np.clip(scaled_array, 0, 1)

def convert_and_scale_img(img, target_vals, img_vals=[None, None, None, None]):
    image_hsv        = color.rgb2hsv(img)
    image_hsv[:,:,2] = scale_mean_std(image_hsv[:,:,2], target_vals[1], target_vals[0], img_vals[1], img_vals[0]) # Set contrast & brightness
    image_hsv[:,:,1] = scale_mean_std(image_hsv[:,:,1], target_vals[2], target_vals[3], img_vals[2], img_vals[3]) # Set saturation

    array = color.hsv2rgb(image_hsv)*255
    return array.astype(np.uint8)

def scale_hsv(folder_in, folder_out, sid, s, target_means, key=2, size=600):      
    # Read NDPI image
    path    = os.path.join(folder_in, sid + '_' + s + '.ndpi')
    histo   = tifffile.imread(path, key=key)
    [w,h,_] = histo.shape  
    print(histo.shape)
    
    # if key == 0:
    #     histo = Image.fromarray(histo)
    #     histo = histo.resize((int(h/2), int(w/2)))  
    #     histo = np.asarray(histo) 
        
    # Reshape image 
    [w,h,_]     = histo.shape
    histo_img   = Image.fromarray(histo)
    histo_img   = histo_img.resize((int(size/w*h), size))
    #histo_img   = histo_img.resize((int(h/16), int(w/16)))
    histo       = np.asarray(histo_img)  
    
    histo = convert_and_scale_img(histo, target_means)
    histo = Image.fromarray(histo)
    histo.save(os.path.join(folder_out, sid + '_' +s) + '_scaled_SN.png')
   
def pad_img(img, path_out, name):
    [w,h,_]      = img.shape
    new_w, new_h = math.ceil(w/5120)*5120, math.ceil(h/5120)*5120
    new_img      = cv2.copyMakeBorder(img, 0, new_h-h, 0, new_w-w, cv2.BORDER_REFLECT)
    
    # new_img = Image.fromarray(new_img)
    # new_img = new_img.resize((int(h/100), int(w/100)))  
    # new_img.save(os.path.join(path_out, name) + '_padded.png')
    return new_img
    
def divide_image(path_in, path_out, name, target_means, img_means, size=512, key=1):
    
    # Read in NDPI image
    histo   = tifffile.imread(path_in + name + '.ndpi', key=key)
    [w,h,_] = histo.shape  

    # Some images don't have target magnification.
    # Get higher resolution and downsample.
    if key == 0:
        histo = Image.fromarray(histo)
        histo = histo.resize((int(h/2), int(w/2)))  
        histo = np.asarray(histo) 
    
    # Pad images when getting large patches
    if size == 5120:
        print('Adding padding')
        histo = pad_img(histo, path_out, name)    
    
    # Check shape and number of patches 
    [w,h,_] = histo.shape
    total   = int(w/size) * int(h/size)
    print('Shape:',histo.shape)
    print('Number of tiles:',total)
    
    # Crete folder 
    if not os.path.exists(path_out):
        os.mkdir(path_out)   
        
    count   = 0   
    for i in range(int(w/size)):
        for j in range(int(h/size)):
            count += 1
            # if count<7680:
            #     continue 
            # else:
            img     = histo[i*size:(i+1)*size, j*size:(j+1)*size, :] 
            new_img = convert_and_scale_img(img, target_means, img_means)
            
            cv2.imwrite(path_out + name + '_' + str(size) + '_' + str(count) + '.png', new_img)
            
            if count%1000 == 0:
                print('Sub-image count: ' + str(count) + ' (' + str(count/total*100) + '%)')       

slices = {
    'HMU_227_KT': {'key': 1, 'nums': ['A3']}, 
}

data         = np.array([[0.10783624, 0.83929284, 0.25240443, 0.22689683],[0.11735257, 0.82440185, 0.21339759, 0.21509128],[0.10156187, 0.82926688, 0.21922099, 0.20029516],[0.12142297, 0.80974221, 0.25997474, 0.23561381],[0.09968247, 0.83442113, 0.22874756, 0.21369536],[0.11756935, 0.80672016, 0.26230924, 0.23160957],[0.11195922, 0.82162308, 0.24369016, 0.23931876],[0.09001202, 0.82550527, 0.2186387 , 0.19443723],[0.09775365, 0.8324575 , 0.22139981, 0.18750221],[0.09591109, 0.83261928, 0.25690729, 0.23656938],[0.08783433, 0.84429093, 0.23577258, 0.20006978],[0.10217619, 0.83944577, 0.2117292 , 0.1976614 ],[0.0867065 , 0.84336719, 0.21030008, 0.18983978],[0.08540002, 0.83344448, 0.25863205, 0.2008503 ],[0.08793532, 0.83587889, 0.28711144, 0.25589292],[0.09575941, 0.84140982, 0.23073615, 0.21190442],[0.11946889, 0.79757324, 0.29824133, 0.25215079],[0.12054214, 0.80396476, 0.31432842, 0.2797655 ],[0.10044404, 0.83792226, 0.26669047, 0.25854141],[0.11770994, 0.83319246, 0.26653702, 0.27643963],[0.09348649, 0.84509718, 0.20991062, 0.21747073],[0.10132566, 0.83084083, 0.24882901, 0.211261  ],[0.11292235, 0.83240618, 0.25225984, 0.25244512],[0.09228317, 0.84953607, 0.22266316, 0.20421559],[0.07319773, 0.86571728, 0.16216143, 0.16783455],[0.07865819, 0.85313034, 0.19098651, 0.19414139],[0.07342325, 0.86165808, 0.15282606, 0.13839211],[0.11526403, 0.80237732, 0.28517211, 0.26474973],[0.10949241, 0.8146374 , 0.19433159, 0.20758568],[0.10331349, 0.82159219, 0.22491241, 0.22951364],[0.104505  , 0.8274592 , 0.17463261, 0.2059832 ],[0.094634  , 0.82674691, 0.21439635, 0.21759465]])
target_means = np.mean(data,axis=0)

def main(): 

    GET_MEAN  = False
    SCALE_IMG = False
    PATCHES   = True   
    
    SIZE = 512
    
    folder_in      = '../../backup_masramon/Histology/NDPI/'  
    folder_down    = './Downsampled/'
    folder_patches = './Patches/'
    
    if GET_MEAN:
        results = np.zeros((2,4))
        i=0
        
        for sid in slices:
            print(sid, ':')
            for s in slices[sid]['nums']:
                print('- ', s)
                results[i,:] = check_hsv(f'{folder_in}{sid}/', sid, s, key=slices[sid]['key'])
                print(results[i,:])
                i+=1
            
        print('\n', results)
        
    if SCALE_IMG:
        for sid in slices:
            print(sid, ':')
            for s in slices[sid]['nums']:
                print('- ', s)
                scale_hsv(f'{folder_in}{sid}/', folder_down, sid, s, target_means, key=slices[sid]['key'])    
                
    if PATCHES:
        for sid in slices:
            print(sid, ':')
            for s in slices[sid]['nums']:
                print('- ', s)
                img_means = check_hsv(f'{folder_in}HMU_201_MB/', 'HMU_201_MB', 'A3', key=2)
                divide_image(f'{folder_in}{sid}/', f'{folder_patches}{sid}_{s}_SN/', f'{sid}_{s}', target_means, img_means, size=SIZE, key=slices[sid]['key'])   
    
main()  
