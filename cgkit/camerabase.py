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
# $Id: camerabase.py,v 1.1 2005/05/12 12:58:28 mbaas Exp $

## \file camerabase.py
## Contains the CameraBase class.

"""This module contains the CameraBase class."""

from Interfaces import *
import protocols
import slots
from cgtypes import *
from math import pi
from worldobject import WorldObject
from scene import getScene
import _core

# CameraBase
class CameraBase(WorldObject):
    """Base class for camera objects.
    """

    def __init__(self,
                 auto_nearfar = True,
                 nearplane = 0.1,
                 farplane = 1000,
                 **params):
        WorldObject.__init__(self, **params)

        self.nearplane_slot = slots.DoubleSlot(nearplane)
        self.farplane_slot = slots.DoubleSlot(farplane)
        self.autonearfar_slot = slots.BoolSlot(auto_nearfar)
        self.addSlot("nearplane", self.nearplane_slot)
        self.addSlot("farplane", self.farplane_slot)
        self.addSlot("autonearfar", self.autonearfar_slot)

    # "output" property...
    exec slots.slotPropertyCode("nearplane")
    exec slots.slotPropertyCode("farplane")
    exec slots.slotPropertyCode("autonearfar")
    

    def protocols(self):
        return [ISceneItem, IComponent, IWorldObject, ICamera]

    # eyeRay
    def eyeRay(self, x0, y0, width, height):
        """Return a ray from the eye position through an image point.

        This method returns a ray whose origin is at the eye position
        and that goes through a given point on the image plane. The
        point on the plane is given by (x0, y0) which each ranges from
        0 to 1. (0,0) is at the upper left and (1,1) at the lower right.
        The arguments width and height determine the ratio of the image
        plane (the absolute values of width and height are irrelevant).
        The return value is a 2-tuple (p,u) where p is the ray origin
        and u the normalized direction. Both vectors are given in world
        space.
        """
        V = self.viewTransformation()
        P = self.projection(width, height, 1, 10)
        R = mat4().rotation(pi, vec3(0,1,0))
        if getScene().handedness=='l':            
            S = mat4().scaling(vec3(-1,1,1))
            I = (P*S*R*V).inverse()
        else:
            I = (P*R*V).inverse()
        x = 2.0*x0-1.0
        y = 1.0-2.0*y0
        q = I*vec3(x,y,0)
        p = self.worldtransform[3]
        p = vec3(p.x, p.y, p.z)
        return (p, (q-p).normalize())

    # getNearFar
    def getNearFar(self):
        """Return the distances to the near and far clipping plane.

        If auto_nearfar is True, the near/far values are computed from
        the scene extent, otherwise the stored values are used.
        
        Compute near and far clipping plane distances from the bounding
        box of the scene. The scene bounding box is converted to a
        bounding sphere and the near and far clipping planes are set
        as tangent planes to the bounding sphere.
        """

        if not self.autonearfar:
            return self.nearplane, self.farplane

        # Get the bounding box of the entire scene
        bbox = getScene().boundingBox()

        # Determine bounding sphere
        bmin,bmax = bbox.getBounds()
        if bmin!=None and bmin!=bmax:
            # Box center (resp. sphere center)
            c = 0.5*(bmin+bmax)
            # Radius of the bounding sphere
            r = (bmax-c).length()
        else:
            c = vec3(0,0,0)
            r = 10

        # Transformation World->Camera
        VT = self.viewTransformation()

#        minnear = (bmax-bmin).length()/1000
        minnear = self.nearplane
        minfar = minnear+1

        # cz: Depth of the center point
        cz = (VT*c).z
        near = max(cz-r, minnear)
        far  = max(cz+r, minfar)

        if (far-near)<0.01:
            far+=1

        return (near,far)
