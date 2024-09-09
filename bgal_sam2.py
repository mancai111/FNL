import sys
import numpy as np
import pandas as pd
import starfile
import traceback
import mrcfile
from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseButton
from skimage import img_as_ubyte
import cv2
import os
from PIL import Image
#from EMAN2 import *

# mrcfile folder from mrcfile package (https://pypi.org/project/mrcfile/#files) should be in the above directory (not installed on biowulf)
# goes through autopick.star file and shows each particle. In plot gui, click the magnifying glass and then click on each particle to select the good ones. Green box means it is selected, black box means it has been unselected. To save, close the figures.

#/mnt/NCEP-CryoEM/active/summer_students/lir13/bgal/MotionCorr/job004/bgal_link/Movies/bGala_00008.mrc

if __name__ == '__main__':

    try:

        #OUTPUT_DIR = sys.argv[1] # Job
        #MICROGRAPHS = sys.argv[2] # Input Micrograph
        #PARAM1 = sys.argv[3] # ang/pix

        #OUTPUT_DIR = 'External/job020/'
        #MICROGRAPHS = 'simulation_1/micrographs.star'
        #PARAM1 = 0.257 # ang/pix

### Output a micrograph (clarity needs to be improve)


        example_mrc = '/mnt/NCEP-CryoEM/active/summer_students/lir13/bgal/MotionCorr/job004/bgal_link/Movies/bGala_02975.mrc'
        with mrcfile.open(example_mrc) as mrc:  # from MotionCorr 002 Micrographs
            im = mrc.data
            im = im/np.max(im) * 255
            print(im)
            print(im.shape)
            print(np.max(im))
            cv2.imwrite('/mnt/NCEP-CryoEM/active/summer_students/lir13/External_Relion_Example/test3.jpg', im)
            #im.save('test.jpg')

        #plt.imshow(im,cmap='gray', interpolation='bilinear')
        #fig, ax = plt.subplots()
        #imF = canny(im, sigma = 0.001)
        #im = cv2.imread('/mnt/NCEP-CryoEM/active/summer_students/lir13/External_Relion_Example/test1.jpg')
        #cv2.imshow("Image", im)
        #img = Image.open(im)
        #img.show()
        #plt.imshow(im)
        #img = EMData(im,0)
        #img.write_image("")
        #plt.imshow(edge, interpolation='bilinear')
        #plt.show()

    except Exception as exception: #if error, tell RELION
        traceback.print_exc()