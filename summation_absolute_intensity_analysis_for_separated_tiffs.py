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
import pandas as pd 
import os
from pandas import ExcelWriter
from pandas import ExcelFile
    
def plot_intensity(y, SD, avg, label, directory):
   
    x = np.arange(len(y))
    
    while(len(avg) < len(y)):
        avg.append(avg[len(avg)-10])

    plt.plot(x, y, color='#2F88C0')
    plt.fill_between(x, avg-SD, avg+SD, alpha=0.5, facecolor='#2F88C0')
    #plt.plot(x, avg, color='#ff0066')
                     
    plt.xlabel('frame')
    plt.ylabel('summation of intensity (*10^8)')
   
    plt.title(label)
   
    plt.savefig(directory + '/analysis/' + label + '.pdf')

def remove_zeros(arr):
    
    new_arr = []
    for i in range(len(arr)):
        if(arr[i] > 0):
            new_arr.append(arr[i])
    return new_arr

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

#parent dirrectory of the ome files (ie, one fish)
directory = '/media/lauderdale/BFR_RAID5/zebrafish_data/wt/20170714_fish1/gfp_separated'
#'/media/lauderdale/BFR_RAID5/zebrafish_data/ptz/20170629_fish1/gfp_separated/*.tif'
window_size = 50;
print('Window Size: ' + str(window_size))

print('starting analysis of ' + directory)

data = ImageSequence(directory + '/*.tif')
print('Loaded in the data')

num_tif = len(data)
num_frames = len(data[0])
num_frames_total = num_tif * num_frames
start_frame = 100
end_frame = 2828
frame_count = 0
minimum = 300

#initializing np arrays
intensities = np.zeros(num_frames_total)
avg_intensities = np.zeros(num_frames_total)

print('entering for loop for calculating sums')
for i in range(6):
    
    print('working on file: ' + str(i))
    video = data[i]#grabbing one ome from the dirrectory
        
    for z in range(0, len(video)):
        img = np.array(video[z])
        sum_frame_intensity = np.sum(img)
        intensities[z+(i*num_frames)] = sum_frame_intensity
        avg_intensities[z+(i*num_frames)] = np.average(img)
        if (i == 0 and frame_count >= start_frame):
            if (np.amin(img) < minimum):
                minimum = np.amin(img)
        elif (i > 0 and frame_count < end_frame):
            if (np.amin(img) < minimum):
                minimum = np.amin(img)
        frame_count += 1

nonzero_intensities = np.array(remove_zeros(intensities))
nonzero_intensities = nonzero_intensities[start_frame:end_frame]
nonzero_intensities = nonzero_intensities - minimum*2048*1024

avg_intensities = np.array(remove_zeros(avg_intensities))
avg_intensities = avg_intensities[start_frame:end_frame]
SD_avg = np.zeros(len(avg_intensities))

window_avgs = np.zeros(len(nonzero_intensities))
SD_sum = np.zeros(len(nonzero_intensities))

initial_sum_avg = np.mean(nonzero_intensities[:window_size])
initial_SD_sum = np.std(nonzero_intensities[:window_size])
final_sum_avg = np.mean(nonzero_intensities[len(nonzero_intensities)-window_size:])
final_SD_sum = np.std(nonzero_intensities[len(nonzero_intensities)-window_size:])

initial_avg_avg = np.mean(avg_intensities[:window_size])
initial_SD_avg = np.std(avg_intensities[:window_size])
final_avg_avg = np.mean(avg_intensities[len(nonzero_intensities)-window_size:])
final_SD_avg = np.std(avg_intensities[len(nonzero_intensities)-window_size:])

for i in range(window_size):
    window_avgs[i] = initial_sum_avg
    SD_sum[i] = initial_SD_sum
    SD_avg[i] = initial_SD_avg
    
for j in range(len(nonzero_intensities)-window_size, len(nonzero_intensities)):
    window_avgs[j] = final_sum_avg
    SD_sum[j] = final_SD_sum
    SD_avg[i] = final_SD_avg

for t in range(window_size, len(nonzero_intensities)-window_size):
    temp_sum_avg = np.mean(nonzero_intensities[t:t+window_size])
    window_avgs[t] = temp_sum_avg
    SD_sum[t] = np.std(nonzero_intensities[t:t+window_size])
    SD_avg[t] = np.std(avg_intensities[t:t+window_size])
    

video_sum_SD = np.zeros(2728)
video_sum_SD[0] = np.std(nonzero_intensities)
video_sum_avg = np.zeros(2728)
video_sum_avg[0] = np.mean(remove_zeros(intensities))
video_avg = np.zeros(2728)
video_avg[0] = np.average(avg_intensities)

#saving analysis to excel file
try:
    os.mkdir(directory + '/analysis')
except OSError:
    print('GFP directory already exists. May overwrite contents.')

analysis = {'nonzero_intensities': nonzero_intensities, 'SD_sum': SD_sum, 'window_avgs': window_avgs, 'avg_intensities': avg_intensities, 'SD_avg': SD_avg, 'video_sum_SD': video_sum_avg, 'video_sum_avg': video_sum_avg, 'video_avg': video_avg}
file = pd.DataFrame(analysis) 
file.to_csv(directory + '/analysis/analysis_' + make_label(directory) + '.csv')

#plotting the intensity
plot_intensity(nonzero_intensities, SD_sum, window_avgs, 'Summation_of_' + make_label(directory), directory)
plot_intensity(avg_intensities, SD_avg, avg_intensities, 'Averages_of_' + make_label(directory), directory)

print ('total: ' + str(np.sum(nonzero_intensities)))
print ('minimum: ' + str(minimum))
print ('avg: ' + str(video_sum_avg))
print('done')

'''
TODO



'''