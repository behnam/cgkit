#!/usr/bin/env python
###########################################################################
# Wrapped Ogre for CGKIT
# Copyright (C) 2004 Ole Ciliox (ole@ira.uka.de)
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
# -*- coding: cp1252 -*-
import sys, os, optparse

#sys.path.append(r"H:\Dokumente und Einstellungen\ol\Eigene Dateien\package\package\DER HORROR\visum2")

from cgkit.all import *
from cgkit.scene import getScene
from math import *
from cgkit._core import OgreCore 
from cgkit.tool import Tool


class OgreViewer(Tool):
    """OgreViewer tool."""
    
    def __init__(self):
        Tool.__init__(self, defaultoptionvar="VIEWEROGRE_DEFAULT_OPTIONS")

        # Search path for OGRE material scripts
        self.materialpath = r".\materials"
        
        Nopt = self.options.navigation_mode
        if Nopt==None or Nopt.lower()=="maya":
            self.navigation_mode = 1
        elif Nopt.lower()=="max":
            self.navigation_mode = 0
        elif Nopt.lower()=="softimage":
            self.navigation_mode = 2
        else:
            raise ValueError, "Unknown navigation mode. '%s'"%Nopt

        Ropt = self.options.render_system
        if Ropt==None or Ropt.lower()=="gl":
            self.use_opengl = 1
        elif Ropt.lower()=="d3d":
            self.use_opengl = 0
        else:
            raise ValueError, "Unknown render system: '%s'"%Ropt

	print "mmmmhh"

        Topt = self.options.shadow_mode
        if Topt==None or Topt.lower()=="stencil_add":
            self.shadowmode = 0
        elif Topt.lower()=="stencil_mod":
            self.shadowmode = 1
        elif Topt.lower()=="texture":
            self.shadowmode = 2	    
        else:
            raise ValueError, "Unknown shadow mode: '%s'"%Topt   

	print "mmmmhh2"


    def setOptions(self, optparser):
        """Add options specific to this tool."""
        Tool.setOptions(self, optparser)
        optparser.add_option("-F", "--full-screen", action="store_true", default=False,
                             help="Full screen display")
        optparser.add_option("-N", "--navigation-mode", metavar="MODE",
                             help="Navigation mode (MAX, Maya, Softimage). Default: Maya")
        optparser.add_option("-d", "--no-shadow", action="store_true", default=False,
                             help="Disable shadows")
        optparser.add_option("-R", "--render-system", metavar="NAME",
                             help="Render system (gl, d3d). Default: gl")
        optparser.add_option("-S", "--stereo", action="store_true", default=False,
                             help="Activate stereo display")
        optparser.add_option("-m", "--shadow-mode", metavar="NAME",
                             help="Shadow Mode  (STENCIL_ADD, STENCIL_MOD, TEXTURE")

	print "mmmmhh0"

    # init
    def init(self):
        pass
        self.keydict = {
            14  : KEY_BACK,
            15  : KEY_TAB,
            28 : KEY_RETURN,
            1 : KEY_ESCAPE,
            57 : KEY_SPACE,
            203 : KEY_LEFT,
            200 : KEY_UP,
            205 : KEY_RIGHT,
            208 : KEY_DOWN,
            58 : KEY_CAPSLOCK,
            42 : KEY_SHIFT_LEFT,
            54 : KEY_SHIFT_RIGHT,
            29 : KEY_CONTROL_LEFT,
            157 : KEY_CONTROL_RIGHT,
            56 : KEY_ALT_LEFT,
            184 : KEY_ALT_RIGHT,
            219 : KEY_WINDOWS_LEFT,
            220 : KEY_WINDOWS_RIGHT,
            221 : KEY_WINDOWS_MENU,
            183 : KEY_PRINT,
            70 : KEY_SCROLL,
            197 : KEY_PAUSE,
            210 : KEY_INSERT,
            211 : KEY_DELETE,
            199 : KEY_HOME,
            207 : KEY_END,
            201 : KEY_PRIOR,
            209 : KEY_NEXT,
            59 : KEY_F1,
            60 : KEY_F2,
            61 : KEY_F3,
            62 : KEY_F4,
            63 : KEY_F5,
            64 : KEY_F6,
            65 : KEY_F7,
            66 : KEY_F8,
            67 : KEY_F9,
            68 : KEY_F10,
            87 : KEY_F11,
            88 : KEY_F12,
            69 : KEY_NUMLOCK,
            82 : KEY_NUMPAD0,
            79 : KEY_NUMPAD1,
            80 : KEY_NUMPAD2,
            81 : KEY_NUMPAD3,
            75 : KEY_NUMPAD4,
            76 : KEY_NUMPAD5,
            77 : KEY_NUMPAD6,
            71 : KEY_NUMPAD7,
            72 : KEY_NUMPAD8,
            73 : KEY_NUMPAD9,
            83 : KEY_NUMPAD_DECIMAL,
            181 : KEY_NUMPAD_DIVIDE,
            55 : KEY_NUMPAD_MULTIPLY,
            74 : KEY_NUMPAD_SUBTRACT,
            78 : KEY_NUMPAD_ADD,
            156 : KEY_NUMPAD_ENTER
            }

    def convertMods(self, mods):
        # ogre specific keymodifier-converting
        res = 0
        if mods & 0x1:
            res |= KEYMOD_SHIFT
        if mods & 0x2:
            res |= KEYMOD_CONTROL
        if mods & 0x8:
            res |= KEYMOD_ALT
        return res

    # action
    def action(self):

        CameraControl(cam=self.cam, mode=self.navigation_mode)
	
	print "mmmmhh3"

        scene = getScene()
        timer = scene.timer()
        worldroot = scene.worldRoot()
        myOgre = OgreCore()
        self.ogrecore = myOgre
        #myOgre.setAmbient(0,0,0)

	# tell ogre which shadow mode to use
	print "mmmmhh4"
	myOgre.setupShadowMode(self.shadowmode,2048)
	#myOgre.setupShadowMode(0,512)

        myOgre.initialize(worldroot,
                          self.options.width,
                          self.options.height,
                          self.options.full_screen,
                          not self.options.no_shadow,
                          self.use_opengl,
                          r".\demosOgre\materials",
#                         self.materialpath,
                          self.options.stereo)

        # signature: cameraObject
        myOgre.setupData(self.cam, 0.1, 1000.0, self.cam.fov)

        # Set background color
        if scene.hasGlobal("background"):
            bg = scene.getGlobal("background")
            r = int(255*bg[0])
            g = int(255*bg[1])
            b = int(255*bg[2])
            myOgre.changeBackgroundColor(r, g, b)

        eventmanager = eventManager()

        running = 1
        while (running):

            ####* #        SIMULATE   
            
            timer.step()

            ####* #        RENDER ONE OGRE FRAME

            myOgre.renderTree()

            #####* #   **  GET EVENTS  
   
            ########################
            #####* #   01  KEYDOWN ?  
  
            kd = myOgre.pumpKeyDowns()
            i = 0
            while ( i<len(kd) ):
                # quit when ESC is pressed
                #print kd
                if (kd[i+1] == 1):
                    #myOgre.rebuildOgreTree(worldroot)
                    running = 0
                code = self.keydict.get(kd[i+1], kd[i+1])
                mods = self.convertMods( kd[i+2] )
                eventmanager.event( KEY_PRESS, KeyEvent(kd[i], code, mods) )
                i = i+3

            #######################
            #####* #   1A  KEYUP ?  
  
            kd = myOgre.pumpKeyUps()
            i = 0
            while ( i<len(kd) ):
                #print kd
                code = self.keydict.get(kd[i+1], kd[i+1])
                mods = self.convertMods( kd[i+2] )
                eventmanager.event( KEY_RELEASE, KeyEvent(kd[i], code, mods) )
                i = i+3

            ##########################
            #####* #   02  MOUSEMOVE ? 

            mm = myOgre.pumpMotions()
            i = 0
            while ( i<len(mm) ):
                #print mm
                btns = 0
                b1,b2,b3 = mm[i+4]
                if b1:
                    btns |= 0x1
                if b2:
                    btns |= 0x2
                if b3:
                    btns |= 0x4 
                eventmanager.event(MOUSE_MOVE, MouseMoveEvent(mm[i]*self.options.width, mm[i+1]*self.options.height, mm[i+2]*self.options.width, mm[i+3]*self.options.height, mm[i], mm[i+1], mm[i+2], mm[i+3], btns) )	
                i = i+5	

            ############################
            #####* #   03  MOUSEBUTTON ? 

            mb = myOgre.pumpMouseButtons()
            i = 0
            while ( i<len(mb) ):
                #print mb
                x = mb[i+2]*self.options.width
                y = mb[i+3]*self.options.height
                x0 = mb[i+2]
                y0 = mb[i+3]
                # relative coords mb[i+4], mb[i+5] not used yet
                if ( mb[i+1] == 0 ): # MOUSE PRESSED
                    if ( mb[i] == 16 ): # LEFT_MOUSE
                        eventname = LEFT_DOWN
                        evt = MouseButtonEvent(1, x, y, x0, y0)
                    elif ( mb[i] == 64 ): # MIDDLE_MOUSE
                        eventname = MIDDLE_DOWN
                        evt = MouseButtonEvent(2, x, y, x0, y0)
                    elif ( mb[i] == 32 ): # RIGHT_MOUSE
                        eventname = RIGHT_DOWN
                        evt = MouseButtonEvent(3, x, y, x0, y0)
                    else: 
                        eventname = MOUSE_BUTTON_DOWN
                        evt = MouseButtonEvent(mb[i], x, y, x0, y0) # ?<---
                    eventmanager.event(eventname, evt)
                elif ( mb[i+1] == 1 ): # MOUSE RELEASED
                    if ( mb[i] == 16 ): # LEFT_MOUSE
                        eventname = LEFT_UP
                        evt = MouseButtonEvent(1, x, y, x0, y0)
                    elif ( mb[i] == 64 ): # MIDDLE_MOUSE
                        eventname = MIDDLE_UP
                        evt = MouseButtonEvent(2, x, y, x0, y0)
			myOgre.changeBackgroundColor(255, 0, 0)
                    elif ( mb[i] == 32 ): # RIGHT_MOUSE
                        eventname = RIGHT_UP
                        evt = MouseButtonEvent(3, x, y, x0, y0)
                    else: 
                        eventname = MOUSE_BUTTON_DOWN
                        evt = MouseButtonEvent(mb[i], x, y, x0, y0) # ?<---
                    eventmanager.event(eventname, evt)
                i = i+6

            #####* #       BREMSE & CO 

            myOgre.clock(int(self.options.fps))    
            #print int(self.options.fps)
            #myOgre.clock(50)        

####################################################
    
viewer = OgreViewer()
viewer.run()
