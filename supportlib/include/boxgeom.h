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

#ifndef BOXGEOM_H
#define BOXGEOM_H

/** \file boxgeom.h
 Contains the box geometry class.
 */

#include "geomobject.h"
#include "proceduralslot.h"

namespace support3d {

/**
  Box geometry.

  This class represents a box centered at the origin.
 */
class BoxGeom : public GeomObject
{
  public:
  /// Length in x direction.
  Slot<double> lx;
  /// Length in y direction.
  Slot<double> ly;
  /// Length in z direction.
  Slot<double> lz;

  /// Number of segments in x
  Slot<int> segmentsx;
  /// Number of segments in y
  Slot<int> segmentsy;
  /// Number of segments in z
  Slot<int> segmentsz;

  Slot<vec3d> cog;
  ProceduralSlot<mat3d, BoxGeom> inertiatensor;

  public:
  BoxGeom(double alx=1.0, double aly=1.0, double alz=1.0, int segsx=1, int segsy=1, int segsz=1);
  ~BoxGeom();

  virtual BoundingBox boundingBox();
  virtual void drawGL();

  //  virtual int uniformCount() const { return 6; }
  //  virtual int varyingCount() const { return 8; }
  //  virtual int vertexCount() const { return 8; }

  boost::shared_ptr<SizeConstraintBase> slotSizeConstraint(VarStorage storage) const;

  void computeInertiaTensor(mat3d& tensor);

  virtual void convert(GeomObject* target);

  private:
  int _vertexIndex(int i, int j, int segsx, int segsy, int offset, int topoffset);
};


}  // end of namespace

#endif
