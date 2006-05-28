/* ======================================================================
 OpenSceneGraph Wrapped
 Copyright (C) 2004 Ole Ciliox (ole@ira.uka.de) 

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
====================================================================== */   

#include <boost/python.hpp>    
#include "osgcore.h"  

using namespace boost::python;  

void class_OsgCore() 
{
  class_<OsgCore>("OsgCore", init<>())
    .def("fooz", &OsgCore::fooz)
	.def("renderFrame", &OsgCore::renderFrame)
	.def("initStuff", &OsgCore::initStuff)
	.def("pumpKeyDowns", &OsgCore::pumpKeyDowns)
	.def("pumpKeyUps", &OsgCore::pumpKeyUps)
	.def("pumpMotions", &OsgCore::pumpMotions)
	.def("setupCamera", &OsgCore::setupCamera)
	.def("pumpMouseDowns", &OsgCore::pumpMouseDowns) 
    ;
};

