######################################################################
# planegeom
######################################################################
# $Id: planegeom.py,v 1.1.1.1 2004/12/12 14:31:11 mbaas Exp $

## \file planegeom.py
## Contains the PlaneGeom class.

import _core

# PlaneGeom
class PlaneGeom(_core.PlaneGeom):
    def __init__(self, lx=1.0, ly=1.0, segmentsx=1, segmentsy=1):
        _core.PlaneGeom.__init__(self, lx, ly, segmentsx, segmentsy)

