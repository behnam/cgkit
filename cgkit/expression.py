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
# $Id: expression.py,v 1.3 2005/10/18 07:02:39 mbaas Exp $

## \file expression.py
## Contains the Expression class.

"""This module contains the Expression class."""

from Interfaces import *
import protocols
import slots
from eventmanager import eventManager
from scene import getScene
import events
from cgtypes import *
from component import *
from sl import *
from math import *
import _core
       

# Expression
class Expression(Component):
    """Compute an output value using a user defined expression.

    This component outputs a single value that is driven by a user defined
    expression. The expression is specified by a string and can use an
    arbitrary number of parameters. The parameters and their default values
    have to be provided to the constructor via keyword arguments. An exception
    is the special variable "t" which will always hold the current time
    (unless you declare it explicitly).
    For each parameter a slot is created (<name>_slot), so it is also
    possible to animate the parameters. The output value can be accessed via
    the "output" and "output_slot" attributes.

    Example:

    \code
    s = Sphere()
    e = Expression("1.0 + amp*sin(freq*t)", amp=0.2, freq=2.0)
    e.output_slot.connect(s.radius_slot)
    \endcode
    
    """

    protocols.advise(instancesProvide=[ISceneItem])

    def __init__(self,
                 expr = "",
                 exprtype = None,
                 name = "Expression",
                 **keyargs
                 ):
        """Constructor.

        If no expression type is given the component tries to determine
        the type itself by executing the expression and inspecting the
        return type.

        \param expr (\c str) Expression
        \param exprtype (\c str) Output type or None
        \param name (\c str) Component name
        \param keyargs Parameters used in the expression
        """
        Component.__init__(self, name=name)

        self.expr = expr
        self.exprtype = exprtype

        # Create a parameter slot for every extra key arg...
        for k in keyargs:
            T = type(keyargs[k])
            if T==float or T==int:
                typ = "double"
                valstr = str(keyargs[k])
            elif T==vec3:
                typ = "vec3"
                x, y, z = keyargs[k]
                valstr = "vec3(%s, %s, %s)"%(x,y,z)
            elif T==vec4:
                typ = "vec4"
                x, y, z, w = keyargs[k]
                valstr = "vec4(%s, %s, %s, %s)"%(x,y,z,w)
            elif T==mat3:
                typ = "mat3"
                valstr = "mat3(%s)"%keyargs[k].toList(rowmajor=True)
            elif T==mat4:
                typ = "mat4"
                valstr = "mat4(%s)"%keyargs[k].toList(rowmajor=True)
            elif T==quat:
                typ = "quat"
                w, x, y, z = keyargs[k]
                valstr = "quat(%s, %s, %s, %s)"%(w,x,y,z)
            else:
                typ = "py"
                valstr = "keyargs[k]"
#                raise ValueError, "Unsupported type: %s"%T
            # Create slot
            exec "self.%s_slot = %sSlot(%s)"%(k, typ.capitalize(), valstr)
            exec "self.addSlot(k, self.%s_slot)"%k

        # If t was not explicitly given use the timer...
        if "t" not in keyargs:
            self.t_slot = DoubleSlot()
            getScene().timer().time_slot.connect(self.t_slot)
            self.addSlot("t", self.t_slot)

        # Store a list of all parameter names
        self.vars = keyargs.keys()
        if "t" not in self.vars:
            self.vars.append("t")

        if self.exprtype==None:
            self.exprtype = self._determineReturnType()

        # Create the output slot
        e = self.exprtype
        if e.lower()=="float":
            e = "double"
        exec "self.output_slot = Procedural%sSlot(self.outProc)"%e.capitalize()
        self.addSlot("output", self.output_slot)

        # Create dependencies
        for v in self.vars:
            exec "self.%s_slot.addDependent(self.output_slot)"%(v)

            

    def protocols(self):
        return [ISceneItem, IComponent]

    def outProc(self):
        for _v in self.vars:
            exec "%s = self.%s_slot.getValue()"%(_v, _v)
        return eval("%s(%s)"%(self.exprtype, self.expr))
     
    ## protected:
        
    # "output" property...
    exec slotPropertyCode("output")

    def _determineReturnType(self):
        """Try to execute the stored expression and return the output type.
        """
        for _v in self.vars:
            exec "%s = self.%s_slot.getValue()"%(_v, _v)
        out = eval(self.expr)
        T = type(out)
        if T==float or T==int:
            return "float"
        if isinstance(out, _core.vec3):
            return "vec3"
        if isinstance(out, _core.vec4):
            return "vec4"
        if isinstance(out, _core.mat3):
            return "mat3"
        if isinstance(out, _core.mat4):
            return "mat4"
        if isinstance(out, _core.quat):
            return "quat"

        if T==tuple or T==list:
            if len(out)==3:
                return "vec3"
            if len(out)==4:
                return "vec4"
            if len(out)==9:
                return "mat3"
            if len(out)==16:
                return "mat4"
            raise ValueError, "Unsupported sequence size: %d"%len(out)

        raise ValueError, "Unknown expression type: %s"%T
        
        
        

        

