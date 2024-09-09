import sys
import numpy as np
import pandas as pd
import starfile
import traceback
import mrcfile
from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseButton
from skimage.filters import roberts, sobel, scharr,prewitt, gaussian, laplace, butterworth
from skimage.feature import canny
from skimage.transform import rescale
import os
# mrcfile folder from mrcfile package (https://pypi.org/project/mrcfile/#files) should be in the above directory (not installed on biowulf)
# goes through autopick.star file and shows each particle. In plot gui, click the magnifying glass and then click on each particle to select the good ones. Green box means it is selected, black box means it has been unselected. To save, close the figures.

def dist_pix(X,Y):
    # Calculate angstrom distance with a given scale of ang/pix and two points' coordinates
    pix_diameter = round((((X[0] - Y[0]) ** 2 + (X[1] - Y[1]) ** 2) ** 0.5))
    return pix_diameter

def dist(X,Y,ang_per_pixel):
    # Calculate angstrom distance with a given scale of ang/pix and two points' coordinates
    ang_diameter = round((((X[0] - Y[0]) ** 2 + (X[1] - Y[1]) ** 2) ** 0.5) * float(ang_per_pixel))
    return ang_diameter
        
def mid(X,Y):
    mid_x = (X[0]+Y[0])/2
    mid_y = (X[1]+Y[1])/2
    mid_coord = (mid_x, mid_y)
    return mid_coord
        
def to_normal(coordinate, scale):
    _x = coordinate[0] * (1/scale)
    _y = coordinate[1] * (1/scale)
    return [_x, _y]

def get_coord(event):
    # Click to get coordinates and show a distance between each two coordinates

    plt.xlim(left = 0)
    plt.ylim(top = 0)

    global x,y
    x, y = event.xdata, event.ydata
    try:
        plt.plot(x, y, 'bo', markersize = 1.5)
    except ValueError:
        pass

    fig.canvas.draw()

    global coords
    if x and y:
        coords.append([round(x),round(y)])
            
            
        if coords and len(coords) % 2 == 0:
            mid_point = mid(coords[-2],coords[-1])
            diameter = dist(coords[-2], coords[-1], PARAM1)
            pix_diameter = dist_pix(coords[-2], coords[-1])

                
            circle = plt.Circle(mid_point, pix_diameter/2, facecolor = 'none', edgecolor='r',linewidth = 1, linestyle = '--')
            ax.add_patch(circle)
            fig.canvas.draw()
                    
                    

            with open(f'{OUTPUT_DIR}/run.out','a') as f: 
                f.write(f'Selected points in pixels: {tuple( to_normal(coords[-2],scale) )} {tuple( to_normal(coords[-1], scale) )}\n')
                f.write(f"The current particle's estimated angstrom diameter is {diameter * (1/scale)}A\n")
                f.write('\n')
                coords.clear()
    else:
        with open(f'{OUTPUT_DIR}/run.out','a') as f: 
            f.write(f'Please click within the micrograph\n')
            f.write('\n')
                

    return



if __name__ == '__main__':

    try:

        OUTPUT_DIR = sys.argv[1] # Job
        MICROGRAPHS = sys.argv[2] # Input Micrograph
        PARAM1 = sys.argv[3] # ang/pix

        #OUTPUT_DIR = 'External/job020/'
        #MICROGRAPHS = 'simulation_1/micrographs.star'
        #PARAM1 = 0.257 # ang/pix

### Output a micrograph (clarity needs to be improve)


        example_mrc = '/mnt/NCEP-CryoEM/active/summer_students/lir13/External_Relion_Example/alan_LDH/bGala_264_00001.mrc'
        with mrcfile.open(example_mrc) as mrc:  # from MotionCorr 002 Micrographs
            mean = np.mean(mrc.data)
            std = np.std(mrc.data)
            im = mrc.data

            # downscale rescale skimage
            scale = 1/4
            ## Gaussian filter to blur image (less noisy), sigma=15 seems to work well
            im = rescale(im, scale, anti_aliasing = False)
            imG = gaussian(im, sigma=15, preserve_range=True)
            imLP = butterworth(imG, 0.02, high_pass=True)
            ## Laplace filter to sharpen edges when subtracted from image (applied to Gaussian filtered image)
            imL = laplace(imLP)
        

        with open(f'{OUTPUT_DIR}/run.out','a') as f: 
            f.write(f'The micrograph has been downscaled by {int(1/scale)}, calculations below are based on original\n')
            f.write('\n')

        with open(f'{OUTPUT_DIR}/circled_micrographs.out','a') as f: 
            f.write(f'{example_mrc}\n')
            f.write('\n')
        

        #plt.imshow(im,cmap='gray', interpolation='bilinear')
        fig, ax = plt.subplots()
        imF = im-imL #easiest to see particles
        #imF = canny(im, sigma = 0.001)

        plt.imshow(im,cmap='gray',interpolation='bilinear')
        #plt.imshow(edge, interpolation='bilinear')


### Interactive part

        coords = []
        cid = fig.canvas.mpl_connect('button_press_event', get_coord)
        plt.show()


        with open(f'{OUTPUT_DIR}/run.out','a') as f: 
            f.write(f'{example_mrc}')
            f.write('\n')


# try other filters to improve resolution of micrographs
# circle needs to be done




#########################

        
        print('Press Continue to next possible micrograph.')
        with open(f'{OUTPUT_DIR}/RELION_JOB_EXIT_SUCCESS','w') as f:
            pass

    except Exception as exception: #if error, tell RELION
        traceback.print_exc()