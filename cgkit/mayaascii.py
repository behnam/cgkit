# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is the Python Computer Graphics Kit.
#
# The Initial Developer of the Original Code is Matthias Baas.
# Portions created by the Initial Developer are Copyright (C) 2004
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
# $Id: mayaascii.py,v 1.10 2005/06/15 19:18:46 mbaas Exp $

import simplecpp

# The keywords that may be used for the value True
_true_keywords = ["true", "on", "yes"]

# MAPreProcessor
class MAPreProcessor(simplecpp.PreProcessor):
    """Preprocess the source file and invoke a callback for each line.
    """
    
    def __init__(self, linehandler):
        simplecpp.PreProcessor.__init__(self)
        self.linehandler = linehandler
        
    def output(self, s):
        # Ignore the preprocessor lines
        if s[0:1]!="#":
            self.linehandler(s)

# PolyFace
class PolyFace:
    """Stores the data of a polyFace value.

    PolyFace objects are returned by the getValue() method of the
    Attribute class when the type was "polyFaces".
    """
    def __init__(self):
        # face (list of ints)
        self.f = None
        # holes (list of list of ints)
        # There's a list if vertex ids for each hole
        self.h = []
        # face tex coords (list of list of ints)
        self.mf = []
        # hole tex coords (list of list of ints)
        self.mh = []
        # tex coords (list of list of 2-tuple (uvset, list of ints))
        # There's a list for each loop (#f + #h).
        # Each list contains a list of 2-tuples (as there can be more than
        # one uvset per face)
        self.mu = []
        # face colors (list of list of ints)
        # There's a list for each loop (#f + #h)
        self.fc = []

    # hasValidTexCoords
    def hasValidTexCoords(self):
        loops = [self.f]+self.h
        if len(self.mu)!=len(loops):
            return False
        for mus,loop in zip(self.mu, loops):
            if len(mus)==0:
                return False
            if len(mus[0][1])!=len(loop):
                return False

        return True

    # newLoop
    def newLoop(self):
        """This is an internal method used during construction of a poly face.

        The method has to be called after a new 'f' or 'h' attribute was
        encountered. The method will then allocate a new empty list for the
        texture coords and face colors. This list is then filled during
        construction.
        This ensures that the number of tex coords and color lists matches
        the number of loops.
        """
        self.mf.append([])
        self.mh.append([])
        self.mu.append([])
        self.fc.append([])

# NurbsCurve
class NurbsCurve:
    """Stores the data of a nurbsCurve value.

    NurbsCurve objects are returned by the getValue() method of the
    Attribute class when the type was "nurbsCurve".
    """
    def __init__(self):
        # Degree
        self.degree = 0
        # Spans
        self.spans = 0
        # Form attribute (0=open, 1=closed, 2=periodic)
        self.form = 0
        # Is the curve rational?
        self.isrational = False
        # Dimension (2 or 3)
        self.dimension = 0
        # Knots
        self.knots = []
        # Control vertices
        self.cvs = []

# NurbsSurface
class NurbsSurface:
    """Stores the data of a nurbsSurface value.

    NurbsSurface objects are returned by the getValue() method of the
    Attribute class when the type was "nurbsSurface".
    """
    def __init__(self):
        # Degree in u and v
        self.udegree = 0
        self.vdegree = 0
        # Form attribute in u and v (0=open, 1=closed, 2=periodic)
        self.uform = 0
        self.vform = 0
        # Is the surface rational?
        self.isrational = False
        # Knots in u and v
        self.uknots = []
        self.vknots = []
        # Control vertices
        self.cvs = []

# Attribute
class Attribute:
    """This class stores an attribute (i.e. the name and its value).
    """
    
    def __init__(self, attr, vals, opts):
        """Constructor.

        attr, vals and opts are the parameters of the onSetAttr() callback.
        """
        self._attr = attr
        self._vals = vals
        self._opts = opts

    # getBaseName
    def getBaseName(self):
        """Return the base name of the attribute.

        This is the first part of the attribute name (and may actually
        refer to another attribute).

        ".t"            -> "t"
        ".ed[0:11]"     -> "ed"
        ".uvst[0].uvsn" -> "uvst"
        """
        a = self._attr.split(".")
        b = a[1].split("[")
        return b[0]

    # getFullName
    def getFullName(self):
        return self._attr

    # getValue
    def getValue(self, type=None, n=None):
        """Return the converted value.

        type is a string containing the required type of the value.

        Valid types are "bool", "int", "float"
        "short2", "short3", "long2", "long3",
        "double2", "double3", "float2", "float3", "string", "int32Array",
        "doubleArray", "polyFaces", "nurbsSurface", "nurbsCurve",
        "double4", "float4" (for colors).
        """
        
        # Check if the value type was specified in the setAttr call
        valtype = self._opts.get("type", [None])[0]
        if valtype==None and type==None:
            valtype = "float"

        # Use the real attribute type if no required type was specified
        if type==None:
            type = valtype

        # Use the provided type if the attribute had no 'type' option
        if valtype==None:
            valtype = type

        # No type information given?
        if valtype==None:
            raise ValueError, "No type information available for attribute '%s'"%self.getBaseName()

        # Check if the type matches the required type...
        if valtype!=type:
            raise ValueError, "Attribute of type %s expected, got %s"%(type, valtype)

        # Convert the values..
        convertername = "convert"+type[0].upper()+type[1:]
        f = getattr(self, convertername)
        vs = f()
        if n==None:
            return vs
        if len(vs)!=n:
            raise ValueError, "%s: %d values expected, got %d"%(self._attr, n, len(vs))
        if n==1:
            return vs[0]
        else:
            return vs

    # The following convert methods have to convert the value list (self._vals)
    # into the appropriate type. The return value is always a list of values.

    def convertInt(self):
        return map(lambda x: int(x), self._vals)

    def convertFloat(self):
        return map(lambda x: float(x), self._vals)

    def convertBool(self):
        res = []
        for v in self._vals:
            res.append(v in _true_keywords)
        return res

    def convertLong2(self):
        res = []
        vs = self._vals
        for i in range(0,len(vs), 2):
            res.append((int(vs[i]), int(vs[i+1])))
        return res

    convertShort2 = convertLong2

    def convertLong3(self):
        res = []
        vs = self._vals
        for i in range(0,len(vs), 3):
            res.append((int(vs[i]), int(vs[i+1]), int(vs[i+2])))
        return res

    convertShort3 = convertLong3

    def convertDouble2(self):
        res = []
        vs = self._vals
        for i in range(0,len(vs), 2):
            res.append((float(vs[i]), float(vs[i+1])))
        return res

    convertFloat2 = convertDouble2

    def convertDouble3(self):
        res = []
        vs = self._vals
        for i in range(0,len(vs), 3):
            res.append((float(vs[i]), float(vs[i+1]), float(vs[i+2])))
        return res

    convertFloat3 = convertDouble3

    def convertDouble4(self):
        res = []
        vs = self._vals
        for i in range(0,len(vs), 4):
            res.append((float(vs[i]), float(vs[i+1]), float(vs[i+2]), float(vs[i+3])))
        return res

    convertFloat4 = convertDouble4

    def convertString(self):
        return map(lambda x: str(x), self._vals)

    def convertInt32Array(self):
        n = int(self._vals[0])
        return map(lambda x: int(x), self._vals[1:n+1])

    def convertDoubleArray(self):
        n = int(self._vals[0])
        return map(lambda x: float(x), self._vals[1:n+1])

    def convertPolyFaces(self):
        res = []
        vs = self._vals
        i=0
        pf = None
        while i<len(vs):
            c = vs[i]
            i+=1
            if c not in ["f", "h", "mf", "mh", "mu", "fc"]:
                raise ValueError, "Unknown polyFace data: %s"%c
            
            if c=="mu":
                uvset = int(vs[i])
                i+=1
                
            n = int(vs[i])
            ids = map(lambda x: int(x), vs[i+1:i+n+1])
            i+=n+1
            
            # Is that already a new polyFace? Then store the previous one
            # and start a new face
            if c=="f":
                if pf!=None:
                    res.append(pf)
                pf = PolyFace()
                pf.f = ids
                pf.newLoop()
            elif c=="h":
                pf.h.append(ids)
                pf.newLoop()
            elif c=="mu":
                pf.mu[-1].append((uvset, ids))
            else:
                # Set the IDs into the corresponding list
                lst = getattr(pf, c)
                lst[-1] = ids

        # Append the last face
        if pf!=None:
            res.append(pf)
            
        return res

    def convertNurbsCurve(self):
        res = []
        vs = self._vals

        while vs!=[]:
            nc = NurbsCurve()
            nc.degree = int(vs[0])
            nc.spans = int(vs[1])
            nc.form = int(vs[2])
            nc.isrational = vs[3] in _true_keywords
            nc.dimension = int(vs[4])
            # Get knots
            n = int(vs[5])
            nc.knots = map(lambda x: float(x), vs[6:n+6])
            vs = vs[n+6:]
            # Get CVs
            n = int(vs[0])
            dim = nc.dimension
            if nc.isrational:
                dim += 1
            cvs = []
            for i in range(n):
                cvs.append( tuple(map(lambda x: float(x), vs[1+i*dim:1+(i+1)*dim])) )
            nc.cvs = cvs
            vs = vs[1+n*dim:]
            res.append(nc)

        return res

    def convertNurbsSurface(self):
        res = []
        vs = self._vals

        while vs!=[]:
            ns = NurbsSurface()
            ns.udegree = int(vs[0])
            ns.vdegree = int(vs[1])
            ns.uform = int(vs[2])
            ns.vform = int(vs[3])
            ns.isrational = vs[4] in _true_keywords
            vs = vs[5:]
            # Get u knots
            n = int(vs[0])
            ns.uknots = map(lambda x: float(x), vs[1:n+1])
            vs = vs[n+1:]
            # Get v knots
            n = int(vs[0])
            ns.vknots = map(lambda x: float(x), vs[1:n+1])
            vs = vs[n+1:]
            # Skip TRIM|NOTRIM
            if vs[0] in ["TRIM", "NOTRIM"]:
                vs = vs[1:]
            # Get CVs
            n = int(vs[0])
            if ns.isrational:
                dim = 4
            else:
                dim = 3
            cvs = []
            for i in range(n):
                cvs.append( tuple(map(lambda x: float(x), vs[1+i*dim:1+(i+1)*dim])) )
            ns.cvs = cvs
            vs = vs[1+n*dim:]
            res.append(ns)

        return res
        
    # setValue
    def setValue(self, value):
        pass

# MultiAttrStorage
class MultiAttrStorage:
    """This helper class serves as MEL style array.

    You can assign values to arbitrary indices which will automatically
    enlarge the array (filling missing values with None).
    The slicing operation is different than Python as the stop index is
    inclusive. The actual array is stored in the _array attribute.

    Example:

    a = MultiAttrStorage()
    a[2] = 5               # -> [None, None, 5]
    a[4:6] = [1,2,3]       # -> [None, None, 5, None, 1, 2, 3]


    Reading an arbitrary attribute from an object of this class will
    automatically create this attribute which will in turn be of type
    MultiAttrStorage. So this class can also be used for compound objects.
    If you want to check such a compound for a particular attribute you
    must not use hasattr() as this would silently create the attribute if
    it didn't already exist and always return True. Instead you have to
    do the check as follows:

    if <attrname> in dir(compound):
       ...
    """
    def __init__(self):
        self._array = []

    def __iter__(self):
        return iter(self._array)

    def __len__(self):
        return len(self._array)

    def __getattr__(self, name):
        if name[:2]=="__":
            raise AttributeError, name
        ma = MultiAttrStorage()
        setattr(self, name, ma)
        return ma

    def __getitem__(self, key):
        if key>=len(self._array):
            ma = MultiAttrStorage()
            self.__setitem__(key, ma)
            return ma
        else:
            return self._array[key]

    def __setitem__(self, key, value):
        al = len(self._array)
        if type(key)==slice:
            if key.stop>=al:
                self._array += (key.stop-al+1)*[None]
            if len(value)!=(key.stop-key.start+1):
                raise ValueError, "%d values expected, got %d"%(key.stop-key.start+1, len(value))
            self._array[key.start:key.stop+1] = value
#            print key.start,key.stop
        else:
            if key<al:
                self._array[key] = value
            else:
                self._array += (key-al)*[None] + [value]

# Node
class Node:
    """Node.
    """
    def __init__(self, nodetype, opts):
        self.nodetype = nodetype
        self.opts = opts
        # Attribute values. Key: base name / Value: List of Attribute objects
        self._setattr = {}

        # If True, accessing attributes will automatically create a new
        # attribute that contains a MultiAttrStorage object
        self._create_attributes = False

        # Key: Local attribute / Value: (nodename, attrname) of source
        self.in_connections = {}
        # Key: Local attribute / Value: List of (node, nodename, attrname) tuples
        self.out_connections = {}

    def __getattr__(self, name):
        if self._create_attributes:
            ma = MultiAttrStorage()
            setattr(self, name, ma)
            return ma
        raise AttributeError, name

    # getName
    def getName(self):
        """Return the node name or None.
        """
        return self.opts.get("name", [None])[0]

    # getParentName
    def getParentName(self):
        """Return the parent's node name or None.
        """
        return self.opts.get("parent", [None])[0]


    # setAttr
    def setAttr(self, attr, vals, opts):
        """Store the attribute value.

        The arguments are the same than the arguments of the onSetAttr()
        callback.
        """
        # Is this setattr call only used to "declare" the size of an array?
        # then ignore the call
        if vals==[] and "size" in opts:
            return
        
        a = Attribute(attr, vals, opts)
        basename = a.getBaseName()
        if basename in self._setattr:
            self._setattr[basename].append(a)
        else:
            self._setattr[basename] = [a]

    # addAttr
    def addAttr(self, opts):
        pass

    # addInConnection
    def addInConnection(self, localattr, node, attr):
        """Add an 'in' connection.

        'in' = node.attr is connected to localattr
        node is a Node object and attr the full attribute name.
        """
        self.in_connections[localattr] = (node, attr)

    # addutConnection
    def addOutConnection(self, localattr, node, nodename, attrname):
        """Add an 'out' connection.

        'out' = localattr is connected to node.attr
        node is a Node object, nodename the name of the node and attrname
        the full attribute name.
        """
        if self.out_connections.has_key(localattr):
            self.out_connections[localattr].append((node, nodename, attrname))
        else:
            self.out_connections[localattr] = [(node, nodename, attrname)]
        

    # getAttrValue
    def getAttrValue(self, lname, sname, type, n=1, default=None):
        """Get the Python value of an attribute.

        lname is the long name, sname the short name. type is the
        required type and n the required number of elements. type and
        n may be None.
        The return value is either a normal Python type (int, float, sequence)
        or a MultiAttrStorage object in cases where the setAttr command
        contained the index operator.
        """
        self._executeAttrs(lname, type, n)
        self._executeAttrs(sname, type, n)
        if hasattr(self, lname):
            return getattr(self, lname)
        return getattr(self, sname, default)

    # getInNode
    def getInNode(self, localattr_long, localattr_short):
        """Return the node and attribute that serves as input for localattr.

        The return value is a 2-tuple (nodename, attrname) that specifies
        the input connection for localattr. (None, None) is returned if there
        is no connection.
        """
        node, attr = self.in_connections.get(localattr_long, (None, None))
        if node==None:
            node, attr = self.in_connections.get(localattr_short, (None, None))
        return node, attr

    # getOutNodes
    def getOutNodes(self, localattr_long, localattr_short):
        """Return the nodes and attributes that this attribute connects to.

        The return value is a list of 3-tuples (node, nodename, attrname) that
        specify the output connections for localattr.
        """
        lst = self.out_connections.get(localattr_long, None)
        if lst==None:
            lst = self.out_connections.get(localattr_short, [])
        return lst

    # getOutAttr
    def getOutAttr(self, localattr_long, localattr_short, dstnodetype):
        """Check if a local attribute is connected to a particular type of node.

        Returns a tuple (node, attrname) where node is the NodeData object
        of the destination node and attrname the name of the destination
        attribute. If there is no connection with a node of type dstnodetype,
        the method returns (None,None).
        """
        cs = self.out_connections.get(localattr_long, None)
        if cs==None:
            cs = self.out_connections.get(localattr_short, None)
            if cs==None:
                return None,None
            
        for node,nodename,attrname in cs:
            if node.nodetype==dstnodetype:
                return node, attrname
        return None,None

    # _executeAttrs
    def _executeAttrs(self, basename, type, n):
        """Retrieve the Python values out of an attribute.

        All stored attributes with the given basename will be 'executed'.
        This means, their Python value will be obtained and stored
        in the node under the same name than the original attribute.
        type is the required type of the attribute (may be None) and
        n the required number of elements (or None = Dynamic array).
        """
        self._create_attributes = True
        efftype = type
        for attr in self._setattr.get(basename, []):
            # Keep the type information once an attribute explicitly
            # provided some info. Later attributes that don't specify
            # the type (as can happen with the texture coordinates) can
            # then be read properly.
            if type==None:
                valtype = attr._opts.get("type", [None])[0]
                if valtype!=None:
                    efftype = valtype
            v = attr.getValue(efftype, n)
            # Unpack the value if the number of elements wasn't known and
            # it turned out to be only one element (in this case, the below
            # assignment will be of the form a[i]=v instead of a[i:j]=v)
            if n==None and len(v)==1:
                v = v[0]
            if attr.getBaseName() in ["in", "from", "for", "if", "while",
                                      "else", "elif", "exec"]:
                cmd = "setattr(self, '%s', v)"%attr.getFullName()[1:]
            else:
                cmd = "self%s = v"%attr.getFullName()
            if v!=[]:
                exec cmd
        self._create_attributes = False

######################################################################

# MAReader
class MAReader:
    """Low level MA (Maya ASCII) reader.
    """
    
    def __init__(self):

        # createNode options
        self.createNode_name_dict = { "n":"name", "p":"parent", "s":"shared" }
        self.createNode_opt_def = { "name" : (1, None),
                                    "parent" : (1, None),
                                    "shared" : (0, None) }

        # setAttr options
        self.setAttr_name_dict = { "k":"keyable",
                                   "l":"lock",
                                   "s":"size",
                                   "typ":"type",
                                   "av":"alteredValue",
                                   "c":"clamp" }
        self.setAttr_opt_def = { "keyable" : (1, None),
                                 "lock" : (1, None),
                                 "size" : (1, None),
                                 "type" : (1, None),
                                 "alteredValue" : (0, None),
                                 "clamp" : (0, None)}

        # fileInfo options
        self.fileInfo_name_dict = { "rm":"remove" }
        self.fileInfo_opt_def = { "remove" : (1, None)}

        # currentUnit options
        self.currentUnit_name_dict = { "l":"linear",
                                       "a":"angle",
                                       "t":"time",
                                       "f":"fullName",
                                       "ua":"updateAnimation"}
        self.currentUnit_opt_def = { "linear" : (1, None),
                                     "angle" : (1, None),
                                     "time" : (1, None),
                                     "fullName" : (0, None),
                                     "updateAnimation" : (1, None)}

        # connectAttr options
        self.connectAttr_name_dict = { "l":"lock",
                                       "f":"force",
                                       "na":"nextAvailable",
                                       "rd":"referenceDest" }
        self.connectAttr_opt_def = { "lock" : (1, None),
                                     "force" : (0, None),
                                     "nextAvailable" : (0, None),
                                     "referenceDest" : (1, None) }

        # disconnectAttr options
        self.fileInfo_name_dict = { "na":"nextAvailable" }
        self.fileInfo_opt_def = { "nextAvailable" : (0, None)}

        # parent options
        self.parent_name_dict = { "w":"world",
                                  "r":"relative",
                                  "a":"absolute",
                                  "add":"addObject",
                                  "rm":"removeObject",
                                  "s":"shape",
                                  "nc":"noConnections" }
        self.parent_opt_def = { "world" : (0, None),
                                "relative" : (0, None),
                                "absolute" : (0, None),
                                "addObject" : (0, None),
                                "removeObject" : (0, None),
                                "shape" : (0, None),
                                "noConnections" : (0, None) }

        # select options
        self.select_name_dict = { "adn":"allDependencyNodes",
                                  "ado":"allDagObjects",
                                  "vis":"visible",
                                  "hi":"hierarchy",
                                  "af":"addFirst",
                                  "r":"replace",
                                  "d":"deselect",
                                  "tgl":"toggle",
                                  "cl":"clear",
                                  "ne":"noExpand" }
        self.select_opt_def = { "all" : (0, None),
                                "allDependencyNodes" : (0, None),
                                "allDagObjects" : (0, None),
                                "visible" : (0, None),
                                "hierarchy" : (0, None),
                                "add" : (0, None),
                                "addFirst" : (0, None),
                                "replace" : (0, None),
                                "deselect" : (0, None),
                                "toggle" : (0, None),
                                "clear" : (0, None),
                                "noExpand" : (0, None) }

        # addAttr options
        self.addAttr_name_dict = { "ln":"longName",
                                   "sn":"shortName",
                                   "bt":"binaryTag",
                                   "at":"attributeType",
                                   "dt":"dataType",
                                   "dv":"defaultValue",
                                   "m":"multi",
                                   "im":"indexMatters",
                                   "min":"minValue",
                                   "hnv":"hasMinValue",
                                   "max":"maxValue",
                                   "hxv":"hasMaxValue",
                                   "ci":"cachedInternally",
                                   "is":"internalSet",
                                   "p":"parent",
                                   "nc":"numberOfChildren",
                                   "uac":"usedAsColor",
                                   "h":"hidden",
                                   "r":"readable",
                                   "w":"writable",
                                   "s":"storable",
                                   "k":"keyable",
                                   "smn":"softMinValue",
                                   "hsn":"hasSoftMinValue",
                                   "smx":"softMaxValue",
                                   "hsx":"hasSoftMaxValue",
                                   "en":"enumName" }
        self.addAttr_opt_def = { "longName" : (1, None),
                                 "shortName" : (1, None),
                                 "binaryTag" : (1, None),
                                 "attributeType" : (1, None),
                                 "dataType" : (1, None),
                                 "defaultValue" : (1, None),
                                 "multi" : (0, None),
                                 "indexMatters" : (1, None),
                                 "minValue" : (1, None),
                                 "hasMinValue" : (1, None),
                                 "maxValue" : (1, None),
                                 "hasMaxValue" : (1, None),
                                 "cachedInternally" : (1, None),
                                 "internalSet" : (1, None),
                                 "parent" : (1, None),
                                 "numberOfChildren" : (1, None),
                                 "usedAsColor" : (0, None),
                                 "hidden" : (1, None),
                                 "readable" : (1, None),
                                 "writable" : (1, None),
                                 "storable" : (1, None),
                                 "keyable" : (1, None),
                                 "softMinValue" : (1, None),
                                 "hasSoftMinValue" : (1, None),
                                 "softMaxValue" : (1, None),
                                 "hasSoftMaxValue" : (1, None),
                                 "enumName" : (1, None) }

        # file options (incomplete)
        self.file_name_dict = { "r":"reference",
                                "rpr":"renamingPrefix",
                                "ns":"namespace" }
        self.file_opt_def = { "reference" : (0, None),
                              "renamingPrefix" : (1, None),
                              "namespace" : (1, None) }


    def read(self, f):
        """Read a MA file.

        f is a file like object.
        """
        self.begin()
        self._linenr = 0
        self.new_cmd = True
        self.cmd = None
        self.args = None

        cpp = MAPreProcessor(self.lineHandler)
        # Read the file and invoke the lineHandler for each line...
        cpp(f)
       
        # Execute the last command
        self.processCommands(";")
        self.end()

    def lineHandler(self, s):
        self._linenr += 1
        z = s.strip()
        if z!="":
            self.processCommands(z)
        

    def begin(self):
        pass

    def end(self):
        pass

    def onFile(self, filename, opts):
        pass
#        print "file", filename, opts

    def onRequires(self, product, version):
        pass
#        print "requires",product, version

    def onFileInfo(self, keyword, value, opts):
        pass
#        print "fileInfo",keyword, value

    def onCurrentUnit(self, opts):
        pass
#        print "currentUnit",opts

    def onCreateNode(self, nodetype, opts):
        pass
#        print "createNode", nodetype, opts

    def onSetAttr(self, attr, vals, opts):
        pass
#        print "setAttr %s = %s %s"%(attr, vals, opts)

    def onConnectAttr(self, srcattr, dstattr, opts):
        pass
#        print "connectAttr %s %s %s"%(srcattr, dstattr, opts)

    def onDisconnectAttr(self, srcattr, dstattr, opts):
        pass
#        print "disconnectAttr %s %s %s"%(srcattr, dstattr, opts)

    def onAddAttr(self, opts):
        pass
#        print "addAttr", opts

    def onParent(self, objects, parent, opts):
        pass
#        print "parent",objects,parent,opts

    def onSelect(self, objects, opts):
        pass
#        print "select",objects,opts


    # onCommand
    def onCommand(self, cmd, args):
        """Generic command callback.
        """
#        print "**",cmd, args
        # setAttr
        if cmd=="setAttr":
            args, opts = self.getOpt(args,
                                     self.setAttr_opt_def,
                                     self.setAttr_name_dict)
            self.onSetAttr(args[0], args[1:], opts)
        # createNode
        elif cmd=="createNode":
            args, opts = self.getOpt(args,
                                     self.createNode_opt_def,
                                     self.createNode_name_dict)
            self.onCreateNode(args[0], opts)
        # connectAttr
        elif cmd=="connectAttr":
            args, opts = self.getOpt(args,
                                     self.connectAttr_opt_def,
                                     self.connectAttr_name_dict)
            self.onConnectAttr(args[0], args[1], opts)
        # disconnectAttr
        elif cmd=="disconnectAttr":
            args, opts = self.getOpt(args,
                                     self.disconnectAttr_opt_def,
                                     self.disconnectAttr_name_dict)
            self.onDisconnectAttr(args[0], args[1], opts)
        # addAttr
        elif cmd=="addAttr":
            args, opts = self.getOpt(args,
                                     self.addAttr_opt_def,
                                     self.addAttr_name_dict)
            self.onAddAttr(opts)
        # parent
        elif cmd=="parent":
            args, opts = self.getOpt(args,
                                     self.parent_opt_def,
                                     self.parent_name_dict)
            self.onParent(args[:-1], args[-1], opts)
        # select
        elif cmd=="select":
            args, opts = self.getOpt(args,
                                     self.select_opt_def,
                                     self.select_name_dict)
            self.onSelect(args, opts)
        # fileInfo
        elif cmd=="fileInfo":
            args, opts = self.getOpt(args,
                                     self.fileInfo_opt_def,
                                     self.fileInfo_name_dict)
            self.onFileInfo(args[0], args[1], opts)
        # currentUnit
        elif cmd=="currentUnit":
            args, opts = self.getOpt(args,
                                     self.currentUnit_opt_def,
                                     self.currentUnit_name_dict)
            self.onCurrentUnit(opts)
        # requires
        elif cmd=="requires":
            args, opts = self.getOpt(args, {}, {})
            self.onRequires(args[0], args[1])
        # file
        elif cmd=="file":
            args, opts = self.getOpt(args,
                                     self.file_opt_def,
                                     self.file_name_dict)
            self.onFile(args[0], opts)


    # getOpt
    def getOpt(self, arglist, opt_def, name_dict):
        """Separate arguments from options and preprocess options.

        arglist is a list of arguments (i.e. the 'command line').
        opt_def specifies the available options and their respective
        number of arguments. name_dict is a dictionary that is used
        to convert short names into long names.

        The return value is a 2-tuple (args, opts) where args is a list
        of arguments and opts is a dictionary containing the options.
        The key is the long name of the option (without leading dash)
        and the value is a list of values.
        """

        args = []
        opts = {}
        
        i=0
        while i<len(arglist):
            a = arglist[i]
            i += 1
            try:
                float(a)
                is_number = True
            except:
                is_number = False
            # Option?
            if a[0]=="-" and not is_number:
                # Convert short names into long names...
                optname = name_dict.get(a[1:], a[1:])
                # Check if the option is known
                if optname not in opt_def:
                    raise SyntaxError, "Unknown option in line %d: %s"%(self._linenr, optname)
                # Get the number of arguments
                numargs, filter = opt_def[optname]
                opts[optname] = arglist[i:i+numargs]
                i += numargs
            else:
                args.append(a)

        return args, opts

            

    # processCommands
    def processCommands(self, s):
        """Process one or more commands.

        s is a string that contains one line of MEL code (may be several
        commands). This method splits the arguments and calls onCommand()
        for every command found.
        """
        a,n = self.splitCommand(s)
        if a!=[]:
            if self.new_cmd:
                self.cmd = a[0]
                self.args = a[1:]
            else:
                self.args += a

        if n==-1:
            # The command isn't finished yet
            if self.cmd!=None:
                self.new_cmd = False
        else:
            # The command is finished, so execute it
            self.onCommand(self.cmd, self.args)
            self.new_cmd = True
            self.cmd = None
            self.args = []
            self.processCommands(s[n+1:])

    # splitCommand
    def splitCommand(self, s):
        """Split a command into its arguments.

        Returns a list of string and the position of the ';' (or -1).
        """
        b,e = self.findString(s)
        if b==None:
            n = s.find(";")
            if n==-1:
                return s.split(), -1
            else:
                return s[:n].split(), n
        else:
            if e==None:
                return s[:b].split() + [s[b:]], -1
            else:
                s2,n = self.splitCommand(s[e+1:])
                if n!=-1:
                    n+=e+1
                return s[:b].split() + [s[b+1:e]] + s2, n

    # findString
    def findString(self, s):
        """Find the first string occurence.

        The return value is a 2-tuple (begin, end) with the indices
        of the opening and closing apostrophes (can also be None).
        """
        offset = 0
        while 1:
            # Search the beginning of a string
            n1 = s.find('"', offset)
            if n1==-1:
                return None,None
            # Search the end of the string (ignore quoted apostrophes)...
            start = n1+1
            n2 = None
            while 1:
                n2 = s.find('"', start)
                if n2==-1:
                    return n1,None
                elif s[n2-1]!='\\':
                    return n1,n2
                else:
                    start = n2+1

