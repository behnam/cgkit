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

#ifndef TRIMESH_H
#define TRIMESH_H

/** \file trimeshgeom.h
 Contains the TriMesh geometry class.
 */

#include "geomobject.h"
#include "slot.h"
#include "arrayslot.h"
#include "proceduralslot.h"
#include "vec3.h"
#include "boundingbox.h"

namespace support3d {

struct IntersectInfo
{
  IntersectInfo() : t(0), u(0), v(0), faceindex(0), hit(false) {}
  double t;
  double u;
  double v;
  int faceindex;
  bool hit;
};

/**
  TriMeshGeom geometry.
 */
class TriMeshGeom : public GeomObject
{
  public:
  NotificationForwarder<TriMeshGeom> _on_verts_event;
  NotificationForwarder<TriMeshGeom> _on_faces_event;

  /// The mesh vertices.
  ArraySlot<vec3d> verts;

  /** The mesh faces.

    Each face is an array of 3 vertex indices.
   */
  ArraySlot<int> faces;

  ProceduralSlot<vec3d, TriMeshGeom> cog;
  ProceduralSlot<mat3d, TriMeshGeom> inertiatensor;

  // Mass properties
  vec3d _cog;
  mat3d _inertiatensor;
  double _volume;

  /// A cache for the bounding box.
  BoundingBox bb_cache;

  /// Size constraint for uniform primitive variables.
  boost::shared_ptr<SizeConstraintBase> uniformSizeConstraint;
  /// Size constraint for varying or vertex primitive variables.
  boost::shared_ptr<SizeConstraintBase> varyingSizeConstraint;
  /// Size constraint for facevarying or facevertex primitive variables.
  boost::shared_ptr<SizeConstraintBase> faceVaryingSizeConstraint;

  /// True if the mass properties are still valid, otherwise they have to be recomputed.
  bool mass_props_valid;
  /// True if bb_cache is still valid, otherwise it has to be recomputed.
  bool bb_cache_valid;

  public:
  TriMeshGeom();

  virtual BoundingBox boundingBox();
  virtual void drawGL();

  /*  virtual int uniformCount() const { return faces.size(); }
  virtual int varyingCount() const { return verts.size(); }
  virtual int vertexCount() const { return verts.size(); }
  virtual int faceVaryingCount() const { return 3*faces.size(); }
  virtual int faceVertexCount() const { return 3*faces.size(); }*/
  virtual boost::shared_ptr<SizeConstraintBase> slotSizeConstraint(VarStorage storage) const;

  void calcMassProperties();
  bool intersectRay(const vec3d& origin, const vec3d& direction, IntersectInfo& info, bool earlyexit=false);

  void onVertsChanged(int start, int end);
  void onVertsResize(int size);
  void onFacesChanged(int start, int end);
  void onFacesResize(int size);

  void computeCog(vec3d& cog);
  void computeInertiaTensor(mat3d& tensor);
};


}  // end of namespace

#endif
