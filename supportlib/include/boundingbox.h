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

#ifndef BOUNDINGBOX_H
#define BOUNDINGBOX_H

/** \file boundingbox.h
 Contains the BoundingBox class.
 */

#include <iostream>
#include "vec3.h"
#include "mat4.h"

// Define the CGKIT_SHARED variable
#ifdef DLL_EXPORT_BOUNDINGBOX
  #include "shared_export.h"
#else
  #include "shared.h"
#endif


namespace support3d {


/**
  Axis aligned bounding box.

 */
class CGKIT_SHARED BoundingBox
{
  private:
  vec3d bmin;
  vec3d bmax;

  public:
  BoundingBox();
  BoundingBox(const vec3d& min, const vec3d& max);
  ~BoundingBox() {}

  void clear();
  /// Return true if the bounding box is empty.
  bool isEmpty() const { return bmin.x>bmax.x; }
  void getBounds(vec3d& min, vec3d& max) const;
  void setBounds(const vec3d& min, const vec3d& max);
  void addPoint(const vec3d& p);
  void addBoundingBox(const BoundingBox& bb);
  void transform(const mat4d& M, BoundingBox& bb);
};

CGKIT_SHARED std::ostream& operator<<(std::ostream& os, const BoundingBox& bb);

}  // end of namespace

#endif
