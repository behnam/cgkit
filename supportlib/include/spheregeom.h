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

#ifndef SPHEREGEOM_H
#define SPHEREGEOM_H

/** \file spheregeom.h
 Contains the sphere geometry class.
 */

#include "geomobject.h"
#include "proceduralslot.h"
#include "sor_triangulator.h"

// Define the CGKIT_SHARED variable
#ifdef DLL_EXPORT_SPHEREGEOM
  #include "shared_export.h"
#else
  #include "shared.h"
#endif

namespace support3d {

/**
  Sphere geometry.
 */
class CGKIT_SHARED SphereGeom : public GeomObject
{
  public:
  /// Sphere radius
  Slot<double> radius;
  /// Number of segments in u
  Slot<int> segmentsu;
  /// Number of segments in v
  Slot<int> segmentsv;

  Slot<vec3d> cog;
  ProceduralSlot<mat3d, SphereGeom> inertiatensor;

  public:
  SphereGeom(double aradius=1.0, int segsu=16, int segsv=8);
  ~SphereGeom();

  virtual BoundingBox boundingBox();
  virtual void drawGL();

  //  virtual int uniformCount() const { return 1; }
  //  virtual int varyingCount() const { return 4; }
  //  virtual int vertexCount() const { return 4; }

  virtual boost::shared_ptr<SizeConstraintBase> slotSizeConstraint(VarStorage storage) const;

  void computeInertiaTensor(mat3d& tensor);

  virtual void convert(GeomObject* target);

  private:
  void createSilhouette(SORTriangulator::SORVertexList& vlist);
};


}  // end of namespace

#endif
