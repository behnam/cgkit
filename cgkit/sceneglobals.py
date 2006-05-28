######################################################################
# globals
######################################################################
# $Id: sceneglobals.py,v 1.1.1.1 2004/12/12 14:31:23 mbaas Exp $

## \file globals.py
## Contains the Globals class.

"""This module contains the Globals class."""

from scene import getScene
from cgtypes import *

# Globals
class Globals:
    """%Globals class.

    This is just a convenience class to provida a "scope" for setting
    the global scene properties.
    """

    def __init__(self,
                 up = (0,0,1),
                 handedness = 'r',
                 unit = "m",
                 unitscale = 1.0,
                 **keyargs):

        scene = getScene()
        scene.up = vec3(up)
        scene.handedness = handedness
        scene.unit = unit
        scene.unitscale = unitscale

        for opt in keyargs:
            scene._globals[opt] = keyargs[opt]
        
