import cv2
import tifffile
    
def main():     
    histo   = tifffile.imread('./HMU_010_FH/HMU_010_FH_A2.ndpi', key=2)
    print(histo.shape)
    cv2.imwrite('./HMU_010_FH/HMU_010_FH_A2.png', histo)
            
main() 