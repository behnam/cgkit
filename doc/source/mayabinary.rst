
:mod:`mayabinary` --- Reading Maya Binary files
===============================================

.. module:: cgkit.mayabinary
   :synopsis: Reading Maya Binary files


This module contains the :class:`MBReader` class which can be used as a base
class for reading Maya Binary (\*.mb) files. The class parses the structure of
the file and invokes a callback method for every chunk found in the file. The
actual decoding of the chunk data has to be done in a derived class.

.. % ----------------------------------------------------------------


MBReader class
--------------

The :class:`MBReader` class reads Maya Binary files and calls appropriate
methods which have to be implemented in a derived class. A Maya Binary file is
composed of chunks that contain the actual data. There can be data chunks that
contain the actual data and group chunks that contain the data chunks.


.. class:: MBReader()

   Creates an instance of the reader.
   
   The class is derived from the :class:`~cgkit.mayaiff.IFFReader` class (defined in the
   :mod:`~cgkit.mayaiff` module). 

.. attribute:: MBReader.filename

   The file name (if it could be obtained). This may be used for generating warning
   or error messages.


.. method:: MBReader.read(file)

   Read the content of a file. *file* is either a file like object that can be used
   to read the content of the file or the name of a file.


.. method:: MBReader.abort()

   Aborts reading the current file. This method can be called in handler methods to
   abort reading the file.


.. method:: MBReader.onBeginGroup(chunk)

   Callback that is called whenever a new group tag begins. *chunk* is a
   :class:`~cgkit.mayaiff.GroupChunk` object containing information about the
   group chunk.


.. method:: MBReader.onEndGroup(chunk)

   Callback that is called whenever a group goes out of scope. *chunk* is a
   :class:`~cgkit.mayaiff.GroupChunk` object containing information
   about the group chunk (it is the same instance that was passed to
   :meth:`onBeginGroup`).


.. method:: MBReader.onDataChunk(chunk)

   Callback that is called for each data chunk. *chunk* is a :class:`~cgkit.mayaiff.Chunk` object
   that contains information about the chunk and that
   can be used to read the actual chunk data.

