# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is the Python Computer Graphics Kit.
#
# The Initial Developer of the Original Code is Matthias Baas.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

import ctypes
import findlib
import decls
from decls import AVRational

def avutil_version():
    """Return the libavutil library version.
    
    Returns a tuple (major,minor,micro) containing the three parts of the
    version number. 
    """
    v = _lib().avutil_version()
    major = v>>16
    minor = (v>>8)&0xff
    micro = v&0xff
    return (major,minor,micro)

def av_free(obj):
    """Free memory which has been allocated with av_malloc(z)() or av_realloc().
    
    *obj* may be a AVFrame object that was allocated using avcodec_alloc_frame()
    (note: *obj* must be the object itself, not a pointer to it).
    """
    if obj is None:
        return
    _lib().av_free(ctypes.byref(obj))

def av_d2q(d, max):
    """Convert a floating point number into a rational.
    
    *d* is the floating point number and *max* the maximum allowed numerator
    and denominator
    Returns a :class:`AVRational` object representing *d*.
    """
    func = _lib().av_d2q
    func.args = [ctypes.c_double, ctypes.c_int]
    func.restype = AVRational
    return func(ctypes.c_double(d), int(max))


# By default, try to load the avutil library that has the same major version
# than the one that was used for creating the cppdefs and decls module.
_libname = "avutil.%s"%(decls.LIBAVUTIL_VERSION_MAJOR)
_libavutil = None

def _lib():
    """Return the avutil shared library.
    """
    global _libavutil
    global _libname
    
    if _libavutil is None:
        _libavutil = findlib.findFfmpegLib(_libname)
    return _libavutil

