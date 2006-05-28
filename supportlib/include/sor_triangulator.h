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

#ifndef SORTRIANGULATOR_H
#define SORTRIANGULATOR_H

/** \file sor_triangulator.h
 Contains the SORTriangulator class.
 */

#include <iostream>
#include <vector>
#include "vec3.h"
#include "trimeshgeom.h"

namespace support3d {

/**
  A silhouette vertex for a surface of revolution.

  \see SORTriangulator
 */
class _SORTri_vertex
{
  public:
  _SORTri_vertex(double apx, double apy, double anx, double any, double av=0.0)
    : px(apx), py(apy), nx(anx), ny(any), v(av) {}

  void set(double apx, double apy, double anx=0, double any=0, double av=0.0)
    { px=apx; py=apy; nx=anx; ny=any; v=av; }

  // 2D point position
  double px;
  double py;
  // Normal
  double nx;
  double ny;
  // Texture coordinate (v direction)
  double v;
};

/**
  Surface of Revolution triangulator.

 */
class SORTriangulator
{
  public:
  typedef _SORTri_vertex SORVertex;
  typedef std::vector<SORVertex> SORVertexList;

  public:
  SORTriangulator() {}
  ~SORTriangulator() {}

  void drawGL(double startangle, double endangle, int segmentsu, SORVertexList& vlist);
  void convertToTriMesh(double startangle, double endangle, int segmentsu,
			SORVertexList& vlist, TriMeshGeom& tm);
};


}  // end of namespace

#endif
