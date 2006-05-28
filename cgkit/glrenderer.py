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
# $Id: glrenderer.py,v 1.3 2005/08/28 19:42:43 mbaas Exp $

## \file glrenderer.py
## Contains the GLRenderer class.

from _OpenGL.GL import *
from _OpenGL.GLU import *
from scene import getScene
import _core

# GLRenderInstance
class GLRenderInstance(_core.GLRenderInstance):
    """GLRenderInstance.

    """

#    protocols.advise(instancesProvide=[ISceneItem])
    
    def __init__(self):
        _core.GLRenderInstance.__init__(self)


    # pick
    def pick(self, x, y, dx=2, dy=2, root=None):
        """Do an OpenGL picking pass at the specified cursor position.

        \param x (\c float) X window coordinate where to pick
        \param y (\c float) Y window coordinate where to pick
        \param dx (\c float) Width of the picking region
        \param dy (\c float) Height of the picking region
        \param root (\c WorldObject) Only check this subtree (None=entire world).
        \return Returns a list of hits. Each hit entry is a 3-tuple (zmin, zmax, object).
        """
        
        scene = getScene()
        vpx,vpy,width,height = self.getViewport()

        glSelectBuffer(50)
        glRenderMode(GL_SELECT)
        glInitNames()
        glPushName(0)

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_BLEND)
        glDisable(GL_NORMALIZE)

        # Projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPickMatrix(x, height-y, dx, dy, [vpx,vpy,width,height])
        glMultMatrixd(self.getProjection().toList())

        # Viewing transformation
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if scene.handedness=='l':
            glScaled(-1,1,1)
        glRotated(180,0,1,0);
        glMultMatrixd(self.getViewTransformation().toList())

        # 'Render' scene
        lut = {}
        if root==None:
            root = scene.worldRoot()
        glPushMatrix()
        # Change to the coordinate system of the parent of the root
        # so that we can continue with the local system
        if root.parent!=None:
            glMultMatrixd(root.parent.worldtransform.toList())
        self._pick_node(root, 0, lut)
        glPopMatrix()

        # Get results
        buffer = glRenderMode(GL_RENDER)
        res = []
        for zmin,zmax,names in buffer:
            idx = names[0]
            res.append((zmin,zmax,lut[idx]))

        # Sort so that nearest object is first
        res.sort()
        return res

    def _pick_node(self, obj, idx, lut):
        """Helper method for the pick() method.

        Returns the current index to use for the object 'names'.
        """
        if not obj.visible:
            return idx

        glPushMatrix()
        glMultMatrixd(obj.localTransform().toList())

        geom = obj.geom
        if geom!=None:
            glLoadName(idx)
            lut[idx] = obj
            idx+=1
            geom.drawGL()

        for child in obj.iterChilds():
            idx = self._pick_node(child, idx, lut)

        glPopMatrix()
        return idx
