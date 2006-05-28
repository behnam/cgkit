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
# $Id: trimesh.py,v 1.3 2005/04/19 08:45:56 mbaas Exp $

## \file trimesh.py
## Contains the TriMesh class.

from cgtypes import vec3
from Interfaces import *
from worldobject import WorldObject
from trimeshgeom import TriMeshGeom
from slots import *
import protocols
import _core


# TriMesh
class TriMesh(WorldObject):

    protocols.advise(instancesProvide=[ISceneItem, IRigidBody])

    def __init__(self,
                 name="TriMesh",
                 dynamics=True,
                 static=False,
                 verts=[],
                 faces=[],
                 **params):
        WorldObject.__init__(self, name=name, **params)

        self.geom = TriMeshGeom()

        self.dynamics_slot = BoolSlot(dynamics)
        self.static_slot = BoolSlot(static)
        self.addSlot("dynamics", self.dynamics_slot)
        self.addSlot("static", self.static_slot)

        tm = self.geom
        
        if len(verts)>0:
            tm.verts.resize(len(verts))
            i = 0
            for v in verts:
                tm.verts.setValue(i, v)
                i+=1

        if len(faces)>0:
            tm.faces.resize(len(faces))
            i = 0
            for f in faces:
                tm.faces.setValue(i, f)
                i+=1
        
    exec slotPropertyCode("static")
    exec slotPropertyCode("dynamics")

