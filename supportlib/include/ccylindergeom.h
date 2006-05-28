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

#ifndef CCYLINDERGEOM_H
#define CCYLINDERGEOM_H

/** \file ccylindergeom.h
 Contains the capped cylinder geometry class.
 */

#include "geomobject.h"
#include "proceduralslot.h"
#include "sor_triangulator.h"

namespace support3d {

/**
  Capped cylinder geometry.
 */
class CCylinderGeom : public GeomObject
{
  public:
  /// Sphere radius
  Slot<double> radius;
  Slot<double> length;
  /// Number of segments in u
  Slot<int> segmentsu;
  /// Number of segments in v for the cylinder part
  Slot<int> segmentsvl;
  /// Number of segments in v for the caps
  Slot<int> segmentsvr;

  Slot<vec3d> cog;
  ProceduralSlot<mat3d, CCylinderGeom> inertiatensor;

  public:
  CCylinderGeom(double aradius=1.0, double alength=1.0, int segsu=16, int segsvl=1, int segsvr=3);
  ~CCylinderGeom();

  virtual BoundingBox boundingBox();
  virtual void drawGL();

  virtual boost::shared_ptr<SizeConstraintBase> slotSizeConstraint(VarStorage storage) const;

  void computeInertiaTensor(mat3d& tensor);

  virtual void convert(GeomObject* target);

  private:
  void createSilhouette(SORTriangulator::SORVertexList& vlist);
};


}  // end of namespace

#endif
