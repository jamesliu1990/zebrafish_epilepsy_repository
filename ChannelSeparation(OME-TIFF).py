#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 18:03:22 2019

@author: jbransonbyers
"""

from pims import ImageSequence
import pims
import numpy as np
import matplotlib.pyplot as plt
import sys
import tifffile as tf
import os
#from skimage.io._plugins import freeimage_plugin as fi
#from libtiff import TIFF


#This script takes ome.tif files as an argument, determines which channel should be RFP and which is GFP
#assuming that the first frame of GFP is brighter than the first frame of RFP. Two files are then saved.
#One for GFP and one for RFP.



list_of_parent_directories = ['/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170714_fish1',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170714_fish2',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170714_fish3',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170714_fish4',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170720_fish1',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170720_fish2',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170720_fish3',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170720_fish4',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170725_fish1',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170725_fish2',\
                              \
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20170627_fish3',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20170628_fish1',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20170629_fish1',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20170629_fish2',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20170803_fish1',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20170810_fish1',\
                              '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20180116_fish1']

for parent_directory in list_of_parent_directories:

    ####################
    
    #parent_directory = '/Volumes/Samsung_T5/zebrafish_data'
    file_list = []
    for root, dirs, files in os.walk(parent_directory):
        for file in files:
            if file.endswith('.tif') and not file.endswith('_suspectedGFP.tif') \
            and not file.endswith('_suspectedRFP.tif') \
            and not file.endswith('_designatedRFP.tif') \
            and not file.endswith('_designatedGFP.tif'):
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
        print('Loading pointer to data...')
        data = np.array(pims.open(directory))
        print('The data has been loaded in...')
        
        
        
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
            rfp_designation = image1
            gfp_designation = image2
            
        else:
            print('Image 2 was brighter. Second frame designated as RFP')
            gfp = data[0::2]
            rfp = data[1::2]
            rfp_designation = image2
            gfp_designation = image1
                
                
        ##########Saving the data as filename_suspectedXFP.tif##########
        gfp_save_dir = directory.rsplit('/',1)[0] + '/gfp_separated' 
        rfp_save_dir = directory.rsplit('/',1)[0] + '/rfp_separated'
        manual_check_dir = directory.rsplit('/',1)[0] + '/manual_channel_check'
                
        print('Creating directories...')
        try:
            os.mkdir(gfp_save_dir)
        except OSError:
            print('GFP directory already exists. May overwrite contents.')
                    
        try:
            os.mkdir(rfp_save_dir)
        except OSError:
            print('RFP directory already exists. May overwrite contents.')     
            
        try:
            os.mkdir(manual_check_dir)
        except OSError:
            print('Manual check directory already exists. May overwrite contents.') 
        
        
        print('Saving to directories...')
        gfp_filename = gfp_save_dir + '/' + filename + '_suspectedGFP.tif'
        tf.imsave(gfp_filename, gfp, bigtiff=True) 
        print('GFP saved')
        
        rfp_filename = rfp_save_dir + '/' + filename + '_suspectedRFP.tif'
        tf.imsave(rfp_filename, rfp, bigtiff=True)
        print('RFP saved')
        
        rfp_manual_filename = manual_check_dir + '/' + filename + '_designatedRFP.tif'
        tf.imsave(rfp_manual_filename, rfp_designation)
        print('RFP manual check saved')
        
        gfp_manual_filename = manual_check_dir + '/' + filename + '_designatedGFP.tif'
        tf.imsave(gfp_manual_filename, gfp_designation)
        print('GFP manual check saved')
        
print('Script complete.')
                            
                            
                            
                            
    
    
    
    