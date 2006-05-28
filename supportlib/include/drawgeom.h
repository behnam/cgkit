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

#ifndef DRAWGEOM_H
#define DRAWGEOM_H

/** \file drawgeom.h
 Contains the "draw" geometry class (which just contains markers, lines, etc.)
 */

#include <vector>
#include "geomobject.h"
#include "vec3.h"

namespace support3d {

/// Holds the parameters of a "Draw" marker.
struct D_Marker
{
  vec3d pos;
  vec3d col;
  float size;

  D_Marker() {}
  D_Marker(const vec3d& apos, const vec3d& acol, float asize)
    : pos(apos), col(acol), size(asize) {}
};

/// Holds the parameters of a "Draw" line.
struct D_Line
{
  vec3d pos1;
  vec3d pos2;
  vec3d col;
  float size;

  D_Line() {}
  D_Line(const vec3d& apos1, const vec3d& apos2, const vec3d& acol, float asize)
    : pos1(apos1), pos2(apos2), col(acol), size(asize) {}
};

/**
  Draw geometry.

  This class represents a collection of markers and lines.
 */
class DrawGeom : public GeomObject
{
  public:
  std::vector<D_Marker> markers;
  std::vector<D_Line> lines;

  public:
  DrawGeom();
  virtual ~DrawGeom();

  virtual BoundingBox boundingBox();
  virtual void drawGL();

  void clear();
  void marker(const vec3d& pos, const vec3d& col=vec3d(1,1,1), float size=1.0f);
  void line(const vec3d& pos1, const vec3d& pos2, const vec3d& col=vec3d(1,1,1), float size=1.0f);
};


}  // end of namespace

#endif
