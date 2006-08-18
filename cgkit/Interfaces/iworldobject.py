# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is the Python Computer Graphics Kit.
#
# The Initial Developer of the Original Code is Matthias Baas.
# Portions created by the Initial Developer are Copyright (C) 2004
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
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
        
