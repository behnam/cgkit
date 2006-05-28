###########################################################################
# cgkit - Python Computer Graphics Kit
# Copyright (C) 2004 Matthias Baas (baas@ira.uka.de)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# cgkit homepage: http://cgkit.sourceforge.net
###########################################################################
# $Id: motionpath.py,v 1.2 2006/01/27 07:51:02 mbaas Exp $

from cgkit.component import Component
from cgkit.slots import *
from math import *

# MotionPath
class MotionPath(Component):
    """Motion path.
    """
    
    def __init__(self,
                 name = "MotionPath",
                 curve = None,
                 begintime = 0.0,
                 endtime = 1.0,
                 loop = False,
                 follow = False,
                 bank = False,
                 bankamplitude = 0.1,
                 auto_insert = True):
        """Constructor.
        """
        Component.__init__(self, name=name, auto_insert=auto_insert)
        
        self.curve = curve

        self.begintime = begintime
        self.endtime = endtime
        self.loop = loop
        self.follow = follow
        self.bank = bank
        self.bankamplitude = bankamplitude

        self.transform_slot = ProceduralMat4Slot(self.computeTransform)
        self.time_slot = DoubleSlot()
        self.time_slot.addDependent(self.transform_slot)
        self.addSlot("transform", self.transform_slot)
        self.addSlot("time", self.time_slot)

    # computeTransform
    def computeTransform(self):
        """Procedural for the transform slot.
        """

        # Determine the native curve parameter t...
        time = self.time_slot.getValue()
        len = self.curve.length()
        s = (time-self.begintime)/(self.endtime-self.begintime)
        if self.loop:
            s %= 1.0
        s *= len
        if s<0:
            s = 0.0
        if s>len:
            s = len
        t = self.arcLenToCurveParam(s)

        # Evaluate the curve
        p, dp, d2p = self.curve.evalFrame(t)

        up = vec3(0,0,1)
        if self.follow:
            try:
                T = mat4().lookAt(p, p+dp, up)
            except:
                T = mat4().translation(p)
        else:
            T = mat4().translation(p)

        if self.bank:
            dp = dp.normalize()

            dt = 0.001
            dp_prev = self.curve.deriv(t-dt).normalize()
            d2p = (dp-dp_prev)/dt
            # Make the 2nd derivative orthogonal to the tangent...
            len = d2p.length()
            u = d2p.cross(dp)
            d2p = dp.cross(u)
            d2p = len*d2p.normalize()            
            if (dp.cross(up)*d2p<0):
                len = -len
            T = T*mat4().rotation(self.bankamplitude*len, vec3(0,0,1))
        return T

    # arcLenToCurveParam
    def arcLenToCurveParam(self, s, eps=0.0001, maxiter=100):
        """Determine the native curve parameter for a given arc length.
        """
        tmin, tmax = self.curve.paraminterval
        totallen = self.curve.arcLen(tmax)
        # Initial "guess"...
        t = tmin+(s/totallen)*(tmax-tmin)

        while maxiter>0:
            F = self.curve.arcLen(t)-s
            if abs(F)<=eps:
                return t

            dF = self.curve.deriv(t).length()
            if abs(dF)<1E-12:
                # TODO: do something
                print "MotionPath: ************ dF==0 !!!"
                dF = 1 
            t -= F/dF
            maxiter -= 1

        print "MotionPath: Maximum number of iterations reached (s=%f)"%s
        return t
        
        
