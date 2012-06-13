# Test the mediafile module

import unittest
import fractions
import numpy
from cgkit import mediafile

import Image

class TestMediaFile(unittest.TestCase):
    """Test the mediafile module.
    """

    def testNumpyFrames(self):
        """Test reading video frames into numpy buffers.
        """
        # Test color access SEPARATE_CHANNELS and all combinations of pixel formats
        # and pixel accesses...
        for pixFmt in [mediafile.RGB, mediafile.BGR, mediafile.RGBA, mediafile.ARGB,
                       mediafile.BGRA, mediafile.ABGR, mediafile.GRAY]:
            for pixAccess in [mediafile.WIDTH_HEIGHT, mediafile.HEIGHT_WIDTH]:
                self._testNumpyFrames(pixelFormat=pixFmt, pixelAccess=pixAccess)

        # Test color access COMBINED_CHANNELS and all valid combinations of pixel formats
        # and pixel accesses...
        for pixFmt in [mediafile.RGBA, mediafile.ARGB, mediafile.BGRA, mediafile.ABGR, mediafile.GRAY]:
            for pixAccess in [mediafile.WIDTH_HEIGHT, mediafile.HEIGHT_WIDTH]:
                self._testNumpyFrames(pixelFormat=pixFmt, pixelAccess=pixAccess, colorAccess=mediafile.COMBINED_CHANNELS)
    
    def _testNumpyFrames(self, pixelFormat, pixelAccess, colorAccess=mediafile.SEPARATE_CHANNELS):
        """Test reading video frames into numpy buffers.
        """
        # Open the video file
        vid = mediafile.open("data/video1.mp4")

        # Determine the number of channels in the output buffer...
        if pixelFormat in [mediafile.RGB, mediafile.BGR]:
            numChannels = 3
        elif pixelFormat==mediafile.GRAY:
            numChannels = 1
        else:
            numChannels = 4
            
        # Initialize the swap flag
        swap = (pixelAccess==mediafile.HEIGHT_WIDTH)

        # Read the frames...
        numFrames = 0        
        for i,frame in enumerate(vid.iterData()):
            numFrames += 1
            
            # Get the numpy array containing the video frame...
            imgArr = frame.numpyArray(pixelFormat=pixelFormat, pixelAccess=pixelAccess, colorAccess=colorAccess)
            
            # Check the shape and dtype of the array...
            if swap:
                shape = (240,320,numChannels)
            else:
                shape = (320,240,numChannels)
            dtype = numpy.uint8
            if colorAccess==mediafile.COMBINED_CHANNELS:
                shape = (shape[0], shape[1])
                if numChannels==4:
                    dtype = numpy.uint32
                
            self.assertEqual(shape, imgArr.shape)
            self.assertEqual(dtype, imgArr.dtype)
            
            # Check the red block           
            self.assertColor((255,0,0), self.readPixel(imgArr, (5,5), swap, pixelFormat))
            # Check the green block
            self.assertColor((0,255,0), self.readPixel(imgArr, (160,5), swap, pixelFormat))
            # Check the blue block
            self.assertColor((0,0,255), self.readPixel(imgArr, (300,5), swap, pixelFormat))
            # Check the cyan block           
            self.assertColor((0,255,255), self.readPixel(imgArr, (5,15), swap, pixelFormat))
            # Check the magenta block
            self.assertColor((255,0,255), self.readPixel(imgArr, (160,15), swap, pixelFormat))
            # Check the yellow block
            self.assertColor((255,255,0), self.readPixel(imgArr, (300,15), swap, pixelFormat))
            # Check the white block
            self.assertColor((255,255,255), self.readPixel(imgArr, (160,25), swap, pixelFormat))
            
            # Check the moving pixels (to make sure we see the correct frame)
            x = 8+i*16
            self.assertColor((255,0,0), self.readPixel(imgArr, (x,40), swap, pixelFormat))
            self.assertColor((0,255,0), self.readPixel(imgArr, (x,50), swap, pixelFormat))
            self.assertColor((0,0,255), self.readPixel(imgArr, (x,60), swap, pixelFormat))
            if i>0:
                x -= 16
                self.assertColor((0,0,0), self.readPixel(imgArr, (x,40), swap, pixelFormat))
                self.assertColor((0,0,0), self.readPixel(imgArr, (x,50), swap, pixelFormat))
                self.assertColor((0,0,0), self.readPixel(imgArr, (x,60), swap, pixelFormat))
            
#            img = Image.fromarray(imgData)
            #img = frame.pilImage()
#            img.save("frame%02d.png"%i)
        
        # Check that we have seen all 20 frames
        self.assertEqual(20, numFrames)
        
        vid.close()
    
    def testVideoProperties(self):
        """Test reading a video file and examining its properties.
        """
        # Open the video file
        vid = mediafile.open("data/video1.mp4")
        
        self.assertEqual(0, vid.numAudioStreams())
        self.assertEqual(1, vid.numVideoStreams())
        stream = vid.videoStreams[0]
        self.assertEqual([], vid.audioStreams)
        self.assertEqual([stream], vid.videoStreams)
        
        self.assertEqual((320,240), stream.size)
        self.assertEqual(320, stream.width)
        self.assertEqual(240, stream.height)
        self.assertEqual(fractions.Fraction(25,1), stream.frameRate)

        vid.close()
    
    def readPixel(self, imgArr, pos, swap=False, pixFmt=mediafile.RGB):
        """Read a pixel from a numpy array.
        
        pos is the (x,y) coordinate of the pixel.
        If swap is True, the pixel is read from (y,x).
        The color is returned as (r,g,b) or (r,g,b,a) (it is rearranged
        based on pixFmt which is the format of the array).
        """
        if swap:
            col = imgArr[pos[1], pos[0]]
        else:
            col = imgArr[pos]

        # COMBINED_CHANNELS?
        if len(imgArr.shape)==2:
            if pixFmt==mediafile.GRAY:
                col = (col,)
            else:
                col = (col&0xff, (col>>8)&0xff, (col>>16)&0xff, col>>24)
        
        if pixFmt==mediafile.RGB or pixFmt==mediafile.RGBA:
            pass
        elif pixFmt==mediafile.BGR:
            col = (col[2], col[1], col[0])
        elif pixFmt==mediafile.ARGB:
            col = (col[1], col[2], col[3], col[0])
        elif pixFmt==mediafile.BGRA:
            col = (col[2], col[1], col[0], col[3])
        elif pixFmt==mediafile.ABGR:
            col = (col[3], col[2], col[1], col[0])
            
        return col
    
    def assertColor(self, expectedCol, col, tolerance=50):
        """Compare two color values.
        
        The colors are 3-tuples with components in the range from 0-255.
        tolerance is the maximum difference that is allowed to be considered
        equal (per channel).
        col may be a 4-tuple. The 4th component must then be 255 (the automatically
        generated alpha).
        """
        # Grayscale? Then convert expectedCol to grayscale (RGB) and expand the input color
        if len(col)==1:
            avg = int(0.3*expectedCol[0]+0.59*expectedCol[1]+0.11*expectedCol[2])
            expectedCol = (avg, avg, avg)
            col = (col[0], col[0], col[0])
            
        for i in range(3):
            if abs(expectedCol[i]-col[i])>tolerance:
                self.fail("Color mismatch: %s != %s (with a tolerance of %s)"%(expectedCol, col, tolerance))
        # Check alpha...
        if len(col)>3:
            self.assertEqual(255,col[3])
            

######################################################################

if __name__=="__main__":
    unittest.main()
