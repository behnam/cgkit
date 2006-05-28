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
# $Id: pidcontroller.py,v 1.1.1.1 2004/12/12 14:31:11 mbaas Exp $

## \file pidcontroller.py
## Contains the PIDController class.

import component
import eventmanager, events
from scene import getScene
from slots import *
from cgtypes import *
import _core

# PIDController
class PIDController(component.Component):
    """PID controller.

    """

    exec slotPropertyCode("input")
    exec slotPropertyCode("output")
    exec slotPropertyCode("setpoint")
    exec slotPropertyCode("maxout")
    exec slotPropertyCode("minout")
    exec slotPropertyCode("Kp")
    exec slotPropertyCode("Ki")
    exec slotPropertyCode("Kd")

    def __init__(self,
                 name = "PIDController",
                 setpoint = 0.0,
                 Kp = 0.0,
                 Ki = 0.0,
                 Kd = 0.0,
                 maxout = 999999,
                 minout = -999999,
                 auto_insert = True):
        """Constructor.
        """
        
        component.Component.__init__(self, name, auto_insert)

        self.input_slot = DoubleSlot()
        self.setpoint_slot = DoubleSlot(setpoint)
        self.maxout_slot = DoubleSlot(maxout)
        self.minout_slot = DoubleSlot(minout)
        self.Kp_slot = DoubleSlot(Kp)
        self.Ki_slot = DoubleSlot(Ki)
        self.Kd_slot = DoubleSlot(Kd)

        self.output_slot = ProceduralDoubleSlot(self.computeOutput)

        self.addSlot("input", self.input_slot)
        self.addSlot("setpoint", self.setpoint_slot)
        self.addSlot("output", self.output_slot)
        self.addSlot("maxout", self.maxout_slot)
        self.addSlot("minout", self.minout_slot)
        self.addSlot("Kp", self.Kp_slot)
        self.addSlot("Ki", self.Ki_slot)
        self.addSlot("Kd", self.Kd_slot)

        self.input_slot.addDependent(self.output_slot)
        self.setpoint_slot.addDependent(self.output_slot)
        self.maxout_slot.addDependent(self.output_slot)
        self.minout_slot.addDependent(self.output_slot)
        self.Kp_slot.addDependent(self.output_slot)
        self.Ki_slot.addDependent(self.output_slot)
        self.Kd_slot.addDependent(self.output_slot)

        self._integral = 0.0
        self._prev_err = 0.0

        eventmanager.eventManager().connect(events.STEP_FRAME, self)
        eventmanager.eventManager().connect(events.RESET, self)
        

    def onStepFrame(self):
        err = self.setpoint-self.input
        dt = getScene().timer().timestep
        self._integral += dt*err

    def onReset(self):
        self._integral = 0.0
        self._prev_err = 0.0

    def computeOutput(self):
        err = self.setpoint-self.input
        dt = getScene().timer().timestep
        I = self._integral
        D = (err-self._prev_err)/dt
#        print "D:",D
        res = self.Kp*err + self.Ki*I + self.Kd*D
        
        self._prev_err = err
        
        maxout = self.maxout
        minout = self.minout
        if res>maxout:
            res = maxout
        elif res<minout:
            res = minout
            
        return res
