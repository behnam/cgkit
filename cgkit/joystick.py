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
# $Id: joystick.py,v 1.1.1.1 2004/12/12 14:31:05 mbaas Exp $

## \file joystick.py
## Contains the Joystick class.

from eventmanager import eventManager
from events import *

# Joystick
class Joystick:
    """Generic joystick class.

    Attributes:

    - id
    - name
    - numaxes
    - numhats
    - numballs
    - numbuttons

    """
    
    def __init__(self, id, name,
                 numaxes=0, numhats=0, numballs=0, numbuttons=0):
        """Constructor.

        \param id (\c int) Device ID (0,1,2...)
        \param name (\c str) The name of the joystick device
        \param numaxes (\c int) The number of axes this joystick has
        \param numhats (\c int) The number of hats this joystick has
        \param numballs (\c int) The number of balls this joystick has
        \param numbuttons (\c int) The number of buttons this joystick has
        """

        self.id = id
        self.name = name
        self.numaxes = numaxes
        self.numhats = numhats
        self.numballs = numballs
        self.numbuttons = numbuttons

        # Current uncalibrated axis values
        self.axis = numaxes*[0.0]
        # Current hat values
        self.hat = numhats*[(0,0)]
        # Current ball values
        self.ball = numballs*[0.0]
        # Current button states
        self.button = numbuttons*[False]

        # Minimum axis values
        self.axis_min = numaxes*[999.0]
        # Maximum axis values
        self.axis_max = numaxes*[-999.0]
        # Middle axis values
        self.axis_mid = numaxes*[0.0]

    def __str__(self):
        return '<Joystick id:%d name:"%s" axes:%d hats:%d balls:%d buttons:%d>'%(self.id, self.name, self.numaxes, self.numhats, self.numballs, self.numbuttons)

    # getAxis
    def getAxis(self, axis):
        """Return an axis value.

        \return Calibrated axis value (\c float).
        """
        if axis>=self.numaxes:
            return 0.0
            
        return self._calibratedAxis(axis, self.axis[axis])

    # getHat
    def getHat(self, hat):
        """Return a hat value.

        \return A tuple (x, y) (\c int, \c int)
        """
        if hat>=self.numhats:
            return 0,0
        
        return self.hat[hat]

    # getBall
    def getBall(self, ball):
        """Return a ball value.

        \return Ball value (\c float)
        """
        if ball>=self.numballs:
            return 0.0
        
        return self.ball[ball]

    # getButton
    def getButton(self, button):
        """Return a button state.

        \return Button state (\c bool)
        """
        if button>=self.numbuttons:
            return False
        
        return self.button[button]

    # setAxis
    def setAxis(self, axis, value):
        """Set a new value for a particular axis.

        The value is the raw (uncalibrated) value from the joystick.

        This method sends a JOYSTICK_AXIS event which contains the
        \em calibrated axis value.

        \param axis (\c int) Axis index
        \param value (\c float) Uncalibrated axis value
        
        \todo Sollte diese Methode setRawAxis() heissen?
        """
        self.axis[axis] = value

        # Adjust min/max values
        if value<self.axis_min[axis]:
            self.axis_min[axis] = value
        if value>self.axis_max[axis]:
            self.axis_max[axis] = value
        
        e = JoystickAxisEvent(self.id, axis, self._calibratedAxis(axis, value))
        eventManager().event(JOYSTICK_AXIS, e)

    # setHat
    def setHat(self, hat, x, y):
        """Set a new value for a particular hat.

        This method sends a JOYSTICK_HAT event.

        \param hat (\c int) Hat index
        \param x (\c int) X value
        \param y (\c int) Y value        
        """
        self.hat[hat]=(x,y)
        e = JoystickHatEvent(self.id, hat, x, y)
        eventManager().event(JOYSTICK_HAT, e)

    # setBall
    def setBall(self, ball, value):
        """Set a new value for a particular ball.

        This method sends a JOYSTICK_BALL event.

        \param ball (\c int) Ball index
        \param value (\c float) Ball value
        """
        self.ball[ball] = value
        e = JoystickBallEvent(self.id, ball, value)
        eventManager().event(JOYSTICK_BALL, e)

    # setButton
    def setButton(self, button, value):
        """Set the state of a particular button.

        This method sends either a JOYSTICK_BUTTON_DOWN or
        JOYSTICK_BUTTON_UP event.

        \param button (\c int) Button index
        \param value (\c bool) State of the button (True = pressed)
        """
        self.button[button] = value
        e = JoystickButtonEvent(self.id, button)
        if value:
            eventManager().event(JOYSTICK_BUTTON_DOWN, e)                
        else:
            eventManager().event(JOYSTICK_BUTTON_UP, e)

    # setAxisMiddle
    def setAxisMiddle(self, axis=None, mid=None):
        """Set the middle position of an axis or all axes.

        Sets the joystick position that will be mapped to the value 0.0.
        This means, if the joystick outputs the (uncalibrated) value
        \a mid, then the calibrated value will just be 0.0.
        
        \param axis (\c int) Axis index (None = all axes)
        \param mid (\c float) Middle value (None = take current value)
        """
        if axis==None:
            axes = range(self.numaxes)
        else:
            axes = [axis]

        for i in axes:
            if mid==None:
                mid = self.axis[i]

            self.axis_mid[i] = mid

    ## protected:

    def _calibratedAxis(self, axis, rawvalue):
        """Return the calibrated axis value.

        \param axis (\c int) Axis index
        \param rawvalue (\c float) Uncalibrated axis value
        \return Calibrated axis value (\c float).
        """
        amid = self.axis_mid[axis]
        amin = self.axis_min[axis]
        amax = self.axis_max[axis]
        
        if rawvalue<amid:
            d = amid-amin
            if d>0:
                return (rawvalue-amid)/d
            else:
                return 0.0
        else:
            d = amax-amid
            if d>0:
                return (rawvalue-amid)/d
            else:
                return 0.0
        
