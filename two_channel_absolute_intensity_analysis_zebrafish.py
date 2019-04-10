'''

Created on Fri Apr  5 16:40:12 2019

@author: Hannah C Schriever and J Branson Byers

DATA STRUCTURE:
    2 channels
    1024x2048 pixels
    512 frames
    
VARIABLES:
    data: (num_ome, 512, 2, 2048, 1024)
    video: (512, 2, 2048, 1024)
    frame: (2, 2048, 1024)
    img: (2048, 1024)
    
can itterate through, it will take it out one at a time and do the analysis.
DO NOT put entire think in np array

ImageSequence(dir)[0] seems to be an entire video with 2 channels
which cnannel is the right one?

GOALS
    average intensity of ENTIRE VIDEO - frame wise
    get avg intensity for each frame, then average those

'''

from pims import ImageSequence
import numpy as np
import matplotlib.pyplot as plt

def print_img(arr):
    plt.imshow(arr, cmap = 'grays')
    plt.show()


def plot_intensity(y, errors, lable):
   
    x = np.arange(len(y))

    plt.plot(x, y, color='#2F88C0')
    plt.fill_between(x, y-errors, y+errors, alpha=0.5, edgecolor='#2F88C0', facecolor='#2F88C0')
   
    plt.xlabel('frame')
    plt.ylabel('avg. intensity')
   
    plt.title('Avg. Intensity over Time: Channel' + label)
   
    plt.show()

def remove_zeros(arr):
    
    new_arr = []
    for i in range(len(arr)):
        if(arr[i] > 0):
            new_arr.append(arr[i])
    return new_arr


#parent dirrectory of the ome files (ie, one fish)
directory = '/media/lauderdale/mnt/remote_servers/data1/image_data/LightSheetMicroscope/20170803/*.tif'

print('starting analysis of ' + directory)

data = ImageSequence(directory)
print('Loaded in the data')
num_ome = len(data)

video = data[0]
frame = video[100]
img = np.array(frame[0])
print_img(img)

img = np.array(frame[1])
print_img(img)

intensities = np.zeros(num_ome * 512)
print('entering for loop')
for i in range(num_ome):
    print('working on file: ' + str(i))
    video = data[i]#grabbing one ome from the dirrectory
    for z in range(len(video)):
        frame = video[z]#still has both channels
        img0 = np.array(frame[0])
        img1 = np.array(frame[1])
        SD0 = np.std(img0)
        SD1 = np.std(img1)
        avg_frame_intensity_0 = np.mean(img0)
        avg_frame_intensity_1 = np.mean(img1)
        intensities_0[z+(i*512)] = avg_frame_intensity_0
        intensities_1[z+(i*512)] = avg_frame_intensity_1
        errors_0[z+(i*512)] = SD0
        errors_1[z+(i*512)] = SD1
     
np.savetxt('20170803_fish1___averages_channel_0.csv', intensities_0, delimiter = ', ')
np.savetxt('20170803_fish1___averages_channel_1.csv', intensities_1, delimiter = ', ')
np.savetxt('20170803_fish1___errors_channel_0.csv', errors_0, delimiter = ', ')
np.savetxt('20170803_fish1___errors_channel_1.csv', errors_1, delimiter = ', ')

nonzero_intensities_0 = np.array(remove_zeros(intensities_0))
nonzero_intensities_1 = np.array(remove_zeros(intensities_1))
avg_video_intensity_0 = np.mean(nonzero_intensities_0)
avg_video_intensity_0 = np.mean(nonzero_intensities_1)
plot_intensity(intensities_0, errors_0, '0')
plot_intensity(intensities_1, errors_1, '1')

print ('Channel 0 avg: ' + str(avg_video_intensity_0))
print ('Channel 1 avg: ' + str(avg_video_intensity_1))
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
