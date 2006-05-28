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
# $Id: euleradapter.py,v 1.1.1.1 2004/12/12 14:30:59 mbaas Exp $

## \file euleradapters.py
## Contains the EulerAdapter class.

import protocols
from Interfaces import *
from component import *
import slots
from cgtypes import *
from math import pi

# EulerAdapter
class EulerAdapter(Component):
    """Euler angle to mat3, mat4 or quat adapter.

    This class can be used to convert euler angles either to a mat3, a mat4
    or a quat. The input slots are \c anglex_slot, \c angley_slot and
    \c anglez_slot. The output slot is \c output_slot. The type of the output
    can be determined in the constructor.
    """

    protocols.advise(instancesProvide=[ISceneItem])

    def __init__(self,
                 anglex = 0,
                 angley = 0,
                 anglez = 0,
                 radians = False,
                 order = "xyz",
                 outtype = "mat3",
                 name="EulerAdapter",
                 auto_insert=True):
        """Constructor.

        \param anglex (\c float) Initial angle around x axis
        \param angley (\c float) Initial angle around y axis
        \param anglez (\c float) Initial angle around z axis
        \param radians (\c bool) True = Angles are specified in radians instead of degrees
        \param order (\c str) The rotation order ("xyz", "xzy", ...)
        \param outtpye (\c str) Output type ("mat3", "mat4", "quat")
        \param name (\c str) Component name
        \param auto_insert (\c bool) Auto insert flag
        """
        Component.__init__(self, name=name, auto_insert=auto_insert)

        if radians:
            self.factor = 1.0
        else:
            self.factor = pi/180.0

        self.anglex_slot = slots.DoubleSlot(anglex)
        self.angley_slot = slots.DoubleSlot(angley)
        self.anglez_slot = slots.DoubleSlot(anglez)
        self.addSlot("anglex", self.anglex_slot)
        self.addSlot("angley", self.angley_slot)
        self.addSlot("anglez", self.anglez_slot)

        if outtype=="mat3":
            self.output_slot = slots.ProceduralMat3Slot(self.computeMat3)
        elif outtype=="mat4":
            self.output_slot = slots.ProceduralMat4Slot(self.computeMat4)
        elif outtype=="quat":
            self.output_slot = slots.ProceduralQuatSlot(self.computeQuat)
        else:
            raise ValueError, "Unknown output type: %s"%outtype
        
        self.addSlot("output", self.output_slot)
            
        self.anglex_slot.addDependent(self.output_slot)
        self.angley_slot.addDependent(self.output_slot)
        self.anglez_slot.addDependent(self.output_slot)

        # self.fromEuler is the mat3() method that computes the matrix
        # from the euler angles. Which one exactly it is depends on the
        # order
        exec "self.fromEuler = mat3().fromEuler%s"%order.upper()

    def protocols(self):
        return [ISceneItem, IComponent]

    def computeMat3(self):
        """Slot procedure."""
        f = self.factor
        return self.fromEuler(f*self.anglex_slot.getValue(),
                              f*self.angley_slot.getValue(),
                              f*self.anglez_slot.getValue())

    def computeMat4(self):
        """Slot procedure."""
        f = self.factor
        m3 = self.fromEuler(f*self.anglex_slot.getValue(),
                            f*self.angley_slot.getValue(),
                            f*self.anglez_slot.getValue())
        res = mat4(1)
        res.setMat3(m3)
        return res

    def computeQuat(self):
        """Slot procedure."""
        f = self.factor
        m3 = self.fromEuler(f*self.anglex_slot.getValue(),
                            f*self.angley_slot.getValue(),
                            f*self.anglez_slot.getValue())
        res = quat().fromMat(m3)
        return res

    ## protected:
        
    # angle properties...
    exec slotPropertyCode("anglex")
    exec slotPropertyCode("angley")
    exec slotPropertyCode("anglez")

    # "output" property...
    exec slotPropertyCode("output")
    

