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
# $Id: asfamcimport.py,v 1.2 2005/04/21 17:25:45 mbaas Exp $

import os.path, glob
from cgtypes import *
from quadrics import Sphere
from joint import Joint
from valuetable import ValueTable
import asfamc
import pluginmanager
from sl import *

# ASFReader
class ASFReader(asfamc.ASFReader):
    """Specialized ASF reader class.

    The class creates a hierarchy of Joint objects.
    """

    def __init__(self, filename):
        asfamc.ASFReader.__init__(self, filename)
        # Bone data
        self.bones = {}
        # cgkit Joint objects (+root)
        self.joints = {}

        self.len_scale = 1.0

    def onUnits(self, units):
        self.len_scale = units.get("length", 1.0)
        
    def onRoot(self, data):
        pos = self.toVec3(data.get("position", (0,0,0)))
        orient = self.toVec3(data.get("orientation", (0,0,0)))
        pos = self.len_scale*vec3(pos)
        orient = vec3(orient)
        self.joints["root"] = Sphere(name="root", pos=pos, radius=0.2)
        # Dummy "bone" data
        self.bones["root"] = { "name":"root",
                               "order":data.get("order"),
                               "direction":vec3(1,0,0),
                               "length":0.0,
                               "axis_order":data.get("axis")[0]}
        

    def onBonedata(self, bones):
        for data in bones:
            name = data.get("name")[0]
            dir = self.toVec3(data.get("direction"))
            length = self.len_scale*float(data.get("length")[0])
            axis = self.toVec3(data.get("axis")[:3])
            axis_order = data.get("axis")[3]
            self.bones[name] = { "name":name,
                                 "direction":dir,
                                 "length":length,
                                 "axis":axis,
                                 "axis_order":axis_order,
                                 "dof":data.get("dof", ""),
                                 "limits":data.get("limits")}

    def onHierarchy(self, links):
        # At the end, this list contains the leaves which need
        # a dummy joint at the end.
        leaves = []
        for parentname, childnames in links:
            leaves += childnames
            if parentname in leaves:
                leaves.remove(parentname)
            # Create the second joint of the bone called parentname
            # (which is the first joint of the bone called data["name"])
            parent = self.joints[parentname]
            data = self.bones[parentname]
            dir = data["direction"].normalize()
            length = data["length"]
            for childname in childnames:
                data = self.bones[childname]
                axis = data["axis"]
                ao = data["axis_order"]
                axis_order = ao[2]+ao[1]+ao[0]
                j = Joint(name = data["name"],
                          rotationorder = axis_order,
                          radius = 0.3,
                          pos = length*dir.normalize(),
                          parent = parent)
                exec "fromEuler = mat3.fromEuler%s"%axis_order.upper()
                R = mat3()
                fromEuler(R, radians(axis.x), radians(axis.y), radians(axis.z))
                j.setOffsetTransform(mat4(1).setMat3(R))
                j.freezePivot()
                self.joints[j.name] = j

        # Create end joints
        for name in leaves:
            parent = self.joints[name]
            data = self.bones[name]
            try:
                dir = data["direction"].normalize()
            except:
                dir = vec3(0)
            length = data["length"]
            Joint(name = name+"_end",
                  rotationorder = "xyz",
                  radius = 0.3,
                  pos = length*dir,
                  parent = parent)

    def toVec3(self, stup):
        return vec3(map(lambda x: float(x), stup))
        
# AMCReader
class AMCReader(asfamc.AMCReader):
    """Specialized AMC reader class.

    When reading the AMC file, the content is just read and stored
    in self.values.
    Once the data is read, the applyMotion() method has to be called
    which takes an instance of an ASFReader class and the framerate
    of the data as input.
    """

    def __init__(self, filename):
        asfamc.AMCReader.__init__(self, filename)

        # Key: Bone name  Value: A list of values (one sublist per frame)
        self.values = {}

    def onFrame(self, framenr, data):
        for name,values in data:
            if name not in self.values:
                self.values[name] = []
            self.values[name].append(values)

    def applyMotion(self, asf, framerate=25):
        """Apply the motion to a previously read skeleton.

        asf is the ASFReader class that has already read the skeleton.
        framerate is the rate that was used to record the motion data.
        """

        for name in self.values.keys():
            track = self.values[name]
            print name,
            if name=="root":
                self.applyRootTrack(asf, track, framerate)
            else:
                self.applyBoneTrack(asf, name, track, framerate)
        print ""

    def applyBoneTrack(self, asf, name, track, framerate):
        data = asf.bones[name]
        order = data["dof"]
        order = map(lambda s: s.lower(), order)
        vtabx = []
        vtaby = []
        vtabz = []
        framenr = 0
        for vals in track:
            t = float(framenr)/framerate
            d = self.valueDict(vals, order)
            if "rx" in d:
                vtabx.append((t,d["rx"]))
            if "ry" in d:
                vtaby.append((t,d["ry"]))
            if "rz" in d:
                vtabz.append((t,d["rz"]))
            framenr += 1

        total_t = float(framenr)/framerate

        joint = asf.joints[name]
        if vtabx!=[]:
            vt = ValueTable(type="double", values=vtabx, modulo=total_t)
            vt.output_slot.connect(joint.anglex_slot)
        if vtaby!=[]:
            vt = ValueTable(type="double", values=vtaby, modulo=total_t)
            vt.output_slot.connect(joint.angley_slot)
        if vtabz!=[]:
            vt = ValueTable(type="double", values=vtabz, modulo=total_t)
            vt.output_slot.connect(joint.anglez_slot)
            

    def applyRootTrack(self, asf, track, framerate):

        len_scale = asf.len_scale
        data = asf.bones["root"]
        order = data["order"]
        order = map(lambda s: s.lower(), order)
        ao = data["axis_order"]
        axis_order = ao[2]+ao[1]+ao[0]
        vtab = []
        vtabrot = []
        framenr = 0
        for vals in track:
            t = float(framenr)/framerate
            d = self.valueDict(vals, order)
            pos = len_scale*vec3(d["tx"], d["ty"], d["tz"])
            vtab.append((t, pos))
            
            ang = vec3(d["rx"], d["ry"], d["rz"])
            exec "fromEuler = mat3.fromEuler%s"%axis_order.upper()
            R = mat3()
            fromEuler(R, radians(ang.x), radians(ang.y), radians(ang.z))
            vtabrot.append((t, R))
            
            framenr += 1

        total_t = float(framenr)/framerate

        vt = ValueTable(values=vtab, modulo=total_t)
        vt.output_slot.connect(asf.joints["root"].pos_slot)
        vr = ValueTable(values=vtabrot, type="mat3", modulo=total_t)
        vr.output_slot.connect(asf.joints["root"].rot_slot)
            

    # valueDict
    def valueDict(self, values, order):
        """Convert a value list into a dictionary.

        values is a sequence of values whose order is defined by the
        argument order. order must be a sequence of strings where each
        string defines the meaning of the corresponding value in the
        list values.
        Example: values = [10,20,30]  order = ["tx", "ty", "tz"]
        Result: {"tx":10, "ty":20, "tz":30}
        """
        if len(values)!=len(order):
            raise ValueError, "Invalid number of values"

        res = {}
        for v,t in zip(values, order):
            res[t]=v
            
        return res

######################################################################

# ASFImporter
class ASFImporter:

    _protocols = ["Import"]

    # extension
    def extension():
        """Return the file extensions for this format."""
        return ["asf"]
    extension = staticmethod(extension)

    # description
    def description(self):
        """Return a short description for the file dialog."""
        return "Acclaim Skeleton File"
    description = staticmethod(description)

    # importFile
    def importFile(self, filename):
        """Import an ASF file."""
        
        asf = ASFReader(filename)
        asf.read()

# AMCImporter
class AMCImporter:

    _protocols = ["Import"]

    # extension
    def extension():
        """Return the file extensions for this format."""
        return ["amc"]
    extension = staticmethod(extension)

    # description
    def description(self):
        """Return a short description for the file dialog."""
        return "Acclaim Motion Capture Data"
    description = staticmethod(description)

    # importFile
    def importFile(self, filename, asf=None, framerate=30):
        """Import an AMC file."""

        if asf==None:
            # Check for an ASF file with the same name than the AMC file
            asf, ext = os.path.splitext(filename)
            asf += ".asf"
            if not os.path.exists(asf):
                dir = os.path.dirname(filename)
                asflist = glob.glob(os.path.join(dir, "*.asf"))
                if len(asflist)==1:
                    asf = asflist[0]
                elif len(asflist)==0:
                    raise ValueError, "No skeleton file found."
                else:
                    raise ValueError, "There are several skeleton files in the directory, please specify one or rename the ASF file so it is identical with the AMC file."

        asf = ASFReader(asf)
        asf.read()

        amc = AMCReader(filename)
#        print 'Reading motion file "%s"...'%amcfile
        amc.read()
#        print "Applying motion..."
        amc.applyMotion(asf, framerate=framerate)
        


######################################################################

# Register the Importer class as a plugin class
pluginmanager.register(ASFImporter)
pluginmanager.register(AMCImporter)

