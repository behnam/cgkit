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
from ffmpeg import decls, cppdefs, avutil, swscale, avformat, avcodec
import ctypes
try:
    import Image
    _pilImportException = None
except ImportError, exc:
    _pilImportException = exc


class MediaFileError(Exception):
    pass

class VideoData:
    """Decoded image data.
    
    This class serves as a container for the data that is passed to the
    video callbacks.
    """
    def __init__(self, pts=None, size=None, frame=None, picture=None, pictureSize=None, swsCtx=None):
        # Presentation timestamp (float)
        self.pts =pts
        # Image size (width, height)
        self.size = size
        
        # AVFrame object (containing the decoded frame (but not as RGB))
        self.frame = frame
        # AVPicture object (for the RGB frame)
        self.picture = picture
        # The size in bytes of a full (RGB) picture
        self.pictureSize = pictureSize
        
        self._swsCtx = swsCtx
    
    def isKeyFrame(self):
        """Check whether the current frame is a key frame or not.
        """
        return self.frame.key_frame==1
    
    def pilImage(self):
        """Return the current frame as a PIL image.
        """
        global _pilImportException
        if _pilImportException is not None:
            raise _pilImportException

        # Convert the frame into RGB
        self.initPicture()
        # Obtain a Python string containing the RGB image data
        dataStr = ctypes.string_at(self.picture.data[0], self.pictureSize)
        # Convert to PIL image
        return Image.fromstring("RGB", self.size, dataStr)

    def initPicture(self):
        """Convert the raw frame into a RGB picture.
        
        Initializes self.picture.
        """
        # Convert the image into RGB format
        height = self.size[1]
        swscale.sws_scale(self._swsCtx, self.frame.data, self.frame.linesize, 0, height, self.picture.data, self.picture.linesize)


class AudioData:
    """Decoded audio data.
    """
    def __init__(self, pts=None, channels=None, framerate=None, samples=None, sampleSize=None):
        # Presentation timestamp (float)
        self.pts = pts
        # The number of channels (int)
        self.channels = channels
        # The framerate in Hz
        self.framerate = framerate
        # The decoded samples
        self.samples = samples
        # The number of bytes in the samples buffer
        self.sampleSize = sampleSize


class StreamBase_ffmpeg(object):
    """Base class for the audio/video streams.
    """
    def __init__(self, stream):
        """Constructor.
        
        stream is a AVStream object.
        """
        object.__init__(self)
        self._stream = stream

        # Get the codec context of the stream
        self._codecCtx = stream.codec.contents

        # Obtain an appropriate decoder...
        self._codec = avcodec.avcodec_find_decoder(self._codecCtx.codec_id)

        if self._codec is not None:
            # Open the codec
            avcodec.avcodec_open(self._codecCtx, self._codec)

    def close(self):
        """Close the stream/codec.
        """
        if self._codecCtx is not None:
            avcodec.avcodec_close(self._codecCtx)
            self._codecCtx = None
            self._codec = None
    
    def decodeBegin(self):
        """This is called right before decoding begins.
        
        The method returns a boolean indicating whether the stream should
        be enabled (True) or not (False). A stream might be enabled if there
        is no callback (i.e. noone is interested in the decoded data).
        """
        pass
    
    def decodeEnd(self):
        """This is called after decoding has finished.
        
        This is only called when decodeBegin() didn't return False or raise
        an error.
        """
        pass
    
    def handlePacket(self, pkt):
        """This is called during decoding to handle an encoded file packet.
        
        This is only called when decodeBegin() didn't return False or raise
        an error.
        """
        pass

    @property
    def fourcc(self):
        v = self._codecCtx.codec_tag
        return "%s%s%s%s"%(chr(v&0xff), chr((v>>8)&0xff), chr((v>>16)&0xff), chr((v>>24)&0xff))

    @property
    def codecName(self):
        if self._codec is None:
            return None
        else:
            return self._codec.name

    @property
    def codecLongName(self):
        if self._codec is None:
            return None
        else:
            return self._codec.long_name
    


class AudioStream_ffmpeg(StreamBase_ffmpeg):
    """Audio stream class.
    """
    def __init__(self, stream):
        StreamBase_ffmpeg.__init__(self, stream)
        self._frameCallback = None
    
    def setFrameCallback(self, callback):
        self._frameCallback = callback

    def decodeBegin(self):
        if self._frameCallback is None:
            return False
        
        tb = self._stream.time_base
        self._timebase = float(tb.num)/tb.den

        # Allocate a buffer for the decoded audio frame
        size = 192000
        self._sampleBuf = (size*ctypes.c_short)()

        self._audioData = AudioData(channels=self._codecCtx.channels, framerate=self._codecCtx.sample_rate, samples=self._sampleBuf)
        return True

    def decodeEnd(self):
        pass
    
    def handlePacket(self, pkt):
        # Decode the frame...
        codecCtx = self._codecCtx
        frameSize,bytesUsed = avcodec.avcodec_decode_audio2(codecCtx, self._sampleBuf, pkt.data, pkt.size)
        
        if frameSize>0:
            self._audioData.pts = pkt.dts*self._timebase
            self._audioData.sampleSize = frameSize
            self._frameCallback(self._audioData)

    @property
    def nchannels(self):
        return self._codecCtx.channels

    @property
    def framerate(self):
        return self._codecCtx.sample_rate

    @property
    def bitrate(self):
        return self._codecCtx.bit_rate


class VideoStream_ffmpeg(StreamBase_ffmpeg):
    """Video stream class.
    """

    def __init__(self, stream):
        StreamBase_ffmpeg.__init__(self, stream)
        self._frameCallback = None
        self._swsCtx = None
        self._picture = None
        self._frame = None
    
    def setFrameCallback(self, callback):
        self._frameCallback = callback
    
    def decodeBegin(self):
        if self._frameCallback is None:
            return False
        
        # Allocate a video frame that will store the decoded frames
        try:
            self._frame = avcodec.avcodec_alloc_frame()
            if self._frame is None:
                raise MemoryError("Failed to allocate AVFrame object")
            
            # Allocate just a picture for the converted image...
            self._picture = decls.AVPicture()
            width = self._codecCtx.width
            height = self._codecCtx.height
            avcodec.avpicture_alloc(self._picture, decls.PIX_FMT_RGB24, width, height)
            # Get the size of the destination image buffer
            self._pictureSize = avcodec.avpicture_get_size(decls.PIX_FMT_RGB24, width, height)
    
            # Allocate a SwsContext structure to convert the image
            self._swsCtx = swscale.sws_getContext(width, height, self._codecCtx.pix_fmt, 
                                                  width, height, decls.PIX_FMT_RGB24, 1)
            
            tb = self._stream.time_base
            self._timebase = float(tb.num)/tb.den
            self._videoData = VideoData(size=(width, height), frame=self._frame,
                                        picture=self._picture, pictureSize=self._pictureSize,
                                        swsCtx=self._swsCtx)
        except:
            self.decodeEnd()
            raise

        return True

    def decodeEnd(self):
        if self._swsCtx is not None:
            swscale.sws_freeContext(self._swsCtx)
            self._swsCtx = None
        if self._picture is not None:
            avcodec.avpicture_free(self._picture)
            self._picture = None
        if self._frame is not None:
            avutil.av_free(self._frame)
            self._frame = None

    def handlePacket(self, pkt):
        # Decode the frame...
        codecCtx = self._codecCtx
        hasFrame,bytes = avcodec.avcodec_decode_video(codecCtx, self._frame, pkt.data, pkt.size)

        if hasFrame:
            # Conversion into RGB or creation of a PIL image is done by the
            # video data object on demand
            
            #print "PTS:%s  DTS:%s  Duration:%s"%(pkt.pts, pkt.dts, pkt.duration)
            self._videoData.pts = pkt.dts*self._timebase
            
            self._frameCallback(self._videoData)

    @property
    def width(self):
        return self._codecCtx.width

    @property
    def height(self):
        return self._codecCtx.height


class Media_Read_ffmpeg(object):
    """Media file reader.
    """
    
    def __init__(self, fileName):
        object.__init__(self)
        
        # Audio streams (AudioStream_ffmpeg objects)
        self.audioStreams = []
        # Video streams (VideoStream_ffmpeg objects)
        self.videoStreams = []
    
        # All streams in file order
        self._streams = []
    
        # The AVFormatContext object for the open file
        self._formatCtx = None
        
        # Open the video file
        self._formatCtx = avformat.av_open_input_file(fileName, None, 0, None)
        # Fill the 'streams' fields...
        avformat.av_find_stream_info(self._formatCtx)

        # Create the stream wrapper objects
        for i in range(self._formatCtx.nb_streams):
            stream = self._formatCtx.streams[i].contents
            codec = stream.codec.contents
            if codec.codec_type==decls.CODEC_TYPE_VIDEO:
                stream = VideoStream_ffmpeg(stream)
                self._streams.append(stream)
                self.videoStreams.append(stream)
            elif codec.codec_type==decls.CODEC_TYPE_AUDIO:
                stream = AudioStream_ffmpeg(stream)
                self._streams.append(stream)
                self.audioStreams.append(stream)
            else:
                self._streams.append(None)

    def close(self):
        """Close the file.
        """
        for stream in self.audioStreams:
            stream.close()
        for stream in self.videoStreams:
            stream.close()
        
        self.audioStreams = []
        self.videoStreams = []
        
        if self._formatCtx is not None:
            avformat.av_close_input_file(self._formatCtx)
            self._formatCtx = None
    
    def numAudioStreams(self):
        """Return the number of audio streams defined in the file.
        """
        return len(self.audioStreams)
    
    def numVideoStreams(self):
        """Return the number of video streams defined in the file.
        """
        return len(self.videoStreams)

    def _frameCallback(self, imgData):
        self._imgData = imgData
    
    def iterFrames(self):
        """Iterate over the frames of the first video stream.
        """
        if len(self.videoStreams)==0:
            return
        
        videoStream = self.videoStreams[0]
        videoStream.setFrameCallback(self._frameCallback)
        if not videoStream.decodeBegin():
            return
        
        ffStream = videoStream._stream
        try:
            self._imgData = None
            for pkt in self.iterPackets():
                if pkt.stream_index==ffStream.index:
                    videoStream.handlePacket(pkt)
                    if self._imgData is not None:
                        yield self._imgData
                        self._imgData = None
        finally:
            videoStream.decodeEnd()
    
    def decode(self, videoCallbacks=None, audioCallbacks=None):
        """Read the individual packets from the streams and pass them to the callbacks.
        """
        if videoCallbacks is None:
            videoCallbacks = []
        if audioCallbacks is None:
            audioCallbacks = []

        # Set the callbacks...
        for stream,callback in zip(self.videoStreams, videoCallbacks):
            if stream is not None:
                stream.setFrameCallback(callback)
        for stream,callback in zip(self.audioStreams, audioCallbacks):
            if stream is not None:
                stream.setFrameCallback(callback)
        
        streams = self._streams
        
        for stream in streams:
            stream.enabled = stream.decodeBegin()
        
        try:
            # Iterate over all packets in the file and pass them to the
            # corresponding stream handler...
            for pkt in self.iterPackets():
                idx = pkt.stream_index
                stream = streams[idx]
                if stream is not None and stream.enabled:
                    stream.handlePacket(pkt)
        finally:
            for stream in streams:
                if stream.enabled:
                    stream.decodeEnd()

    def iterPackets(self):
        """Iterate over all raw packets in the file.
        
        Yields AVPacket objects with the current packet. Actually, it always
        yields the same object that just has a new packet in it, so it's not
        valid to store the packet for later use.
        """
        formatCtx = self._formatCtx
        if formatCtx is None:
            return

        pkt = decls.AVPacket()
        eof = False
        while not eof:
            # Read the next frame packet...
            try:
                eof = not avformat.av_read_frame(formatCtx, pkt)
                if not eof:
                    yield pkt
            finally:
                avformat.av_free_packet(pkt)

    @property
    def title(self):
        if self._formatCtx is None:
            return ""
        else:
            return self._formatCtx.title

    @property
    def author(self):
        if self._formatCtx is None:
            return ""
        else:
            return self._formatCtx.author

    @property
    def copyright(self):
        if self._formatCtx is None:
            return ""
        else:
            return self._formatCtx.copyright

    @property
    def album(self):
        if self._formatCtx is None:
            return ""
        else:
            return self._formatCtx.album

    @property
    def comment(self):
        if self._formatCtx is None:
            return ""
        else:
            return self._formatCtx.comment

    @property
    def year(self):
        if self._formatCtx is None:
            return 0
        else:
            return self._formatCtx.year

    @property
    def track(self):
        if self._formatCtx is None:
            return 0
        else:
            return self._formatCtx.track

    @property
    def genre(self):
        if self._formatCtx is None:
            return ""
        else:
            return self._formatCtx.genre



class VideoStream_Write_ffmpeg:
    def __init__(self, formatCtx, size, frameRate, pixelAspect):
        """Constructor.
        
        formatCtx is a AVFormatContext object.
        size is a tuple (width, height) containing the resolution of the
        video images.
        frameRate is the target framerate. It can be a single int or float
        or a tuple (num,den).
        pixelAspect is a float containing the pixel aspect ratio.
        """
        self._formatCtx = formatCtx
        self._size = size
        self._pixelAspect = pixelAspect
        
        try:
            # Check if frameRate is a 2-tuple
            num,den = frameRate
        except:
            # Turn the framerate into a rational...
            r = avutil.av_d2q(frameRate, 255)
            frameRate = (r.num, r.den)
        
        # The framerate as a tuple (num, den).
        self._frameRate = frameRate

        # Create an AVStream
        self._stream = self._createStream()
        
        # Get the codec context of the stream
        self._codecCtx = self._stream.codec.contents
        
        width,height = self._size
        # Set up the buffer that can store the encoded frame
        self._bufSize = 6*width*height+200
        self._buffer = ctypes.create_string_buffer(self._bufSize)

        self._frame = avcodec.avcodec_alloc_frame()
        if self._frame is None:
            raise MemoryError("Failed to allocate AVFrame object")
        avcodec.avpicture_alloc(self._frame, self._codecCtx.pix_fmt, width, height)

        # Allocate a picture for the converted image...
        self._picture = decls.AVPicture()
        avcodec.avpicture_alloc(self._picture, self._codecCtx.pix_fmt, width, height)
        # Get the size of the destination image buffer
        self._pictureSize = avcodec.avpicture_get_size(self._codecCtx.pix_fmt, width, height)
        
        self._pkt = decls.AVPacket()
        avformat.av_init_packet(self._pkt)
        #pkt.stream_index = outputstream.index
        
        self._currentPts = 0


    def close(self):
        pass
    
    def writeFrame(self, frame):
        buf = ctypes.addressof(self._buffer)
        self._frame.pts = self._currentPts
        self._currentPts += 1
        bytes = avcodec.avcodec_encode_video(self._codecCtx, buf, self._bufSize, self._frame)
#        print "pts", self._frame.pts
        print "bytes",bytes
        if bytes>0:
            self._pkt.data = ctypes.cast(self._buffer, ctypes.POINTER(ctypes.c_uint8))
            self._pkt.size = bytes
            self._pkt.pts = self._frame.pts
#            if self._codecCtx.coded_frame.contents.key_frame:
#                self._pkt.flags |= cppdefs.PKT_FLAG_KEY
                
            avformat.av_interleaved_write_frame(self._formatCtx, self._pkt)

    def _createStream(self):
        """Create the AVStream and open the codec.
        """
        
        # Allocate a new stream
        stream = avformat.av_new_stream(self._formatCtx, self._formatCtx.nb_streams)
        # Initialize it as a video stream
        avcodec.avcodec_get_context_defaults2(stream.codec.contents, decls.CODEC_TYPE_VIDEO)

        outputFormat = self._formatCtx.oformat.contents
        codecCtx = stream.codec.contents
        
        if outputFormat.flags & decls.AVFMT_GLOBALHEADER:
            stream.codec.contents.flags |= decls.CODEC_FLAG_GLOBAL_HEADER
        
        # Prepare the codec...
        codecId = avformat.av_guess_codec(outputFormat, decls.CODEC_TYPE_VIDEO, fileName=self._formatCtx.filename)
        if codecId is None:
            raise ValueError("Could not determine video codec to use for encoding the video.")
        codec = avcodec.avcodec_find_encoder(codecId)
        if codec is None:
            raise ValueError("Could not find encoder.")

        if codec.supported_framerates:
            print "mediafile: supported framerates available"
        else:
            print "mediafile: supported framerates not available"

        codecCtx.codec_id = codecId
        num,den = self._frameRate
        codecCtx.time_base.den = num
        codecCtx.time_base.num = den
        width,height = self._size
        codecCtx.width = width
        codecCtx.height = height
        codecCtx.sample_aspect_ratio = avutil.av_d2q(self._pixelAspect, 255)
        codecCtx.pix_fmt = decls.PIX_FMT_YUV420P
        stream.sample_aspect_ratio = codecCtx.sample_aspect_ratio
        
        # Check if the codec supports the pixel format (if not, switch the format)
        if codec.pix_fmts:
            i = 0
            while codec.pix_fmts[i]!=-1:
                if codecCtx.pix_fmt==codec.pix_fmts[i]:
                    break
                i += 1
            else:
                codecCtx.pix_fmt = codec.pix_fmts[0]
        
        # Open the codec
        avcodec.avcodec_open(codecCtx, codec)
        
        return stream
    

class Media_Write_ffmpeg(object):
    """Media file writer.
    """
    
    def __init__(self, fileName):
        object.__init__(self)
        
        self._formatCtx = None
        self._headerWritten = False
        
        # A list of VideoStream_Write_ffmpeg objects
        self._videoStreams = []
        
        # Create and initialize the AVFormatContext structure...
        self._formatCtx = self._createFormatContext(fileName)
        
        # Open the file
        status = avformat.url_fopen(self._formatCtx.pb, fileName, decls.URL_WRONLY)
        if status<0:
            self._freeFormatContext()
            raise MediaFileError('Could not write file "%s"'%fileName)

    def close(self):
        """Close the file.
        """
        if self._formatCtx is not None:
            for stream in self._videoStreams:
                stream.close()
            self._videoStreams = []

            if self._formatCtx.pb:
                if self._headerWritten:
                    avformat.av_write_trailer(self._formatCtx)
                avformat.url_fclose(self._formatCtx.pb)
            self._freeFormatContext()

    def createVideoStream(self, size, frameRate=30, pixelAspect=1.0):
        """Add a new video stream to the file.
        """
        try:
            stream = VideoStream_Write_ffmpeg(self._formatCtx,
                                              size=size,
                                              frameRate=frameRate,
                                              pixelAspect=pixelAspect)
            self._videoStreams.append(stream)
        except:
            self.close()
            raise

    def writeFrame(self, frame):
        if not self._headerWritten:
            self._writeHeader()
        
        self._videoStreams[0].writeFrame(frame)
    
    def _writeHeader(self):
        avformat.av_write_header(self._formatCtx)
        self._headerWritten = True
    
    def _createFormatContext(self, fileName):
        """Create a new AVFormatContext and initialize it.
        
        fileName is the name of the output file (this will determine the format
        of the file).
        Returns a AVFormatContext object.
        """
        # Determine the output format (AVOutputFormat object) from the file name...
        fmt = avformat.av_guess_format(fileName=fileName)
        if fmt is None:
            raise MediaFileError('Cannot determine output format for file "%s"'%fileName)
        
        # Create a new AVFormatContext struct
        formatCtx = avformat.avformat_alloc_context()
        
        # Initialize some fields...
        formatCtx.oformat = ctypes.pointer(fmt)
        formatCtx.filename = fileName
        formatCtx.timestamp = 0          # Where should this timestamp come from?

        mux_preload = 0.5
        mux_max_delay = 0.7
        formatCtx.preload = int(mux_preload*cppdefs.AV_TIME_BASE)
        formatCtx.max_delay= (int)(mux_max_delay*cppdefs.AV_TIME_BASE)
        formatCtx.loop_output = cppdefs.AVFMT_NOOUTPUTLOOP
        formatCtx.flags |= cppdefs.AVFMT_FLAG_NONBLOCK
        
        # Do we have to call av_set_parameters() here? (this is done in ffmpeg.c)
        
        return formatCtx
    
    def _freeFormatContext(self):
        """Free the internal AVFormatContext struct.
        """
        if self._formatCtx is not None:
            avutil.av_free(self._formatCtx)
            self._formatCtx = None

    def writeFrame__dummy(self):
        # Create a packet struct and initialize it
        pkt = AVPacket()
        avcodec.av_init_packet(pkt)
        #pkt.stream_index = outputstream.index
        
        #big_picture.pts= ost->sync_opts;
        
        # Encode the frame
        bytes = avcodec.avcodec_encode_video(codecCtx, buf, bufsize, picture)
        if bytes>0:
            pkt.data = buf
            pkt.size = bytes
#            pkt.pts = ...
            if codecCtx.coded_frame.key_frame:
                pkt.flags |= PKT_FLAG_KEY
                
            avformat.av_interleaved_write_frame(formatCtx, pkt)


######################################################################

_av_is_registered = False

def open(name, mode="r", **keyargs):
    """Open an audio/video file.

    *name* is the name of the media file to read or write. *mode* determines
    whether an existing file will be read or a new file will be created. Valid
    values are ``"r"`` for reading a file and ``"w"`` for writing a file.
     
    Returns a :class:`Media_Read` or :class:`Media_Write` object representing
    the open file.
    """
    global _av_is_registered
    if not _av_is_registered:
        avformat.av_register_all()
        _av_is_registered = True

    if mode=="r":
        return Media_Read_ffmpeg(name, **keyargs)
    elif mode=="w":
        return Media_Write_ffmpeg(name, **keyargs)
    else:
        raise ValueError("Unknown mode '%s' (must be 'r' or 'w')"%mode)
        
