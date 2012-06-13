
:mod:`mediafile` --- Read or write audio/video files
====================================================

.. module:: cgkit.mediafile
   :synopsis: Read or write audio/video files

This module can be used to read and write video or audio files. The module
uses the low-level :mod:`ffmpeg` module which requires the ffmpeg shared libraries
to be installed on the system. Those libraries are not shipped with cgkit.

..  autofunction:: cgkit.mediafile.open

Media_Read object
-----------------

..  class:: Media_Read

    An instance of this class is returned by the :func:`open()` function.
    The object is used for reading audio or video files. A file contains
    a number of streams whose properties can be accessed through the
    :class:`AudioStream` and :class:`VideoStream` objects. The actual
    stream data can be read in one of two ways, you can either iterate
    over the individual frames using :meth:`iterData()` or you can set
    a callback on the stream objects and then call :meth:`decode()` 
    which will read the file and call the appropriate callbacks.

    ..  attribute:: audioStreams

        A list of :class:`AudioStream` objects, one for every audio stream
        in the file.
  
    ..  attribute:: videoStreams
  
        A list of :class:`VideoStream` objects, one for every video stream
        in the file.
  
    ..  method:: close()
  
        Close the file and free up resources.

    ..  method:: numAudioStreams()
  
        Return the number of audio streams in the file.
     
    ..  method:: numVideoStreams()
  
        Return the number of video streams in the file.

    ..  method:: iterData(streams=None)
  
        Iterate over the data of the specified streams. *streams* is a
        sequence of Stream objects. If ``None`` is passed, the first
        video stream is selected.
        Depending on the type of stream, the method yields :class:`VideoData`
        or :class:`AudioData` objects.
  
    ..  method:: decode()
  
        Decode the stream data and pass it to the stream callbacks. You have
        to call :meth:`setDataCallback()` on any stream you are interested in.


Media_Write object
------------------

..  class:: Media_Write
  
    .. method:: close()
  
       Close the file and free up resources.

Audio Stream object
-------------------

..  class:: AudioStream

    This class stores the properties of one particular audio stream in a
    video or audio file.

    ..  method:: setDataCallback(callback)
    
        Set a callback that gets called with decoded data. *callback* must
        be a callable taking a data object as input. You can also pass
        ``None`` to remove any previously set callback.
    
    ..  method:: getDataCallback()
    
        Return the currently set data callback.
    
    ..  attribute:: index
    
        The index of the stream.
    
    ..  attribute:: codecName
    
        The (short) name of the codec.
        
    ..  attribute:: codecLongName
    
        The long name of the codec.

    ..  attribute:: fourCC
    
        The four-character code of the codec.
    
    ..  attribute:: bitRate
    
        The average bit rate (bits per second) as an integer.

    ..  attribute:: timeBase
    
        The fundamental time unit (in seconds) as a :class:`Fraction` object. 
        Time stamps and the duration are given in these units.
    
    ..  attribute:: duration
    
        An integer containing the duration of the video stream in :attr:`timeBase`
        units.
    
    ..  attribute:: numChannels
    
        The number of audio channels in the stream.
    
    ..  attribute:: sampleRate
    
        The sample rate (samples per second) as an integer.
        

Video Stream object
-------------------

..  class:: VideoStream

    This class stores the properties of one particular video stream in a
    video file.

    ..  method:: setDataCallback(callback)
    
        Set a callback that gets called with decoded data. *callback* must
        be a callable taking a data object as input. You can also pass
        ``None`` to remove any previously set callback.
    
    ..  method:: getDataCallback()
    
        Return the currently set data callback.

    ..  attribute:: index
    
        The index of the stream.

    ..  attribute:: codecName
    
        The (short) name of the codec.
        
    ..  attribute:: codecLongName
    
        The long name of the codec.

    ..  attribute:: fourCC
    
        The four-character code of the codec.
    
    ..  attribute:: bitRate
    
        The average bit rate (bits per second) as an integer.

    ..  attribute:: timeBase
    
        The fundamental time unit (in seconds) as a :class:`Fraction` object. 
        Time stamps and the duration are given in these units.
    
    ..  attribute:: duration
    
        An integer containing the duration of the video stream in :attr:`timeBase`
        units.

    ..  attribute:: size
    
        A tuple (*width*, *height*) containing the size of a video frame in pixels.
    
    ..  attribute:: width
  
        The width of a video frame in pixels.
    
    ..  attribute:: height
    
        The height of a video frame in pixels.

    ..  attribute:: frameRate
    
        The frame rate (frames per second) as a :class:`Fraction` object. 
        
    ..  attribute:: numFrames
    
        The total number of frames or ``None`` if the number of frames is not
        known.
    
    ..  attribute:: pixelAspect
    
        The pixel aspect ratio as a :class:`Fraction` object or ``None`` if
        the aspect ratio is not known.

VideoData
---------

..  class:: VideoData

    An object of this class is used to access a decoded video frame.

    ..  attribute:: stream
    
        The parent :class:`VideoStream` object.
    
    ..  attribute:: pts
    
        ...
        
    ..  attribute:: size
    
        A tuple (*width*, *height*) specifying the resolution of the video frame.

    ..  method:: isKeyFrame()

        Check whether the current frame is a key frame or not.

    ..  method:: numpyArray(pixelFormat=RGB, pixelAccess=WIDTH_HEIGHT, colorAccess=SEPARATE_CHANNELS)
    
        Returns a :mod:`numpy` array containing the video frame.
        
        *pixelFormat* specifies the number and order of the channels in the
        returned buffer. The source video frames are converted into the
        specified format. Valid formats are: ``RGB``, ``BGR``, ``RGBA``, ``ARGB``,
        ``BGRA``, ``ABGR``, ``GRAY``.
        
        *pixelAccess* defines the order of the x,y indices when accessing
        a pixel in the returned buffer. The value can either be ``WIDTH_HEIGHT``
        to specify the pixel position as (x,y) or ``HEIGHT_WIDTH`` if (y,x)
        is required. If you pass the array on to other modules, you have to
        pick the order that those other modules expect. For example, if you
        want to convert the array into a PIL image using PIL's :meth:`fromarray()`
        method, you have to pick ``HEIGHT_WIDTH``, otherwise the width and height
        of the PIL image will be swapped. However, if you want to blit the
        image onto a :mod:`pygame` surface, the order must be ``WIDTH_HEIGHT``.
        
        *colorAccess* specifies whether the color channels should be accessed
        as a third index (``SEPARATE_CHANNELS``) or if the entire pixel should
        be stored as a single 8bit or 32bit integer value (``COMBINED_CHANNELS``).
        The latter is only allowed if the pixel format contains 1 or 4 channels.
        
        Note that the *pixelAccess* and *colorAccess* parameters do not affect
        the underlying memory layout of the buffer, they only affect the shape
        and strides of the returned array. This changes the way
        that individual pixels are accessed via the :mod:`numpy` array.
        The memory layout is always so that rows are stored one after another
        without any gaps and the channel values of an individual pixel are
        always stored next to each other.  
        
        The underlying numpy array is reused for every frame, so if you need
        to keep the array you have to copy it.
            
    ..  method:: pilImage()

        Returns a PIL image containing the video frame. 


AudioData
---------

..  class:: AudioData

    An object of this class is used to access decoded audio data.

    ..  attribute:: stream
    
        The parent :class:`AudioStream` object.
    
    ..  attribute:: pts
    
        ...
        
    ..  attribute:: channels
    
        The number of audio channels in the stream.
    
    ..  attribute:: framerate
    
        The frame rate in Hz.
    
    ..  attribute:: samples
    
    ..  attribute:: sampleSize
    
    
  
Examples
--------

In the following example, a video file is opened, the number of video streams
is examined and all the frames are extracted as numpy arrays. The numpy array
uses the default format and shape.

    >>> from cgkit import mediafile
    >>> vid = mediafile.open("MVI_0001.MOV")
    >>> vid.numVideoStreams()
    1
    >>> for data in vid.iterData():
    ...     # Get the current video frame as a numpy array. If necessary,
    ...     # pass input parameters to specify format and shape of the array.
    ...     arr = data.numpyArray()
    ...     print (arr.shape)
    ...
    (1280, 720, 3)
    (1280, 720, 3)
    ...
    >>> vid.close()

In the above example, we had to close the file manually in order to prevent
memory leaks. Just as a regular Python file, a media file object can also
be used inside a with statement. The file is then automatically closed,
even in the error case. Another variation of the above example is that
the numpy array is created so that the Y component is the first index.

    >>> with mediafile.open("MVI_0001.MOV") as vid:
    ...     for data in vid.iterData():
    ...         arr = data.numpyArray(pixelAccess=mediafile.HEIGHT_WIDTH)
    ...         print (arr.shape)
    ... 
    (720, 1280, 3)
    (720, 1280, 3)
    ...

    