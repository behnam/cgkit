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
# $Id: camcontrol.py,v 1.4 2005/08/31 14:49:13 mbaas Exp $

## \file camcontrol.py
## Contains the CameraControl class.

import component
import eventmanager
from scene import getScene
from events import *
from keydefs import *
from cgtypes import *

# CameraControl
class CameraControl(component.Component):
    """Camera control component.

    This component lets you control a camera interactively with the mouse.

    Todo: - About what point rotates the FreeCam?
          - Make movement distances customizable (auto configurable?)
    """
    
    def __init__(self,
                 cam,
                 name = "CameraControl",
                 mode = 0,
                 auto_insert = True):
        """Constructor.

        \param cam (\c ...Cam?...) Camera to control
        \param name (\c str) Name of the component
        \param mode (\c int) 0=Emulate MAX behavior, 1=Emulate Maya behavior
        \param auto_insert (\c bool) Insert into scene or not
        """
        
        component.Component.__init__(self, name=name, auto_insert=auto_insert)
        
        # mode: 0=Emulate MAX / 1=Emulate Maya / 2=Emulate Softimage (Navigation tool)
        self.mode = mode  
        self.cam = cam
        self.left_down = False
        self.middle_down = False
        self.right_down = False
        self.alt_down = False
        self.ctrl_down = False
        em = eventmanager.eventManager()
        em.connect(KEY_PRESS, self)
        em.connect(KEY_RELEASE, self)
        em.connect(LEFT_DOWN, self)
        em.connect(LEFT_UP, self)
        em.connect(MIDDLE_DOWN, self)
        em.connect(MIDDLE_UP, self)
        em.connect(RIGHT_DOWN, self)
        em.connect(RIGHT_UP, self)
        em.connect(MOUSE_MOVE, self)
        em.connect(MOUSE_WHEEL, self)
        em.connect(SPACE_MOTION, self)

    def panCondition(self):
        """Return True if the panning mode is active.
        """
        if self.mode==0:
            # MAX
            return self.middle_down and not self.alt_down and not self.ctrl_down
        elif self.mode==1:
            # Maya
            return self.middle_down and self.alt_down
        else:
            # Softimage
            return self.left_down

    def rotCondition(self):
        """Return True if rotation mode is active.
        """
        if self.mode==0:
            # MAX
            return self.middle_down and self.alt_down and not self.ctrl_down
        elif self.mode==1:
            # Maya
            return self.left_down and self.alt_down
        else:
            # Softimage
            return self.right_down

    def fbCondition(self):
        """Return True if 'forward/backward' movement mode is active.
        """        
        if self.mode==0:
            # MAX
            return self.middle_down and self.alt_down and self.ctrl_down
        elif self.mode==1:
            # Maya
            return self.right_down and self.alt_down
        else:
            # Softimage
            return self.middle_down

    def translateXYAmount(self, evt):
        """Return the amount of sideways movement."""
        if self.mode==0:
            # MAX
            return 0.003*evt.dx, 0.003*evt.dy
        elif self.mode==1:
            # Maya
            return 0.003*evt.dx, 0.003*evt.dy
        else:
            # Softimage
            return 0.002*evt.dx, 0.002*evt.dy

    def translateZAmount(self, evt):
        """Return the amount of 'forward/backward' movement."""
        if self.mode==0:
            # MAX
            return -0.01*evt.dy
        elif self.mode==1:
            # Maya
            return 0.004*(evt.dy+evt.dx)
        else:
            # Softimage
            return 0.008*(evt.dy-evt.dx)

    def rotationAmount(self, evt):
        """Return the amount of rotation."""
        if self.mode==0:
            # MAX
            return 0.01*evt.dx, 0.01*evt.dy
        elif self.mode==1:
            # Maya
            return 0.01*evt.dx, 0.01*evt.dy
        else:
            # Softimage
            return 0.015*evt.dx, 0.015*evt.dy

    # onKeyPress
    def onKeyPress(self, e):
        """Set key flags."""
        if e.altKey():
            self.alt_down = True
        elif e.controlKey():
            self.ctrl_down = True

    # onKeyRelease
    def onKeyRelease(self, e):
        """Unset key flags."""
        if e.altKey():
            self.alt_down = False
        elif e.controlKey():
            self.ctrl_down = False

    # onMouseMove
    def onMouseMove(self, e):

        if self.panCondition():
            dx, dy = self.translateXYAmount(e)
            self.translateXY(dx, dy)

        elif self.rotCondition():
            dx, dy = self.rotationAmount(e)
            self.rotate(dx, dy)
            
        elif self.fbCondition():
            f = self.translateZAmount(e)
            self.translateZ(f)

    def onMouseWheel(self, e):
        self.translateZ(0.002*e.delta)
                            
    def onLeftDown(self, e):
        self.left_down = True

    def onLeftUp(self, e):
        self.left_down = False

    def onMiddleDown(self, e):
        self.middle_down = True

    def onMiddleUp(self, e):
        self.middle_down = False

    def onRightDown(self, e):
        self.right_down = True

    def onRightUp(self, e):
        self.right_down = False

    # translateXY
    def translateXY(self, dx, dy):
        """Translate the camera in local XY.
        """

        T = self.cam.transform
        bx = vec3(tuple(T.getColumn(0))[:3])
        by = vec3(tuple(T.getColumn(1))[:3])
        if hasattr(self.cam, "target"):
            f = (self.cam.target-self.cam.pos).length()
            dx *= f
            dy *= f
        delta = dx*bx + dy*by
        self.cam.pos += delta
        if hasattr(self.cam, "target"):
            self.cam.target += delta

    # rotate
    def rotate(self, dx, dy):
        """Rotate around target."""
       
        T = self.cam.transform
        if hasattr(self.cam, "target"):
            pivot = self.cam.target
        else:
            pivot = vec3(0)
        up = getScene().up
        R = mat4(1).rotation(-dx, up)
        dp = self.cam.pos-pivot
        self.cam.pos = pivot + R*dp
            
        T = self.cam.transform
        bx = vec3(tuple(T.getColumn(0))[:3])
        R = mat4(1).rotation(dy, bx)
        dp = self.cam.pos-pivot
        self.cam.pos = pivot + R*dp

    # translateZ
    def translateZ(self, dz):
        """Move in viewing direction.
        """

        T = self.cam.transform
        bz = vec3(tuple(T.getColumn(2))[:3])
        if hasattr(self.cam, "target"):
            f = (self.cam.target-self.cam.pos).length()
        else:
            f = 1
        delta = f*dz*bz
        self.cam.pos += delta
#        self.cam.target += delta            
        

    # onSpaceMotion
    def onSpaceMotion(self, e):
        """
        this is still somewhat experimental
        (should distinguish between the camera types as it's meant to be
        used with a FreeCamera)
        """

        scene = getScene()

        tr = 0.001*e.translation
        rot = e.rotation

        if scene.handedness=='r':
            tr.x = -tr.x
            rot.y = -rot.y
            rot.z = -rot.z

        M = mat4().translation(tr)

        if rot!=vec3(0):
            a = 0.0002*rot.length()
            M = M*mat4().rotation(a, rot)

        T = self.cam.transform*M
        # Align camera to up direction
        R = T.getMat3()
        bz = vec3(tuple(T.getColumn(2))[:3])
        by = scene.up
        bx = by.cross(bz)
        by = bz.cross(bx)
        try:
            R = mat3(bx.normalize(), by.normalize(), bz.normalize())
        except:
            R = mat3(1)
        T.setMat3(R)

        self.cam.transform = T
