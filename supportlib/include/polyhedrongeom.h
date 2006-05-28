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

#ifndef POLYHEDRON_H
#define POLYHEDRON_H

/** \file polyhedrongeom.h
 Contains the Polyhedron geometry class.
 */

#include <vector>
#include <list>
#include "geomobject.h"
#include "slot.h"
#include "arrayslot.h"
#include "proceduralslot.h"
#include "vec3.h"
#include "boundingbox.h"

#ifdef WIN32
#include <windows.h>
#endif

#if defined(__APPLE__) || defined(MACOSX)
#include "OpenGL/gl.h"
#include "OpenGL/glu.h"
#else
#include "GL/gl.h"
#include "GL/glu.h"
#endif

namespace support3d {

/**
  This class can be used to allocate small data items of equal size.

  This class is for internal use in conjunction withe the OpenGL
  polygon tesselator. The class is used to allocate small data buffers
  that will store vertex information.
 
  The class allocates larger memory blocks that will be "sliced" into smaller
  buffers. The allocated memory is not freed until the object is destroyed,
  this means once enough memory was allocated, providing small data buffers
  should be fast.
 
  Usage: Before memory buffers are requested, the size of a buffer has to
  be set via setDataSize(). Then new buffers can be requested using
  newDataPtr(). If those pointers aren't required anymore, reset() has
  to be called so that the allocated memory can be reused.
 */
class DataMemoryManager
{
  private:
  int blocksize;
  int datasize;

  std::vector<void*> memptrs;
  std::vector<int> used;
  unsigned int currentblock;

  public:
  DataMemoryManager(int ablocksize);
  ~DataMemoryManager();

  void setDataSize(int size);
  void reset();
  void* newDataPtr();

  protected:
  void* alloc();
  void free();
};



/**
  PolyhedronGeom geometry.

  This is a simple polyhedron class that can just store and display
  polyhedrons made of general planar concave polygons.
   
 */
class PolyhedronGeom : public GeomObject
{
  public:
  typedef std::vector<int> VertexLoop;
  typedef std::vector<VertexLoop*> Poly;
  typedef std::vector<int>::iterator LoopIterator;

  public:
  NotificationForwarder<PolyhedronGeom> _on_verts_event;

  /// The polyhedron vertices.
  ArraySlot<vec3d> verts;

  /// The polys
  std::vector<Poly*> polys;


  //  ProceduralSlot<vec3d, PolyhedronGeom> cog;
  //  ProceduralSlot<mat3d, PolyhedronGeom> inertiatensor;

  // Mass properties
  //  vec3d _cog;
  //  mat3d _inertiatensor;
  //  double _volume;

  /// A cache for the bounding box.
  BoundingBox bb_cache;

  /// Size constraint for uniform primitive variables.
  boost::shared_ptr<SizeConstraintBase> uniformSizeConstraint;
  /// Size constraint for varying or vertex primitive variables.
  boost::shared_ptr<SizeConstraintBase> varyingSizeConstraint;
  /// Size constraint for facevarying or facevertex primitive variables.
  boost::shared_ptr<SizeConstraintBase> faceVaryingSizeConstraint;

  /// True if the mass properties are still valid, otherwise they have to be recomputed.
    //  bool mass_props_valid;
  /// True if bb_cache is still valid, otherwise it has to be recomputed.
  bool bb_cache_valid;

  private:
  /// Tesselator object (used by \em every PolyhedronGeom).
  static GLUtesselator* tess;
  static DataMemoryManager dataMemManager;

  public:
  PolyhedronGeom();
  virtual ~PolyhedronGeom();

  virtual BoundingBox boundingBox();
  virtual void drawGL();

  /*  virtual int uniformCount() const { return polys.size(); }
  virtual int varyingCount() const { return verts.size(); }
  virtual int vertexCount() const { return verts.size(); }*/
  int faceVaryingCount() const;
  /*  virtual int faceVertexCount() const { return faceVaryingCount(); }*/
  virtual boost::shared_ptr<SizeConstraintBase> slotSizeConstraint(VarStorage storage) const;

  //  void calcMassProperties();

  bool hasPolysWithHoles() const;

  int getNumPolys() const { return polys.size(); }
  int getNumLoops(int poly) const;
  int getNumVerts(int poly, int loop) const;
  void setNumPolys(int num);
  void setNumLoops(int poly, int num);
  // Get a copy of a loop
  std::vector<int> getLoop(int poly, int loop);
  // Set a copy of a loop
  void setLoop(int poly, int loop, const std::vector<int>& vloop);
  // Iterate over the vertex indices of one particular loop
  LoopIterator loopBegin(int poly, int loop);
  LoopIterator loopEnd(int poly, int loop);
 

  void onVertsChanged(int start, int end);
  void onVertsResize(int size);

  //  void computeCog(vec3d& cog);
  //  void computeInertiaTensor(mat3d& tensor);

  virtual void convert(GeomObject* target);

  private:
  void deletePoly(int poly);
  void computeNormal(int poly, vec3d& N);
};


}  // end of namespace

#endif
