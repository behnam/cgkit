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

#ifndef PRIMVARACCESS_H
#define PRIMVARACCESS_H

/** \file primvaraccess.h
 Contains the PrimVarAccess class.
 */

#include <string>
#include "geomobject.h"

namespace support3d {

/**
  Helper class to access primitive variables during rendering.

  The class takes the geom and information about the variable in
  question as input to its constructor. During rendering, the 
  onFace() method has to be called for each face and onVertex() for
  each vertex. These methods return the next value if available.

  The class supports the following variable types:

  - constant (in which case onFace() returns a value each time)
  - uniform (onFace() returns a value)
  - varying (onVertex() returns a value)
  - facevarying (onVertex() returns a value)
  - user + facevarying faces variable (onVertex() returns a value)
  - Optional: user + uniform int[3] faces variable (onVertex() returns a value). This mode can only be used with TriMeshGeom classes!

  Example:

  \code 
  PrimVarAccess<vec3d> normals(geom, std::string("N"), NORMAL, 1, std::string("Nfaces"));
  vec3d* N;

  for(...each face...)
  {
    if (normals.onFace(N))
    {
      // ...do something with the normal...
    }

    for(...each vertex i...)
    {
	if (normals.onVertex(i, N))
	{
	  // ...do something with the normal...
        }
    }
  }
  \endcode
 */
template<class T>
class PrimVarAccess
{
  public:
  /** 
    Access mode.

    - 0: No access. Variable is not available or of wrong type.
    - 1: Variable is constant
    - 2: Variable is uniform
    - 3: Variable is varying
    - 4: Variable is facevarying
    - 5: Variable is user (+ faces, either facevarying or uniform int[3] (trimesh only!))
  */
  int mode;

  /**
     A pointer to the raw variable data.
  */
  T* var_ptr;

  /**
     A pointer to the raw variable data that contains the "XYZfaces" variable.
  */
  int* varfaces_ptr;

  /**
    Multiplicity of the variable.
   */
  int mult;

  public:
  PrimVarAccess(GeomObject& geom, std::string varname, VarType vartype, int varmult, std::string varfacesname=std::string(""), bool trimesh_flag=false);
  
  bool onFace(T*& value);
  bool onVertex(int idx, T*& value);
};

//////////////////////////////////////////////////////////////////////

/**
  Constructor.

  If the varfacesname argument is an empty string, then the mode using
  the "faces" variable is disabled. When the class is used for a 
  TriMeshGeom the \a trimesh_flag argument should be true to enable
  faces that are declared as "uniform int[3]".

  \param geom Geometry that is currently being processed
  \param varname The name of the variable that should be read
  \param vartype The required type of the variable (INT, FLOAT, ...)
  \param varmult The required multiplicty of the variable
  \param varfacesname The name of the corresponding "faces" variable
  \param trimesh_flag Determines whether uniform int[3] faces are allowed
 */
template<class T>
PrimVarAccess<T>::PrimVarAccess(GeomObject& geom, std::string varname, VarType vartype, int varmult, std::string varfacesname, bool trimesh_flag)
  : mode(0), var_ptr(0), varfaces_ptr(0), mult(varmult)
{
  PrimVarInfo* info;

  // Check if the variable is available
  info = geom.findVariable(varname);
  if (info!=0)
  {
    // Is the variable of the correct type and multiplicity?
    if (info->type==vartype && info->multiplicity==varmult)
    {
      var_ptr = dynamic_cast<ArraySlot<T>* >(info->slot)->dataPtr();
      switch(info->storage)
      {
       // "constant"?
       case CONSTANT: mode = 1; break;
       // "uniform"?
       case UNIFORM: mode = 2; break;
       // "varying"?
       case VARYING: mode = 3; break;
       // "facevarying"?
       case FACEVARYING: mode = 4; break;
       // "user"?
       case USER:
	 if (varfacesname!="")
	 {
	   // Check if the corresponding "faces" variable is available...
	   info = geom.findVariable(varfacesname);
	   if (info!=0 && info->type==INT)
	   {
	     varfaces_ptr = dynamic_cast<ArraySlot<int>* >(info->slot)->dataPtr();
	     if (info->storage==UNIFORM && info->multiplicity==3 && trimesh_flag)
	     {
	       mode = 5;
	     }
	     else if (info->storage==FACEVARYING && info->multiplicity==1)
	     {
	       mode = 5;
	     }
	   }
	 }
      }
    }
  }
}

/**
   Per face method.

   This method must be called before a face is processed. If there is a
   value available for the entire face then this value is passed back
   via \a value and \c true is returned.
   It is assumed that faces are processed in order (i.e. the first call
   will return the value for the first face, the second call the value
   for the second face and so on).

   \param[out] value Variable value for the next face
   \return True if there was a value, otherwise false.
 */
template<class T>  
bool PrimVarAccess<T>::onFace(T*& value)
{
  switch(mode)
  {
    // constant?
   case 1: value = var_ptr;
           return true;
     
   // uniform?
   case 2: value = var_ptr;
           var_ptr += mult;
           return true;

  default: return false;
  }
}

/**
  Per vertex method.

  This method must be called before a vertex is processed. If there is
  a value available for the vertex then this value is passed back via
  \a value and \c true is returned.
  It is assumed that the vertices are processed in order (unless the storage
  class of the variable is "varying").

  \param idx This is the index of the vertex (required for "varying" variables)
  \param[out] value Variable value for the next vertex
  \return True if there was a value, otherwise false.
 */
template<class T>  
bool PrimVarAccess<T>::onVertex(int idx, T*& value)
{
  int vidx;
  switch(mode)
  {
    // varying?
    case 3: value = var_ptr + mult*idx; 
            return true;

    // facevarying?
    case 4: value = var_ptr; 
            var_ptr += mult; 
            return true;

    // user (+uniform int[3] or facevarying faces)?
    // (both cases can be treated identically)
    case 5: vidx = *varfaces_ptr;
            varfaces_ptr++;
            value = var_ptr + mult*vidx;
            return true;

    // default: no value
    default: return false;
  }
}


} // end of namespace

#endif

