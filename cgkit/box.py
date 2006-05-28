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
# $Id: box.py,v 1.2 2005/04/19 08:45:49 mbaas Exp $

## \file box.py
## Contains the Box class.

import protocols
from Interfaces import *
from slots import *
from cgtypes import vec3
from worldobject import WorldObject
from boxgeom import BoxGeom

# Box
class Box(WorldObject):

    protocols.advise(instancesProvide=[ISceneItem, IRigidBody])

    def __init__(self,
                 name = "Box",
                 dynamics = True,
                 static = False,
                 lx=1.0, ly=1.0, lz=1.0,
                 segmentsx=1, segmentsy=1, segmentsz=1, **params):
        WorldObject.__init__(self, name=name, **params)

        self.geom = BoxGeom(lx, ly, lz, segmentsx, segmentsy, segmentsz)

        self.dynamics_slot = BoolSlot(dynamics)
        self.static_slot = BoolSlot(static)
        self.addSlot("dynamics", self.dynamics_slot)
        self.addSlot("static", self.static_slot)

    exec slotPropertyCode("dynamics")
    exec slotPropertyCode("static")
        
