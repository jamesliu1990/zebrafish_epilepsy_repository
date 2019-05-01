# -*- coding: utf-8 -*-
"""
Created on Tue Jun 06 14:28:32 2017

@author: kner
"""

import numpy as np
import ctypes as ct

dcimgapi = ct.cdll.LoadLibrary('dcimgapi.dll')
#dcimgapi = ct.WinDLL('dcimgapi.dll')

#BEGIN_DCIMG_DECLARE( struct, DCIMG_OPENA )
#{
#	int32			size;				// [in] size of this structure
#	int32			reserved;
#	HDCIMG			hdcimg;				// [out]
#	LPCSTR			path;				// [in] DCIMG file path
#}
#END_DCIMG_DECLARE( DCIMG_OPENA )

#DCIMG_IDPARAML
DCIMG_IDPARAML_NUMBEROF_TOTALFRAME = 0			# number of total frame in the file
DCIMG_IDPARAML_NUMBEROF_SESSION = 1			# number of session in the file.
DCIMG_IDPARAML_NUMBEROF_FRAME = 2				# number of frame in current session.
DCIMG_IDPARAML_SIZEOF_USERDATABIN_SESSION = 4      # byte size of current session binary USER META DATA.
DCIMG_IDPARAML_SIZEOF_USERDATABIN_FILE = 5		# byte size of file binary USER META DATA.
DCIMG_IDPARAML_SIZEOF_USERDATATEXT_SESSION = 7     # byte size of current session text USER META DATA.
DCIMG_IDPARAML_SIZEOF_USERDATATEXT_FILE = 8	     # byte size of file text USER META DATA.
DCIMG_IDPARAML_IMAGE_WIDTH = 9					# image width in current session.
DCIMG_IDPARAML_IMAGE_HEIGHT = 10			     # image height in current session.
DCIMG_IDPARAML_IMAGE_ROWBYTES = 11				# image rowbytes in current session.
DCIMG_IDPARAML_IMAGE_PIXELTYPE = 12				# image pixeltype in current session.
DCIMG_IDPARAML_MAXSIZE_USERDATABIN = 13	            # maximum byte size of frame binary USER META DATA in current session.
DCIMG_IDPARAML_MAXSIZE_USERDATABIN_SESSION =14	# maximum byte size of session binary USER META DATA in the file.
DCIMG_IDPARAML_MAXSIZE_USERDATATEXT = 16	      # maximum byte size of frame text USER META DATA in current session.
DCIMG_IDPARAML_MAXSIZE_USERDATATEXT_SESSION = 17    # maximum byte size of session tex USER META DATA in the file.
DCIMG_IDPARAML_CURRENT_SESSION = 19		      # current session index
DCIMG_IDPARAML_NUMBEROF_VIEW = 20				# number of view in current session.
DCIMG_IDPARAML_FILEFORMAT_VERSION = 21			# file format version
DCIMG_IDPARAML_CAPABILITY_IMAGEPROC = 22		# capability of image processing

class GUID(ct.Structure):
        _fields_ = [("Data1", ct.c_uint32), ("Data2", ct.c_ushort), 
                    ("Data3", ct.c_ushort), ("Data4", ct.c_char_p)]
                    
class INIT(ct.Structure):
    _fields_ = [("size", ct.c_int32), ("reserved", ct.c_int32), ("guid", ct.POINTER(GUID))]
    
    
LPCSTR = ct.c_char_p
HDCIMG = ct.c_void_p
class OPEN(ct.Structure):
    _fields_ = [("size", ct.c_int32), ("reserved", ct.c_int32), 
                ("hdcimg", HDCIMG), ("path", LPCSTR)]

# DCIMG_PIXELTYPE
DCIMG_PIXELTYPE_NONE		= 0x00000000
DCIMG_PIXELTYPE_MONO8		= 0x00000001
DCIMG_PIXELTYPE_MONO16	= 0x00000002
PIXELTYPE = ct.c_int32

class TIMESTAMP(ct.Structure):
    _fields_ = [("sec", ct.c_uint32), ("microsec", ct.c_int32)]

''' copyframe() and lockframe() use this structure. Some members have different direction.
	[i:o] means, the member is input at copyframe() and output at lockframe().
	[i:i] and [o:o] means always input and output at both function.
	"input" means application has to set the value before calling.
	"output" means function filles a value at returning. '''
class FRAME(ct.Structure):
     _fields_ = [("size", ct.c_int32), ("iKind", ct.c_int32),
                ("option", ct.c_int32),
                ("iFrame", ct.c_int32), ("buf", ct.POINTER(ct.c_uint16)), 
                ("rowbytes", ct.c_int32), ("type", PIXELTYPE),
                ("width", ct.c_int32), ("height", ct.c_int32),
                ("left", ct.c_int32), ("top", ct.c_int32),
                ("timestamp", TIMESTAMP), ("framestamp", ct.c_int32),
                ("camerastamp", ct.c_int32), ("conversionfactor_coeff", ct.c_double),
                ("conversionfactor_offset", ct.c_double)]

def read_frame(fn='test2.dcimg'):
    ''' simple example of pulling out basic information and one frame from
        dcimg file '''
        
    #fn = 'test2.dcimg'
    h=0
    iparams = INIT()
    temp = GUID()
    temp.Data4 = ct.c_char_p('00000000')
    iparams.guid = ct.pointer(temp)
    iparams.size = ct.sizeof(iparams)
    
    h = dcimgapi.dcimg_init(ct.pointer(iparams))
    print(hex(np.uint32(h)))
    
    iopen = OPEN()
    iopen.size = ct.sizeof(iopen)
    iopen.path = LPCSTR(fn)
    
    h = dcimgapi.dcimg_openA(ct.pointer(iopen))
    print(hex(np.uint32(h)))
    
    nwidth = ct.c_int32(0)
    h = dcimgapi.dcimg_getparaml( iopen.hdcimg, DCIMG_IDPARAML_IMAGE_WIDTH, ct.byref(nwidth) )
    print(hex(np.uint32(h)))
    print(nwidth.value)
    
    nframes = ct.c_int32(0)
    h = dcimgapi.dcimg_getparaml( iopen.hdcimg, DCIMG_IDPARAML_NUMBEROF_TOTALFRAME, ct.byref(nframes) )
    print(hex(np.uint32(h)))
    print(nframes.value)
    
    nsessions = ct.c_int32(0)
    h = dcimgapi.dcimg_getparaml( iopen.hdcimg, DCIMG_IDPARAML_NUMBEROF_SESSION, ct.byref(nsessions) )
    print(hex(np.uint32(h)))
    print(nsessions.value)
    
    h = dcimgapi.dcimg_setsessionindex( iopen.hdcimg, ct.c_int32(0) )
    print(hex(np.uint32(h)))
    
    iframe = FRAME()
    iframe.size = ct.c_int32(ct.sizeof(iframe))
    iframe.iFrame = ct.c_int32(10)
    #data = np.zeros((2048,2048), dtype=np.uint16)
    h = dcimgapi.dcimg_lockframe( iopen.hdcimg, ct.byref(iframe) )
    print(hex(np.uint32(h)))
    data = np.fromiter(iframe.buf, dtype=np.uint16, count=(2048*2048))
    
    h = dcimgapi.dcimg_close(iopen.hdcimg)
    print(hex(np.uint32(h)))
    return data

