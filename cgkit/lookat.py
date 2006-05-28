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
# $Id: lookat.py,v 1.2 2005/07/21 15:07:11 mbaas Exp $

## \file lookat.py
## Contains the LookAt component.

"""This module contains the LookAt component which has a position
slot (pos) and a target slot (target) which are both of type vec3.
The output (output) is a mat3 that contains a rotation so that when positioned
at pos the z axis points to target."""

from component import createFunctionComponent
from cgtypes import *
from sl import radians
import scene

def _lookat(pos=vec3(0), target=vec3(0), up=vec3(0,0,1), roll=0.0):
    try:
        M = mat4().lookAt(pos, target, up)
    except:
        M = mat4(1)

    return M.getMat3()*mat3().rotation(radians(roll), vec3(0,0,1))

LookAt = createFunctionComponent(_lookat) # "mat3 (vec3 pos, vec3 target, vec3 up, double roll)")
