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

#define DLL_EXPORT_SPHEREGEOM
#include "spheregeom.h"
#include "trimeshgeom.h"
#include "fixedsizeconstraints.h"
#include <cmath>

#ifdef WIN32
#include <windows.h>
#endif

#if defined(__APPLE__) || defined(MACOSX)
#include "OpenGL/gl.h"
#else
#include "GL/gl.h"
#endif

namespace support3d {

SphereGeom::SphereGeom(double aradius, int segsu, int segsv)
: radius(aradius,0),
  segmentsu(segsu,0), segmentsv(segsv,0),
  cog(vec3d(0,0,0), Slot<vec3d>::NO_INPUT_CONNECTIONS),
  inertiatensor()
{
  inertiatensor.setProcedure(this, &SphereGeom::computeInertiaTensor);
  radius.addDependent(&inertiatensor);
  addSlot("radius", radius);
  addSlot("cog", cog);
  addSlot("inertiatensor", inertiatensor);
  addSlot("segmentsu", segmentsu);
  addSlot("segmentsv", segmentsv);
}

SphereGeom::~SphereGeom()
{
  radius.removeDependent(&inertiatensor);
}

BoundingBox SphereGeom::boundingBox()
{
  double r = radius.getValue();
  BoundingBox res(vec3d(-r,-r,-r), vec3d(r,r,r));
  return res;
}

void SphereGeom::drawGL()
{
  SORTriangulator sor;
  SORTriangulator::SORVertexList vlist;
  int segsu = segmentsu.getValue();

  if (segsu<3)
    segsu=3;

  createSilhouette(vlist);
  sor.drawGL(0.0, 360.0, segsu, vlist);
}

// slotSizeConstraint
boost::shared_ptr<SizeConstraintBase> SphereGeom::slotSizeConstraint(VarStorage storage) const
{
  switch(storage)
  {
  case UNIFORM:  
    return sizeConstraint_one;
  case VARYING:
  case VERTEX:  
    return sizeConstraint_four;
  default:
    return sizeConstraint_zero;
  }  
}


/**
  Computes the inertia tensor of the sphere.

  The inertia tensor of the sphere with respect to its local
  coordinate system L is computed. 

  This method is used for the inertiatensor slot.

  \param[out] tensor Receives the result.
 */
void SphereGeom::computeInertiaTensor(mat3d& tensor)
{
  double r = radius.getValue();
  tensor = mat3d(0.4*r*r);
}


/**
  Convert to TriMesh
 */
void SphereGeom::convert(GeomObject* target)
{
  TriMeshGeom* tm = dynamic_cast<TriMeshGeom*>(target);

  // Check if the target geom is really a TriMesh
  if (tm==0)
  {
    throw ENotImplementedError("Conversion not supported by the SphereGeom");
  }

  SORTriangulator sor;
  SORTriangulator::SORVertexList vlist;
  int segsu = segmentsu.getValue();

  if (segsu<3)
    segsu=3;

  createSilhouette(vlist);
  sor.convertToTriMesh(0.0, 360.0, segsu, vlist, *tm);
}

/**
  Helper method.

  This method creates the silhouette for the SORTriangulator class.

  \param[out] vlist Empty vertex list which will receive the result
 */
void SphereGeom::createSilhouette(SORTriangulator::SORVertexList& vlist)
{
  double rad = radius.getValue();
  int segsv = segmentsv.getValue();
  int i;

  if (segsv<2)
    segsv=2;

  // Create silhouette...
  for(i=0; i<=segsv; i++)
  {
    double v = double(i)/segsv;
    double t = v*3.1415926535897931;
    double nx = sin(t);
    double ny = -cos(t);
    double px = rad*nx;
    double py = rad*ny;
    if (i==0)
    {
      px = 0;
      py = -rad;
      nx = 0;
      ny = -1;
    }
    if (i==segsv)
    {
      px = 0;
      py = rad;
      nx = 0;
      ny = 1;
    }
    SORTriangulator::SORVertex vert(px, py, nx, ny, v);
    vlist.push_back(vert);
  }
}


}  // end of namespace
