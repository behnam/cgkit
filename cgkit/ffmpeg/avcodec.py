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
from ctypes import *
import findlib
import avutil

# This is defined here and in avformat
AV_NOPTS_VALUE = 0x8000000000000000

AV_TIME_BASE = 1000000
  
# Error codes
AVERROR_UNKNOWN = -22      #   AVERROR(EINVAL)  /**< unknown error */
AVERROR_IO = -5            #   AVERROR(EIO)     /**< I/O error */
AVERROR_NUMEXPECTED = -33  #   AVERROR(EDOM)    /**< Number syntax expected in filename. */
AVERROR_INVALIDDATA = -22  #   AVERROR(EINVAL)  /**< invalid data found */
AVERROR_NOMEM = -12        #   AVERROR(ENOMEM)  /**< not enough memory */
#AVERROR_NOFMT = -42        #   AVERROR(EILSEQ)  /**< unknown format */
AVERROR_NOFMT = -92        #   AVERROR(EILSEQ)  /**< unknown format */
#AVERROR_NOTSUPP = -40      #   AVERROR(ENOSYS)  /**< Operation not supported. */
AVERROR_NOTSUPP = -78      #   AVERROR(ENOSYS)  /**< Operation not supported. */
AVERROR_NOENT = -2         #   AVERROR(ENOENT)  /**< No such file or directory. */
AVERROR_EOF = -32          #   AVERROR(EPIPE)   /**< End of file. */

# CodecType enum values
CODEC_TYPE_UNKNOWN = -1
CODEC_TYPE_VIDEO = 0
CODEC_TYPE_AUDIO = 1
CODEC_TYPE_DATA = 2
CODEC_TYPE_SUBTITLE = 3
CODEC_TYPE_ATTACHMENT = 4
CODEC_TYPE_NB = 4

class AVCodecError(Exception):
    pass

######################################################################
# Data Structures
######################################################################

class AVCodec(Structure):
    pass

AVCodec._fields_ = [("name", c_char_p),
                ("type", c_int),   # enum CodecType
                ("id", c_int),    # enum CodecID
                ("priv_data_size", c_int),
                ("init", c_void_p),  # function pointer
                ("encode", c_void_p),  # function pointer
                ("close", c_void_p),  # function pointer
                ("decode", c_void_p),  # function pointer
                ("capabilities", c_int),   # CODEC_CAP_*
                ("next", POINTER(AVCodec)),
                ("flush", c_void_p),  # function pointer
                ("supported_framerates", POINTER(avutil.AVRational)),  # array of supported framerates, or NULL if any, array is terminated by {0,0}
                ("pix_fmts", POINTER(c_int)),    # array of supported pixel formats, or NULL if unknown, array is terminated by -1
                ("long_name", c_char_p),
                ("supported_samplerates", POINTER(c_int)),  # array of supported audio samplerates, or NULL if unknown, array is terminated by 0
                ("sample_fmts", POINTER(c_int)),   # array of supported sample formats, or NULL if unknown, array is terminated by -1
                ("channel_layouts", POINTER(c_longlong))   # array of support channel layouts, or NULL if unknown. array is terminated by 0
                ]

class AVCodecContext(Structure):
    _fields_ = [("av_class", POINTER(avutil.AVClass)),
                ("bit_rate", c_int),
                ("bit_rate_tolerance", c_int),
                ("flags", c_int),
                ("sub_id", c_int),
                ("me_method", c_int),
                ("extradata", c_void_p),   # uint8*
                ("extradata_size", c_int),
                ("time_base", avutil.AVRational),
                ("width", c_int),
                ("height", c_int),
                ("gop_size", c_int),
                ("pix_fmt", c_int),   #  enum PixelFormat
                ("rate_emu", c_int),
                ("draw_horiz_band", c_void_p),   # function pointer
                ("sample_rate", c_int),
                ("channels", c_int),
                ("sample_fmt", c_int),  # enum SampleFormat
                ("frame_size", c_int),
                ("frame_number", c_int),
                ("real_pict_num", c_int),
                ("delay", c_int),
                ("qcompress", c_float),
                ("qblur", c_float),
                ("qmin", c_int),
                ("qmax", c_int),
                ("max_qdiff", c_int),
                ("max_b_frames", c_int),
                ("b_quant_factor", c_float),
                ("rc_strategy", c_int),
                ("b_frame_strategy", c_int),
                ("hurry_up", c_int),
                ("codec", POINTER(AVCodec)),
                ("priv_data", c_void_p),
#                ("rtp_mode", c_int),
                ("rtp_payload_size", c_int),
                ("rtp_callback", c_void_p),  # function pointer
                ("mv_bits", c_int),
                ("header_bits", c_int),
                ("i_tex_bits", c_int),
                ("p_tex_bits", c_int),
                ("i_count", c_int),
                ("p_count", c_int),
                ("skip_count", c_int),
                ("misc_bits", c_int),
                ("frame_bits", c_int),
                ("opaque", c_void_p),
                ("codec_name", c_char*32),
                ("codec_type", c_int),    # enum CodecType
                ("codec_id", c_int),      # enum CodecID
                ("codec_tag", c_uint)
                # ...
                ]

class AVPicture(Structure):
    _fields_ = [("data", c_void_p*4),
                ("linesize", c_int*4)]

class AVFrame(Structure):
    """
    This structure begins just like an AVPicture but has more entries.
    """
    _fields_ = [("data", c_void_p*4),
                ("linesize", c_int*4),
                ("base", c_void_p*4),
                ("key_frame", c_int),
                ("pict_type", c_int),
                ("pts", c_longlong),
                ("coded_picture_number", c_int),
                ("display_picture_number", c_int),
                ("quality", c_int),
                ("age", c_int),
                ("reference", c_int)
                #...
                ]

######################################################################
# Functions
######################################################################

def avcodec_version():
    """Return the libavcodec library version.
    
    Returns a tuple (major,minor,micro) containing the three parts of the
    version number. 
    """
    v = _lib().avcodec_version()
    major = v>>16
    minor = (v>>8)&0xff
    micro = v&0xff
    return (major,minor,micro)

def avcodec_find_decoder(id):
    """Finds a decoder with a matching codec ID.
    
    id is an integer containing the codec id.
    Returns a AVCodec object or None if no decoder was found.
    """
    # The returned pointer is owned by the library, so we don't have to
    # do anything to get rid of it.
    func = _lib().avcodec_find_decoder
    func.restype = POINTER(AVCodec)
    res = func(id)
    if res:
        return res.contents
    else:
        return None

def avcodec_find_decoder_by_name(name):
    """Finds a registered decoder with the specified name.
    
    Returns a AVCodec object or None if no decoder was found.
    """
    # The returned pointer is owned by the library, so we don't have to
    # do anything to get rid of it.
    func = _lib().avcodec_find_decoder_by_name
    func.args = [ctypes.c_char_p]
    func.restype = POINTER(AVCodec)
    res = func(name)
    if res:
        return res.contents
    else:
        return None
    
def avcodec_open(avctx, codec):
    """Initializes the AVCodecContext to use the given AVCodec. 

    avctx is a AVCodecContext object and codec a AVCodec object.
    Raises an exception when an error occurs.

    Prior to using this function the context has to be allocated.

    The functions avcodec_find_decoder_by_name(), avcodec_find_encoder_by_name(),
    avcodec_find_decoder() and avcodec_find_encoder() provide an easy way for 
    retrieving a codec.
    
    Warning: This function is not thread safe!
    """
    ret = _lib().avcodec_open(byref(avctx), byref(codec))
    if ret<0:
        # It can happen that the file was actually opened, so try to close it again.
        # The line is commented out because closing it here seems to cause more harm
        # (sometimes it leads to the lib not being able to open anything at all anymore)
        #avcodec_close(avctx)
        raise AVCodecError("Error: %s"%ret)
    return ret    
    
def avcodec_close(codecCtx):
    """Close the codec.
    """
    return _lib().avcodec_close(byref(codecCtx))
    
def avcodec_alloc_frame():
    """Allocates an AVFrame and sets its fields to default values. 

    The resulting struct can be deallocated by simply calling avutil.av_free().
    Returns an AVFrame object.
    """
    func = _lib().avcodec_alloc_frame
    func.restype = POINTER(AVFrame)
    res = func()
    if res:
        return res.contents
    else:
        return None
    
def avcodec_decode_video(codecCtx, picture, buf, bufsize):
    """Decodes a video frame from buf into picture. 

    The avcodec_decode_video() function decodes a video frame from the input
    buffer buf of size buf_size. To decode it, it makes use of the video
    codec which was coupled with avctx using avcodec_open(). The resulting 
    decoded frame is stored in picture.    
    Returns a tuple (got_picture, bytes) where got_picture is a boolean that
    indicates whether a frame was decoded (True) or not and bytes is the number
    of bytes used.
    """
    got_picture = c_int()
    ret = _lib().avcodec_decode_video(byref(codecCtx), byref(picture), byref(got_picture), buf, bufsize)
    if ret<0:
        raise AVCodecError("Error: %s"%ret)
    return bool(got_picture.value), ret

def avcodec_decode_audio2(codecCtx, sampleBuf, buf, bufsize):
    """Decode an audio frame.
    
    sampleBuf is a ctypes short array.
    buf is the encoded data and bufsize the size of the encoded data.
    Returns the frameSize (size in bytes of the decoded frame) and the number
    of bytes that have been used from buf.
    """
    frameSize = c_int(ctypes.sizeof(sampleBuf))
    ret = _lib().avcodec_decode_audio2(byref(codecCtx), sampleBuf, byref(frameSize), buf, bufsize)
    if ret<0:
        raise AVCodecError("Error: %s"%ret)
    return frameSize.value, ret

def avpicture_alloc(picture, pix_fmt, width, height):
    """Allocate memory for a picture. 

    Call avpicture_free() to free it.
    
    picture     the AVPicture obejct to be filled in 
    pix_fmt     the format of the picture 
    width     the width of the picture 
    height     the height of the picture
    """
    ret = _lib().avpicture_alloc(byref(picture), pix_fmt, width, height)
    if ret<0:
        raise RuntimeError, "Error: %s"%ret
    
def avpicture_free(picture):
    """Free a picture previously allocated by avpicture_alloc().
    """
    _lib().avpicture_free(byref(picture))
    
def avpicture_get_size(pix_fmt, width, height):
    """Calculate image size.
    
    Calculate the size in bytes that a picture of the given 
    width and height would occupy if stored in the given picture format.
    
    pix_fmt     the given picture format 
    width     the width of the image 
    height     the height of the image
    
    Returns the size in bytes.
    """
    ret = _lib().avpicture_get_size(pix_fmt, width, height)
    if ret<0:
        raise AVCodecError("Error: %s"%ret)
    return ret

def avpicture_fill(picture, ptr, pix_fmt, width, height):
    """Fill in the AVPicture fields. 

    The fields of the given AVPicture are filled in by using the 'ptr'
    address which points to the image data buffer. Depending on the
    specified picture format, one or multiple image data pointers and
    line sizes will be set. If a planar format is specified, several
    pointers will be set pointing to the different picture planes and
    the line sizes of the different planes will be stored in the
    lines_sizes array.
    
    picture     AVPicture whose fields are to be filled in 
    ptr     Buffer which will contain or contains the actual image data 
    pix_fmt     The format in which the picture data is stored. 
    width     the width of the image in pixels 
    height     the height of the image in pixels  

    Returns the size of the image data in bytes
    """
    return _lib().avpicture_fill(byref(picture), ptr, pix_fmt, width, height)

def avcodec_flush_buffers(codecCtx):
    """Flush buffers.

    Should be called when seeking or when switching to a different stream.
    """
    _lib().avcodec_flush_buffers(byref(codecCtx))

######################################################################

_libname = "avcodec.52"
_libavcodec = None

def _lib():
    """Return the avcodec shared library.
    """
    global _libavcodec
    global _libname
    if _libavcodec is None:
        _libavcodec = findlib.findFfmpegLib(_libname)
    return _libavcodec

