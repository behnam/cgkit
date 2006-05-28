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
# $Id: glpointlight.py,v 1.4 2005/07/03 09:43:36 mbaas Exp $

## \file glpointlight.py
## Contains the GLPointLight class.

import protocols
import scene
from Interfaces import *
from slots import *
from cgtypes import vec3
from worldobject import _initWorldObject, _preInitWorldObject
import cmds
import _core

# GLPointLight
class GLPointLight(_core.GLPointLight):

    protocols.advise(instancesProvide=[ISceneItem])

    def __init__(self,
                 name="GLPointLight",
                 enabled=True,
                 intensity=1.0,
                 ambient=None,
                 diffuse=None,
                 specular=None,
                 constant_attenuation=1.0,
                 linear_attenuation=0.0,
                 quadratic_attenuation=0.0,
                 cast_shadow = False,
                 parent = None,
                 auto_insert = True,
                 **params
                 ):
        exec _preInitWorldObject
        _core.GLPointLight.__init__(self, name)

        _initWorldObject(self, name=name, parent=parent,
                         auto_insert=auto_insert,
                         **params)

        self.enabled = enabled
        self.intensity = intensity
        if ambient!=None:
            self.ambient = vec3(ambient)
        if diffuse!=None:
            self.diffuse = vec3(diffuse)
        if specular!=None:
            self.specular = vec3(specular)
        self.constant_attenuation = constant_attenuation
        self.linear_attenuation = linear_attenuation
        self.quadratic_attenuation = quadratic_attenuation

        self.cast_shadow = cast_shadow

    def protocols(self):
        return [ISceneItem]


        
