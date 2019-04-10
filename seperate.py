# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 21:22:07 2019

@author: Liu Yang, Kner Lab.
"""

import tifffile as tf
import numpy as N
import pylab as P


class seperatechannel(object):
    
    def __init__(self,img_stack=None):
        self.img = img_stack
        self.str1 = 'gfp.tif'
        self.str2 = 'rfp.tif'
        
    def sep(self,img):
#        test = img[0]
#        small = test[518:518+200,930:930+200] ## random pick a region to evaluate
#        if test.sum() > 110:
#            n = 0
#        else:
#            n=1
        n=0
        img1 = img[n]
        img2 = img[n+1]
            
        if img1.sum() > img2.sum():
            gfp = img[0::2]
            rfp = img[1::2]
        else:
            rfp = img[1::2]
            gfp = img[0::2]
        self.gfp = gfp
        self.rfp = rfp
        tf.imsave(self.str1,gfp.astype('uint16')) ## save the gfp rfp seperatly 
        tf.imsave(self.str2,rfp.astype('uint16'))
        
#    def analyize(self):
#        gfp = self.gfp
#        rfp = self.rfp