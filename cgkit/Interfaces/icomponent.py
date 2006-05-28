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
# $Id: icomponent.py,v 1.1.1.1 2004/12/12 14:31:41 mbaas Exp $

from protocols import Interface

class IComponent(Interface):
    """The base component protocol.

    Every component must have a \c name attribute.

    \todo Define a slot iterator
    """

    def slot(self, name):
        """Return the slot with the given name.

        \param name (\c str) Slot name
        \return Slot object (\c ISlot)
        \todo What happens if there is no slot with the given name?
        """

    def addSlot(self, name, slot):
        """Add a new slot to this component.

        \param name (\c str) Slot name
        \param slot (\c ISlot) The slot to be added
        """

    def removeSlot(self, name):
        """Remove a slot.
        
        \param name (\c str) Slot name
        """
