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

import sys
from ctypes import *
import findlib
import avutil
import avcodec

# This is defined here and in avcodec
AV_NOPTS_VALUE = 0x8000000000000000

MAX_STREAMS = 20

# av_seek_frame() flags
AVSEEK_FLAG_BACKWARD = 1   # Seek backwards
AVSEEK_FLAG_BYTE = 2  # seeking based on position in bytes 
AVSEEK_FLAG_ANY = 4   # Seek to any frame, even non keyframes

class AVFormatError(Exception):
    pass

######################################################################
# Data Structures
######################################################################

class ByteIOContext(Structure):
    _fields_ = [("buffer", c_char_p),
                ("buffer_size", c_int),
                ("buf_ptr", c_char_p),
                ("buf_end", c_char_p),
                ("opaque", c_void_p),
                ("read_packet", c_void_p), # function pointer
                ("write_packet", c_void_p), # function pointer
                ("seek", c_void_p), # function pointer
                ("pos", c_longlong),
                ("must_flush", c_int),
                ("eof_reached", c_int),
                ("write_flag", c_int),
                ("is_streamed", c_int),
                ("max_packet_size", c_int),
                ("checksum", c_ulong),
                ("checksum_ptr", c_char_p),
                ("update_checksum", c_void_p), # function pointer
                ("error", c_int),
                ("read_pause", c_void_p), # function pointer
                ("read_seek", c_void_p)] # function pointer

class AVPacket(Structure):
    pass

AVPacket._fields_ = [("pts", c_longlong),
                ("dts", c_longlong),
                ("data", c_void_p),  # uint8*
                ("size", c_int),
                ("stream_index", c_int),
                ("flags", c_int),
                ("duration", c_int),
                ("destruct", CFUNCTYPE(None, POINTER(AVPacket))),   # function pointer
                ("priv", c_void_p),
                ("pos", c_longlong),
                ("convergence_duration", c_longlong)]

class AVPacketList(Structure):
    pass

AVPacketList._fields_ = [("pkt", AVPacket),
                         ("next", POINTER(AVPacketList))]

class AVProbeData(Structure):
    pass

AVProbeData._field_ = [("filename", c_char_p),
                       ("buf", c_char_p),
                       ("buf_size", c_int)]

MAX_REORDER_DELAY = 16

class AVStream(Structure):
    _fields_ = [("index", c_int),
                ("id", c_int),
                ("codec", POINTER(avcodec.AVCodecContext)),
                ("r_frame_rate", avutil.AVRational),
                ("priv_data", c_void_p),
#                ("codec_info_duration", c_longlong),
#                ("codec_info_nb_frames", c_int),
                ("first_dts", c_longlong),
                ("pts", avutil.AVFrac),
                ("time_base", avutil.AVRational),
                ("pts_wrap_bits", c_int),
                ("stream_copy", c_int),
                ("discard", c_int),    # enum AVDiscard
                ("quality", c_float),
                ("start_time", c_longlong),
                ("duration", c_longlong),
                ("language", c_char*4),
                ("need_parsing", c_int),  # enum AVStreamParseType
                ("parser", c_void_p),     # AVCodecParserContext*
                ("cur_dts", c_longlong),
                ("last_IP_duration", c_int),
                ("last_IP_pts", c_longlong),
                ("index_entries", c_void_p),  # AVIndexEntry*
                ("nb_index_entries", c_int),
                ("index_entries_allocated_size", c_uint),
                ("nb_frames", c_longlong),
                
                ("unused", c_longlong*5),   # ??? #ifdef'ed ???
                ("filename", c_char_p),
                ("disposition", c_int),
                ("probe_data", AVProbeData),
                ("pts_buffer", c_longlong*(MAX_REORDER_DELAY+1)),
                ("sample_aspect_ratio", avutil.AVRational),
                ("metadata", c_void_p)   # AVMetaData*
#                ("pts_buffer", c_longlong*(MAX_REORDER_DELAY+1)),
#                ("filename", c_char_p)
                ]
    
    
class AVFormatContext(Structure):
    _fields_ = [("av_class", POINTER(avutil.AVClass)),
                ("iformat", c_void_p), # AVInputFormat*
                ("oformat", c_void_p), # AVOutputFormat*
                ("priv_data", c_void_p),
                ("pb", POINTER(ByteIOContext)),
                ("nb_streams", c_uint),
                ("streams", POINTER(AVStream)*MAX_STREAMS),
                ("filename", c_char*1024),
                ("timestamp", c_longlong),
                ("title", c_char*512),
                ("author", c_char*512),
                ("copyright", c_char*512),
                ("comment", c_char*512),
                ("album", c_char*512),
                ("year", c_int),
                ("track", c_int),
                ("genre", c_char*32),
                ("ctx_flags", c_int),
                ("packet_buffer", POINTER(AVPacketList)),
                ("start_time", c_longlong),
                ("duration", c_longlong),
                ("file_size", c_longlong),
                ("bit_rate", c_int),
                ("cur_st", POINTER(AVStream)),
                ("cur_ptr", c_void_p),
                ("cur_len", c_int),
                ("cur_pkt", AVPacket),
                ("data_offset", c_longlong),
                ("index_built", c_int),
                ("mux_rate", c_int),
                ("packet_size", c_int),
                ("preload", c_int),
                ("max_delay", c_int),
                ("loop_output", c_int),
                ("flags", c_int),
                ("loop_input", c_int),
                ("probesize", c_uint),
                ("max_analyze_duration", c_int),
                ("key", c_void_p),
                ("keylen", c_int),
                ("nb_programs", c_uint),
                ("programs", c_void_p),  # AVProgram**
                ("video_codec_id", c_int),  # enum
                ("audio_codec_id", c_int),  # enum
                ("subtitle_codec_id", c_int), # enum
                ("max_index_size", c_uint),
                ("max_picture_buffer", c_uint),
                ("nb_chapters", c_uint),
                ("chapters", c_void_p),  # AVChapter**
                ("debug", c_int),
                ("raw_packet_buffer", c_void_p),  # AVPacketList*
                ("raw_packet_buffer_end", c_void_p),  # AVPacketList*
                ("packet_buffer_end", c_void_p),  # AVPacketList*
                ("metadata", c_void_p)  # AVMetaData*
                ]

class AVOutputFormat(Structure):
    _fields_ = [("name", c_char_p),
                ("long_name", c_char_p)
                # ...
               ]

class AVInputFormat(Structure):
    _fields_ = [("name", c_char_p),
                ("long_name", c_char_p)
                # ...
               ]

######################################################################
# Functions
######################################################################

def avformat_version():
    """Return the libavformat library version.
    
    Returns a tuple (major,minor,micro) containing the three parts of the
    version number. 
    """
    v = _lib().avformat_version()
    major = v>>16
    minor = (v>>8)&0xff
    micro = v&0xff
    return (major,minor,micro)

def av_register_all():
    """Initialize libavformat and register all the (de)muxers and protocols.
    
    This must be called at the beginning before any file is opened.
    """
    _lib().av_register_all()

def av_oformat_next(fmt=None):
    """Return the first/next registered output format.
    
    If *fmt* is ``None``, the first registered output format is returned
    as a :class:`AVOutputFormat` object. If that object is passed back in
    as input, the next registered format is returned and so on. If there
    are no more formats available, ``None`` is returned.
    """
    func = _lib().av_oformat_next
    func.restype = POINTER(AVOutputFormat)
    if fmt is None:
        ptr = None
    else:
        ptr = byref(fmt)
    res = func(ptr)
    if res:
        res = res.contents
    else:
        res = None
    return res

def av_iformat_next(fmt=None):
    """Return the first/next registered input format.
    
    If *fmt* is ``None``, the first registered input format is returned
    as a :class:`AVInputFormat` object. If that object is passed back in
    as input, the next registered format is returned and so on. If there
    are no more formats available, ``None`` is returned.
    """
    func = _lib().av_iformat_next
    func.restype = POINTER(AVOutputFormat)
    if fmt is None:
        ptr = None
    else:
        ptr = byref(fmt)
    res = func(ptr)
    if res:
        res = res.contents
    else:
        res = None
    return res

def av_open_input_file(fileName, format=None, buf_size=0, params=None):
    """Open a media file as input. 

    *fileName* is a string containing the file to open.
    *format* is an optional :class:`AVInputFormat` object that can be specified
    to force a particular file format (AVInputFormat is not yet exposed).
    *buf_size* is an optional buffer size (or 0/``None`` if the default size is ok) 
    *params* is an optional :class:`AVFormatParameters` object if extra parameters
    have to be passed.
    
    The return value is a :class:`AVFormatContext` object that contains information
    about the format and that serves as a handle to the open file.
    In case of an error, an :exc:`AVFormatError` exception is thrown.
    """
    # Check input parameters
    if not isinstance(fileName, basestring):
        raise ValueError, "fileName must be a string"
    if buf_size is None:
        buf_size = 0
    elif type(buf_size)!=int:
        raise ValueError, "buf_size must be an int or None"
    if format is not None:
        raise ValueError, "format parameter is not yet supported"
    if params is not None:
        raise ValueError, "params parameter is not yet supported"
    
    formatCtxPtr = POINTER(AVFormatContext)()
    ret = _lib().av_open_input_file(byref(formatCtxPtr), fileName, format, buf_size, params)
    if ret!=0:
        raise AVFormatError("Error %s"%ret)
    return formatCtxPtr.contents

def av_close_input_file(formatCtx):
    """Close a media file (but not its codecs).

    *formatCtx* is the format context as returned by :func:`av_open_input_file()`
    If it is ``None``, the function returns immediately.
    """
    if formatCtx is None:
        return
    _lib().av_close_input_file(byref(formatCtx))

def av_find_stream_info(formatCtx):
    """Read packets of a media file to get stream information.

    This is useful for file formats with no headers such as MPEG. This
    function also computes the real frame rate in case of mpeg2 repeat
    frame mode. The logical file position is not changed by this
    function; examined packets may be buffered for later processing.

    *formatCtx* is the media file handle as returned by :func:`av_open_input_file()`.
    The return value is the integer that was returned by the underlying
    C function (it is always >=0). In the case of an error, an :exc:`AVFormatError`
    exception is thrown.
    """
    ret = _lib().av_find_stream_info(byref(formatCtx))
    if ret<0:
        raise AVFormatError("Error: %s"%ret)
    return ret

def av_read_frame(formatCtx, pkt):
    """Return the next frame of a stream. 

    *formatCtx* is the media file handle as returned by :func:`av_open_input_file()`.
    *pkt* is a :class:`AVPacket` object that will be filled with the packet data.

    The returned packet is valid until the next :func:`av_read_frame()` or until
    :func:`av_close_input_file()` and must be freed with :func:`av_free_packet()`.
    For video, the packet contains exactly one frame. For audio, it contains an
    integer number of frames if each frame has a known fixed size (e.g. PCM
    or ADPCM data). If the audio frames have a variable size (e.g. MPEG audio),
    then it contains one frame.

    ``pkt.pts``, ``pkt.dts`` and ``pkt.duration`` are always set to correct values
    in ``AVStream.timebase`` units (and guessed if the format cannot provided them).
    ``pkt.pts`` can be ``AV_NOPTS_VALUE`` if the video format has B frames, so it is
    better to rely on ``pkt.dts`` if you do not decompress the payload.
    
    Returns False when EOF was reached.
    """
    ret = _lib().av_read_frame(byref(formatCtx), byref(pkt))
    # Is this really EOF?
#    if ret==-1:
#        return False
    if ret<0:
        if formatCtx.pb:
            if formatCtx.pb.contents.eof_reached:
                return False
        raise AVFormatError("Error: %s"%ret)
    return True

def av_seek_frame(formatCtx, stream_index, timestamp, flags):
    """Seek to the key frame at timestamp. 

    'timestamp' in 'stream_index'. 

    stream_index     If stream_index is (-1), a default stream is selected, and timestamp is automatically converted from AV_TIME_BASE units to the stream specific time_base. 
    timestamp     timestamp in AVStream.time_base units or if there is no stream specified then in AV_TIME_BASE units 
    flags     flags which select direction and seeking mode (AVSEEK_FLAG_*)
    """
    ret = _lib().av_seek_frame(byref(formatCtx), stream_index, int(timestamp), flags)
    if ret<0:
        raise AVFormatError("Error: %s"%ret)
    return ret

def av_write_header(formatCtx):
    """Allocate stream private data and write the stream header.
    """
    ret = _lib().av_write_header(byref(formatCtx))
    if ret!=0:
        raise AVFormatError("Error: %s"%ret)

def av_write_trailer(formatCtx):
    """Writes the stream trailer to an output media file and frees the file private data.
    
    May only be called after a successful call to av_write_header().
    """
    ret = _lib().av_write_trailer(byref(formatCtx))
    if ret!=0:
        raise AVFormatError("Error: %s"%ret)
 
def av_write_frame(formatCtx, pkt):
    """Writes a packet to an output media file.

    The packet shall contain one audio or video frame.
    The packet must be correctly interleaved according to the container
    specification, if not then av_interleaved_write_frame() must be used.
    Returns 1 if end of stream is wanted, 0 otherwise.
    """
    ret = _lib().av_write_frame(byref(formatCtx), byref(pkt))
    if ret<0:
        raise AVFormatError("Error: %s"%ret)
    return ret

def av_interleaved_write_frame(formatCtx, pkt):
    """Writes a packet to an output media file ensuring correct interleaving.

    The packet must contain one audio or video frame.
    If the packets are already correctly interleaved, the application should
    call av_write_frame() instead as it is slightly faster. It is also important
    to keep in mind that completely non-interleaved input will need huge amounts
    of memory to interleave with this, so it is preferable to interleave at the
    demuxer level.
    Returns 1 if end of stream is wanted, 0 otherwise.
    """
    ret = _lib().av_interleaved_write_frame(byref(formatCtx), byref(pkt))
    if ret<0:
        raise AVFormatError("Error: %s"%ret)
    return ret


def av_free_packet(pkt):
    """Call the packet's destruct() function.
    """
    if pkt is None:
        return
    # How to test if pkt.destruct is 0?
    pkt.destruct(byref(pkt))

def dump_format(formatCtx, index, url, is_output):
    _lib().dump_format(byref(formatCtx), index, url, is_output) 

#####################################################

_libname = "avformat.52"
_libavformat = None

def _lib():
    """Return the avformat shared library.
    """
    global _libavformat
    global _libname
    if _libavformat is None:
        _libavformat = findlib.findFfmpegLib(_libname)
    return _libavformat

