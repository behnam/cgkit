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
# $Id: joints.py,v 1.1.1.1 2004/12/12 14:31:05 mbaas Exp $

## \file joints.py
## Contains the joint classes.

from worldobject import WorldObject
from slots import *

# HingeJoint
class HingeJoint(WorldObject):
    
    def __init__(self,
                 name="HingeJoint",
                 transform=None,
                 pos=None, rot=None, scale=None,
                 pivot=None,
                 offsetTransform=None,
                 body1=None, body2=None,
                 auto_insert=True):
        
        WorldObject.__init__(self, name=name, transform=transform,
                             pos=pos, rot=rot, scale=scale, pivot=pivot,
                             offsetTransform=offsetTransform,
                             auto_insert=auto_insert)

        self.lostop_slot = DoubleSlot()
        self.histop_slot = DoubleSlot()
        self.motorvel_slot = DoubleSlot()
        self.motorfmax_slot = DoubleSlot()
        self.bounce_slot = DoubleSlot()

        self.body1 = body1
        self.body2 = body2

