import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import skimage
import os
import sys
import traceback

sys.path.append('/mnt/NCEP-CryoEM/active/summer_students/lir13/External_Relion_Example/')
import mrcfile

# mrcfile folder from mrcfile package (https://pypi.org/project/mrcfile/#files) should be in the above directory (not installed on biowulf)


# goes through autopick.star file and shows each particle. In plot gui, click the magnifying glass and then click on each particle to select the good ones. Green box means it is selected, black box means it has been unselected. To save, close the figures.

#todo: use param1 for box size

if __name__ == '__main__':
    filt = 'L' #options: '', 'G', 'L' , 'lowpass'
    try:

        OUTPUT_DIR = sys.argv[1]
        MICROGRAPHS = sys.argv[2]
        COORDS = sys.argv[3]
        PARAM1 = sys.argv[4] #box size
        PARAM2 = sys.argv[5] #number of new micrographs to look at per run


        def sq(x0, y0, d,
               fom=-1000):  # draws a square around particle at x0,y0 with edge length d. fom is for showing figure of merit on the image
            x = np.linspace(x0 - 0.5 * d, x0 + 0.5 * d)
            y = np.linspace(y0 - 0.5 * d, y0 + 0.5 * d)
            plt.plot(x, np.min(y) * np.ones(len(x)), c='green')
            plt.plot(x, np.max(y) * np.ones(len(x)), c='green')
            plt.plot(np.max(x) * np.ones(len(y)), y, c='green')
            plt.plot(np.min(x) * np.ones(len(y)), y, c='green')
            if fom != -1000:
                plt.text(x0, y0, fom)


        mrcpaths = []
        appaths = []
        with open(COORDS) as aps:  # read autopick.star to get micrograph and autopick paths
            lines = aps.readlines()
            lines = lines[8::]
            for linei in lines:
                spliti = linei.split()
                if len(spliti) == 2:
                    mrcpaths.append(spliti[0])
                    appaths.append(spliti[1])

        mppaths = []
        ct = 1  # for testing
        mrcpaths_used = []
        for mrcpath, appath in zip(mrcpaths,
                                   appaths):  # loop over all micrographs and coordinate files listed in autopick.star file
            skip = False
            #ct += 1
            if ct > int(PARAM2): #when ct number of micrographs have been analyzed, stop the script
                break

            apsplit = appath.split('/')  # get name for each _manualpick.star file
            n = apsplit[-1]
            n = n.replace('autopick', 'manualpick')
            mppath = f'{OUTPUT_DIR}/Micrographs/{n}'  # used later to name files

            if os.path.isfile(mppath):  # if _manualpick.star file already exists (already went through this micrograph), skip
                skip = True

            if skip:
                pass
            else:
                ct += 1
                print(f'{mrcpath} {appath}')
                # opens 2D micrograph mrc file and reads data, plots it
                with mrcfile.open(mrcpath) as mrc:  # from MotionCorr 002 Micrographs
                    mean = np.mean(mrc.data)
                    std = np.std(mrc.data)
                    im = mrc.data
                    # Gaussian filter to blur image (less noisy), sigma=15 seems to work well
                    imG = skimage.filters.gaussian(mrc.data, sigma=15, preserve_range=True)
                    # Laplace filter to sharpen edges when subtracted from image (applied to Gaussian filtered image)
                    imL = skimage.filters.laplace(imG)

                    imLP = skimage.filters.butterworth(im,0.5,high_pass=False)

                    ylen = len(im)
                    xlen = len(im[0])

                with open(appath) as pf:  # from autopick 066 Micrographs
                    lines = pf.readlines()
                    lines = lines[10::]  # autopick data starts on line 10
                    pl = []
                    for linei in lines:
                        spliti = linei.split()
                        if len(spliti) == 5:  # if line has data (last few lines might be just spaces)
                            pl.append([float(spliti[0]), float(spliti[1]), spliti[2]])  # [x,y,fom]

                #vmin=mean - 3*std,vmax=mean + 3*std #display like RELION with sigma = 3

                # plt.imshow(im,cmap='gray', interpolation='bilinear')
                # plt.figure()
                imF = im-imL #easiest to see particles
                # plt.imshow(imF,cmap='gray',interpolation='bilinear')

                # draw squares on autopicked particles
                d = int(PARAM1)  # used for displaying zoomed in particles
                # for i,p in enumerate(pl):
                #    sq(p[0],p[1],d)

                selected = []


                def onclick(event):
                    for i, ax in enumerate(axes):
                        if event.inaxes == ax:  # find which particle is on this subplot
                            # highlight selected plot
                            print(i)
                            if i not in selected:  # if not already selected, add to selected list
                                selected.append(i)  # defined outside of function
                                # todo: show when selected
                                for j in range(0, 8):
                                    ax.plot([0, d], [j, j], c='green')
                                    ax.plot([0, d], [d - j, d - j], c='green')
                                    ax.plot([j, j], [0, d], c='green')
                                    ax.plot([d - j, d - j], [0, d], c='green')

                            else:  # if already selected, unselect
                                selected.remove(i)
                                for j in range(0, 8):
                                    ax.plot([0, d], [j, j], c='black')
                                    ax.plot([0, d], [d - j, d - j], c='black')
                                    ax.plot([j, j], [0, d], c='black')
                                    ax.plot([d - j, d - j], [0, d], c='black')


                axes = []
                for i, p in enumerate(pl):
                    if i % 12 == 0:  # new figure every 12
                        fig = plt.figure(figsize=(10, 4), dpi=200)
                        cid = fig.canvas.mpl_connect('button_press_event', onclick)
                    axes.append(fig.add_subplot(3, 4, i % 12 + 1))
                    if filt == 'G':
                        plt.imshow(imG[int(p[1] - d * 0.5):int(p[1] + d * 0.5), int(p[0] - d * 0.5):int(p[0] + d * 0.5)], cmap='gray')
                    elif filt == 'L':
                        plt.imshow(imF[int(p[1] - d * 0.5):int(p[1] + d * 0.5), int(p[0] - d * 0.5):int(p[0] + d * 0.5)], cmap='gray', interpolation = 'bilinear')
                    elif filt == 'lowpass':
                        plt.imshow(imLP[int(p[1] - d * 0.5):int(p[1] + d * 0.5), int(p[0] - d * 0.5):int(p[0] + d * 0.5)], cmap='gray', interpolation = 'bilinear')
                    else:
                        plt.imshow(im[int(p[1] - d * 0.5):int(p[1] + d * 0.5), int(p[0] - d * 0.5):int(p[0] + d * 0.5)], cmap='gray', interpolation = 'bilinear')
                    plt.title(p[2])

                plt.tight_layout()
                plt.show()

                # after closing figures, write selected particles to _manualpick.star
                print(selected)

                mppaths.append(mppath)
                mrcpaths_used.append(mrcpath)
                if os.path.isdir(f'{OUTPUT_DIR}/Micrographs') == False:
                    os.mkdir(f'{OUTPUT_DIR}/Micrographs')
                with open(mppath, 'w') as mp:  # write _manualpick.star file
                    mp.write('\n')
                    mp.write('# version 30001\n')
                    mp.write('\n')
                    mp.write('data_\n')
                    mp.write('\n')
                    mp.write('loop_\n')
                    mp.write('_rlnCoordinateX #1\n')
                    mp.write('_rlnCoordinateY #2\n')
                    mp.write('_rlnClassNumber #3\n')
                    mp.write('_rlnAnglePsi #4\n')
                    mp.write('_rlnAutopickFigureOfMerit #5\n')
                    for i in selected:
                        lenxstr = len(str(int(pl[i][0])))
                        lenystr = len(str(int(pl[i][1])))
                        mp.write(
                            f" {str(pl[i][0])}{'.000000'}{' ' * (4 - lenxstr)}{' ' * (6 - lenystr)}{pl[i][1]}{'.000000'}            2   -999.00000   -999.00000 \n")

        # after looping through all micrographs in autopick.star
        #filect = 0
        if os.path.isfile(f'{OUTPUT_DIR}/manualpick.star') == False:
            with open(f'{OUTPUT_DIR}/manualpick.star','w') as mp:  # write manualpick.star file with micrograph and _manualpick.star paths
                mp.write('# version 30001\n')
                mp.write('\n')
                mp.write('data_coordinate_files\n')
                mp.write('loop_\n')
                mp.write('_rlnMicrographName #1 \n')
                mp.write('_rlnMicrographCoordinates #2 \n')
        with open(f'{OUTPUT_DIR}/manualpick.star',
                  'a') as mp:  # append manualpick.star file with micrograph and _manualpick.star paths

            for mrcpath, mppath in zip(mrcpaths_used, mppaths):
                mp.write(f'{mrcpath} {mppath}\n')

        # upon success, write success file so RELION knows it succeeded
        print('SUCCESS! Continue to next micrograph with Continue button.')
        with open(f'{OUTPUT_DIR}/RELION_JOB_EXIT_SUCCESS','w') as f:
            pass


    except Exception as exception: #if error, tell RELION
        traceback.print_exc()
        with open(f'{OUTPUT_DIR}/RELION_JOB_EXIT_FAILURE','w') as f:
            pass

