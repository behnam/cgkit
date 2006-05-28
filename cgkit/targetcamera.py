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
# $Id: targetcamera.py,v 1.8 2005/07/21 15:07:11 mbaas Exp $

## \file targetcamera.py
## Contains the TargetCamera class.

"""This module contains the TargetCamera class."""

from Interfaces import *
import protocols
import slots
from cgtypes import *
from math import pi
from worldobject import WorldObject
from scene import getScene
import camerabase, lookat
import sys
import _core

# TargetCamera
class TargetCamera(camerabase.CameraBase):
    """A camera object that always looks at a particular target.
    """

    protocols.advise(instancesProvide=[ISceneItem, ICamera])

    def __init__(self,
                 name = "TargetCamera",
                 fov = 45.0,
                 target = vec3(0,0,0),
                 roll = 0.0,
                 up = None,
                 fstop = 0,
                 focallength = 0,
                 **params):
        
        camerabase.CameraBase.__init__(self, name=name, **params)

        target = vec3(target)

        # FOV
        self.fov_slot = slots.DoubleSlot(fov)
        self.addSlot("fov", self.fov_slot)

        # Target
        self.target_slot = slots.Vec3Slot(target)
        self.addSlot("target", self.target_slot)

        # Roll
        self.roll_slot = slots.DoubleSlot(roll)
        self.addSlot("roll", self.roll_slot)

        # Up
        self.up_slot = slots.Vec3Slot()
        self.addSlot("up", self.up_slot)
        if up==None:
            self.up_slot.setValue(getScene().up)
        else:
            self.up_slot.setValue(vec3(up))

        self._lookat = lookat.LookAt()
        self._lookat.name = "TargetCamera_LookAt"
        self._lookat.output_slot.connect(self.rot_slot)
        self.pos_slot.connect(self._lookat.pos_slot)
        self.target_slot.connect(self._lookat.target_slot)
        self.roll_slot.connect(self._lookat.roll_slot)
        self.up_slot.connect(self._lookat.up_slot)

        # fstop
        self.fstop_slot = slots.DoubleSlot(fstop)
        self.addSlot("fstop", self.fstop_slot)
        
        # focal length
        self.focallength_slot = slots.DoubleSlot(focallength)
        self.addSlot("focallength", self.focallength_slot)


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
        del self.target_slot
        del self._lookat.output_slot
        del self._lookat.pos_slot
        del self._lookat.target_slot
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
    exec slots.slotPropertyCode("roll")
    exec slots.slotPropertyCode("up")

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
        
    # "target" property...
    
    def _getTarget(self):
        """Return the current target position.

        This method is used for retrieving the \a target property.

        \return Target position (\c vec3)
        """
        return self.target_slot.getValue()

    def _setTarget(self, pos):
        """Set a new target position.

        This method is used for setting the \a target property.

        \param pos (\c vec3) Target position
        """
        pos = vec3(pos)
        self.target_slot.setValue(pos)

    target = property(_getTarget, _setTarget, None, "Target position")
