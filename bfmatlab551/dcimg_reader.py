# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 16:08:45 2017

class for reading dcimg files

@author: kner
"""

import dcimg_defs as defs
import numpy as np
ct = defs.ct

dcimgapi = ct.cdll.LoadLibrary('dcimgapi.dll')

class dcimg_reader(object):
    
    def __init__(self, filename):
        iparams = defs.INIT()
        temp = defs.GUID()
        temp.Data4 = ct.c_char_p(b'00000000')
        iparams.guid = ct.pointer(temp)
        iparams.size = ct.sizeof(iparams)
        
        h = dcimgapi.dcimg_init(ct.pointer(iparams))
        if (h!=1):
            print(hex(np.uint32(h)))
        self.iparams = iparams
    
        iopen = defs.OPEN()
        iopen.size = ct.sizeof(iopen)
        iopen.path = defs.LPCSTR(filename.encode())
    
        h = dcimgapi.dcimg_openA(ct.pointer(iopen))
        if (h!=1):
            print(hex(np.uint32(h)))
        self.hdcimg = iopen.hdcimg
        # for matlab declare other member data
        self.width = None
        self.height = None
        self.rowbytes = None
        self.pixelsize = None
        self.totalsessions = None
        self.totalframes = None
        self.data = None
        self.dataset = None
            
    def __del__(self):
        h = dcimgapi.dcimg_close(self.hdcimg)
        if (h==1):
            print('file closed')
        else:
            print('problems')
            print(hex(np.uint32(h)))
    
    def getinfo(self):
        nwidth = ct.c_int32(0)
        h = dcimgapi.dcimg_getparaml( self.hdcimg, defs.DCIMG_IDPARAML_IMAGE_WIDTH, ct.byref(nwidth) )
        if (h!=1):
            print(hex(np.uint32(h)))
        self.width = nwidth.value
        nheight = ct.c_int32(0)
        h = dcimgapi.dcimg_getparaml( self.hdcimg, defs.DCIMG_IDPARAML_IMAGE_HEIGHT, ct.byref(nheight) )
        if (h!=1):
            print(hex(np.uint32(h)))
        self.height = nheight.value
        nrowbytes = ct.c_int32(0)
        h = dcimgapi.dcimg_getparaml( self.hdcimg, defs.DCIMG_IDPARAML_IMAGE_ROWBYTES, ct.byref(nrowbytes) )
        if (h!=1):
            print(hex(np.uint32(h)))
        self.rowbytes = nrowbytes.value
        npixelsize = ct.c_int32(0)        
        h = dcimgapi.dcimg_getparaml( self.hdcimg, defs.DCIMG_IDPARAML_IMAGE_PIXELTYPE, ct.byref(npixelsize) )
        if (h!=1):
            print(hex(np.uint32(h)))
        if not (npixelsize.value == defs.DCIMG_PIXELTYPE_MONO16):
            print('pixel size not 16 bit.')
        self.pixelsize = npixelsize.value
        nsessions = ct.c_int32(0)
        h = dcimgapi.dcimg_getparaml( self.hdcimg, defs.DCIMG_IDPARAML_NUMBEROF_SESSION, ct.byref(nsessions))
        if (h!=1):
            print(hex(np.uint32(h)))
        self.totalsessions = nsessions.value
        # get number of frames
        nframes = ct.c_int32(0)
        h = dcimgapi.dcimg_getparaml( self.hdcimg, defs.DCIMG_IDPARAML_NUMBEROF_TOTALFRAME, ct.byref(nframes))
        if (h!=1):
            print(hex(np.uint32(h)))
        self.totalframes = nframes.value

    def getFrame(self,frameno,sessionno=0):
        h = dcimgapi.dcimg_setsessionindex( self.hdcimg, ct.c_int32(sessionno) )
        if (h!=1):
            print(hex(np.uint32(h)))
    
        iframe = defs.FRAME()
        iframe.size = ct.c_int32(ct.sizeof(iframe))
        iframe.iFrame = ct.c_int32(frameno)
        #data = np.zeros((2048,2048), dtype=np.uint16)
        h = dcimgapi.dcimg_lockframe( self.hdcimg, ct.byref(iframe) )
        if (h!=1):
            print(hex(np.uint32(h)))
        datasize = self.width*self.height
        data = np.fromiter(iframe.buf, dtype=np.uint16, count=datasize)
        self.data = data.reshape(self.width,self.height)
        return True
        
    def getFrames(self,frame_beg,frame_end,sessionno=0):
        if (frame_beg>frame_end) or (frame_beg<0):
            print('Invalid frame values!')
            return False
        if frame_end>self.totalframes:
            print('last frame is greater than total number of frames!')
            return False
            
        h = dcimgapi.dcimg_setsessionindex( self.hdcimg, ct.c_int32(sessionno) )
        if (h!=1):
            print(hex(np.uint32(h)))
        
        Nf = frame_end - frame_beg
        self.dataset = np.zeros((Nf,self.width,self.height), dtype=np.uint16)
        for m in range(Nf):
            self.getFrame(frame_beg+m,sessionno)
            self.dataset[m] = self.data.copy()
        del self.data
        return True