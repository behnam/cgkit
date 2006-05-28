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
# $Id: bvhimport.py,v 1.1 2005/02/11 14:32:34 mbaas Exp $

from cgtypes import *
from joint import Joint
from valuetable import ValueTable
import bvh
import pluginmanager
from sl import *

# BVHReader
class BVHReader(bvh.BVHReader):
    """Specialized BVH reader class.

    This class creates a hierarchy of joints and applies the motion to it.
    """
    
    def __init__(self, filename):
        bvh.BVHReader.__init__(self, filename)
      

    def onHierarchy(self, root):
        self.createSkeleton(root)
        self.root = root

    def onMotion(self, frames, dt):
        self.frames = frames
        self.dt = dt
        self.currentframe = 0

    def onFrame(self, values):
        self.applyMotion(self.root, values)
        self.currentframe += 1

    def applyMotion(self, node, values):
        """Apply a motion sample to the skeleton.

        node is the current joint and values the joint angles for the
        entire skeleton.
        The method returns the remaining joint angles.
        """

        t = self.currentframe*self.dt
        
        nc = len(node.channels)
        vals = values[:nc]
        pos = vec3()
        pos_flag = False
        for ch,v in zip(node.channels, vals):
            if ch=="Xrotation":
                node.vtx.add(t, v)
            elif ch=="Yrotation":
                node.vty.add(t, v)
            elif ch=="Zrotation":
                node.vtz.add(t, v)
            elif ch=="Xposition":
                pos.x = v
                pos_flag = True
            elif ch=="Yposition":
                pos.y = v
                pos_flag = True
            elif ch=="Zposition":
                pos.z = v
                pos_flag = True

        if pos_flag:
            node.vtpos.add(t, pos)
            
        values = values[nc:]
        for c in node.children:
            values = self.applyMotion(c, values)
        return values

    # createSkeleton
    def createSkeleton(self, node, parent=None):
        """Create the skeleton hierarchy.

        This method creates the skeleton recursively. Each invocation
        creates one joint.
        """
        order = self.rotationOrder(node.channels)
        # Create a new Joint object
        j = Joint(name = node.name,
                  pos = vec3(node.offset),
                  rotationorder = order,
                  parent = parent)
        # Store the joint in the node so that later the motion can be applied
        node.joint = j
        
        vtx = ValueTable(type="double")
        vty = ValueTable(type="double")
        vtz = ValueTable(type="double")
        vtx.output_slot.connect(j.anglex_slot)
        vty.output_slot.connect(j.angley_slot)
        vtz.output_slot.connect(j.anglez_slot)
        node.vtx = vtx
        node.vty = vty
        node.vtz = vtz
        if node.isRoot():
            vtpos = ValueTable(type="vec3")
            vtpos.output_slot.connect(j.pos_slot)
            node.vtpos = vtpos
            
        for c in node.children:
            self.createSkeleton(c, j)

    # rotationOrder
    def rotationOrder(self, channels):
        """Determine rotation order string from the channel names.
        """
        res = ""
        for c in channels:
            if c[-8:]=="rotation":
                res += c[0]

        # Complete the order string if it doesn't already contain
        # all three axes
        m = { "":"XYZ",
              "X":"XYZ", "Y":"YXZ", "Z":"ZXY",
              "XY":"XYZ", "XZ":"XZY",
              "YX":"YXZ", "YZ":"YZX",
              "ZX":"ZXY", "ZY":"ZYX" }
        if res in m:
            res = m[res]
        return res

######################################################################

# BVHImporter
class BVHImporter:

    _protocols = ["Import"]

    # extension
    def extension():
        """Return the file extensions for this format."""
        return ["bvh"]
    extension = staticmethod(extension)

    # description
    def description(self):
        """Return a short description for the file dialog."""
        return "Biovision Hierarchical"
    description = staticmethod(description)

    # importFile
    def importFile(self, filename):
        """Import a BVH file."""
        
        bvh = BVHReader(filename)
        bvh.read()


######################################################################

# Register the Importer class as a plugin class
pluginmanager.register(BVHImporter)

