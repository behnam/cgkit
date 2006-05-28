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
# $Id: ccylindergeom.py,v 1.1.1.1 2004/12/12 14:30:55 mbaas Exp $

## \file ccylindergeom.py
## Contains the CCylinderGeom class.

import _core

# CCylinderGeom
class CCylinderGeom(_core.CCylinderGeom):
    def __init__(self, radius=1.0, length=1.0, segmentsu=16, segmentsvl=1, segmentsvr=4):
        _core.CCylinderGeom.__init__(self, radius, length, segmentsu, segmentsvl, segmentsvr)

