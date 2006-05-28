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

#ifndef TORUSGEOM_H
#define TORUSGEOM_H

/** \file torusgeom.h
 Contains the torus geometry class.
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
  Torus geometry.
 */
class CGKIT_SHARED TorusGeom : public GeomObject
{
  public:
  /// Major radius
  Slot<double> major;
  /// Minor radius
  Slot<double> minor;
  /// Number of segments in u
  Slot<int> segmentsu;
  /// Number of segments in v
  Slot<int> segmentsv;

  Slot<vec3d> cog;
  ProceduralSlot<mat3d, TorusGeom> inertiatensor;

  public:
  TorusGeom(double amajor=1.0, double aminor=0.1, int segsu=16, int segsv=8);
  ~TorusGeom();

  virtual BoundingBox boundingBox();
  virtual void drawGL();

  boost::shared_ptr<SizeConstraintBase> slotSizeConstraint(VarStorage storage) const;

  void computeInertiaTensor(mat3d& tensor);

  virtual void convert(GeomObject* target);

  private:
  void createSilhouette(SORTriangulator::SORVertexList& vlist);
};


}  // end of namespace

#endif
