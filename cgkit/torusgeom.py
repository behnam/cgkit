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
# $Id: torusgeom.py,v 1.1 2005/03/08 20:24:34 mbaas Exp $

## \file torusgeom.py
## Contains the TorusGeom class.

import _core

# TorusGeom
class TorusGeom(_core.TorusGeom):
    def __init__(self, major=1.0, minor=0.1, segmentsu=16, segmentsv=8):
        _core.TorusGeom.__init__(self, major, minor, segmentsu, segmentsv)

