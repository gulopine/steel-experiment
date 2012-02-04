File Formats Made Easy
======================

Steel is a framework for specifying the format of binary data structures, such
as files. It allows you to define a structure using a standard Python class,
much like features found in Django and Elixir. Steel can provide the basis for:

 * metadata extraction,
 * format conversion,
 * data import and export,
 * compatibility layers

or anything else that relies on data stored in a binary format.

Requirements
------------

Python 3. Yup, Python 3. Many of its features make it simply unreasonable to try
to support Python 2 as well.

Defining a structure
--------------------

To get an idea of how it works, start with a simple example to get the width and
height of a PNG image. The `PNG specification`_ looks fairly complex, but for
just getting the width and height, it gets pretty simple::

    class PNG(steel.Structure):
        signature = steel.FixedString(b'\x89PNG\x0d\x0a\x1a\x0a')
        ihdr_size = steel.Integer(size=4)
        ihdr_id = steel.FixedString(b'IHDR')
        width = steel.Integer(size=4)
        height = steel.Integer(size=4)

And with that, you have enough to be able to get some simple attributes out of
any valid PNG file you run across. There's a whole more to these files, of
course, but for this basic operation you don't need to deal with the rest of it.

Parsing a file
--------------

Defining a structure in Python is a handy way to document a file format, but the
real job is to parse actual files with it and get useful data out of them. By
passing in a file or file-like object to the ``PNG`` class, you get an instance
that can easily access specific data within the file::

    >>> from urllib.request import urlopen
    >>> file = urlopen('http://importsteel.org/examples/steel.png')
    >>> data = PNG(file)
    >>> data.width, data.height
    (32, 32)

Attribute access is lazy, which means that Steel won't read any of the file
until you try to access an attribute. Once you do, it'll read only as much of
the file as it needs to bring you the data you asked for. This makes it a lot
faster when parsing just the beginning of the file, while also reducing memory
because it doesn't have to keep track of attributes you haven't asked for.

Referencing other fields
------------------------

Sometimes, the very definition of a field relies on the value of another field.
For example, you might have a block of data that can vary in size from file to
file. The size of such a block will typically be stored in the file before the
block itself, so you'll need to refer to that size field when defining the data
field.

Keeping with the PNG theme, the ``ihdr_size`` referenced earlier is actually the
size of the entire ``IHDR`` chunk. One way to start down the road of "properly"
parsing of the PNG format is to grab data chunk by chunk, using the lengths to
determine how much data to read for each chunk. To do this, you can actually
use the length field itself directly as the size of the data for the chunk::

    class PNG(steel.Structure):
        signature = steel.FixedString(b'\x89PNG\x0d\x0a\x1a\x0a')
        ihdr_size = steel.Integer(size=4)
        ihdr_id = steel.FixedString(b'IHDR')
        ihdr_data = steel.Integer(size=ihdr_size)

Now you can get at the data just like the width and height from earlier::

    >>> file = urlopen('http://importsteel.org/examples/steel.png')
    >>> data = PNG(file)
    >>> data.ihdr_size
    13
    >>> len(data.ihdr_data)
    13

Parsing bytes
-------------

Of course, that data is now just raw bytes. You can still get to the width and
height, but you'll have to parse these bytes using the format of the ``IHDR``
block, but like before, you only need to parse part of it::

    class Header(steel.Structure):
        width = steel.Integer(size=4)
        height = steel.Integer(size=4)

And to pass the bytes into this new structure, you'll need to wrap them in
something that acts like a file::

    >>> import io
    >>> file = io.BytesIO(data.ihdr_data)
    >>> ihdr = Header(file)
    >>> ihdr.width, ihdr.height
    (32, 32)

Parsing chunks
--------------

So far, we've been dealing with PNG data solely as a sequence of fields, but
there's actually a bit more structure at work. PNG is a chunked format, which
means that -- aside from the first 8 bytes -- all the data in the file is stored
in a series of individual chunks. This allows a program to read the chunks it
understands, while still providing a way to skip chunks it doesn't know about.

This allows new features to be added to the format without impacting existing
programs. It's sort of like XML for binary data, but Steel makes it much less
annoying to work with. In general, it works by requiring some very basic things
from every chunk, regardless of what it contains::

     * an ID, which indicates what kind of data is in the chunk
     * the size of the chunk's data
     * the data itself

Every chunk must contain at least these three things in order to work properly,
though the data block may be empty if the size is zero. PNG also includes a
Cyclic Redundancy Check for each chunk to help detect any errors in transit, but
Steel can still work with that just fine. So the first step is to describe the
structure of a general chunk::

    from steel import chunks, integrity

    class Chunk(chunks.Chunk):
        size = steel.Integer(size=4)
        id = steel.Bytes(size=4)
        payload = chunks.Payload(size=size)
        crc = integrity.CRC32(size=4, first=id)

This just defines what it means to be a chunk in PNG. To define the ``IHDR``
chunk itself, you can reuse the structure from earlier but with one change::

    @Chunk('IHDR')
    class Header(steel.Structure):
        width = steel.Integer(size=4)
        height = steel.Integer(size=4)

Even though this class doesn't define all the fields in the ``IHDR`` chunk,
Steel knows the size of the chunk and will just skip the data that's not
accounted for by fields. That's another example of the extensibility of chunks.
Even if a known chunk grows extra data in a new version of the format, existing
software can still read what it knows about and ignore the rest.

Referencing other structures
----------------------------

The simplest way to use this new chunk is to reference it directly within the
PNG class itself. You can do this using the ``Reference`` field::

    class PNG(steel.Structure):
        signature = steel.FixedString(b'\x89PNG\x0d\x0a\x1a\x0a')
        header = steel.Reference(Header)

This will actually work with any Steel structure; the chunk used here is just
one example. When populating this reference, the attribute will contain the same
object as if you had instantiated ``Header`` directly, just like you did earlier
with the ``BytesIO`` approach. The difference is that it's handled automatically
for you::

    >>> file = urlopen('http://importsteel.org/examples/steel.png')
    >>> data = PNG(file)
    >>> data.header.width, data.header.height
    (32, 32)

.. _`PNG specification`: http://www.w3.org/TR/PNG/
