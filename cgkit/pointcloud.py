# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is the Python Computer Graphics Kit.
#
# The Initial Developer of the Original Code is Matthias Baas.
# Portions created by the Initial Developer are Copyright (C) 2009
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
# $Id: riutil.py,v 1.1.1.1 2004/12/12 14:31:21 mbaas Exp $

# Point cloud test

import ctypes
import rmanlibutil

class PtcReader:
    def __init__(self, fileName, libName):
        """Constructor.
        
        fileName is the name of the point cloud file and libName the name
        of the shared library that implements the point cloud API.
        """
        
        self._handle = None
        
        ptclib = self._loadPtcLib(libName)
        
        # Store the functions pointers that are still required
        self._PtcReadDataPoint = ptclib.PtcReadDataPoint
        self._PtcClosePointCloudFile = ptclib.PtcClosePointCloudFile

        self._PtcGetPointCloudInfo = ptclib.PtcGetPointCloudInfo

        # Just open the file to find out the number of variables in the file...
        nvars = ctypes.c_int()
        handle = ptclib.PtcOpenPointCloudFile(fileName, ctypes.byref(nvars), None, None)
        if handle is None:
            raise IOError("Cannot open point cloud file %s"%fileName)
        ptclib.PtcClosePointCloudFile(handle)
        
        # Now prepare storage for the variable names and types and open the file for real...
        numVars = nvars.value
        types = (numVars*ctypes.c_char_p)()
        names = (numVars*ctypes.c_char_p)()
        handle = ptclib.PtcOpenPointCloudFile(fileName, ctypes.byref(nvars), types, names)
        if handle is None:
            raise IOError("Cannot open point cloud file %s"%fileName)
        
        self._handle = handle

        self.variables = []
        self.npoints = None
        self.bbox = None
        self.datasize = None
        self.world2eye = None
        self.world2ndc = None
        self.format = None
        
        code = ""
        idx = 0
        for i in range(numVars):
            name = names[i]
            type = types[i]
            self.variables.append((type, name))
            if type=="float":
                code += "dataDict['%s'] = data[%s]\n"%(name,idx)
                idx += 1
            elif type in ["vector", "point", "normal", "color"]:
                code += "dataDict['%s'] = data[%s:%s]\n"%(name,idx,idx+3)
                idx += 3
            elif type=="matrix":
                code += "dataDict['%s'] = data[%s:%s]\n"%(name,idx,idx+16)
                idx += 16
            else:
                raise RuntimeError("Unknown variable type in point cloud file: %s"%type)
        # Compile the code that will pick the correct data components and put them into a dict
        self._dataCollectionCode = compile(code, "<string>", "exec")
        
        n = ctypes.c_int()
        ptclib.PtcGetPointCloudInfo.argtypes = [ptclib.PtcPointCloud, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        if ptclib.PtcGetPointCloudInfo(handle, "npoints", ctypes.byref(n))==1:
            self.npoints = n.value
        if ptclib.PtcGetPointCloudInfo(handle, "datasize", ctypes.byref(n))==1:
            self.datasize = n.value
        ptclib.PtcGetPointCloudInfo.argtypes = [ptclib.PtcPointCloud, ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
        b = (6*ctypes.c_float)()
        if ptclib.PtcGetPointCloudInfo(handle, "bbox", b)==1:
            self.bbox = list(b)
        f = (3*ctypes.c_float)()
        if ptclib.PtcGetPointCloudInfo(handle, "format", f)==1:
            self.format = list(f)
        m = (16*ctypes.c_float)()
        if ptclib.PtcGetPointCloudInfo(handle, "world2eye", m)==1:
            self.world2eye = list(m)
        if ptclib.PtcGetPointCloudInfo(handle, "world2ndc", m)==1:
            self.world2ndc = list(m)

        if self.datasize is None:
            raise IOError("Could not obtain datasize value from point cloud file %s."%fileName)

        # Set up storage for reading individual data points
        self._pos = (3*ctypes.c_float)()
        self._normal = (3*ctypes.c_float)()
        self._radius = ctypes.c_float()
        self._data = (self.datasize*ctypes.c_float)()

    def __del__(self):
        self.close()
    
    def close(self):
        if self._handle is not None:
            print "CLOSE ptc file"
            self._PtcClosePointCloudFile(self._handle)
            self._handle = None
    
    def readDataPoint(self):
        if self._handle is None:
            raise IOError("The point cloud file has already been closed.")
        
        res = self._PtcReadDataPoint(self._handle, self._pos, self._normal, self._radius, self._data)
        if res==0:
            return None
        else:
            dataDict = {}
            data = self._data
            exec self._dataCollectionCode
            return tuple(self._pos), tuple(self._normal), self._radius.value, dataDict


    def _loadPtcLib(self, libName):
        """Load a RenderMan library providing the point cloud API.
        """
        resolvedLibName = rmanlibutil.resolveRManLib(libName)
        ptclib = ctypes.cdll.LoadLibrary(resolvedLibName)
        
        ptclib.PtcPointCloud = ctypes.c_void_p
        
        # Reading point cloud files
        ptclib.PtcOpenPointCloudFile.argtypes = [ctypes.c_char_p,
                                                 ctypes.POINTER(ctypes.c_int),
                                                 ctypes.POINTER(ctypes.c_char_p),
                                                 ctypes.POINTER(ctypes.c_char_p)]
        ptclib.PtcOpenPointCloudFile.restype = ptclib.PtcPointCloud
        
        ptclib.PtcGetPointCloudInfo.argtypes = [ptclib.PtcPointCloud, ctypes.c_char_p, ctypes.c_char_p]
        ptclib.PtcGetPointCloudInfo.restype = ctypes.c_int
        
        ptclib.PtcReadDataPoint.argtypes = [ptclib.PtcPointCloud,
                                            ctypes.POINTER(ctypes.c_float),
                                            ctypes.POINTER(ctypes.c_float),
                                            ctypes.POINTER(ctypes.c_float),
                                            ctypes.POINTER(ctypes.c_float)]
        ptclib.PtcReadDataPoint.restype = ctypes.c_int
        
        ptclib.PtcClosePointCloudFile.argtypes = [ptclib.PtcPointCloud]
        ptclib.PtcClosePointCloudFile.restype = None
        
        return ptclib
    
    
class PtcWriter:
    def __init__(self, fileName, vars, world2eye, world2ndc, format, libName):
        """Constructor.
        
        fileName is the name of the point cloud file and libName the name
        of the shared library that implements the point cloud API.
        """
        
        self._handle = None
        
        ptclib = self._loadPtcLib(libName)
        
        # Store the functions pointers that are still required
        self._PtcWriteDataPoint = ptclib.PtcWriteDataPoint
        self._PtcFinishPointCloudFile = ptclib.PtcFinishPointCloudFile

        xres,yres,aspect = format
        
        m = (16*ctypes.c_float)()
        m[0] = 1.0
        m[5] = 1.0
        m[10] = 1.0
        m[15] = 1.0
        
        n = len(vars)
        cvartypes = (n*ctypes.c_char_p)()
        cvarnames = (n*ctypes.c_char_p)()
        idx = 0
        code = ""
        for i in range(n):
            type,name = vars[i]
            cvartypes[i] = type
            cvarnames[i] = name
            if type=="float":
                code += "cdata[%s] = data.get('%s', 0.0)\n"%(idx, name)
                idx += 1
            elif type in ["vector", "point", "normal", "color"]:
                code += "cdata[%s:%s] = data.get('%s', (0.0,0.0,0.0))\n"%(idx,idx+3,name)
                idx += 3
            elif type=="matrix":
                code += "cdata[%s:%s] = data.get('%s'), (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))\n"%(idx,idx+16,name)
                idx += 16
            else:
                raise RuntimeError("Unknown point cloud variable type: %s"%type)

        self._dataSize = idx
        self._dataInitCode = code
        
        cformat = (3*ctypes.c_float)(float(xres), float(yres), float(aspect))
        
        handle = ptclib.PtcCreatePointCloudFile(fileName, n, cvartypes, cvarnames, m, m, cformat)
        if handle is None:
            raise IOError("Cannot open point cloud file %s for writing"%fileName)

        self._handle = handle
        
    def __del__(self):
        self.close()
    
    def close(self):
        if self._handle is not None:
            print "CLOSE ptc file (write)"
            self._PtcFinishPointCloudFile(self._handle)
            self._handle = None

    def writeDataPoint(self, point, normal, radius, data):
        """Write a point into the point cloud file.
        
        point and normal are vectors (any 3-sequence of floats) and radius
        a float. data is a dict that contains the extra variables that
        must have been declared in the constructor. Undeclared values are
        ignored, missing declared valued are set to 0.
        """
        if self._handle is None:
            raise IOError("The point cloud file has already been closed.")

        p = (3*ctypes.c_float)(*tuple(point))
        n = (3*ctypes.c_float)(*tuple(normal))
        cdata = (self._dataSize*ctypes.c_float)()
        exec self._dataInitCode
        res = self._PtcWriteDataPoint(self._handle, p, n, radius, cdata)
        if res==0:
            raise IOError("Failed to write point cloud data point")

    def _loadPtcLib(self, libName):
        """Load a RenderMan library providing the point cloud API.
        """
        resolvedLibName = rmanlibutil.resolveRManLib(libName)
        ptclib = ctypes.cdll.LoadLibrary(resolvedLibName)
        
        ptclib.PtcPointCloud = ctypes.c_void_p

        # Writing point cloud files
        ptclib.PtcCreatePointCloudFile.argtypes = [ctypes.c_char_p,
                                                   ctypes.c_int,
                                                   ctypes.POINTER(ctypes.c_char_p),
                                                   ctypes.POINTER(ctypes.c_char_p),
                                                   ctypes.POINTER(ctypes.c_float),
                                                   ctypes.POINTER(ctypes.c_float),
                                                   ctypes.POINTER(ctypes.c_float)]
        ptclib.PtcCreatePointCloudFile.restype = ptclib.PtcPointCloud
        
        ptclib.PtcWriteDataPoint.argtypes = [ptclib.PtcPointCloud,
                                             ctypes.POINTER(ctypes.c_float),
                                             ctypes.POINTER(ctypes.c_float),
                                             ctypes.c_float,
                                             ctypes.POINTER(ctypes.c_float)]
        ptclib.PtcWriteDataPoint.restype = ctypes.c_int
        
        ptclib.PtcFinishPointCloudFile.argtypes = [ptclib.PtcPointCloud]
        ptclib.PtcFinishPointCloudFile.restype = None
        
        return ptclib


def open(fileName, mode="r", libName=None, **kwargs):
    """Open a point cloud file for reading or writing.
    """
    if mode=="r":
        return PtcReader(fileName, libName, **kwargs)
    elif mode=="w":
        return PtcWriter(fileName, libName=libName, **kwargs)
    else:
        raise ValueError('Invalid file mode: "%s" (expected "r" or "w")'%mode)

###################################################################

if __name__=="__main__":
    from cgkit.cgtypes import *
    import random
    
    if 1:
        print "---WRITE---"
        ptc = open("test.ptc", "w", "3delight", vars=[("float", "spam"), ("vector", "dir")], world2eye=None, world2ndc=None, format=(320,240,1.333))
        for i in range(100):
            x = random.random()
            y = random.random()
            z = random.random()
            ptc.writeDataPoint((x,y,z), (0,1,0), 0.2, {"spam":0.5})
        ptc.close()
    
    print "----READ----"
    rd = open("test.ptc", "r", "3delight")
    print rd.variables
    print "npoints:",rd.npoints
    print "datasize",rd.datasize
    print "bbox",rd.bbox
    print "format",rd.format
    print "world2eye",rd.world2eye
    print "world2ndc",rd.world2ndc
    p,n,r,data = rd.readDataPoint()
    print p,n,r,data
    print rd.readDataPoint()
