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
# $Id: ifsimport.py,v 1.1.1.1 2004/12/12 14:31:04 mbaas Exp $

import os.path, struct
from cgtypes import *
from worldobject import WorldObject
from trimesh import TriMesh
from trimeshgeom import TriMeshGeom
import pluginmanager

# IfsImporter
class IfsImporter:
    """IFS importer.

    This class imports models from the Brown Mesh Set library which are
    stored in the Indexed Face Set (IFS) format.
    """

    _protocols = ["Import"]

    # extension
    def extension():
        """Return the file extensions for this format."""
        return ["ifs"]
    extension = staticmethod(extension)

    # description
    def description(self):
        """Return a short description for the file dialog."""
        return "Indexed face set"
    description = staticmethod(description)

    # importFile
    def importFile(self, filename):
        """Import an IFS file."""

        f = file(filename, "rb")

        # Check the header...
        s = self.readString(f)
        if s!="IFS":
            raise ValueError, 'The file "%s" is is not a IFS file.'%filename

        # Read (and ignore) the version number
        s = f.read(4)
        ver = struct.unpack("<f", s)[0]

        # Read the model name
        modelname = self.readString(f)

        # Create the mesh geom
        tm = TriMeshGeom()

        # Read vertices...
        s = self.readString(f)
        if s!="VERTICES":
            raise ValueError, "Vertices chunk expected, got '%s' instead."%s

        s = f.read(4)
        numverts = int(struct.unpack("<I", s)[0])
        tm.verts.resize(numverts)

        for i in range(numverts):
            s = f.read(12)
            x,y,z = struct.unpack("<fff", s)
            tm.verts[i] = vec3(x,y,z)

        # Read faces...
        s = self.readString(f)
        if s!="TRIANGLES":
            raise ValueError, "Triangle chunk expected, got '%s' instead."%s
            
        s = f.read(4)
        numfaces = int(struct.unpack("<I", s)[0])
        tm.faces.resize(numfaces)

        for i in range(numfaces):
            s = f.read(12)
            a,b,c = struct.unpack("<III", s)
            tm.faces[i] = (int(a), int(b), int(c))

        # Create a world object
        obj = TriMesh(name=modelname)
        obj.geom = tm


    def readString(self, fhandle):
        """Read a string.

        \param fhandle Open file handle
        \return String
        """
        s = fhandle.read(4)
        w = int(struct.unpack("<I", s)[0])
        s = fhandle.read(w)
        # Return the string without the trailing \000
        return s[:-1]


######################################################################

# Register the IfsImporter class as a plugin class
pluginmanager.register(IfsImporter)
