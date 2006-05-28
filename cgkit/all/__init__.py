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
# $Id: __init__.py,v 1.8 2006/05/26 21:32:01 mbaas Exp $

"""The 'all' sub package imports all names from cgkit.

You can import from this package if you simply want to make available
(almost) all the objects, functions, etc. defined in cgkit (e.g. for
interactive sessions or simple scripts):

from cgkit.all import *
"""

from cgkit import _core

from cgkit.eventmanager import eventManager
from cgkit.events import *
from cgkit.keydefs import *
from cgkit.application import getApp

from cgkit.cgtypes import vec3, vec4, mat3, mat4, quat, getEpsilon, setEpsilon, slerp, squad
from cgkit.scene import Scene, getScene
from cgkit.sceneglobals import Globals
from cgkit.worldobject import WorldObject
from cgkit.material import Material
from cgkit.glmaterial import GLMaterial, GLTexture, GLShader, GLSLANG_VERTEX, GLSLANG_FRAGMENT, GL_DECAL, GL_REPLACE, GL_BLEND, GL_MODULATE, GL_NEAREST, GL_LINEAR, GL_NEAREST_MIPMAP_NEAREST, GL_NEAREST_MIPMAP_LINEAR, GL_LINEAR_MIPMAP_NEAREST, GL_LINEAR_MIPMAP_LINEAR, GL_CLAMP, GL_REPEAT, GL_RGB, GL_RGBA
from cgkit.lightsource import LightSource
from cgkit.component import Component, createFunctionComponent
from cgkit.slots import DoubleSlot, BoolSlot, IntSlot, Vec3Slot, Vec4Slot, Mat3Slot, Mat4Slot, QuatSlot, PySlot, slotPropertyCode, ProceduralIntSlot, ProceduralDoubleSlot, ProceduralVec3Slot, ProceduralVec4Slot, ProceduralMat3Slot, ProceduralMat4Slot, ProceduralQuatSlot, NotificationForwarder, UserSizeConstraint, LinearSizeConstraint
from cgkit.slots import Dependent
from cgkit.boundingbox import BoundingBox

### Geom objects:
from cgkit.spheregeom import SphereGeom
from cgkit.ccylindergeom import CCylinderGeom
from cgkit.torusgeom import TorusGeom
from cgkit.boxgeom import BoxGeom
from cgkit.planegeom import PlaneGeom
from cgkit.trimeshgeom import TriMeshGeom
from cgkit.polyhedrongeom import PolyhedronGeom
from cgkit.drawgeom import DrawGeom
from cgkit.beziercurvegeom import BezierCurveGeom, BezierPoint

### Geometry world objects:
from cgkit.quadrics import Sphere
from cgkit.ccylinder import CCylinder
from cgkit.torus import Torus
from cgkit.box import Box
from cgkit.plane import Plane
from cgkit.trimesh import TriMesh
from cgkit.polyhedron import Polyhedron
from cgkit.draw import Draw
from cgkit.ribarchive import RIBArchive
from cgkit.beziercurve import BezierCurve

from cgkit.joint import Joint

### Dynamics world objects
from cgkit.odedynamics import ODEDynamics, ODEContactProperties, ODEBallJoint, ODEHingeJoint, ODESliderJoint, ODEHinge2Joint, ODE_COLLISION
from cgkit.joints import HingeJoint

### Camera/light
from cgkit.targetcamera import TargetCamera
from cgkit.freecamera import FreeCamera
from cgkit.lookat import LookAt
from cgkit.glpointlight import GLPointLight
from cgkit.glfreespotlight import GLFreeSpotLight
from cgkit.gltargetspotlight import GLTargetSpotLight
from cgkit.glfreedistantlight import GLFreeDistantLight
from cgkit.gltargetdistantlight import GLTargetDistantLight

from cgkit.spotlight3ds import SpotLight3DS
from cgkit.material3ds import Material3DS, TextureMap3DS
from cgkit.objmaterial import OBJMaterial, OBJTextureMap

from cgkit.camcontrol import CameraControl

from cgkit.group import Group
from cgkit.tunnel import Tunnel
from cgkit.flockofbirds import FlockOfBirds
from cgkit.valuetable import ValueTable
from cgkit.expression import Expression
from cgkit.euleradapter import EulerAdapter
from cgkit.pidcontroller import PIDController
from cgkit.gnuplotter import GnuPlotter
from cgkit.slideshow import SlideShow, Slide, XFade, XCube
from cgkit.motionpath import MotionPath

from cgkit.glrenderer import GLRenderInstance

from cgkit.joystick import Joystick

CONSTANT = _core.VarStorage.CONSTANT
UNIFORM = _core.VarStorage.UNIFORM
VARYING = _core.VarStorage.VARYING
VERTEX = _core.VarStorage.VERTEX
FACEVARYING = _core.VarStorage.FACEVARYING
FACEVERTEX = _core.VarStorage.FACEVERTEX
USER = _core.VarStorage.USER

INT = _core.VarType.INT
FLOAT = _core.VarType.FLOAT
STRING = _core.VarType.STRING
COLOR = _core.VarType.COLOR
POINT = _core.VarType.POINT
VECTOR = _core.VarType.VECTOR
NORMAL = _core.VarType.NORMAL
MATRIX = _core.VarType.MATRIX
HPOINT = _core.VarType.HPOINT

### Importer
import cgkit.offimport
import cgkit.pyimport
import cgkit.dddsimport
import cgkit.x3dimport
import cgkit.ifsimport
import cgkit.objimport
import cgkit.stlimport
import cgkit.asfamcimport
import cgkit.bvhimport
import cgkit.maimport
import cgkit.plyimport
import cgkit.lwobimport
### Exporter
import cgkit.ribexport
import cgkit.offexport
import cgkit.objexport
import cgkit.plyexport

from cgkit.rmshader import RMMaterial, RMLightSource, RMShader
from cgkit.ribexport import ShadowPass, FlatReflectionPass

from cgkit.cmds import *
