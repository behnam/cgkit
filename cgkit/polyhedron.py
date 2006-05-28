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
# $Id: polyhedron.py,v 1.1 2005/02/20 18:30:41 mbaas Exp $

## \file polyhedron.py
## Contains the Polyhedron class.

from cgtypes import *
from Interfaces import *
from worldobject import WorldObject
from polyhedrongeom import PolyhedronGeom
from slots import *
import protocols
import _core


# Polyhedron
class Polyhedron(WorldObject):

    protocols.advise(instancesProvide=[ISceneItem])

    def __init__(self,
                 name = "Polyhedron",
#                 dynamics = False,
#                 static = False,
                 verts = [],
                 polys = [],
                 **params):
        WorldObject.__init__(self, name=name, **params)

        self.geom = PolyhedronGeom()

#        self.dynamics = dynamics
#        self.static_slot = BoolSlot(static)

        ph = self.geom
        
        if len(verts)>0:
            ph.verts.resize(len(verts))
            i = 0
            for v in verts:
                ph.verts.setValue(i, vec3(v))
                i+=1

        if len(polys)>0:
            ph.setNumPolys(len(polys))
            i = 0
            for poly in polys:
                ph.setPoly(i, poly)
                i+=1
        
    exec slotPropertyCode("static")

