
:mod:`mediafile` --- Read or write audio/video files
====================================================

.. module:: cgkit.mediafile
   :synopsis: Read or write audio/video files

..  autofunction:: cgkit.mediafile.open

Media_Read objects
------------------

..  class:: Media_Read

  .. attribute:: audioStreams
  
  .. attribute:: videoStreams
  
  .. method:: close()
  
     Close the file and free up resources.

  .. method:: numAudioStreams()
  
     Return the number of audio streams in the file.
     
  .. method:: numVideoStreams()
  
     Return the number of video streams in the file.

  .. method:: iterFrames()
  
     Iterate over the frames of the first video stream.

Media_Write objects
-------------------

..  class:: Media_Write
  
  .. method:: close()
  
     Close the file and free up resources.




