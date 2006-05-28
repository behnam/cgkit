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
#include "torusgeom.h"
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

// Obviously some header on Linux creates stray macros "major" and "minor".
// Undo this bad habit so it doesn't interfere with the below variables...
#ifdef major
#undef major
#endif
#ifdef minor
#undef minor
#endif

namespace support3d {

TorusGeom::TorusGeom(double amajor, double aminor, int segsu, int segsv)
 : major(amajor,0), minor(aminor,0),
  segmentsu(segsu,0), segmentsv(segsv,0),
  cog(vec3d(0,0,0), Slot<vec3d>::NO_INPUT_CONNECTIONS),
  inertiatensor()
{
  inertiatensor.setProcedure(this, &TorusGeom::computeInertiaTensor);
  major.addDependent(&inertiatensor);
  minor.addDependent(&inertiatensor);
  addSlot("major", major);
  addSlot("minor", minor);
  addSlot("cog", cog);
  addSlot("inertiatensor", inertiatensor);
  addSlot("segmentsu", segmentsu);
  addSlot("segmentsv", segmentsv);
}

TorusGeom::~TorusGeom()
{
  major.removeDependent(&inertiatensor);
  minor.removeDependent(&inertiatensor);
}

BoundingBox TorusGeom::boundingBox()
{
  double minr = minor.getValue();
  double maj = major.getValue()+minr;
  BoundingBox res(vec3d(-maj,-maj,-minr), vec3d(maj,maj,minr));
  return res;
}

void TorusGeom::drawGL()
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
boost::shared_ptr<SizeConstraintBase> TorusGeom::slotSizeConstraint(VarStorage storage) const
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
  Computes the inertia tensor of the torus.

  The inertia tensor of the torus with respect to its local
  coordinate system L is computed. 

  This method is used for the inertiatensor slot.

  \param[out] tensor Receives the result.
  \todo Compute inertia tensor
 */
void TorusGeom::computeInertiaTensor(mat3d& tensor)
{
  tensor = mat3d(0);
}


/**
  Convert to TriMesh
 */
void TorusGeom::convert(GeomObject* target)
{
  TriMeshGeom* tm = dynamic_cast<TriMeshGeom*>(target);

  // Check if the target geom is really a TriMesh
  if (tm==0)
  {
    throw ENotImplementedError("Conversion not supported by the TorusGeom");
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
  \todo Is silhouette closed? (in v direction?)
 */
void TorusGeom::createSilhouette(SORTriangulator::SORVertexList& vlist)
{
  double majr = major.getValue();
  double minr = minor.getValue();
  int segsv = segmentsv.getValue();
  int i;

  if (segsv<3)
    segsv=3;

  // Create silhouette...
  for(i=0; i<=segsv; i++)
  {
    double v = double(i)/segsv;
    double t = v*2*3.1415926535897931;
    double nx = cos(t);
    double ny = sin(t);
    double px = minr*nx;
    double py = minr*ny;
    SORTriangulator::SORVertex vert(majr+px, py, nx, ny, v);
    vlist.push_back(vert);
  }
}


}  // end of namespace
