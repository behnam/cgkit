# Initialization

# Import the modules so that the epsilon value can be changed
import vec3 as _vec3_module
import vec4 as _vec4_module
import mat3 as _mat3_module
import mat4 as _mat4_module
import quat as _quat_module

# Import types into the cgtypes namespace
from vec3 import vec3
from vec4 import vec4
from mat3 import mat3
from mat4 import mat4
from quat import quat, slerp, squad

# getEpsilon
def getEpsilon():
    """Return the epsilon threshold which is used for doing comparisons."""
    return _vec3_module._epsilon

# setEpsilon
def setEpsilon(eps):
    """Set a new epsilon threshold and returns the previously set value.
    """
    res = getEpsilon()
    eps = float(eps)
    _vec3_module._epsilon = eps
    _vec4_module._epsilon = eps
    _mat3_module._epsilon = eps
    _mat4_module._epsilon = eps
    _quat_module._epsilon = eps
    return res


