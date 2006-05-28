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
# $Id: x3dimport.py,v 1.2 2005/04/15 13:30:35 mbaas Exp $

import os.path
import _core
from cgtypes import *
from scene import getScene
from worldobject import WorldObject
from trimesh import TriMesh
from trimeshgeom import TriMeshGeom
from targetcamera import TargetCamera
from glpointlight import GLPointLight
from glfreespotlight import GLFreeSpotLight
from glfreedistantlight import GLFreeDistantLight
from glmaterial import GLMaterial, GLTexture
from box import Box
from quadrics import Sphere
from group import Group
import pluginmanager
from sl import *


# VRMLImporter
class VRMLImporter:

    _protocols = ["Import"]

    # extension
    def extension():
        """Return the file extensions for this format."""
        return ["wrl"]
    extension = staticmethod(extension)

    # description
    def description(self):
        """Return a short description for the file dialog."""
        return "Virtual Reality Modeling Language (VRML)"
    description = staticmethod(description)

    # importFile
    def importFile(self, filename):
        """Import a VRML file."""

        imp = _core.X3DReader(False)
        imp.read(filename)
        
#        _core.cyber(filename)
#        return

#        sg = _core.X3DSceneGraph()
#        if not sg.load(filename):
#            print "%s (%d): %s"%(sg.getParserErrorMessage(),
#                                 sg.getParserErrorLineNumber(),
#                                 sg.getParserErrorToken())
#            return

#        sg.foo("b = TriMeshGeom()")

# X3DImporter
class X3DImporter:

    _protocols = ["Import"]

    # extension
    def extension():
        """Return the file extensions for this format."""
        return ["x3d"]
    extension = staticmethod(extension)

    # description
    def description(self):
        """Return a short description for the file dialog."""
        return "Extensible 3D (X3D)"
    description = staticmethod(description)

    # importFile
    def importFile(self, filename):
        """Import a X3D file."""

        imp = _core.X3DReader()
        imp.read(filename)

     
######################################################################

# Register the Importer class as a plugin class
if hasattr(_core, "cyber"):
    pluginmanager.register(VRMLImporter)
    pluginmanager.register(X3DImporter)
