#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 09:25:44 2019

@author: hannah schriever and branson byers
"""

import pandas as pd 
import os
import matplotlib.pyplot as plt
from pandas import ExcelFile
import numpy as np

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

def plot_intensity(y, SD, avg, label):
   
    x = np.arange(len(y))
    
    while(len(avg) < len(y)):
        avg.append(avg[len(avg)-10])

    plt.plot(x, y, color='#2F88C0')
    plt.fill_between(x, avg-SD, avg+SD, alpha=0.5, facecolor='#2F88C0')
    #plt.plot(x, avg, color='#ff0066')
                     
    plt.xlabel('frame')
    plt.ylabel('summation of intensity (*10^8)')
   
    plt.title('Summation of Intensity over Time: Channel ' + label)
   
    plt.show()

    
#store excel file data in arrays
'''
directories = ['/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170714_fish1/gfp_separated/analysis',\
               '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170714_fish2/gfp_separated/analysis',\
               '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170714_fish4/gfp_separated/analysis',\
               '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170720_fish1/gfp_separated/analysis',\
               '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170720_fish2/gfp_separated/analysis',\
               '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170720_fish3/gfp_separated/analysis',\
               '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170725_fish1/gfp_separated/analysis',\
               '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170725_fish2/gfp_separated/analysis',\
               '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20170628_fish1/gfp_separated/analysis',\
               '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20170629_fish1/gfp_separated/analysis',\
               '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20170629_fish2/gfp_separated/analysis',\
               '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20170810_fish1/gfp_separated/analysis',\
               '/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20180116_fish1/gfp_separated/analysis']
'''
directories = ['/home/lauderdale/Desktop']

nonzero_intensities = [len(directories)]
SD = [len(directories)]
window_avgs = [len(directories)]
avg_intensities = [len(directories)]
video_sum_SD = [len(directories)]
video_sum_avg = [len(directories)]
video_avg = [len(directories)]

for i in range(len(directories)):

    directory = directories[i]
    
    csv_read = pd.read_csv(directory + '/analysis.csv', sep = ',')
    nonzero_intensities[i] = np.array(csv_read['nonzero_intensities'])
    SD[i] = np.array(csv_read['SD'])
    window_avgs[i] = np.array(csv_read['window_avgs'])
    avg_intensities[i] = np.array(csv_read['avg_intensities'])
    video_sum_SD[i] = np.array(csv_read['video_sum_SD'])
    video_sum_avg[i] = np.array(csv_read['video_sum_avg'])
    video_avg[i] = np.array(csv_read['video_avg'])
    

plot_intensity(nonzero_intensities[0], SD[0], window_avgs[0], 'Summation of ' + make_label(directory))

#pass those arrays into graphers that label and save them in analysis folder
    #average graph
    #summation graph
    #dot plot average graph
    #dot plot summation graph
    
    
    
    
'''

WT
20170714_fish1
20170714_fish2
20170714_fish4
20170720_fish1
20170720_fish2
20170720_fish3
20170725_fish1
20170725_fish2

PTZ
20170628_fish1
20170629_fish1
20170629_fish2
20170810_fish1
20180116_fish1

analysis = {'nonzero_intensities': nonzero_intensities, 'SD': SD, 'window_avgs': window_avgs, 'avg_intensities': avg_intensities, 'video_sum_SD': video_sum_avg, 'video_sum_avg': video_sum_avg, 'video_avg': video_avg}

'''