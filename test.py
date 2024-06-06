import os
import tifffile
    
folder_in  = '../../backup_masramon/Histology/NDPI/'  
path       = os.path.join(folder_in, 'HMU_180_KF/HMU_180_KF_A4.ndpi')
histo      = tifffile.imread(path, key=2)
print(histo.shape)
    

