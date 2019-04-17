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

def calculate_window_sums(video_window, index):
    window_sums = np.zeros(len(video_window))
    if((index % 2) == 0):
        for z in range(0, len(video_window), 2):
            window_sums[z] = np.sum(video_window[z])
    else:
        for z in range(1, len(video_window), 2):
            window_sums[z] = np.sum(video_window[z])
    return window_sums
    
def plot_intensity(y, SD, avg, label):
   
    x = np.arange(len(y))
    
    while(len(avg) < len(y)):
        avg.append(avg[len(avg)-10])

    plt.plot(x, y, color='#2F88C0')
    plt.fill_between(x, avg-SD, avg+SD, alpha=0.5, facecolor='#2F88C0')
    plt.plot(x, avg, color='#ff0066')
                     
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
directory = '/media/lauderdale/Samsung_T5/zebrafish_data/GFP_separated'
window_size = 50;
print('Window Size: ' + str(window_size))

print('starting analysis of ' + directory)

data = ImageSequence(directory)
print('Loaded in the data')

print('it takes this long')
num_tif = len(data)
num_frames = num_tif * len(data[0])
total = 0
print('boop')

#initializing np arrays
intensities = np.zeros(num_frames)
window_avgs = np.zeros(num_frames)
window_sums = np.zeros(window_size)
initial_sums = np.zeros(window_size)
final_sums = np.zeros(window_size)

print('entering for loop')
for i in range(num_tif):
    
    print('working on file: ' + str(i))
    video = data[i]#grabbing one ome from the dirrectory
    total = total + np.sum(video)
    
    for z in range(0, window_size):
        initial_sums[z] = np.sum(video[z])
    initial_sum_avg = np.mean(remove_zeros(initial_sums))
    
    for z in range(len(video)-window_size, len(video)):
        for j in range(0, window_size):
            final_sums[j] = np.sum(video[z])
    final_sum_avg = np.mean(remove_zeros(final_sums))
    
    print('here')
    
    for z in range(0, len(video)):
        
        if(z >= window_size and z < len(video)-window_size-1):
            for l in range(0,window_size):
                for n in range(z-window_size, z+window_size):
                    window_sums[l] = np.sum(video[n])
            window_avgs[z] = np.mean(remove_zeros(window_sums))
        elif(z < window_size):
            window_avgs[z] = initial_sum_avg
        elif(z >= len(video)-window_size):
            window_avgs[z] = final_sum_avg
                        
        img = np.array(video[z])
        sum_frame_intensity = np.sum(img)
        intensities[z+(i*1024)] = sum_frame_intensity
     
#np.savetxt('20170706_fish2b___sum_channel_0.csv', intensities, delimiter = ', ')

SD = np.std(remove_zeros(intensities))
avg = np.mean(remove_zeros(intensities))

nonzero_intensities = np.array(remove_zeros(intensities))
plot_intensity(nonzero_intensities, SD, remove_zeros(window_avgs), '0')

print ('Channel 0 sum: ' + str(np.sum(nonzero_intensities)))
print('done')

'''
TODO



'''