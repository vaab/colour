======
Colour
======

.. image:: https://pypip.in/v/colour/badge.png
    :target: https://pypi.python.org/pypi/colour

.. image:: https://secure.travis-ci.org/vaab/colour.png?branch=master
    :target: http://travis-ci.org/vaab/colour

Converts and manipulates common color representation (RGB, HSV, web, ...)


Feature
=======

  - Damn simple and pythonic way to manipulate color representation (see
    examples below)

  - Full conversion between RGB, HSV, 6-digit hex, 3-digit hex, human color

  - One object (``Color``) or bunch of single purpose function (``rgb2hex``,
    ``hsl2rgb`` ...)

  - ``web`` format that use the smallest representation between 6-digit,
    3-digit, fully spelled color, that is compatible with CSS or HTML color
    specifications.

  - smooth intuitive color scale generation choosing N color gradients.


Installation
============

You don't need to download the GIT version of the code as ``colour`` is
available on the PyPI. So you should be able to run::

    pip install colour


Usage
=====

To get complete demo of each function, please read the source code which is
heavily documented and provide a lot of examples in doctest format.

Here is a reduced sample of a common usage scenario:


Instanciation
-------------

Let's create blue color:

    >>> from colour import Color
    >>> c = Color("blue")
    >>> c
    <Color blue>

Please note that all these are equivalent examples to create the red color::

    Color("red")           ## human, web compatible representation
    Color(red=1)           ## default amount of blue and green is 0.0
    Color("blue", hue=0)   ## hue of blue is 0.66, hue of red is 0.0
    Color("#f00")          ## standard 3 hex digit web compatible representation
    Color("#ff0000")       ## standrad 6 hex digit web compatible representation
    Color(hue=0, saturation=1, luminance=0.5)
    Color(hsl=(0, 1, 0.5)) ## full 3-uple HSL specification
    Color(rgb=(1, 0, 0))   ## full 3-uple RGB specification
    Color(Color("red"))    ## recursion doesn't break object


Reading values
--------------

Several representation are accessible:

    >>> c.hex
    '#00f'
    >>> c.hsl  # doctest: +ELLIPSIS
    (0.66..., 1.0, 0.5)
    >>> c.rgb
    (0.0, 0.0, 1.0)

And their different parts are also independantly accessible, as the different
amount of red, blue, green, of the RGB format:

    >>> c.red
    0.0
    >>> c.blue
    1.0
    >>> c.green
    0.0

Or the hue, saturation and luminance of the HSL representation.

    >>> c.hue  # doctest: +ELLIPSIS
    0.66...
    >>> c.saturation
    1.0
    >>> c.luminance
    0.5


Modifying color objects
-----------------------

All these property are read/write, so let's add some red to this color:

    >>> c.red = 1
    >>> c
    <Color magenta>

We might want to de-saturate this color:

    >>> c.saturation = 0.5
    >>> c
    <Color #bf40bf>

And of course, the string convertion will give the web representation which is
human, or 3-digit, or 6-digit hex representation depending which is usable::

    >>> print "%s" % c
    #bf40bf

    >>> c.luminance = 1
    >>> print "%s" % c
    white


Ranges of colors
----------------

You can get some color scale of variation between two Color objects quite
easily. Here, is the color scale of the rainbow between red and blue:

    >>> red = Color("red")
    >>> blue = Color("blue")
    >>> list(red.range_to(blue, 5))
    [<Color red>, <Color yellow>, <Color green>, <Color cyan>, <Color blue>]

Or the different amount of gray between black and white:

    >>> black = Color("black")
    >>> white = Color("white")
    >>> list(black.range_to(white, 6))
    [<Color black>, <Color #333>, <Color #666>, <Color #999>, <Color #ccc>, <Color white>]


If you have to create graphical representation with color scale between red and green:

    >>> green = Color("green")
    >>> list(red.range_to(green, 5))
    [<Color red>, <Color #ff7f00>, <Color yellow>, <Color chartreuse>, <Color green>]

Notice how naturally, the yellow is displayed in human format and in the middle
of the scale. And that the quite unusual (but compatible) 'chartreuse' color
specification has been used in place of the hexadecimal representation.


Building arbitrary color from an input string
---------------------------------------------

Sometimes, you just want to get a color to colorize *something*. If you can turn
this something into a string, then you can use the ``from_string`` function from
the module, which will give you a color which will stay the same if the input
string stays the same::

    >>> from colour import from_string
    >>> from_string("Something")
    <Color ...>
    >>> from_string("Something") == from_string("Something")
    True

Astring is really just a string, so you can use the ``str()`` function for
example to turn any object into a string to be fed to the function, and it will
work (as long as ``str()`` does its job)::

    >>> o = object()
    >>> from_string(str(o)) == from_string(str(o))
    True

Of course, although there's a tiny probability that different strings yield the
same color, most of the time, different inputs will produce different colors::

    >>> from_string("a") != from_string("b")
    True
