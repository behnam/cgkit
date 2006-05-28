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

/** \file shared_export.h
 Defines macros necessary for creating the DLL.

 This file should only be included when the DLL is being created.
 */

#undef CGKIT_SHARED

#ifdef WIN32
  #ifdef _LIB
    #define CGKIT_SHARED
  #else
    #define CGKIT_SHARED __declspec(dllexport) 
  #endif
#else
  #define CGKIT_SHARED 
#endif
