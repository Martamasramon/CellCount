# Imports
import os
from PIL import Image
import tifffile
    
def resize_histo_png(folder, sid, slices, size=600):      
          
    for i in range(len(slices)):
        # Read NDPI image
        path    = os.path.join(folder, sid + '_' +slices[i] + '.ndpi')
        histo   = tifffile.imread(path, key=1)
            
        # Get original image size
        print(histo.shape)
        [w,h,_]     = histo.shape
        
        # Reshape image
        histo_img   = Image.fromarray(histo)
        histo_img   = histo_img.resize((int(size/w*h), size))
        
        # Save as png
        histo_img.save(os.path.join(folder, sid + '_' +slices[i]) + '_downscale.png')
          
slices = {
    'HMU_176_IJ': ['A3']
    }

def main():   
    folder = './Whole images/'  
    for sid in slices:
        resize_histo_png(folder, sid, slices[sid], size=600)
            
main() 