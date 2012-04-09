
:mod:`ffmpeg` --- FFmpeg wrapper
================================

.. module:: cgkit.ffmpeg
   :synopsis: FFmpeg wrapper modules

This module is a thin ctypes-based wrapper around the functions provided by the
`ffmpeg <http://www.ffmpeg.org/>`_ libraries. The libraries themselves
are not part of cgkit, they must be installed separately as shared libraries.

The module was built against ffmpeg version 0.7.6 (avformat 52.110.0,
avcodec 52.122.0, avutil 50.43.0, swscale 0.14.1). If the ffmpeg libraries
on your system are different, you may not be able to use this wrapper module
because of changes in the ffmpeg API.

avformat
--------

..  autofunction:: cgkit.ffmpeg.avformat.avformat_version

..  autofunction:: cgkit.ffmpeg.avformat.av_register_all

..  autofunction:: cgkit.ffmpeg.avformat.av_iformat_next

..  autofunction:: cgkit.ffmpeg.avformat.av_oformat_next

..  autofunction:: cgkit.ffmpeg.avformat.av_open_input_file

..  autofunction:: cgkit.ffmpeg.avformat.av_close_input_file

..  autofunction:: cgkit.ffmpeg.avformat.av_find_stream_info

..  autofunction:: cgkit.ffmpeg.avformat.av_read_frame

..  autofunction:: cgkit.ffmpeg.avformat.av_seek_frame

..  autofunction:: cgkit.ffmpeg.avformat.avformat_alloc_context

..  autofunction:: cgkit.ffmpeg.avformat.av_guess_format

..  autofunction:: cgkit.ffmpeg.avformat.av_guess_codec

..  autofunction:: cgkit.ffmpeg.avformat.av_new_stream


avcodec
-------

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_version

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_find_decoder

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_find_decoder_by_name

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_find_encoder

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_find_encoder_by_name

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_open

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_close

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_alloc_frame

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_decode_video2

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_decode_audio3

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_encode_video

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_flush_buffers

..  autofunction:: cgkit.ffmpeg.avcodec.avpicture_alloc

..  autofunction:: cgkit.ffmpeg.avcodec.avpicture_free

..  autofunction:: cgkit.ffmpeg.avcodec.av_init_packet

..  autofunction:: cgkit.ffmpeg.avcodec.av_free_packet

..  autofunction:: cgkit.ffmpeg.avcodec.avpicture_get_size

..  autofunction:: cgkit.ffmpeg.avcodec.avpicture_fill


Codec types:

- ``CODEC_TYPE_UNKNOWN``
- ``CODEC_TYPE_VIDEO``
- ``CODEC_TYPE_AUDIO``
- ``CODEC_TYPE_DATA``
- ``CODEC_TYPE_SUBTITLE``
- ``CODEC_TYPE_ATTACHMENT``


swscale
-------

There are the following functions in the module:

..  autofunction:: cgkit.ffmpeg.swscale.swscale_version

..  autofunction:: cgkit.ffmpeg.swscale.sws_getContext

..  autofunction:: cgkit.ffmpeg.swscale.sws_freeContext

..  autofunction:: cgkit.ffmpeg.swscale.sws_scale


avutil
------

There are the following functions in the module:

..  autofunction:: cgkit.ffmpeg.avutil.avutil_version

..  autofunction:: cgkit.ffmpeg.avutil.av_free

..  autofunction:: cgkit.ffmpeg.avutil.av_d2q

..  autofunction:: cgkit.ffmpeg.avutil.av_strerror

..  autofunction:: cgkit.ffmpeg.avutil.av_get_sample_fmt_name

..  autofunction:: cgkit.ffmpeg.avutil.av_get_sample_fmt

..  autofunction:: cgkit.ffmpeg.avutil.av_get_bytes_per_sample

..  autofunction:: cgkit.ffmpeg.avutil.av_get_pix_fmt

..  autofunction:: cgkit.ffmpeg.avutil.av_get_pix_fmt_name

The module defines the following pixel format constants:

- ``PIX_FMT_NONE``
- ``PIX_FMT_YUV420P``
- ``PIX_FMT_YUYV422``
- ``PIX_FMT_RGB24``
- ``PIX_FMT_BGR24``
- ``PIX_FMT_YUV422P``
- ``PIX_FMT_YUV444P``
- ``PIX_FMT_RGB32``
- ``PIX_FMT_YUV410P``

..  class:: AVRational

  ..  attribute:: num

    An integer containing the numerator.
    
  ..  attribute:: den 

    An integer containing the denominator.

:class:`AVFormatContext`
------------------------

..  class:: AVFormatContext

  .. attribute:: iformat
  
     This is a pointer to an :class:`AVInputFormat` object.
     Only one of *iformat* and *oformat* can contain a valid object, the other
     one is NULL.

  .. attribute:: oformat
  
     This is a pointer to an :class:`AVOutputFormat` object.
     Only one of *iformat* and *oformat* can contain a valid object, the other
     one is NULL.
  
  .. attribute:: nb_streams
  
     The number of streams in the file.
     
  .. attribute:: streams
  
     A list of :class:`AVStream` objects representing the file's streams.
     
  .. attribute:: filename
  
     The name of the file.
     
  .. attribute:: timestamp
  
     ...
     
  .. attribute:: title
  .. attribute:: author
  .. attribute:: copyright
  .. attribute:: comment
  .. attribute:: album
  .. attribute:: year
  .. attribute:: track
  .. attribute:: genre

  .. attribute:: start_time
  
     Decoding: Position of the first frame of the component, in
     ``AV_TIME_BASE`` fractional seconds. NEVER set this value directly,
     it is deduced from the AVStream values. 
       
  .. attribute:: duration

     Decoding: duration of the stream, in ``AV_TIME_BASE`` fractional
     seconds. NEVER set this value directly, it is deduced from the
     AVStream values.
  
  .. attribute:: file_size
  
     Decoding: Total file size, 0 if unknown.
  
  .. attribute:: bit_rate

     Decoding: Total stream bitrate in bit/s, 0 if not
     available. Never set it directly if the file_size and the
     duration are known as FFmpeg can compute it automatically.

:class:`AVStream`
------------------

..  class:: AVStream

  .. attribute:: index

     The stream index inside the file.

  .. attribute:: id

     Format-specific stream id.

  .. attribute:: codec

     A :class:`AVCodecContext` object.
 
  .. attribute:: r_frame_rate
  .. attribute:: time_base

     This is a :class:`AVRational` object containing the fundamental unit of
     time (in seconds) in terms of which frame timestamps are represented.
     For fixed-fps content, time base should be 1/framerate and timestamp
     increments should be 1.

  .. attribute:: quality
  .. attribute:: start_time

     Decoding: pts of the first frame of the stream in ``time_base`` units.
     Only set this if you are absolutely 100% sure that the value you set
     it to really is the pts of the first frame.
     This may be undefined (AV_NOPTS_VALUE).
     
     Note: The ASF header does NOT contain a correct start_time the ASF
     demuxer must NOT set this.

  .. attribute:: duration

     Decoding: duration of the stream, in stream time base.
     If a source file does not specify a duration, but does specify
     a bitrate, this value will be estimated from bitrate and file size.

  .. attribute:: language

     ISO 639-2/B 3-letter language code (empty string if undefined).
     
  .. attribute:: nb_frames

     The number of frames in this stream if known or 0.

  .. attribute:: sample_aspect_ratio
  
     An :class:`AVRational` containing the sample aspect ratio (0 if unknown).
     This is the width of a pixel divided by the height of the pixel.
     
     * Encoding: Set by user.
     * Decoding: Set by libavformat.


:class:`AVPacket`
-----------------

..  class:: AVPacket

  .. attribute:: pts
  
     An integer containing the presentation timestamp (in ``stream.time_base``
     units). This is the time at which the decompressed packet has to be presented
     to the user. The value can be ``AV_NOPTS_VALUE`` if it is not stored in the
     file.

  .. attribute:: dts

     Decompression timestamp (in ``stream.time_base`` units). This is the time
     at which the packet is decompressed.
     Can be ``AV_NOPTS_VALUE`` if it is not stored in the file.

  .. attribute:: data

     This is a pointer containing the address of the packet data.

  .. attribute:: size

     The size of the packet data in bytes.

  .. attribute:: stream_index

     The index of the stream this packet belongs to.

  .. attribute:: flags
  .. attribute:: duration

     The duration of this packet in ``stream.time_base`` units or 0 if unknown.
     Equals next_pts - this_pts in presentation order.

  .. attribute:: pos

     The byte position within the stream or -1 if unknown.

  .. attribute:: convergence_duration

:class:`AVCodecContext`
-----------------------

..  class:: AVCodecContext

  .. attribute:: bit_rate
   
     The average bitrate.
     
     * Encoding: Set by user; unused for constant quantizer encoding.
     * Decoding: Set by libavcodec. 0 or some bitrate if this info is available in the stream.

  .. attribute:: bit_rate_tolerance
  
     Number of bits the bitstream is allowed to diverge from the reference.
     The reference can be CBR (for CBR pass1) or VBR (for pass2)

     * Encoding: Set by user; unused for constant quantizer encoding.
     * Decoding: unused

  .. attribute:: codec_tag
  
     Fourcc (LSB first, so "ABCD" -> ('D'<<24) + ('C'<<16) + ('B'<<8) + 'A')).
     
     * Encoding: Set by user, if not then the default based on codec_id will be used.
     * Decoding: Set by user, will be converted to uppercase by libavcodec during init.

  .. attribute:: time_base
  
     This is a :class:`AVRational` containing the fundamental unit of time
     (in seconds) in terms of which frame timestamps are represented.
     For fixed-fps content, timebase should be 1/framerate and timestamp
     increments should be identically 1.
     
     * Encoding: MUST be set by user.
     * Decoding: Set by libavcodec.

  .. attribute:: width

     Picture width (video only).
     
     * Encoding: MUST be set by user.
     * Decoding: Set by libavcodec.

  .. attribute:: height

     Picture height (video only).
     
     * Encoding: MUST be set by user.
     * Decoding: Set by libavcodec.

  .. attribute:: sample_aspect_ratio
  
     An :class:`AVRational` containing the sample aspect ratio (0 if unknown).
     This is the width of a pixel divided by the height of the pixel.
     Numerator and denominator must be relatively prime and smaller than 256
     for some video standards.
     
     * Encoding: Set by user.
     * Decoding: Set by libavcodec.

  .. attribute:: gop_size
  
     The number of pictures in a group of pictures, or 0 for intra_only.
     
     * Encoding: Set by user.
     * Decoding: unused

  .. attribute:: pix_fmt
  
     Pixel format, see PIX_FMT_xxx.
     
     * Encoding: Set by user.
     * Decoding: Set by libavcodec.

  .. attribute:: coded_frame
  
     A pointer to an :class:`AVFrame` object containing the picture in the bitstream.
     
     * Encoding: Set by libavcodec.
     * Decoding: Set by libavcodec.


:class:`AVCodec`
----------------

..  class:: AVCodec

:class:`AVFrame`
----------------

..  class:: AVFrame

  .. attribute:: data
  
    A list of 4 pointers.
    
  .. attribute:: linesize
  
    A list of 4 integers.
    
  .. attribute:: base

  .. attribute:: key_frame
  
     Indicates whether this frame is a key frame (1) or not (0).
     This is always set by libavcodec (encoding and decoding).

  .. attribute:: pict_type

  .. attribute:: pts
  
     Presentation time stamp in time_base units.
     If ``AV_NOPTS_VALUE`` then frame_rate = 1/time_base will be assumed.
     
     * Encoding: MUST be set by user.
     * Decoding: Set by libavcodec.

  .. attribute:: coded_picture_number

  .. attribute:: display_picture_number

  .. attribute:: quality

  .. attribute:: age

  .. attribute:: reference

  .. attribute:: interlaced_frame

  .. attribute:: top_field_first

  .. attribute:: pan_scan
  

:class:`AVPicture`
------------------

..  class:: AVPicture

  .. attribute:: data
  
    A list of 4 pointers.
    
  .. attribute:: linesize
  
    A list of 4 integers containing the size of a single line.
    
