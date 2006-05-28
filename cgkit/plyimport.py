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
# $Id: plyimport.py,v 1.4 2005/05/09 14:34:24 mbaas Exp $

import os.path
import _core
from cgtypes import *
from geomobject import *
from polyhedron import *
import pluginmanager


# PLYImporter
class PLYImporter:

    _protocols = ["Import"]

    # extension
    def extension():
        """Return the file extensions for this format."""
        return ["ply"]
    extension = staticmethod(extension)

    # description
    def description(self):
        """Return a short description for the file dialog."""
        return "Polygon (PLY)"
    description = staticmethod(description)

    # importFile
    def importFile(self, filename, includevar=None, excludevar=None, invertfaces=False):
        """Import a PLY file.

        includevar is a list of primitive variable names that should be
        imported. excludevar is a list of primitive variable names that
        should not be imported.
        invertfaces specifies if the face orientations should be inverted
        or not.
        """

        self.includevar = includevar
        self.excludevar = excludevar

        imp = _core.PLYReader()
        imp.open(filename)
        # Obtain the header information
        header = imp.readHeader()

        # Create the variable declaration tuples for importing the data...
        inttypes = ["int8", "uint8", "int16", "uint16", "int32", "uint32",
                    "char", "uchar", "short", "ushort", "int", "uint"]
        vardecl = []
        vec3vars = {}
        elements, comment, objinfo = header
        for elname, ninstances, properties in elements:
            for propname, type, len_type, val_type in properties:
                # Vertex indices? (they are handled by default)
                if elname=="vertex" and propname in ["x", "y", "z"]:
                    continue
                # Vertex indices? (they are handled by default)
                if elname=="face" and propname in ["vertex_indices"]:
                    continue
                # Normals?
                if propname in ["nx", "ny", "nz"]:
                    if "N" not in vec3vars and self.isVarAccepted("N"):
                        vardecl.append(("N", NORMAL, elname, ("nx", "ny", "nz")))
                        vec3vars["N"] = True
                    continue

                if type=="list":
                    type = val_type
                if type in inttypes:
                    t = INT
                else:
                    t = FLOAT
                if self.isVarAccepted(propname):
                    vardecl.append((propname, t, elname, (propname,)))

#        print vardecl

        # Create a polyhedron
        name = os.path.splitext(os.path.basename(filename))[0]
        p = Polyhedron(name=name)
        # Set the comment and objinfo
        if comment!="":
            p.geom.newVariable("comment", CONSTANT, STRING)
            s = p.geom.slot("comment")
            s[0] = comment
        if objinfo!="":
            p.geom.newVariable("obj_info", CONSTANT, STRING)
            s = p.geom.slot("obj_info")
            s[0] = objinfo

        # Read the model
        imp.read(p.geom, vardecl, invertfaces)

        imp.close()

    # isVarAccepted
    def isVarAccepted(self, name):
        """Return True if the variable should be imported.

        name is the name of the primitive variable (which is not necessarily
        the ply property!).
        """
        if self.includevar!=None:
            if name not in self.includevar:
                return False
        if self.excludevar!=None:
            if name in self.excludevar:
                return False
        return True

######################################################################

# Register the Importer class as a plugin class
pluginmanager.register(PLYImporter)
