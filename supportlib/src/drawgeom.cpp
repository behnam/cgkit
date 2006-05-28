/*======================================================================
 cgkit - Python Computer Graphics Kit
 Copyright (C) 2004 Matthias Baas (baas@ira.uka.de)

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

 cgkit homepage: http://cgkit.sourceforge.net
======================================================================*/

#include "drawgeom.h"
#include "sor_triangulator.h"

#ifdef WIN32
#include <windows.h>
#endif

#if defined(__APPLE__) || defined(MACOSX)
#include "OpenGL/gl.h"
#else
#include "GL/gl.h"
#endif

namespace support3d {

DrawGeom::DrawGeom()
: markers(0), lines()
{
}

DrawGeom::~DrawGeom()
{
}

// Calculate bounding box
BoundingBox DrawGeom::boundingBox()
{
  BoundingBox bb;

  // Markers...
  std::vector<D_Marker>::iterator mit;
  for(mit=markers.begin(); mit!=markers.end(); mit++)
  {
    bb.addPoint(mit->pos);
  }

  // Lines...
  std::vector<D_Line>::iterator lit;
  for(lit=lines.begin(); lit!=lines.end(); lit++)
  {
    bb.addPoint(lit->pos1);
    bb.addPoint(lit->pos2);
  }

  return bb;
}

// Draw the objects
void DrawGeom::drawGL()
{
  SORTriangulator sor;
  SORTriangulator::SORVertexList vlist;
  SORTriangulator::SORVertex vert(0, -1, 0, 0, 0);
  vlist.push_back(vert);
  vert.set(1, 0, 0, 0, 0);
  vlist.push_back(vert);
  vert.set(0, 1, 0, 0, 0);
  vlist.push_back(vert); 

  glPushAttrib(GL_ENABLE_BIT);
  glDisable(GL_LIGHTING);

  // Draw markers (points)...
  std::vector<D_Marker>::iterator mit;
//  glBegin(GL_POINTS);
  for(mit=markers.begin(); mit!=markers.end(); mit++)
  {
    glColor3d(mit->col.x, mit->col.y, mit->col.z);
//    glPointSize(mit->size);
//    glVertex3d(mit->pos.x, mit->pos.y, mit->pos.z);
    glPushMatrix();
    glTranslated(mit->pos.x, mit->pos.y, mit->pos.z);
    glScaled(mit->size, mit->size, mit->size);
    sor.drawGL(0.0, 360.0, 4, vlist);
    glPopMatrix();
  }
//  glEnd();

  // Draw lines...
  std::vector<D_Line>::iterator lit;
  glBegin(GL_LINES);
  for(lit=lines.begin(); lit!=lines.end(); lit++)
  {
    glColor3d(lit->col.x, lit->col.y, lit->col.z);
    // The following generates an error which later lead to an Exception
    // if Python OpenGL calls were made (at least on my machine)
//    glLineWidth(lit->size);
    glVertex3d(lit->pos1.x, lit->pos1.y, lit->pos1.z);
    glVertex3d(lit->pos2.x, lit->pos2.y, lit->pos2.z);
  }
  glEnd();

  glPopAttrib();
}

/**
  Clear all stored objects.
 */
void DrawGeom::clear()
{
  markers.clear();
  lines.clear();
}

/**
  Add a marker object.
 */
void DrawGeom::marker(const vec3d& pos, const vec3d& col, float size)
{
  D_Marker m(pos, col, size);
  markers.push_back(m);
}

/**
  Add a line object.
 */
void DrawGeom::line(const vec3d& pos1, const vec3d& pos2, const vec3d& col, float size)
{
  D_Line l(pos1, pos2, col, size);
  lines.push_back(l);
}


}  // end of namespace

