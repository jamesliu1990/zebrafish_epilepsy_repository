#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 15:42:15 2019

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


def plot_intensity(y, SD, avg, label):
   
    x = np.arange(len(y))
    

    plt.plot(x, y, color='#2F88C0')
    plt.fill_between(x, avg-SD, avg+SD, alpha=0.5, facecolor='#2F88C0')
    
    plt.xlabel('frame')
    plt.ylabel('summation of intensity (*10^8)')
   
    plt.title('Summation of Intensity over Time: Channel ' + label)
   
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

intensities = np.zeros(num_tif * 1024)
total = 0
print('entering for loop')
for i in range(num_tif):
    print('working on file: ' + str(i))
    video = data[i]#grabbing one ome from the dirrectory
    total = total + np.sum(video)
    for z in range(0, len(video), 2):
        
        img = np.array(video[z])
        sum_frame_intensity = np.sum(img)
        intensities[z+(i*1024)] = sum_frame_intensity
     
#np.savetxt('20170706_fish2b___sum_channel_0.csv', intensities, delimiter = ', ')

SD = np.std(remove_zeros(intensities))
avg = np.mean(remove_zeros(intensities))

nonzero_intensities = np.array(remove_zeros(intensities))
plot_intensity(nonzero_intensities, SD, avg, '0')

print ('Channel 0 sum: ' + str(np.sum(nonzero_intensities)))
print('done')

'''
TODO



'''

