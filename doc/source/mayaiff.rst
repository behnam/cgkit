
:mod:`mayaiff` --- Reading Maya IFF files
=========================================

.. module:: cgkit.mayaiff
   :synopsis: Reading Maya IFF files


This module contains the :class:`IFFReader` class which can be used as a base
class for reading Maya IFF files. The class parses the structure of
the file and invokes a callback method for every chunk found in the file. The
actual decoding of the chunk data has to be done in a derived class.

.. % ----------------------------------------------------------------


IFFReader class
---------------

The :class:`IFFReader` class reads Maya IFF files and calls appropriate
methods which have to be implemented in a derived class. A Maya IFF file is
composed of chunks that contain the actual data. There can be data chunks that
contain the actual data and group chunks that contain the data chunks.


..  class:: IFFReader(iffType=None)

    Creates an instance of the reader.
    *iffType* may be a four-character string defining the type of IFF files
    the object is supposed to handle (it is the type of the first group chunk).
    If ``None`` is passed, any IFF file will be processed. For example, when set
    to ``"Maya"``, the :meth:`read()` method will raise an error if the input file
    is not a Maya binary file.

    ..  attribute:: filename

        The file name (if it could be obtained). This may be used for generating warning
        or error messages.


    ..  method:: read(file)
    
        Read the content of a file. *file* is either a file like object that can be used
        to read the content of the file or the name of a file.

    ..  method:: abort()
    
        Aborts reading the current file. This method can be called in handler methods to
        abort reading the file.

    ..  method:: onBeginGroup(chunk)
    
        Callback that is called whenever a new group tag begins. *chunk* is a
        :class:`GroupChunk` object containing information about the
        group chunk.

    ..  method:: onEndGroup(chunk)
    
        Callback that is called whenever a group goes out of scope. *chunk* is a
        :class:`GroupChunk` object containing information
        about the group chunk (it is the same instance that was passed to
        :meth:`onBeginGroup`).

    ..  method:: onDataChunk(chunk)
    
        Callback that is called for each data chunk. *chunk* is a :class:`Chunk` object
        that contains information about the chunk and that
        can be used to read the actual chunk data.

.. % ----------------------------------------------------------------


.. _chunkclass:

Chunk class
-----------

A :class:`Chunk` object is passed to the callback methods of the
:class:`MBReader` class. It contains information about the current chunk and it
can be used to read the actual chunk data. A :class:`Chunk` object has the
following attributes and methods:


.. class:: Chunk()


   .. attribute:: Chunk.tag

      This is a string containing four characters that represent the chunk name.


   .. attribute:: Chunk.size

      The size in bytes of the data part of the chunk.


   .. attribute:: Chunk.pos

      The absolute position of the data part within the input file.


   .. attribute:: Chunk.depth

      The depth of the chunk (i.e. how deep it is nested). The root has a depth of 0.


   .. attribute:: Chunk.parent

      The GroupChunk object of the parent chunk. In the case of the root group chunk
      this attribute is ``None``.


   .. method:: Chunk.chunkPath()

      Return a string containing the full path to this chunk. The result is a
      concatenation of all chunk names that lead to this chunk.


   .. method:: Chunk.read(bytes=-1)

      Read the specified number of bytes from the chunk. If bytes is -1 the entire
      chunk data is read. The return value is a string containing the binary data.

.. % ----------------------------------------------------------------


.. _groupchunkclass:

GroupChunk class
----------------

The :class:`GroupChunk` class is derived from the :class:`Chunk` class,
so it has the same attributes and methods. In
addition it defines one more attribute:


.. class:: GroupChunk()


   .. attribute:: GroupChunk.type

      This is a string containing four characters that represent the group type.

