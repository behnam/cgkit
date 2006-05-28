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
# $Id: __init__.py,v 1.2 2005/08/29 15:24:13 mbaas Exp $


try:
    # The 3DxWare wrapper is in the root cgkit directory so that the
    # boost dll can be found.
    from cgkit._spacedevice import *

    SI_ANY_DEVICE = -1
    
    _spacedevice_available = True
except:
    _spacedevice_available = False

    # Define dummy classes/functions:
    
    class SpaceDevice:
        def __init__(self):
            raise RuntimeError("The spacedevice module is not available")


def available():
    """Returns True if the spacedevice functionality is available.
    """
    return _spacedevice_available

