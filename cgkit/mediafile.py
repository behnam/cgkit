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
from ffmpeg import avutil, swscale, avformat, avcodec
import ctypes


class ImageData:
    """Decoded image data.
    
    This class serves as a container for the data that is passed to the
    video callbacks.
    """
    def __init__(self, pts=None, size=None, data=None):
        # Presentation timestamp (float)
        self.pts =pts
        # Image size (width, height)
        self.size = size
        # Image data (str)
        self.data = data

class AudioData:
    def __init__(self, pts=None, channels=None, framerate=None, samples=None, sampleSize=None):
        self.pts = pts
        self.channels = channels
        self.framerate = framerate
        self.samples = samples
        self.sampleSize = sampleSize


class StreamBase_ffmpeg(object):
    """Base class for audio/video stream.
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
        print "CODEC",self._codec

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
        try:
            frameSize,bytesUsed = avcodec.avcodec_decode_audio2(codecCtx, self._sampleBuf, pkt.data, pkt.size)
        except avcodec.AVCodecError, exc:
            print "Error decoding audio frame:",exc
            raise
        
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
            self._picture = avcodec.AVPicture()
            width = self._codecCtx.width
            height = self._codecCtx.height
            avcodec.avpicture_alloc(self._picture, avutil.PIX_FMT_RGB24, width, height)
            # Get the size of the destination image buffer
            self._pictureSize = avcodec.avpicture_get_size(avutil.PIX_FMT_RGB24, width, height)
    
            # Allocate a SwsContext structure to convert the image
            self._swsCtx = swscale.sws_getContext(width, height, self._codecCtx.pix_fmt, 
                                                  width, height, avutil.PIX_FMT_RGB24, 1)
            
            tb = self._stream.time_base
            self._timebase = float(tb.num)/tb.den
            self._imageData = ImageData(size=(width, height))
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
        try:
            hasFrame,bytes = avcodec.avcodec_decode_video(codecCtx, self._frame, pkt.data, pkt.size)
        except avcodec.AVCodecError, exc:
            print "Error decoding video frame:",exc
            hasFrame = False

        if hasFrame:
            # Convert the image into RGB format
            frame = self._frame
            pic = self._picture
            print frame.linesize
            swscale.sws_scale(self._swsCtx, frame.data, frame.linesize, 0, codecCtx.height, pic.data, pic.linesize)
            # Obtain a Python string containing the raw image data
            data = ctypes.string_at(pic.data[0], self._pictureSize)
            print self._pictureSize
    
            #print "PTS:%s  DTS:%s  Duration:%s"%(pkt.pts, pkt.dts, pkt.duration)
            self._imageData.pts = pkt.dts*self._timebase
            self._imageData.data = data
            
            self._frameCallback(self._imageData)

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
            if codec.codec_type==avcodec.CODEC_TYPE_VIDEO:
                stream = VideoStream_ffmpeg(stream)
                self._streams.append(stream)
                self.videoStreams.append(stream)
            elif codec.codec_type==avcodec.CODEC_TYPE_AUDIO:
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

        pkt = avformat.AVPacket()
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

######################################################################

_av_is_registered = False

def open(name, mode="r", **keyargs):
    """Open an audio/video file.
    
    Returns a Media object representing the open file.
    """
    global _av_is_registered
    if not _av_is_registered:
        avformat.av_register_all()
        _av_is_registered = True

    if mode=="r":
        return Media_Read_ffmpeg(name, **keyargs)
    elif mode=="w":
        return None
#        return Media_Write_ffmpeg(name, **keyargs)
    else:
        raise ValueError("Unknown mode '%s' (must be 'r' or 'w')"%mode)
        
