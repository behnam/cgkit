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
# $Id: freecamera.py,v 1.6 2005/05/12 12:58:29 mbaas Exp $

## \file freecamera.py
## Contains the FreeCamera class.

"""This module contains the FreeCamera class."""

from Interfaces import *
import protocols
import slots
from cgtypes import *
from math import pi
from worldobject import WorldObject
from scene import getScene
import camerabase
import sys
import _core
       

# FreeCamera
class FreeCamera(camerabase.CameraBase):
    """A camera object that is free to move and rotate.
    """

    protocols.advise(instancesProvide=[ISceneItem, ICamera])

    def __init__(self,
                 name = "FreeCamera",
                 target = None,
                 fov = 45.0,
                 fstop = 0,
                 focallength = 0,
                 **params):
        
        camerabase.CameraBase.__init__(self, name=name, **params)

        # FOV
        self.fov_slot = slots.DoubleSlot(fov)
        self.addSlot("fov", self.fov_slot)

        # fstop
        self.fstop_slot = slots.DoubleSlot(fstop)
        self.addSlot("fstop", self.fstop_slot)
        
        # focal length
        self.focallength_slot = slots.DoubleSlot(focallength)
        self.addSlot("focallength", self.focallength_slot)

        # Initial targeting
        if target!=None:
            up = getScene().up
            self.transform = mat4().lookAt(self.pos, vec3(target), up)


    def protocols(self):
        return [ISceneItem, IComponent, IWorldObject, ICamera]

    def destroy(self):
#        self.fov_slot.setController(None)
#        self.target_slot.setController(None)
#        self._lookat.pos_slot.setController(None)
#        self._lookat.target_slot.setController(None)
#        self.transform_slot.setController(None)
#        self.pos_slot.setController(None)
#        self.rot_slot.setController(None)
#        self.scale_slot.setController(None)
        del self.fov_slot
        del self.fstop_slot
        del self.focallength_slot

    # projection
    def projection(self, width, height, near, far):
        return mat4().perspective(self.fov, float(width)/height, near, far)

    # viewTransformation
    def viewTransformation(self):
        return self.worldtransform.inverse()


    ## protected:

    exec slots.slotPropertyCode("fstop")
    exec slots.slotPropertyCode("focallength")

    # "fov" property...
    
    def _getFOV(self):
        """Return the current field of view.

        This method is used for retrieving the \a fov property.

        \return Field of view in angles (\c float)
        """
        return self.fov_slot.getValue()

    def _setFOV(self, fov):
        """Set the field of view.

        This method is used for setting the \a fov property.

        \param fov (\c float) Field of view in angles (0-180)
        """
        fov = float(fov)
        if fov<0:
            fov = 0.0
        if fov>180:
            fov = 180.0
        self.fov_slot.setValue(fov)

    fov = property(_getFOV, _setFOV, None, "Field of view (in angles)")
        
