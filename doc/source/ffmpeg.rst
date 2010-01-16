
:mod:`ffmpeg` --- FFmpeg wrapper
================================

.. module:: cgkit.ffmpeg
   :synopsis: FFmpeg wrapper modules

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

..  autofunction:: cgkit.ffmpeg.avformat.av_free_packet


..  class:: AVFormatContext

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
  .. attribute:: duration
  .. attribute:: file_size
  .. attribute:: bit_rate


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


..  class:: AVPacket

  .. attribute:: pts
  
     An integer containing the presentation timestamp (in ``stream.time_base``
     units). This is the time at which the decompressed packet has to be presented
     to the user. The value can be ``AV_NOPTS_VALUE`` if it is not stored in the
     file.

  .. attribute:: dts

     Decompression timestamp (in ``stream.time_base``units). This is the time
     at which the packet is decompressed.
     Can be ``AV_NOPTS_VALUE`` if it is not stored in the file.

  .. attribute:: data

     This is an integer containing the address of the packet data.

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


avcodec
-------

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_version

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_find_decoder

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_find_decoder_by_name

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_open

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_close

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_alloc_frame

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_decode_video

..  autofunction:: cgkit.ffmpeg.avcodec.avcodec_flush_buffers

..  autofunction:: cgkit.ffmpeg.avcodec.avpicture_alloc

..  autofunction:: cgkit.ffmpeg.avcodec.avpicture_free

..  autofunction:: cgkit.ffmpeg.avcodec.avpicture_get_size

..  autofunction:: cgkit.ffmpeg.avcodec.avpicture_fill



..  class:: AVCodecContext


..  class:: AVCodec


..  class:: AVFrame


..  class:: AVPicture


Codec types:

- ``CODEC_TYPE_UNKNOWN``
- ``CODEC_TYPE_VIDEO``
- ``CODEC_TYPE_AUDIO``
- ``CODEC_TYPE_DATA``
- ``CODEC_TYPE_SUBTITLE``
- ``CODEC_TYPE_ATTACHMENT``


avutil
------

There are the following functions in the module:

..  autofunction:: cgkit.ffmpeg.avutil.avutil_version

..  autofunction:: cgkit.ffmpeg.avutil.av_free

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



