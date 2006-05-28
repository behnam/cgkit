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
# $Id: isceneitem.py,v 1.1.1.1 2004/12/12 14:31:43 mbaas Exp $

from protocols import Interface

class ISceneItem(Interface):
    """The base scene item protocol that must be supported by all scene items.

    A scene item must have an attribute \c name of type \c str which
    contains its name.
    """

    def protocols(self):
        """Return a list of supported protocols."""
        

class ISceneItemContainer(ISceneItem):
    """This interface must be supported by scene items that can contain children.

    The children must support the ISceneItem protocol.
    """

    def lenChilds(self):
        """Return the number of children."""

    def iterChilds(self):
        """Return an iterator that iterates over all children."""

    def addChild(self, child):
        """Add a children."""

    def removeChild(self, child):
        """Remove an existing children."""

    def findChildByName(self, name):
        """Return the children with the specified name.

        \return Child or None.
        """
