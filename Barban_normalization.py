# -*- coding: utf-8 -*-
"""
Spyder Editor

Author: Yang Liu
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#values = pd.read_csv(path)
#value = values.iloc[:].values
import matplotlib.pyplot as plt

class Barban:
    def __init__(self,fps,path):
        self.fps = fps
        
        
    def normalization(self,value,width): 
        """width is sliding window size in seconds, fps is imaging speed 22.72 fps"""
        shape = value.shape
        num_points = shape[0]
        framenum = int(np.round(width*22.72)-1)
        newvalue = np.array([])
        for i in np.arange(framenum,num_points):
            normdata = value[i-framenum:i]
            """get lower 50% value """
            a = np.percentile(normdata, 50, interpolation='midpoint') 
            b = normdata[normdata<a];
            norvalue = value[i]/np.mean(b);
            newvalue = np.append(newvalue,norvalue)
            plt.figure()
            plt.plot(newvalue)
        return newvalue
            
