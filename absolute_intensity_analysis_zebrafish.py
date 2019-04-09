from pims import ImageSequence
import numpy as np
import matplotlib.pyplot as plt

def print_img(arr):
    plt.imshow(arr, cmap = grays)
    plt.show()


def plot_intensity(y, avg):
   
    x = np.arange(len(y))
    x2 = np.arange(len(y))
    y2 = np.empty(len(y))
    y2.fill(avg)
   
    plt.plot(x, y)
    plt.plot(x2, y2, label = 'video average')
   
    plt.xlabel('frame')
    plt.ylabel('avg. intensity')
   
    plt.title('Avg. Intensity over Time')
   
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
        img = np.array(frame[1])
        img = famne[0]
        avg_frame_intensity = np.mean(img)
        intensities[z+(i*512)] = avg_frame_intensity
     
np.savetxt('20170803_fish1.csv', intensities, delimiter = '\n')
nonzero_intensities = np.array(remove_zeros(intensities))
avg_video_intensity = np.mean(nonzero_intensities)
plot_intensity(nonzero_intensities, avg_video_intensity)

print(avg_video_intensity)
print('done')
