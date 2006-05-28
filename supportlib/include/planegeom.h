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

#ifndef PLANEGEOM_H
#define PLANEGEOM_H

/** \file planegeom.h
 Contains the plane geometry class.
 */

#include "geomobject.h"

namespace support3d {

/**
  Plane geometry.

  This class represents a plane (XY plane). For visualization it has a width and length
  and is centered at the origin, however conceptually it can be used as an infinite plane
  (e.g. in the dynamics simulation).
 */
class PlaneGeom : public GeomObject
{
  public:
  /// Length in x direction.
  Slot<double> lx;
  /// Length in y direction.
  Slot<double> ly;
  /// Number of segments in x
  Slot<int> segmentsx;
  /// Number of segments in y
  Slot<int> segmentsy;

  public:
  PlaneGeom(double alx=1.0, double aly=1.0, int segsx=1, int segsy=1);
  
  virtual BoundingBox boundingBox();
  virtual void drawGL();

  boost::shared_ptr<SizeConstraintBase> slotSizeConstraint(VarStorage storage) const;

  virtual void convert(GeomObject* target);
};


}  // end of namespace

#endif
