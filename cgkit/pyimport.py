###########################################################################
# cgkit - Python Computer Graphics Kit
# Copyright (C) 2004 Matthias Baas (baas@ira.uka.de)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# cgkit homepage: http://cgkit.sourceforge.net
###########################################################################
# $Id: pyimport.py,v 1.4 2005/08/30 09:59:07 mbaas Exp $

import sys, os.path, copy
import pluginmanager
import cgkit.scene

# PyImporter
class PyImporter:

    _protocols = ["Import"]

    # extension
    def extension():
        return ["py"]
    extension = staticmethod(extension)

    # description
    def description(self):
        return "Python file"
    description = staticmethod(description)

    # importFile
    def importFile(self, filename):
        """Import a Python source file."""

        file_globals = {}
        # Use all globals from the cgkit package
        # Commented out the following line as is imported from cgkit.all now
#        file_globals = copy.copy(cgkit.__dict__)
        # Add some modules...
        exec "from cgkit.all import *" in file_globals
        exec "from cgkit.sl import *" in file_globals
        exec "from math import *" in file_globals
        # ...and some special global names...
        scene = cgkit.scene.getScene()
        file_globals["scene"] = scene
        file_globals["timer"] = scene.timer()
        file_globals["worldroot"] = scene.worldRoot()
        file_globals["eventmanager"] = cgkit.eventmanager.eventManager()
        
        paths = sys.path
        # Add the directory of the input file to the module search paths
        # so that local imports do work
        sys.path = [os.path.abspath(os.path.dirname(filename))] + sys.path
        # Import the file
        execfile(filename, file_globals)
        # Restore the old search paths
        sys.path = paths


######################################################################

# Register the OffImporter class as a plugin class
pluginmanager.register(PyImporter)
