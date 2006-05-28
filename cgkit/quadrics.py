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
# $Id: quadrics.py,v 1.3 2006/05/17 12:10:53 mbaas Exp $

## \file quadrics.py
## Contains the quadrics classes.

from cgtypes import vec3
from Interfaces import *
from worldobject import WorldObject
from spheregeom import SphereGeom
from slots import *
import protocols
import _core

# Sphere
class Sphere(WorldObject):

    protocols.advise(instancesProvide=[ISceneItem, IRigidBody])

    def __init__(self,
                 name="Sphere",
                 dynamics=True,
                 static=False,
                 radius=1.0,
                 segmentsu=16,
                 segmentsv=8,
                 **params):
        WorldObject.__init__(self, name=name, **params)

        self.geom = SphereGeom(radius, segmentsu, segmentsv)

        self.dynamics_slot = BoolSlot(dynamics)
        self.static_slot = BoolSlot(static)
        self.addSlot("dynamics", self.dynamics_slot)
        self.addSlot("static", self.static_slot)

    exec slotPropertyCode("dynamics")
    exec slotPropertyCode("static")

    def protocols(self):
        return [ISceneItem, IRigidBody]
