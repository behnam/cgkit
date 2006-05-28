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


#ifndef DEBUGINFO_H
#define DEBUGINFO_H

#include <iostream>
#include "stdio.h"

// Define the CGKIT_SHARED variable
#ifdef DLL_EXPORT_DEBUGINFO
  #include "shared_export.h"
#else
  #include "shared.h"
#endif

CGKIT_SHARED extern char _debug_buf[];
CGKIT_SHARED extern bool _debug_on;

CGKIT_SHARED void set_debug_flag(bool flag);
CGKIT_SHARED bool get_debug_flag();

// Output a text or anything else that can be put on a stream
#define DEBUGINFO(obj, msg) if (_debug_on) std::cerr<<"0x"<<std::hex<<(long)obj<<std::dec<<": "<<msg<<std::endl;

// Output a debug message with one argument. txt must be a format string suitable for sprintf.
#define DEBUGINFO1(obj, txt, arg) if (_debug_on) { sprintf(_debug_buf, txt, arg); std::cerr<<"0x"<<std::hex<<(long)obj<<std::dec<<": "<<_debug_buf<<std::endl; }

// Output a debug message with two arguments. txt must be a format string suitable for sprintf.
#define DEBUGINFO2(obj, txt, arg1, arg2) if (_debug_on) { sprintf(_debug_buf, txt, arg1, arg2); std::cerr<<"0x"<<std::hex<<(long)obj<<std::dec<<": "<<_debug_buf<<std::endl; }

// Output a debug message with three arguments. txt must be a format string suitable for sprintf.
#define DEBUGINFO3(obj, txt, arg1, arg2, arg3) if (_debug_on) { sprintf(_debug_buf, txt, arg1, arg2, arg3); std::cerr<<"0x"<<std::hex<<(long)obj<<std::dec<<": "<<_debug_buf<<std::endl; }

#endif
