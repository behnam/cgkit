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
# $Id: spotlight3ds.py,v 1.2 2005/07/03 09:43:36 mbaas Exp $

## \file spotlight3ds.py
## Contains the SpotLight3DS class.

import protocols
from Interfaces import *
from slots import *
import lookat
from lightsource import LightSource

# SpotLight3DS
class SpotLight3DS(LightSource):
    """This class represents a spotlight as it appears in 3DS files.

    The direction of the light is the local positive Z axis.
    """

    protocols.advise(instancesProvide=[ISceneItem])

    def __init__(self,
                 name="SpotLight3DS",
                 enabled = True,   # off
                 intensity = 1.0,  # multiplier

                 see_cone = False,
                 roll = 0.0, 
                 outer_range = 0,
                 inner_range = 0,
                 attenuation = 0,
                 rectangular_spot = 0,
                 shadowed = False,
                 shadow_bias = 0,
                 shadow_filter = 4.0,
                 shadow_size = 256,
                 spot_aspect = 0,
                 use_projector = False,
                 projector = 0,
                 overshoot = False,
                 ray_shadows = False,
                 ray_bias = False,
                 hotspot = 43,
                 falloff = 45,
                 color = (1,1,1),
                 target=vec3(0,0,0),  # spot
#                 transform = None,
#                 pos = None, rot = None, scale = None,
#                 pivot= None,
#                 offsetTransform = None,
#                 auto_insert=True,
                 **params
                 ):

        LightSource.__init__(self, name=name, **params)

        target = vec3(target)

        # Target
        self.target_slot = Vec3Slot(target)
        self.addSlot("target", self.target_slot)

        self.enabled = enabled
        self.intensity = intensity
        self.attenuation = attenuation
        self.attenuation = attenuation
        self.inner_range = inner_range
        self.outer_range = outer_range
        self.falloff = falloff
        self.hotspot = hotspot
        self.overshoot = overshoot
        self.color = color
        self.shadowed = shadowed
        self.cast_shadow = shadowed
        self.shadow_filter = shadow_filter
        self.shadow_bias = shadow_bias
        self.shadow_size = shadow_size

        # Create the internal LookAt component
        self._lookat = lookat.LookAt()
        self._lookat.name = "SpotLight3DS_LookAt"
        self._lookat.output_slot.connect(self.rot_slot)
        self.pos_slot.connect(self._lookat.pos_slot)
        self.target_slot.connect(self._lookat.target_slot)
        

    # Create the "target" property
    exec slotPropertyCode("target")

    def protocols(self):
        return [ISceneItem]

    

        
