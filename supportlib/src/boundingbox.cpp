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

#define DLL_EXPORT_BOUNDINGBOX
#include "boundingbox.h"

template<class T>
const T& xmin(const T& x, const T& y)
{
  return (x<=y)? x : y;
}

template<class T>
const T& xmax(const T& x, const T& y)
{
  return (x>y)? x : y;
}


namespace support3d {

BoundingBox::BoundingBox()
  : bmin(0,0,0), bmax(-1,0,0)
{
}

BoundingBox::BoundingBox(const vec3d& min, const vec3d& max)
  : bmin(0,0,0), bmax(-1,0,0)
{
  setBounds(min, max);
}

/**
  Make the bounding box empty.  
 */
void BoundingBox::clear()
{
  bmin.set(0,0,0);
  bmax.set(-1,0,0);
}

/**
  Return the minimum and maximum bound.

  \param[out] min Minimum bound.
  \param[out] max Maximum bound.
  \todo What happens if the bounding box is empty?
 */
void BoundingBox::getBounds(vec3d& min, vec3d& max) const 
{ 
  if (isEmpty())
  {
    min = min;
    max = min;
  }
  else
  {
    min = bmin;
    max = bmax; 
  }
}

/**
  Set new bounds for the bounding box. 
  
  The rectangle given by b1 and b2 defines the new bounding box.

  \param min 1st bound
  \param max 2nd bound
 */
void BoundingBox::setBounds(const vec3d& min, const vec3d& max)
{
  bmin.set(xmin(min.x, max.x), xmin(min.y, max.y), xmin(min.z, max.z));
  bmax.set(xmax(min.x, max.x), xmax(min.y, max.y), xmax(min.z, max.z));
}

/**
   Enlarge the bounding box so that the point p is enclosed in the box.

  \param p The point that should be enclosed in the box.
 */
void BoundingBox::addPoint(const vec3d& p)
{
  if (isEmpty())
  {
    bmin = p;
    bmax = p;
  }
  else
  {
    bmin.set(xmin(bmin.x, p.x), xmin(bmin.y, p.y), xmin(bmin.z, p.z));
    bmax.set(xmax(bmax.x, p.x), xmax(bmax.y, p.y), xmax(bmax.z, p.z));
  }
}

/**
  Enlarge the bounding box so that bb is enclosed in the box.

  \param bb The bounding box that should be enclosed in this box.
 */
void BoundingBox::addBoundingBox(const BoundingBox& bb)
{
  if (bb.isEmpty())
    return;

  addPoint(bb.bmin);
  addPoint(bb.bmax);
}

/**
	Returns a transformed bounding box. 
  
  The transformation is given by M. The result will still be axis aligned, 
  so the volume will not be preserved.

  The bounding box on which this method is called remains unchanged.
  It is allowed to pass \a *this as \a bb.

  \param M Transformation matrix
  \param[out] bb  Result.
 */
void BoundingBox::transform(const mat4d& M, BoundingBox& bb)
{
  double x1,y1,z1;
  double x2,y2,z2;
  if (!isEmpty())
  {
    bmin.get(x1, y1, z1);
    bmax.get(x2, y2, z2);
    bb.clear();
    bb.addPoint( M*vec3d(x1,y1,z1) );
    bb.addPoint( M*vec3d(x1,y1,z2) );
    bb.addPoint( M*vec3d(x1,y2,z1) );
    bb.addPoint( M*vec3d(x1,y2,z2) );
    bb.addPoint( M*vec3d(x2,y1,z1) );
    bb.addPoint( M*vec3d(x2,y1,z2) );
    bb.addPoint( M*vec3d(x2,y2,z1) );
    bb.addPoint( M*vec3d(x2,y2,z2) );
  }
  else
  {
    bb.clear();
  }
}


std::ostream& operator<<(std::ostream& os, const BoundingBox& bb)
{
  os<<"<BoundingBox: ";
  if (bb.isEmpty())
  {
    os<<"empty>";
  }
  else
  {
    vec3d bmin, bmax;
    bb.getBounds(bmin, bmax);
    os<<bmin<<" - "<<bmax<<">";
  }
  return os;
}

}  // end of namespace
