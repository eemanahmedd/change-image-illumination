#  Import packages
import cv2
import imageio
import shutil
import glob
import os
import numpy as np
from tqdm import tqdm


#  Change the illumination of the frame
def adjust_gamma(image, gamma=1.0):

    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")

    return cv2.LUT(image, table)


# Check if the image is dark or light
def img_estim(img, thrshld):
    is_light = np.mean(img) > thrshld
    return 'light' if is_light else 'dark'


light_img_means = []
dark_img_means = []

#  to find values of light max and dark min to distinguish between the images
dark_max = (0, 1)
light_max = (0,1)
dark_min = (1000, 1)
light_min = (1000, 1)

for image in tqdm(glob.glob(r"C:\Users\Eman\Downloads\evaluation\bright\*")):
    
    img = cv2.imread(image, 1)
    mean = np.mean(img)
    if mean < light_min[0]:
        light_min = (mean, os.path.basename(image))
    if mean > light_max[0]:
        light_max = (mean, os.path.basename(image))
    light_img_means.append(mean)
    brightness = img_estim(img, 108)
    

 
for image in tqdm(glob.glob(r"C:\Users\Eman\Downloads\evaluation\dark\*")):
    img = cv2.imread(image, 1)
    mean = np.mean(img)
    if mean < dark_min[0]:
        dark_min = (mean, os.path.basename(image))
    if mean > dark_max[0]:
        dark_max = (mean, os.path.basename(image))
    dark_img_means.append(np.mean(img))
    brightness = img_estim(img, 108)
    

print(f'light min: {light_min}, dark max {dark_max}')