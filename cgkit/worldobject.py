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
# $Id: worldobject.py,v 1.3 2005/08/15 15:47:56 mbaas Exp $

## \file worldobject.py
## Contains the WorldObject class.

#from _core import WorldObject as _WorldObject
#from _core import _WorldObjectChildIterator
import _core
from Interfaces import ISceneItem, ISceneItemContainer
import protocols
import scene
from cgtypes import *

# WorldObject
class WorldObject(_core.WorldObject):
    """The base class for a world object.

    A world object is a scene item that has a position and orientation in
    space and that can usually be represented by 3D geometry.

    Attributes:

    - name
    - transform
    - pos
    - rot
    - scale
    - pivot
    - mass

    If you access an attribute that's actually stored in the geom then
    the attribute access is forwarded to the geom. This means you can
    access the geom slots through the world object (for example, if you
    attach a sphere geom to a world object, then the world object "has"
    an attribute 'radius').
    """

    protocols.advise(instancesProvide=[ISceneItem, ISceneItemContainer])
    
    def __init__(self,
                 name="object",
                 transform = None,
                 pos = None, rot = None, scale = None,
                 pivot = None,
                 offsetTransform = None,
                 parent = None,
                 mass = None,
                 material = None,
                 visible = True,
                 linearvel = None,
                 angularvel = None,
                 auto_insert = True):
        """Constructor.

        \param name (\c str) Object name
        \param transform (\c mat4) Initial transform
        \param pos (\c vec3) Initial position
        \param rot (\c mat3) Initial rotation
        \param scale (\c vec3) Initial scaling
        \param pivot (\c vec3) Initial pivot point (takes precedence over offsetTransform)
        \param offsetTransform (\c mat4) Initial offset transform
        \param parent (\c WorldObject or \c str) Parent object or None
        \param mass (\c float) Total mass
        \param material (\c Material) Material class (or a sequence of materials)
        \param visible (\c Bool) Visibility flag
        \param linearvel (\c vec3) Linear velocity
        \param angularvel (\c vec3) Angular velocity
        \param auto_insert (\c bool) If True, the object is inserted into the
                        scene automatically
        """
        exec _preInitWorldObject
        _core.WorldObject.__init__(self, name)

        _initWorldObject(self, name=name,
                         transform=transform, pos=pos, rot=rot,
                         scale=scale, pivot=pivot,
                         offsetTransform=offsetTransform,
                         parent=parent,
                         mass=mass, material=material,
                         visible=visible,
                         linearvel=linearvel, angularvel=angularvel,
                         auto_insert=auto_insert)
        
#        if offsetTransform!=None:
#            self.setOffsetTransform(offsetTransform)
#        if pivot!=None:
#            self.pivot = pivot
#        if transform!=None:
#            self.transform = transform
#        if pos!=None:
#            self.pos = pos
#        if rot!=None:
#            self.rot = rot
#        if scale!=None:
#            self.scale = scale
#        if mass!=None:
#            self.mass = mass
#        if material!=None:
#            self.material = material

#        if auto_insert:
#            scene.getScene().insert(self)

    def protocols(self):
        return [ISceneItem, ISceneItemContainer]

    def __getattr__(self, name):
        if self.geom!=None and name[:2]!="__":
            if hasattr(self.geom, name):
                return getattr(self.geom, name)
            elif self.geom.hasSlot(name):
                return self.geom.slot(name).getValue()
#        if self.geom!=None and self.geom.hasSlot(name):
#            exec "res=self.geom.%s"%name
#            return res
        raise AttributeError, 'Object "%s" has no attribute "%s"'%(self.name, name)
    
    def __setattr__(self, name, val):
        if self.geom!=None and self.geom.hasSlot(name):
#            print "self.geom.%s=%s"%(name, val)
            exec "self.geom.%s=%s"%(name, val)
        else:
            _core.WorldObject.__setattr__(self, name, val)
        

# This string has to be executed at the beginning of a constructor
# that has to initialize a _core.WorldObject object.
_preInitWorldObject = """
if auto_insert:
    if parent==None:
        parent = scene.getScene().worldRoot()
    else:
        if type(parent) in [str, unicode]:
            parent = scene.getScene().worldObject(parent)
    name = parent.makeChildNameUnique(name)
"""
    
# Common WorldObject initializations
def _initWorldObject(self, name, parent, transform=None,
                     pos=None, rot=None, scale=None,
                     pivot=None, offsetTransform=None,
                     mass=None, material=None, visible=True,
                     linearvel=None, angularvel=None,
                     auto_insert=True):
    """Helper function for usage in constructors.
    """
    if offsetTransform!=None:
        self.setOffsetTransform(offsetTransform)
    if pivot!=None:
        self.pivot = vec3(pivot)
    if transform!=None:
        self.transform = transform
    if pos!=None:
        self.pos = vec3(pos)
    if rot!=None:
        self.rot = mat3(rot)
    if scale!=None:
        self.scale = vec3(scale)
    if mass!=None:
        self.mass = mass
    if material!=None:
        try:
            # Check if material is a sequence or not. If it is not a
            # sequence the following line will raise an exception.
            len(material)
        except:
            material = [material]
        self.setNumMaterials(len(material))
        for i,mat in enumerate(material):
            self.setMaterial(mat, i)
    if linearvel!=None:
        self.linearvel = vec3(linearvel)
    if angularvel!=None:
        self.angularvel = vec3(angularvel)

    self.visible = visible

    if auto_insert:
        parent.addChild(self)
#        scene.getScene().insert(self)

