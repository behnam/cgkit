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
# Portions created by the Initial Developer are Copyright (C) 2004
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
# -------------------------------------------------------------
# The RenderMan (R) Interface Procedures and Protocol are:
# Copyright 1988, 1989, 2000, Pixar
# All Rights Reserved
#
# RenderMan (R) is a registered trademark of Pixar
# -------------------------------------------------------------
# $Id: ri.py,v 1.4 2006/02/14 19:29:39 mbaas Exp $

import ctypes, types, re
import _cri
from _cri import importRINames
import ri

def loadRI(libName):
    """Load a RenderMan library and return a module-like handle to it.
    
    libName is the name of a shared library that implements the RenderMan
    interface. The name can either be an absolute file name or just the
    name of the library (without suffix or "lib" prefix) in which case 
    the function tries to find the library file itself.
    The return value is the library handle as returned by the ctypes 
    LoadLibrary() function. This handle has already been prepared so that
    it can be used like a module that contains the RenderMan interface.
    """
 
    _ri = _cri.loadRI(libName)
    
    return _RenderManAPI(_ri)

class _RenderManAPI:
    
    def __init__(self, rimod):
        self._ri = rimod
        
        # Regular expression to parse declarations
        self._declRe = re.compile(r"^\s*(?:(constant|uniform|varying|vertex) )?\s*"
                                   "(float|integer|string|color|point|vector|normal|matrix|hpoint)\s*"
                                   "(?:\[\s*([0-9]+)\s*\])?\s*(\w+)$")
        
        # Copy the RI_ and Rt attributes...
        for name in dir(rimod):
            if name[:2] in ["Rt", "RI"]:
                setattr(self, name, getattr(rimod, name))
                
        for name in ["RiErrorAbort", "RiErrorIgnore", "RiErrorPrint",
                     "RiBoxFilter", "RiTriangleFilter", "RiCatmullRomFilter",
                     "RiGaussianFilter", "RiSincFilter",
                     "RiBezierBasis", "RiBSplineBasis", "RiCatmullRomBasis",
                     "RiHermiteBasis", "RiPowerBasis"]:
            if hasattr(rimod, name):
                setattr(self, name, getattr(rimod, name))
                
        # Copy the doc strings from the ri module into the Ri methods...
#        for name in dir(self):
#            method = getattr(self.__class__, name)
#            if not callable(method):
#                continue
#            func = getattr(ri, name, None)
#            if func is not None and hasattr(func, "__doc__"):
#                method.__doc__ = func.__doc__

        # Key: Variable name - Value: (class, type, n)
        self._declarations = {}
        self._standardDeclarations(self._ri)
        
    def _getRiLastError(self):
        return self._ri.RiLastError
    
    def _setRiLastError(self, val):
        self._ri.RiLastError = val
        
    RiLastError = property(_getRiLastError, _setRiLastError)
    LastError = property(_getRiLastError, _setRiLastError)
        
    def RiArchiveRecord(self, type, format, *args):
        self._ri.RiArchiveRecord(type, format, *args)

    def RiAreaLightSource(self, name, *paramlist, **keyparams):
        self._ri.RiAreaLightSource(name, *self._createCParamList(paramlist, keyparams))

    def RiAtmosphere(self, name, *paramlist, **keyparams):
        self._ri.RiAtmosphere(name, *self._createCParamList(paramlist, keyparams))

    def RiAttribute(self, name, *paramlist, **keyparams):
        self._ri.RiAttribute(name, *self._createCParamList(paramlist, keyparams))
        
    def RiAttributeBegin(self):
        self._ri.RiAttributeBegin()

    def RiAttributeEnd(self):
        self._ri.RiAttributeEnd()

    def RiBasis(self, ubasis, ustep, vbasis, vstep):
        ubasis = self._toCArray(self._ri.RtFloat, ubasis)
        vbasis = self._toCArray(self._ri.RtFloat, vbasis)
        self._ri.RiBasis(ubasis, ustep, vbasis, vstep)

    def RiBegin(self, name):
        self._ri.RiBegin(name)
        
    def RiBlobby(self, nleaf, code, floats, strings, *paramlist, **keyparams):
        code = self._toCArray(self._ri.RtInt, code)
        floats = self._toCArray(self._ri.RtFloat, floats)
        strings = self._toCArray(self._ri.RtString, strings)
        self._ri.RiBlobby(nleaf, len(code), code, len(floats), floats, len(strings), strings, *self._createCParamList(paramlist, keyparams))

    def RiBound(self, bound):
        bound = self._toCArray(self._ri.RtFloat, bound)
        self._ri.RiBound(bound)

    def RiClipping(self, near, far):
        self._ri.RiClipping(near, far)
        
    def RiClippingPlane(self, x, y, z, nx, ny, nz):
        self._ri.RiClippingPlane(x, y, z, nx, ny, nz)
    
    def RiColor(self, Cs):
        Cs = self._toCArray(self._ri.RtFloat, Cs)
        self._ri.RiColor(Cs)
        
    def RiColorSamples(self, nRGB, RGBn):
        nRGB = self._toCArray(self._ri.RtFloat, nRGB)
        RGBn = self._toCArray(self._ri.RtFloat, RGBn)
        if len(nRGB)!=len(RGBn):
            raise ValueError, "The conversion matrices must have the same number of elements."
        if len(nRGB)%3!=0:
            raise ValueError, "Invalid number of elements in the conversion matrices."
        n = len(nRGB)/3
        self._ri.RiColorSamples(n, nRGB, RGBn)

    def RiConcatTransform(self, transform):
        transform = self._toCArray(self._ri.RtFloat, transform)
        self._ri.RiConcatTransform(transform)
        
    def RiCone(self, height, radius, thetamax, *paramlist, **keyparams):
        self._ri.RiCone(height, radius, thetamax, *self._createCParamList(paramlist, keyparams))

    def RiContext(self, handle):
        self._ri.RiContext(handle)
    
    def RiCoordinateSystem(self, spacename):
        self._ri.RiCoordinateSystem(spacename)
        
    def RiCoordSysTransform(self, spacename):
        self._ri.RiCoordSysTransform(spacename)
    
    def RiCropWindow(self, left, right, bottom, top):
        self._ri.RiCropWindow(left, right, bottom, top)
        
    def RiCurves(self, type, nvertices, wrap, *paramlist, **keyparams):
        nvertices = self._toCArray(self._ri.RtInt, nvertices)
        self._ri.RiCurves(type, len(nvertices), nvertices, wrap, *self._createCParamList(paramlist, keyparams))

    def RiCylinder(self, radius,zmin,zmax,thetamax,*paramlist, **keyparams):
        self._ri.RiCylinder(radius, zmin, zmax, thetamax, *self._createCParamList(paramlist, keyparams))
   
    def RiDeclare(self, name, declaration):

        # Process the declaration internally so that parameter lists can be
        # constructed properly...
        decl = "%s %s"%(declaration, name)
        m = self._declRe.match(decl)
        if m is None:
            raise ValueError, "Invalid declaration: %s"%decl
        # Groups is a 4-tuple (class, type, n, name)
        grps = m.groups()
        self._declarations[grps[3]] = grps[:3]
        
        # Forward the call...
        return self._ri.RiDeclare(name, declaration)

    def RiDepthOfField(self, fstop, focallength, focaldistance):
        self._ri.RiDepthOfField(fstop, focallength, focaldistance)
        
    def RiDetail(self, bound):
        bound = self._toCArray(self._ri.RtFloat, bound)
        self._ri.RiDetail(bound)
    
    def RiDetailRange(self, minvisible, lowertransition, uppertransition, maxvisible):
        self._ri.RiDetailRange(minvisible, lowertransition, uppertransition, maxvisible)

    def RiDisk(self, height, radius, thetamax, *paramlist, **keyparams):
        self._ri.RiDisk(height, radius, thetamax, *self._createCParamList(paramlist, keyparams))

    def RiDisplacement(self, name, *paramlist, **keyparams):
        self._ri.RiDisplacement(name, *self._createCParamList(paramlist, keyparams))
        
    def RiDisplay(self, name, type, mode, *paramlist, **keyparams):
        self._ri.RiDisplay(name, type, mode, *self._createCParamList(paramlist, keyparams))

    def RiEnd(self):
        self._ri.RiEnd()
        
    def RiErrorHandler(self, handler):
        try:
            self._ri.RiErrorHandler(handler)
        except ctypes.ArgumentError:
            self._ri.RiErrorHandler(self._ri.RtErrorHandler(handler))

    def RiExposure(self, gain, gamma):
        self._ri.RiExposure(gain, gamma)

    def RiExterior(self, name, *paramlist, **keyparams):
        self._ri.RiExterior(name, *self._createCParamList(paramlist, keyparams))
    
    def RiFormat(self, xres, yres, aspect):
        self._ri.RiFormat(xres, yres, aspect)
        
    def RiFrameAspectRatio(self, frameratio):
        self._ri.RiFrameAspectRatio(frameratio)

    def RiFrameBegin(self, number):
        self._ri.RiFrameBegin(number)

    def RiFrameEnd(self):
        self._ri.RiFrameEnd()

    def RiGeneralPolygon(self, nverts, *paramlist, **keyparams):
        nverts = self._toCArray(self._ri.RtInt, nverts)
        self._ri.RiGeneralPolygon(len(nverts), nverts, *self._createCParamList(paramlist, keyparams))

    def RiGeometricApproximation(self, type, value):
        self._ri.RiGeometricApproximation(type, value)
        
    def RiGeometry(self, type, *paramlist, **keyparams):
        self._ri.RiGeometry(type, *self._createCParamList(paramlist, keyparams))

    def RiGetContext(self):
        return self._ri.RiGetContext()
    
    def RiHider(self, type, *paramlist, **keyparams):
        self._ri.RiHider(type, *self._createCParamList(paramlist, keyparams))

    def RiHyperboloid(self, point1, point2, thetamax, *paramlist, **keyparams):
        point1 =self._toCArray(self._ri.RtFloat, point1)
        point2 =self._toCArray(self._ri.RtFloat, point2)
        self._ri.RiHyperboloid(point1, point2, thetamax, *self._createCParamList(paramlist, keyparams))

    def RiIdentity(self):
        self._ri.RiIdentity()
        
    def RiIlluminate(self, light, onoff):
        self._ri.RiIlluminate(light, onoff)
        
    def RiImager(self, name, *paramlist, **keyparams):
        self._ri.RiImager(name, *self._createCParamList(paramlist, keyparams))
   
    def RiInterior(self, name, *paramlist, **keyparams):
        self._ri.RiInterior(name, *self._createCParamList(paramlist, keyparams))

    def RiLightSource(self, name, *paramlist, **keyparams):
        return self._ri.RiLightSource(name, *self._createCParamList(paramlist, keyparams))

    def RiMakeCubeFaceEnvironment(self, px,nx,py,ny,pz,nz, texname, fov, filterfunc, swidth, twidth, *paramlist, **keyparams):
        self._ri.RiMakeCubeFaceEnvironment(px, nx, py, ny, pz, nz, texname, fov, self._ri.RtFilterFunc(filterfunc), swith, twidth, *self._createCParamList(paramlist, keyparams))

    def RiMakeLatLongEnvironment(self, picname, texname, filterfunc, swidth, twidth, *paramlist, **keyparams):
        self._ri.RiMakeLatLongEnvironment(picname, texname, self._ri.RtFilterFunc(filterfunc), swith, twidth, *self._createCParamList(paramlist, keyparams))
        
    def RiMakeShadow(self, picname, shadowname, *paramlist, **keyparams):
        self._ri.RiMakeShadow(picname, texname, *self._createCParamList(paramlist, keyparams))

    def RiMakeTexture(self, picname, texname, swrap, twrap, filterfunc, swidth, twidth, *paramlist, **keyparams):
        self._ri.RiMakeTexture(picname, texname, swrap, twrap, self._ri.RtFilterFunc(filterfunc), swith, twidth, *self._createCParamList(paramlist, keyparams))

    def RiMatte(self, onoff):
        self._ri.RiMatte(onoff)

    def RiMotionBegin(self, *times):
        # For some reason the time values must be doubles...
        times = tuple(map(lambda v: ctypes.c_double(v), self._flatten(times)))
        self._ri.RiMotionBegin(len(times), *times)
        
    def RiMotionEnd(self):
        self._ri.RiMotionEnd()

    def RiNuPatch(self, nu, uorder, uknot, umin, umax, nv, vorder, vknot, vmin, vmax, *paramlist, **keyparams):
        uknot = self._toCArray(self._ri.RtFloat, uknot)
        vknot = self._toCArray(self._ri.RtFloat, vknot)
        self._ri.RiNuPatch(nu, uorder, uknot, umin, umax, nv, vorder, vknot, vmin, vmax, *self._createCParamList(paramlist, keyparams))

    def RiObjectBegin(self, *paramlist, **keyparams):
        return self._ri.RiObjectBegin(*self._createCParamList(paramlist, keyparams))
        
    def RiObjectEnd(self):
        self._ri.RiObjectEnd()
    
    def RiObjectInstance(self, handle):
        self._ri.RiObjectInstance(handle)

    def RiOpacity(self, Os):
        Os = self._toCArray(self._ri.RtFloat, Os)
        self._ri.RiOpacity(Os)

    def RiOption(self, name, *paramlist, **keyparams):
        self._ri.RiOption(name, *self._createCParamList(paramlist, keyparams))

    def RiOrientation(self, orientation):
        self._ri.RiOrientation(orientation)

    def RiParaboloid(self, rmax, zmin, zmax, thetamax, *paramlist, **keyparams):
        self._ri.RiParaboloid(rmax, zmin, zmax, thetamax, *self._createCParamList(paramlist, keyparams))

    def RiPatch(self, type, *paramlist, **keyparams):
        self._ri.RiPatch(type, *self._createCParamList(paramlist, keyparams))

    def RiPatchMesh(self, type, nu, uwrap, nv, vwrap, *paramlist, **keyparams):
        self._ri.RiPatchMesh(type, nu, uwrap, nv, vwrap, *self._createCParamList(paramlist, keyparams))

    def RiPerspective(self, fov):
        self._ri.RiPerspective(fov)

    def RiPixelFilter(self, function, xwidth, ywidth):
        xwidth = self._ri.RtFloat(xwidth)
        ywidth = self._ri.RtFloat(ywidth)
        # Try passing the function in directlry first (in case it's a standard
        # filter). If this fails, function must be a custom filter.
        try:
            self._ri.RiPixelFilter(function, xwidth, ywidth)
        except ctypes.ArgumentError:
            self._ri.RiPixelFilter(self._ri.RtFilterFunc(function), xwidth, ywidth)
    
    def RiPixelSamples(self, xsamples, ysamples):
        self._ri.RiPixelSamples(xsamples, ysamples)

    def RiPixelVariance(self, variance):
        self._ri.RiPixelVariance(variance)
    
    def RiPoints(self, *paramlist, **keyparams):
        params = self._createCParamList(paramlist, keyparams)
        for i in range(0, len(params), 2):
            if params[i]=="P":
                n = len(params[i+1])
                if n%3!=0:
                    raise ValueError, 'Invalid number of floats in the "P" parameter.'
                n /= 3  
                break
        else:
            raise ValueError, 'Parameter "P" is missing.'  
        self._ri.RiPoints(n, *params)

    def RiPointsGeneralPolygons(self, nloops, nverts, vertids, *paramlist, **keyparams):
        nloops = self._toCArray(self._ri.RtInt, nloops)
        nverts = self._toCArray(self._ri.RtInt, nverts)
        vertids = self._toCArray(self._ri.RtInt, vertids)
        self._ri.RiPointsGeneralPolygons(len(nloops), nloops, nverts, vertids, *self._createCParamList(paramlist, keyparams))

    def RiPointsPolygons(self, nverts, vertids, *paramlist, **keyparams):
        nverts = self._toCArray(self._ri.RtInt, nverts)
        vertids = self._toCArray(self._ri.RtInt, vertids)
        self._ri.RiPointsPolygons(len(nverts), nverts, vertids, *self._createCParamList(paramlist, keyparams))

    def RiPolygon(self, *paramlist, **keyparams):
        params = self._createCParamList(paramlist, keyparams)
        for i in range(0, len(params), 2):
            if params[i]=="P":
                n = len(params[i+1])
                if n%3!=0:
                    raise ValueError, 'Invalid number of floats in the "P" parameter.'
                n /= 3  
                break
        else:
            raise ValueError, 'Parameter "P" is missing.'  
        self._ri.RiPolygon(n, *params)

    def RiProcedural(self, data, bound, subdividefunc, freefunc):
        raise RuntimeError, "Not yet supported"

    def RiProjection(self, name, *paramlist, **keyparams):
        self._ri.RiProjection(name, *self._createCParamList(paramlist, keyparams))

    def RiQuantize(self, type, one, min, max, ditheramplitude):
        self._ri.RiQuantize(type, one, min, max, ditheramplitude)

    def RiReadArchive(self, filename, callback=None, *ignore):
        raise RuntimeError, "Not yet supported"

    def RiRelativeDetail(self, relativedetail):
        self._ri.RiRelativeDetail(relativedetail)

    def RiReverseOrientation(self):
        self._ri.RiReverseOrientation()

    def RiRotate(self, angle, *axis):
        axis = self._toCArray(self._ri.RtFloat, axis)
        self._ri.RiRotate(angle, *tuple(axis))

    def RiScale(self, *scale):
        scale = self._toCArray(self._ri.RtFloat, scale)
        self._ri.RiScale(*tuple(scale))

    def RiScreenWindow(self, left, right, bottom, top):
        self._ri.RiScreenWindow(left, right, bottom, top)

    def RiShadingInterpolation(self, type):
        self._ri.RiShadingInterpolation(type)

    def RiShadingRate(self, size):
        self._ri.RiShadingRate(size)

    def RiShutter(self, opentime, closetime):
        self._ri.RiShutter(opentime, closetime)

    def RiSides(self, nsides):
        self._ri.RiSides(nsides)

    def RiSkew(self, angle, *vecs):
        vecs = self._flatten(vecs)
        self._ri.RiSkew(angle, *vecs)
        
    def RiSolidBegin(self, type):
        self._ri.RiSolidBegin(type)

    def RiSolidEnd(self):
        self._ri.RiSolidEnd()

    def RiSphere(self, radius,zmin,zmax,thetamax,*paramlist, **keyparams):
        self._ri.RiSphere(radius, zmin, zmax, thetamax, *self._createCParamList(paramlist, keyparams))

    def RiSubdivisionMesh(self, scheme, nverts, vertids, tags, nargs, intargs, floatargs, *paramlist, **keyparams):
        nverts = self._toCArray(self._ri.RtInt, nverts)
        vertids = self._toCArray(self._ri.RtInt, vertids)
        tags = self._toCArray(self._ri.RtToken, tags)
        nargs = self._toCArray(self._ri.RtInt, nargs)
        intargs = self._toCArray(self._ri.RtInt, intargs)
        floatargs = self._toCArray(self._ri.RtFloat, floatargs)
        self._ri.RiSubdivisionMesh(scheme, len(nverts), nverts, vertids, len(tags), tags, nargs, intargs, floatargs, *self._createCParamList(paramlist, keyparams))

    def RiSurface(self, name, *paramlist, **keyparams):
        self._ri.RiSurface(name, *self._createCParamList(paramlist, keyparams))

    def RiTextureCoordinates(self, s1, t1, s2, t2, s3, t3, s4, t4):
        self._ri.RiTextureCoordinates(s1, t1, s2, t2, s3, t3, s4, t4)

    def RiTorus(self, major, minor, phimin, phimax, thetamax, *paramlist, **keyparams):
        self._ri.RiTorus(major, minor, phimin, phimax, thetamax, *self._createCParamList(paramlist, keyparams))
        
    def RiTransform(self, transform):
        transform = self._toCArray(self._ri.RtFloat, transform)
        self._ri.RiTransform(transform)

    def RiTransformBegin(self):
        self._ri.RiTransformBegin()

    def RiTransformEnd(self):
        self._ri.RiTransformEnd()

    def RiTransformPoints(self, fromspace, tospace, points):
        raise RuntimeError, "not yet implemented (interface?)"
        points = self._toCArray(self._ri.RtFloat, points)
        n = len(points)/3
        res = self._ri.RiTransformPoints(fromspace, tospace, n, points)
        return res
    
    def RiTranslate(self, *translate):
        translate = self._toCArray(self._ri.RtFloat, translate)
        self._ri.RiTranslate(*tuple(translate))
    
    def RiTrimCurve(self, ncurves, order, knot, min, max, n, u, v, w):
        ncurves = self._toCArray(self._ri.RtInt, ncurves)
        order = self._toCArray(self._ri.RtInt, order)
        knot = self._toCArray(self._ri.RtFloat, knot)
        min = self._toCArray(self._ri.RtFloat, min)
        max = self._toCArray(self._ri.RtFloat, max)
        n = self._toCArray(self._ri.RtInt, n)
        u = self._toCArray(self._ri.RtFloat, u)
        v = self._toCArray(self._ri.RtFloat, v)
        w = self._toCArray(self._ri.RtFloat, w)
        self._ri.RiTrimCurve(len(ncurves), ncurves, order, knot, min, max, n, u, v, w)

    def RiWorldBegin(self):
        self._ri.RiWorldBegin()

    def RiWorldEnd(self):
        self._ri.RiWorldEnd()

        
    def _toCArray(self, ctype, seq):
        """Convert and flatten a sequence into a ctypes array.
        
        ctype is the base type of the array and seq is the sequence that is
        to be flattened and converted. The return value is a ctypes
        array type with ctype as element type.
        """
        # Check if seq is already a ctypes sequence
        seq = self._flatten(seq)
        return (len(seq)*ctype)(*seq)
        
    def _flatten(self, seq):
        """Return a list of the individual items in a (possibly nested) sequence.
        """
        res = []
        ScalarTypes = [types.IntType, types.LongType, types.FloatType, types.StringType]
        for v in seq:
            vtype = type(v)
            # v=scalar?
            if vtype in ScalarTypes:
                res.append(v)
            # no scalar or string. Then it's supposed to be a sequence
            else:
                res += self._flatten(v)
        return res
        
    def _createCParamList(self, paramlist, keyparams):    
        """
        Combine the keyparams with the paramlist into one paramlist
        and convert sequence values.
        Appends None (RI_NULL) to the parameter list.
        """
        res = list(paramlist)
        # Check if the number of values is uneven (this is only allowed when
        # the last value is None (RI_NULL) in which case this last value is ignored)
        if (len(res)%2==1):
           if res[-1] is None:
               res = res[:-1]
           else:
               raise ValueError, "The parameter list must contain an even number of values" 

        # Append the params from the keyparams dict to the parameter list
        map(lambda param: res.extend(param), keyparams.iteritems())
    
        # Check if the values need conversion...
        for i in range(0, len(res), 2):
            token = res[i].strip()
            
            ##### Determine the type of the variable #####
            
            # Try to process any inline declaration...
            m = self._declRe.match(token)
            # No inline declaration or invalid declaration...
            if m is None:
                # If the token doesn't contain a space then it must have been 
                # just a name without inline declaration. In this case, try
                # to get the declaration from the previously declared tokens...
                if token.find(" ")==-1:
                    decl = self._declarations.get(token, None)
                    if decl is None:
                        raise ValueError, 'Token "%s" is not declared.'%token
                else:
                    raise ValueError, 'Invalid inline declaration: %s'%token
            else:
                decl = m.groups()[:3]
                
            cls,type,n = decl
            
            # The actual size is not checked here, so we only determine
            # the "base" type...
            if type=="integer":
                ctype = self._ri.RtInt
            elif type=="string":
                ctype = self._ri.RtString
            else:
                ctype = self._ri.RtFloat 
            
            # Is the value already a ctypes array? Then there's nothing to do
            # TODO: Check if the array is of the correct type (_type_ is type)
            if isinstance(res[i+1], ctypes.Array):
                continue
            # Convert the value(s) into a ctypes array (even single values
            # must be converted)...
            values = self._flatten([res[i+1]])
            # Convert the sequence into a ctypes array...
            res[i+1] = (len(values)*ctype)(*values)

        res.append(None)
        return res

    def _standardDeclarations(self, ri):
        """Predeclare standard parameters.
        """
        decls = {ri.RI_AMPLITUDE:"uniform float",
                 ri.RI_BACKGROUND:"color",
                 ri.RI_BEAMDISTRIBUTION:"float",
                 ri.RI_CONEANGLE:"float",
                 ri.RI_CONEDELTAANGLE:"float",
                 ri.RI_CONSTANTWIDTH:"constant float",
                 ri.RI_CS:"varying color",
                 ri.RI_DISTANCE:"float",
                 ri.RI_FOV:"float",
                 ri.RI_FROM:"point",
                 ri.RI_INTENSITY:"float",
                 ri.RI_KA:"uniform float",
                 ri.RI_KD:"uniform float",
                 ri.RI_KR:"uniform float",
                 ri.RI_KS:"uniform float",
                 ri.RI_LIGHTCOLOR:"color",
                 ri.RI_MAXDISTANCE:"float",
                 ri.RI_MINDISTANCE:"float",
                 ri.RI_N:"varying normal",
                 ri.RI_NP:"uniform normal",
                 ri.RI_ORIGIN:"integer[2]",
                 ri.RI_OS:"varying color",
                 ri.RI_P:"vertex point", 
                 ri.RI_PW:"vertex hpoint",
                 ri.RI_PZ:"vertex point",
                 ri.RI_ROUGHNESS:"uniform float",
                 ri.RI_S:"varying float", 
                 ri.RI_SPECULARCOLOR:"uniform color",
                 ri.RI_ST:"varying float[2]",
                 ri.RI_T:"varying float",
                 ri.RI_TEXTURENAME:"string",
                 ri.RI_TO:"point",
                 ri.RI_WIDTH:"varying float",
                 "shader":"string",
                 "archive":"string",
                 "texture":"string",
                 "procedural":"string",
                 "endofframe":"integer",
                 "sphere":"float",
                 "coordinatesystem":"string",
                 "name":"string",
                 "sense":"string"
                }
        
        # Fill the declarations dict...
        for name,decl in decls.iteritems():
            m = self._declRe.match("%s %s"%(decl, name))
            grps = m.groups()
            self._declarations[grps[3]] = grps[:3]
