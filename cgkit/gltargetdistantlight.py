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
# $Id: gltargetdistantlight.py,v 1.4 2005/07/03 09:43:36 mbaas Exp $

## \file gltargetdistantlight.py
## Contains the GLTargetDistantLight class.

import protocols
import scene
from Interfaces import *
from slots import *
from cgtypes import vec3
from worldobject import _initWorldObject, _preInitWorldObject
import lookat
import cmds
import _core

# GLTargetDistantLight
class GLTargetDistantLight(_core.GLDistantLight):
    """This class represents an OpenGL distant light.

    The direction of the light is the local positive Z axis.
    """

    protocols.advise(instancesProvide=[ISceneItem])

    def __init__(self,
                 name="GLDistantLight",
                 parent=None,
                 enabled=True,
                 intensity=1.0,
                 ambient=None,
                 diffuse=None,
                 specular=None,
                 target=vec3(0,0,0),
                 cast_shadow = False,
                 auto_insert=True,
                 **params
                 ):
        exec _preInitWorldObject
        _core.GLDistantLight.__init__(self, name)

        _initWorldObject(self, name=name, parent=parent,
                         auto_insert=auto_insert,
                         **params)

        target = vec3(target)

        # Target
        self.target_slot = Vec3Slot(target)
        self.addSlot("target", self.target_slot)

        self.enabled = enabled
        self.intensity = intensity
        if ambient!=None:
            self.ambient = vec3(ambient)
        if diffuse!=None:
            self.diffuse = vec3(diffuse)
        if specular!=None:
            self.specular = vec3(specular)

        self.cast_shadow = cast_shadow

        # Create the internal LookAt component
        self._lookat = lookat.LookAt()
        self._lookat.name = "GLTargetDistant_LookAt"
        self._lookat.output_slot.connect(self.rot_slot)
        self.pos_slot.connect(self._lookat.pos_slot)
        self.target_slot.connect(self._lookat.target_slot)
        

    # Create the "target" property
    exec slotPropertyCode("target")

    def protocols(self):
        return [ISceneItem]

    

        
