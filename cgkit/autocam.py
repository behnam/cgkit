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
# $Id: autocam.py,v 1.1.1.1 2004/12/12 14:30:54 mbaas Exp $

## \file autocam.py
## Contains the AutoCam class.

"""This module contains the AutoCam class."""

from Interfaces import *
import protocols
import slots
import _core
from eventmanager import eventManager
from scene import getScene
import events
from cgtypes import *
from component import *
       

# AutoCam
class AutoCam(Component):
    """AutoCam
    """

    protocols.advise(instancesProvide=[ISceneItem])

    def __init__(self, name="AutoCam"):
        Component.__init__(self, name=name)

        # Input
        self.input_slot = slots.Vec3Slot()
        self.addSlot("input", self.input_slot)

        # Output
        self.output_slot = slots.Vec3Slot()
        self.addSlot("output", self.output_slot)

        self.accel_factor = 0.5
        self.out_offset = vec3(0,0,0)

        self.out = vec3(0,0,0)
        self.out_velocity = vec3(0,0,0)

        eventManager().connect(events.STEP_FRAME, self)

    def protocols(self):
        return [ISceneItem, IComponent, IWorldObject, ICamera]

#    def destroy(self):
#        del self.fov_slot
#        del self.target_slot

    def onStepFrame(self):
        dt = getScene().timer().timestep
        diff = self.input-self.out
        if (diff.length()<1.0):
            a = -0.75*self.out_velocity
        else:
            a = self.accel_factor*(self.input-self.out)
        self.out_velocity += dt*a
        self.out = self.out + dt*self.out_velocity
        self.output = self.out+self.out_offset
     
    ## protected:
        
    # "input" property...
    exec slotPropertyCode("input")

    # "output" property...
    exec slotPropertyCode("output")

        

