#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 12:25:31 2019

@author: Hannah C Schriever and J Branson Byers

DATA STRUCTURE
data: (num_tif, frames, y, x)
video: (frame, y, x)

"""

from pims import ImageSequence
import numpy as np
import matplotlib.pyplot as plt

def print_img(arr):
    plt.imshow(arr, cmap = 'grays')
    plt.show()


def plot_intensity(y, errors, error_no_corr, label):
   
    x = np.arange(len(y))

    plt.plot(x, y, color='#2F88C0')
    plt.fill_between(x, y-errors, y+errors, alpha=0.5, facecolor='#2F88C0')
    plt.fill_between(x, y-error_no_corr, y+error_no_corr, alpha=0.5, facecolor='#ff0066')
    
    plt.xlabel('frame')
    plt.ylabel('avg. intensity')
   
    plt.title('Avg. Intensity over Time: Channel ' + label)
   
    plt.show()

def remove_zeros(arr):
    
    new_arr = []
    for i in range(len(arr)):
        if(arr[i] > 0):
            new_arr.append(arr[i])
    return new_arr

#parent dirrectory of the ome files (ie, one fish)
directory = '/media/lauderdale/mnt/remote_servers/data1/image_data/LightSheetMicroscope/20180116/DSLM/fish1_run1_PTZ/fish1_run1_PTZ(10).tif'

print('starting analysis of ' + directory)

data = ImageSequence(directory)
print('Loaded in the data')
num_tif = len(data)

intensities_0 = np.zeros(num_tif * 1024)
errors_0 = np.zeros(num_tif * 1024)
error_not_corrected = np.zeros(num_tif * 1024)
window_SD = np.zeros(num_tif * 1024)
#errors_1 = np.zeros(num_ome * 512)
print('entering for loop')
for i in range(num_tif):
    print('working on file: ' + str(i))
    video = data[i]#grabbing one ome from the dirrectory
    #SD_window = np.std(video)
    for z in range(101, len(video)-101, 2):
        
        SD_window = np.std(video[z-100, z+100])
        img0 = np.array(video[z])
        SD = np.std(img0)
        SD0 = abs(SD_window - np.std(img0))
        avg_frame_intensity_0 = np.mean(img0)
        intensities_0[z+(i*1024)] = avg_frame_intensity_0
        errors_0[z+(i*1024)] = SD0
        error_not_corrected[z+(i*1024)] = SD
        window_SD[z+(i*1024)] = SD_window
     
#np.savetxt('20170706_fish2b___averages_channel_0.csv', intensities_0, delimiter = ', ')
#np.savetxt('20170706_fish2b___averages_channel_1.csv', intensities_1, delimiter = ', ')
#np.savetxt('20170706_fish2b___errors_channel_0.csv', errors_0, delimiter = ', ')
#np.savetxt('20170706_fish2b___errors_channel_1.csv', errors_1, delimiter = ', ')

errors_corrected = np.zeros(num_tif * 1024)
errors_corrected = error_not_corrected - window_SD
errors_corrected = np.absolute(errors_corrected)

nonzero_intensities_0 = np.array(remove_zeros(intensities_0))
#nonzero_intensities_1 = np.array(remove_zeros(intensities_1))
avg_video_intensity_0 = np.mean(nonzero_intensities_0)
#avg_video_intensity_1 = np.mean(nonzero_intensities_1)
plot_intensity(nonzero_intensities_0, remove_zeros(errors_corrected), remove_zeros(error_not_corrected), '26')
#plot_intensity(intensities_1, errors_1, '1')

print ('Channel 0 avg: ' + str(avg_video_intensity_0))
#print ('Channel 1 avg: ' + str(avg_video_intensity_1))
print('done')

'''
TODO

* need to make this analyze both channels
* need to plot both channel analysis with error bars
* need to save excel file with RFP values, GFP values, and SD value
* calculate SD for each frame
* can try to separate the channels by average intensity?
* error can be taken in as a np array

'''
