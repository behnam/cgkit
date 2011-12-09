# Test the mediafile module

import unittest
from cgkit import mediafile
    

class TestMediaFile(unittest.TestCase):
    """Test the mediafile module.
    """
    
    def testRead(self):
        
        # Open the video file
        vid = mediafile.open("data/video1.mp4")
        
        self.assertEqual(0, vid.numAudioStreams())
        self.assertEqual(1, vid.numVideoStreams())
        stream = vid.videoStreams[0]
        self.assertEqual(320, stream.width)
        self.assertEqual(240, stream.height)
        
#        for i,frame in enumerate(vid.iterFrames()):
#            img = frame.pilImage()
#            img.save("frame%02d.png"%i)
        
        vid.close()

######################################################################

if __name__=="__main__":
    unittest.main()
