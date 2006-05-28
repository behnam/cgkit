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
# $Id: drawtextgeom.py,v 1.2 2005/08/28 19:42:43 mbaas Exp $

import sys
from cgkit.geomobject import GeomObject
from cgkit.boundingbox import BoundingBox
from cgkit.cgtypes import *
from _OpenGL.GL import *
try:
    from OpenGL.GLUT import *
    has_glut = True
except:
    has_glut = False
    

# DrawTextGeom
class DrawTextGeom(GeomObject):
    """Geometry object that draw text strings.

    This is similar to the C++ Draw class, except that it only draws
    texts using GLUT. This functionality isn't incorporated into the
    C++ class to prevent a dependency from GLUT. Whereas using Python
    you can still use everything else from cgkit if GLUT isn't available
    (in this case, a warning will be printed and the texts are simply not
    drawn).
    """

    def __init__(self):
        """Constructor.
        """
        global has_glut
        GeomObject.__init__(self)
        
        self.text = []
        self.boundingbox = BoundingBox()

        if not has_glut:
            print >>sys.stderr, "WARNING: Cannot draw texts. GLUT is not available."

    def uniformCount(self):
        return 0

    def varyingCount(self):
        return 0

    def vertexCount(self):
        return 0

    def boundingBox(self):
        return self.boundingbox

    def drawGL(self):
        global has_glut
        if not has_glut:
            return
        
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glDisable(GL_LIGHTING)
#        glDisable(GL_DEPTH_TEST)

        for pos,txt,font,col in self.text:
            x,y,z = pos
            r,g,b = col
            glColor3d(r,g,b)
            glRasterPos3d(x,y,z)
            self._drawText(txt, font)

        glPopAttrib()

    # clear
    def clear(self):
        """Clear all texts."""
        self.text = []
        self.boundingbox = BoundingBox()
        
    # addText
    def addText(self, pos, txt, font=None, color=(1,1,1)):
        """Add a text string.

        pos contains the 3D position of the string, txt is a string
        containing the actual text. font can be one of the constants
        defined in GLUT:

        - GLUT_BITMAP_8_BY_13
        - GLUT_BITMAP_9_BY_15
        - GLUT_BITMAP_TIMES_ROMAN_10
        - GLUT_BITMAP_TIMES_ROMAN_24
        - GLUT_BITMAP_HELVETICA_10
        - GLUT_BITMAP_HELVETICA_12
        - GLUT_BITMAP_HELVETICA_18

        color is the color of the text.
        """
        if font==None:
            try:
                font = GLUT_BITMAP_9_BY_15
            except:
                font = 0
        self.text.append((pos,txt,font,color))
        self.boundingbox.addPoint(vec3(pos))


    def _drawText(self, txt, font):
        for c in txt:
            glutBitmapCharacter(font, ord(c))
