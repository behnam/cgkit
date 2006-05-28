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
# $Id: preferences.py,v 1.1.1.1 2004/12/12 14:31:13 mbaas Exp $

## \file preferences.py
## \brief Contains the Preferences class.

import sys, os, os.path, pickle

# Preferences
class Preferences(object):
    """This class stores arbitrary values persistently.

    This class can be used just like a dictionary.
    """

    def __init__(self, filename):
        """Constructor."""

        # If filename is no absolute path make it relative to the default
        # config file path
        if not os.path.isabs(filename):
            filename = os.path.join(configPath(), filename)
            
        self._prefs = {}
        self._filename = filename

    def __len__(self):
        return len(self._prefs)

    def __iter__(self):
        return self._prefs.iteritems()

    def __getitem__(self, key):
        if key in self._prefs:
            return self._prefs[key]
        else:
            return None

    def __setitem__(self, key, value):
        self._prefs[key]=value

    def __delitem__(self, key):
        if key in self._prefs:
            del self._prefs[key]

    def __contains__(self, item):
        return item in self._prefs

    def get(self, key, default=None):
        return self._prefs.get(key, default)

    # load
    def load(self):
        """Load the preferences.

        """

        f = open(self._filename)
        id = pickle.load(f)
        if id!=1:
            raise Exception, "Unknown config file format"
        self._prefs = pickle.load(f)
        f.close()


    # save
    def save(self):
        """Save the preferences.

        """
        
        self._preparePath(os.path.dirname(self._filename))
        
        f = open(self._filename, "w")
        pickle.dump(1, f)
        pickle.dump(self._prefs, f)
        f.close()


    ######################################################################
    ## protected:

    def _preparePath(self, path):
        """Prepare a path so that every directory on the path exists.

        Checks if the path exists and creates it if it does not exist.
        """
        if not os.path.exists(path):
            parent = os.path.dirname(path)
            if parent!="":
                self._preparePath(parent)
            os.mkdir(path)        

    # "filename" property

    def _getFilename(self):
        """Return the filename.

        This method is used for retrieving the \a filename property.

        \return Filename (\c str).
        """
        return self._filename

    filename = property(_getFilename, None, None, "File name")
    

######################################################################

def configPath(appname="gaia"):
    """Return the full path where config files are located.

    \todo Change "gaia" as default application name
    """
    
    # Windows? (XP)
    if sys.platform=="win32":
        if os.environ.has_key("APPDATA"):
            return os.path.abspath(os.path.join(os.environ["APPDATA"], appname.capitalize()))
        else:
            return None
    # Other
    else:
        if os.environ.has_key("HOME"):
            return os.path.abspath(os.environ["HOME"])
        else:
            return None


######################################################################

if __name__=="__main__":

    print configPath()
            
            

    
