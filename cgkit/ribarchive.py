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
# $Id: ribarchive.py,v 1.1.1.1 2004/12/12 14:31:18 mbaas Exp $

## \file ribarchive.py
## Contains the RIBArchive class.

import protocols
from cgkit.Interfaces import *
from worldobject import WorldObject
from geomobject import GeomObject
from boundingbox import BoundingBox
import ribexport
from ri import *

# RIBArchiveGeom
class RIBArchiveGeom(GeomObject):

    protocols.advise(instancesProvide=[ribexport.IGeometry])

    def __init__(self, filename):
        GeomObject.__init__(self)
        self.filename = filename

    def uniformCount(self):
        return 0

    def varyingCount(self):
        return 0

    def vertexCount(self):
        return 0

    def boundingBox(self):
        return BoundingBox()

    def drawGL(self):
        pass

    def render(self, matid):
        if matid!=0:
            return

        if self.filename!=None:
            RiReadArchive(self.filename)


# RIBArchive
class RIBArchive(WorldObject):
    """RIB archive.

    This class represents an archive file on disk. The file will
    be included via a call to RiReadArchive().    
    """

    protocols.advise(instancesProvide=[ISceneItem])

    def __init__(self,
                 name = "RIBArchive",
                 filename = None,
                 **params):
        WorldObject.__init__(self, name=name, **params)

        self.geom = RIBArchiveGeom(filename)

