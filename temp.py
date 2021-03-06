from pims import ImageSequence
import pims
import numpy as np
import matplotlib.pyplot as plt
import sys
import tifffile as tf
import os
#from skimage.io._plugins import freeimage_plugin as fi
#from libtiff import TIFF


#This script takes a tiff stack as an argument, determines which channel should be RFP and which is GFP
#assuming that the first frame of GFP is brighter than the first frame of RFP. Two files are then saved.
#One for GFP and one for RFP.



list_of_parent_directories = ['/Volumes/Samsung_T5/zebrafish_data']

for parent_directory in list_of_parent_directories:

    ####################
    
    #parent_directory = '/Volumes/Samsung_T5/zebrafish_data'
    file_list = []
    for root, dirs, files in os.walk(parent_directory):
        for file in files:
            if file.endswith('.tif'):
                file_list.append(os.path.join(root, file))
                
                
                ####################
                
                
                
    for directory in file_list:
        #insert the directory here
        #directory = sys.argv[1] #name of the file should be included in the command line
        
        #directory = '/Users/jbransonbyers/Hard_Storage/zebrafish_project/server_mount/droplet/data1/image_data/LightSheetMicroscope/20180116/DSLM/fish1_run1_PTZ/fish1_run1_PTZ(1).tif'
        #directory = '/Users/jbransonbyers/Desktop/Bransonwithboxes.tiff'
        #directory = '/Users/jbransonbyers/Hard_Storage/zebrafish_project/temp_data/fish1_run1_PTZ(1).tif'
        #directory = '/Volumes/Samsung_T5/zebrafish_data/fish1_run1_PTZ(1).tif'
        #directory = '/Volumes/Samsung_T5/zebrafish_data/*.tif'
        filename = directory.rsplit('/',1)[1].split('.',2)[0]#trims out the file name (includeding tif extension)
        print('The filename is: ' + filename)
        print('Starting channel separation of ' + directory)
        
        
        #Shape of the data when read in as a tiff
        #Coordinate 0: stack number (1)
        #Coordinate 1: number of frames (1023)
        #Coodinate 2: height in pixels (1024)
        #Coordinate 3: width in pixels (2048)
        #data = np.array(ImageSequence(directory), 'uint16')
        data = np.array(pims.open(directory))
        print('The data has been loaded in')
        
        
        
        ##########Pull out first sencond frames. One is GFP. One is RFP.##########
        image1 = data[0]
        image2 = data[1]
        print('videos read into variables')
        
        #show the images
        print('Image 1')
        plt.imshow(image1, cmap = 'gray')
        plt.show()
        
        print('Image 2')
        plt.imshow(image2, cmap = 'gray')
        plt.show()
        print('images plotted')
        
        
        
        ###########Determine which is GFP and which is RFP##########
        print('comparing images')
        if np.sum(image1) > np.sum(image2):
            print('Image 1 was brighter. First frame designated RFP.')
            rfp = data[0::2]
            gfp = data[1::2]
            
        else:
            print('Image 2 was brighter. Second frame designated as RFP')
            gfp = data[0::2]
            rfp = data[1::2]
                
                
                
        ##########Saving the data as filename_suspectedXFP.tif##########
        gfp_save_dir = directory.rsplit('/',1)[0] + '/GFP_separated' 
        rfp_save_dir = directory.rsplit('/',1)[0] + '/RFP_separated'
                
        print('Creating directories...')
        try:
            os.mkdir(gfp_save_dir)
        except OSError:
        print('GFP directory already exists. May overwrite contents.')
                    
        try:
            os.mkdir(rfp_save_dir)
        except OSError:
        print('RFP directory already exists. May overwrite contents.')        
        
        
        print('Saving to directories...')
        gfp_filename = gfp_save_dir + '/' + filename + '_suspectedGFP.tif'
        tf.imsave(gfp_filename, gfp, bigtiff=True) 
        print('GFP saved')
        
        rfp_filename = rfp_save_dir + '/' + filename + '_suspectedRFP.tif'
        tf.imsave(rfp_filename, rfp, bigtiff=True)
        print('RFP saved')
        
        print('Script complete.')
                            
                            
                            
                            
    
    
    
    