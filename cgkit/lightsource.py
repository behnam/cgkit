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
# $Id: lightsource.py,v 1.1.1.1 2004/12/12 14:31:06 mbaas Exp $

## \file lightsource.py
## Contains the LightSource base class.

import protocols
import scene
from Interfaces import *
from worldobject import _initWorldObject, _preInitWorldObject
import _core

# LightSource
class LightSource(_core.LightSource):

    protocols.advise(instancesProvide=[ISceneItem, ISceneItemContainer])

    def __init__(self,
                 name="LightSource",
                 parent = None,
                 auto_insert = True,
                 **params):

        exec _preInitWorldObject
        _core.LightSource.__init__(self, name)

        _initWorldObject(self, name=name, auto_insert=auto_insert,
                         parent=parent, **params)
    
        
