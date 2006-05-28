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

#define DLL_EXPORT_VEC3
#include "vec3.h"

namespace support3d {

// Klammerpaar und Trennzeichen für Ein-/Ausgabe
template<> float vec3<float>::epsilon = 1E-7f;
template<> double vec3<double>::epsilon = 1E-12;
template<> long double vec3<long double>::epsilon = 1E-12;

template<> short vec3<short>::epsilon = 0;
template<> int  vec3<int>::epsilon = 0;
template<> long int vec3<long int>::epsilon = 0;

}  // end of namespace
