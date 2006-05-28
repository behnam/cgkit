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
# $Id: plyexport.py,v 1.2 2005/05/08 22:17:42 mbaas Exp $

import os.path, sys
from cgtypes import *
from scene import getScene
from geomobject import *
from trimeshgeom import TriMeshGeom
from polyhedrongeom import PolyhedronGeom
import pluginmanager
import cmds
import _core

# PLYExporter
class PLYExporter:

    _protocols = ["Export"]

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

    # exportFile
    def exportFile(self, filename, object=None, mode="ascii"):
        """Export a PLY file.

        object is the object to export. If it is None, it will be taken
        from the scene. If there is more than one object in the scene,
        an exception is thrown.
        mode specifies whether the output file will be ascii or binary.
        The values can be "ascii", "little_endian", "big_endian".
        """

        if object==None:
            # Get a list of all objects that have a geom
            objs = list(getScene().walkWorld())
            objs = filter(lambda obj: obj.geom!=None, objs)
            if len(objs)==0:
                raise ValueError, "No object to export."
            elif len(objs)>1:
                raise ValueError, "Only a single object can be exported."
            object = objs[0]
            
        object = cmds.worldObject(object)
        if object.geom==None:
            raise ValueError, "No geometry attached to object %s"%object.name
        geom = self.convertObject(object)
        if geom==None:
            raise ValueError, "Cannot export geometry of type %s as a PLY file"%(object.geom.__class__.__name__)

        # Open the file...
        ply = _core.PLYWriter()
        try:
            mode = eval ("_core.PlyStorageMode.%s"%mode.upper())
        except:
            raise ValueError, "Invalid mode: %s"%mode
        ply.create(filename, mode)

        # Set comment
        var = geom.findVariable("comment")
        if var!=None and var[1]==CONSTANT and var[2]==STRING and var[3]==1:
            slot = geom.slot("comment")
            for s in slot[0].split("\n"):
                ply.addComment(s)
        # Set obj_info
        var = geom.findVariable("obj_info")
        if var!=None and var[1]==CONSTANT and var[2]==STRING and var[3]==1:
            slot = geom.slot("obj_info")
            for s in slot[0].split("\n"):
                ply.addObjInfo(s)

        # Write the model
        ply.write(geom, object.worldtransform)
        ply.close()

    # convertObject
    def convertObject(self, obj):
        """Converts an object into a polyhedron or trimesh if necessary.

        The return value is a GeomObject (TriMeshGeom or PolyhedronGeom)
        or None.
        """
        geom = obj.geom
        if isinstance(geom, TriMeshGeom):
            return geom
        
        if not isinstance(geom, PolyhedronGeom):
            # Try to convert into a polyhedron...
            pg = PolyhedronGeom()
            try:
                geom.convert(pg)
                geom = pg
            except:
                pass

        # Is it a PolyhedronGeom that has no polys with holes? then return
        # the geom...
        if isinstance(geom, PolyhedronGeom) and not geom.hasPolysWithHoles():
            return geom

        # Try to convert into a triangle mesh...
        tm = TriMeshGeom()
        try:
            geom.convert(tm)
            return tm
        except:
            pass

        return None
        

######################################################################

# Register the exporter class as a plugin class
pluginmanager.register(PLYExporter)
