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
# $Id: draw.py,v 1.1.1.1 2004/12/12 14:30:59 mbaas Exp $

## \file draw.py
## Contains the Draw class.

import protocols
from Interfaces import *
from cgtypes import vec3
from worldobject import WorldObject
from drawgeom import DrawGeom

# Draw
class Draw(WorldObject):

    protocols.advise(instancesProvide=[ISceneItem])

    def __init__(self,
                 name="Draw",
                 **params):
        WorldObject.__init__(self, name=name, **params)
        self.geom = DrawGeom()

    def clear(self):
        self.geom.clear()

    def marker(self, pos, col=(1,1,1), size=1.0):
        self.geom.marker(vec3(pos), vec3(col), size)

    def line(self, pos1, pos2, col=(1,1,1), size=1.0):
        self.geom.line(vec3(pos1), vec3(pos2), vec3(col), size)
        
