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
# $Id: __init__.py,v 1.1 2005/01/09 20:13:06 mbaas Exp $

from constants import *

try:
    # The wintab wrapper is in the root cgkit directory so that the
    # boost dll can be found.
    from cgkit._wintab import *
    _wintab_available = True
except:
    _wintab_available = False

    # Define dummy classes/functions:
    
    class Context:
        def __init__(self):
            raise RuntimeError("The Wintab driver is not installed")

    def info(category):
        raise RuntimeError("The Wintab driver is not installed")



def available():
    """Returns True if the Wintab functionality is available.
    """
    return _wintab_available

    
