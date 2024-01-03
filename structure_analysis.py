from sklearn.cluster import KMeans
import numpy as np
import os
import cv2
import tifffile

def cluster(folder_in, folder_out, sid, slice_num):
    
    # Read NDPI image
    img   = tifffile.imread(os.path.join(folder_in, sid + '_' +slice_num + '.ndpi'), key=3)

    # Save grayscale image
    gray_img = ImageOps.grayscale(Image.fromarray(img))
    gray_img.save(os.path.join(folder_out, sid + '_' +slices[i]) + '_grayscale.png')

    # Reshape the image to a 2D array of pixels
    w, h, d = img.shape
    img_2d = np.reshape(img, (w * h, d))
    
    # Apply k-means
    kmeans   = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(img_2d)
    clusters = kmeans.predict(img_2d)

    # Reshape into 2D image
    clustered_img = clusters.reshape(w, h)
    
    # Save clusters
    img  = cv2.imwrite(os.path.join(folder_out, sid + '_' +slice_num + '_clusters.png'), clustered_img)
    
  
slices = {
    'HMU_180_KF': ['A3']
}

def main(): 

    folder_in  = './Whole images/'  
    folder_out = './ST analysis/'  
    
    for sid in slices:
        for i in range(len(slices[sid])):
            cluster(folder_in, folder_out, sid, slices[sid][i])
            
main()  