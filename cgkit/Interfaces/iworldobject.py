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
# $Id: iworldobject.py,v 1.1.1.1 2004/12/12 14:31:43 mbaas Exp $

from protocols import Interface
from icomponent import IComponent

class IWorldObject(IComponent):
    """The world object protocol.

    A world object must have the following attributes:

    - geom (\c IGeomObject)
    - transform (\c mat4)
    - transform_slot (\c Mat4Slot)
    - pos (\c vec3) 
    - pos_slot (\c Vec3Slot)
    """

    def lenChilds(self):
        """Return the number of children world objects."""

    def iterChilds(self):
        """Return an iterator that iterates over all children.

        \return Iterator
        """

    def addChild(self, child):
        """Add another world object as children object.

        \param child (\c IWorldObject)
        """
        
