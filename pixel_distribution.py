#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 20:05:52 2019

@author: hannah schriever and Branson Byers
"""

from pims import ImageSequence
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import os
from pandas import ExcelWriter
from pandas import ExcelFile
import math

def plot(values, label):
    
    x = np.arange(len(values))

    plt.plot(x, values, color='#2F88C0')
                     
    plt.xlabel('Intensity Values')
    plt.ylabel('Number of Pixels')
   
    plt.title('Distribution of Pixel Intensity: ' + label)
   
    plt.show()

def make_label(directory):
    
    label = ''
    start_adding = False
    
    for i in range(len(directory)):
        if (directory[i] == '2'):
            start_adding = True
        if (start_adding and directory[i] != '/'):
            label += directory[i]
        if (directory[i] == '/' and start_adding):
            break
        
    return label

directory = '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20170629_fish1/gfp_separated'
print('starting analysis of ' + directory)

data = ImageSequence(directory + '/*.tif')
print('Loaded in the data')

#initializing np arrays
#values = np.zeros(1000)

values = np.array(data[0])
values = values.flatten()
plt.hist(values)




'''
print('entering for loop for calculating sums')
for i in range(6):
    
    print('working on file: ' + str(i))
    video = data[i]#grabbing one ome from the dirrectory
    
    for z in range(0, len(video)):
            
        img = video[z]
            
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                
                index = math.floor(img[y,x])
                if(index < len(values)):
                    values[index] += 1
                else:
                    print("index " + str(index) + ' is out of range')
     
    
    for z in range(0, len(video)):
        for y in range(2048):
            for x in range(1024):
                
                index = math.floor(video[z,y,x])
                if(index < len(values)):
                    values[index] += 1
                else:
                    print("index " + str(index) + ' is out of range')
                    
    #values[video[:,:,:]] += 1
    
    video = video.flatten()
    plt.hist(video)     
      '''     
#plot(values, make_label(directory))