# Test the ffmpeg module

import unittest
from cgkit.ffmpeg import avformat
from cgkit.ffmpeg import decls
    

class TestFfmpeg(unittest.TestCase):
    """Test the ffmpeg sub-package.
    """
    
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self._avInitialized = False
    
    def setUp(self):
        # Initialize ffmpeg once
        if not self._avInitialized:
            avformat.av_register_all()
            self._avInitialized = True
    
    def testAvFormat(self):
        """avformat test: Reading a video file.
        """

#        print ("AvFormat lib version: %s"%(avformat.avformat_version(),))
#        print (decls.LIBAVFORMAT_VERSION_MAJOR, decls.LIBAVFORMAT_VERSION_MINOR, decls.LIBAVFORMAT_VERSION_MICRO)
        
        # Open the video file
        formatCtx = avformat.av_open_input_file("data/video1.mp4", None, 0, None)
        
        self.assertEqual(decls.AVFormatContext, type(formatCtx))
        self.assertEqual("data/video1.mp4", formatCtx.filename)
        self.assertEqual(1, formatCtx.nb_streams)
        
        # Fill the 'streams' fields...
        avformat.av_find_stream_info(formatCtx)

        self.assertEqual(0.8, float(formatCtx.duration)/decls.AV_TIME_BASE)  # 20 frames with a framerate of 25 -> 0.8s
        self.assertEqual(4787, formatCtx.file_size)
        
        # Get the video stream (there is only one stream)
        stream = formatCtx.streams[0].contents
        self.assertEqual(decls.AVStream, type(stream))
        self.assertEqual(20, stream.nb_frames)         # 20 frames
        self.assertEqual(1, stream.time_base.num)      # 1/25 seconds per time unit
        self.assertEqual(25, stream.time_base.den)
        self.assertEqual(20, stream.duration)          # 20 time units (frames)
        self.assertEqual(0, stream.start_time)
        self.assertEqual(25, stream.r_frame_rate.num)  # 25 frames per second
        self.assertEqual(1, stream.r_frame_rate.den)

        # Get the video codec        
        codec = stream.codec.contents
        self.assertEqual(decls.AVCodecContext, type(codec))
        self.assertEqual(decls.CODEC_TYPE_VIDEO, codec.codec_type)
        self.assertEqual(0x31637661, codec.codec_tag)  # "fvc1"
        self.assertEqual(320, codec.width)
        self.assertEqual(240, codec.height)
        self.assertEqual(decls.PIX_FMT_YUV420P, codec.pix_fmt)
        self.assertEqual(37740, codec.bit_rate)  # 37kb/s

        # Close the file again
        avformat.av_close_input_file(formatCtx)


######################################################################

if __name__=="__main__":
    unittest.main()
