# -*- coding: utf-8 -*-
"""Color Library

.. :doctest:

This module defines several color formats that can be converted to one or
another.

Formats
-------

HSL:
    3-uple of Hue, Saturation, Value all between 0.0 and 1.0

RGB:
    3-uple of Red, Green, Blue all between 0.0 and 1.0

HEX:
    string object beginning with '#' and with red, green, blue value.
    This format accept color in 3 or 6 value ex: '#fff' or '#ffffff'

WEB:
    string object that defaults to HEX representation or human if possible

Usage
-----

Several function exists to convert from one format to another. But all
function are not written. So the best way is to use the object Color.

Please see the documentation of this object for more information.

.. note:: Some constants are defined for convenience in HSL, RGB, HEX

"""

from __future__ import with_statement, print_function

import os.path
import re

##
## Some Constants
##

## Soften inequalities and some rounding issue based on float
FLOAT_ERROR = 0.0000005

RGB_FILE = os.path.join(os.path.dirname(__file__), 'rgb.txt')

LONG_HEX_COLOR = re.compile(r'^#[0-9a-fA-F]{6}$')
SHORT_HEX_COLOR = re.compile(r'^#[0-9a-fA-F]{3}$')


class HSL:
    BLACK = (0.0  , 0.0, 0.0)
    WHITE = (0.0  , 0.0, 1.0)
    RED   = (0.0  , 1.0, 0.5)
    GREEN = (1.0/3, 1.0, 0.5)
    BLUE  = (2.0/3, 1.0, 0.5)
    GRAY  = (0.0  , 0.0, 0.5)


class C_RGB:
    """RGB colors container

    Provides a quick color access.

    >>> from colour import RGB

    >>> RGB.WHITE
    (1.0, 1.0, 1.0)
    >>> RGB.BLUE
    (0.0, 0.0, 1.0)

    >>> RGB.DONOTEXISTS  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: ... has no attribute 'DONOTEXISTS'

    """

    def __getattr__(self, value):
        return hsl2rgb(getattr(HSL, value))


class C_HEX:
    """RGB colors container

    Provides a quick color access.

    >>> from colour import HEX

    >>> HEX.WHITE
    '#fff'
    >>> HEX.BLUE
    '#00f'

    >>> HEX.DONOTEXISTS  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: ... has no attribute 'DONOTEXISTS'

    """

    def __getattr__(self, value):
        return rgb2hex(getattr(RGB, value))

RGB = C_RGB()
HEX = C_HEX()


##
## Convertion function
##


def hsl2rgb(hsl):
    """Convert HSL representation towards RGB

    :param h: Hue, position around the chromatic circle (h=1 equiv h=0)
    :param s: Saturation, color saturation (0=full gray, 1=full color)
    :param l: Ligthness, Overhaul lightness (0=full black, 1=full white)
    :rtype: 3-uple for RGB values in float between 0 and 1

    Hue, Saturation, Range from Lightness is a float between 0 and 1

    Note that Hue can be set to any value but as it is a rotation
    around the chromatic circle, any value above 1 or below 0 can
    be expressed by a value between 0 and 1 (Note that h=0 is equiv
    to h=1).

    This algorithm came from:
    http://www.easyrgb.com/index.php?X=MATH&H=19#text19

    Here are some quick notion of HSL to RGB convertion:

    >>> from colour import hsl2rgb

    With a lightness put at 0, RGB is always rgbblack

    >>> hsl2rgb((0.0, 0.0, 0.0))
    (0.0, 0.0, 0.0)
    >>> hsl2rgb((0.5, 0.0, 0.0))
    (0.0, 0.0, 0.0)
    >>> hsl2rgb((0.5, 0.5, 0.0))
    (0.0, 0.0, 0.0)

    Same for lightness put at 1, RGB is always rgbwhite

    >>> hsl2rgb((0.0, 0.0, 1.0))
    (1.0, 1.0, 1.0)
    >>> hsl2rgb((0.5, 0.0, 1.0))
    (1.0, 1.0, 1.0)
    >>> hsl2rgb((0.5, 0.5, 1.0))
    (1.0, 1.0, 1.0)

    With saturation put at 0, the RGB should be equal to Lightness:

    >>> hsl2rgb((0.0, 0.0, 0.25))
    (0.25, 0.25, 0.25)
    >>> hsl2rgb((0.5, 0.0, 0.5))
    (0.5, 0.5, 0.5)
    >>> hsl2rgb((0.5, 0.0, 0.75))
    (0.75, 0.75, 0.75)

    With saturation put at 1, and lightness put to 0.5, we can find
    normal full red, green, blue colors:

    >>> hsl2rgb((0 , 1.0, 0.5))
    (1.0, 0.0, 0.0)
    >>> hsl2rgb((1 , 1.0, 0.5))
    (1.0, 0.0, 0.0)
    >>> hsl2rgb((1.0/3 , 1.0, 0.5))
    (0.0, 1.0, 0.0)
    >>> hsl2rgb((2.0/3 , 1.0, 0.5))
    (0.0, 0.0, 1.0)

    Of course:
    >>> hsl2rgb((0.0, 2.0, 0.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Saturation must be between 0 and 1.

    And:
    >>> hsl2rgb((0.0, 0.0, 1.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Lightness must be between 0 and 1.

    """
    h, s, l = [float(v) for v in hsl]

    if not (0.0 - FLOAT_ERROR <= s <= 1.0 + FLOAT_ERROR):
        raise ValueError("Saturation must be between 0 and 1.")
    if not (0.0 - FLOAT_ERROR <= l <= 1.0 + FLOAT_ERROR):
        raise ValueError("Lightness must be between 0 and 1.")

    if s == 0:
        return l, l, l

    if l < 0.5:
        v2 = l * (1.0 + s)
    else:
        v2 = (l + s) - (s * l)

    v1 = 2.0 * l - v2

    r = _hue2rgb(v1, v2, h + (1.0 / 3))
    g = _hue2rgb(v1, v2, h          )
    b = _hue2rgb(v1, v2, h - (1.0 / 3))

    return r, g, b


def rgb2hsl(rgb):
    """Convert RGB representation towards HSL

    :param r: Red amount (float between 0 and 1)
    :param g: Green amount (float between 0 and 1)
    :param b: Blue amount (float between 0 and 1)
    :rtype: 3-uple for HSL values in float between 0 and 1

    This algorithm came from:
    http://www.easyrgb.com/index.php?X=MATH&H=19#text19

    Here are some quick notion of RGB to HSL convertion:

    >>> from colour import rgb2hsl

    Note that if red amount is equal to green and blue, then you
    should have a gray value (from black to white).


    >>> rgb2hsl((1.0, 1.0, 1.0))  # doctest: +ELLIPSIS
    (..., 0.0, 1.0)
    >>> rgb2hsl((0.5, 0.5, 0.5))  # doctest: +ELLIPSIS
    (..., 0.0, 0.5)
    >>> rgb2hsl((0.0, 0.0, 0.0))  # doctest: +ELLIPSIS
    (..., 0.0, 0.0)

    If only one color is different from the others, it defines the
    direct Hue:

    >>> rgb2hsl((0.5, 0.5, 1.0))  # doctest: +ELLIPSIS
    (0.66..., 1.0, 0.75)
    >>> rgb2hsl((0.2, 0.1, 0.1))  # doctest: +ELLIPSIS
    (0.0, 0.33..., 0.15...)

    Having only one value set, you can check that:

    >>> rgb2hsl((1.0, 0.0, 0.0))
    (0.0, 1.0, 0.5)
    >>> rgb2hsl((0.0, 1.0, 0.0))  # doctest: +ELLIPSIS
    (0.33..., 1.0, 0.5)
    >>> rgb2hsl((0.0, 0.0, 1.0))  # doctest: +ELLIPSIS
    (0.66..., 1.0, 0.5)

    Of course:
    >>> rgb2hsl((0.0, 2.0, 0.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Green must be between 0 and 1. You provided 2.0.

    And:
    >>> rgb2hsl((0.0, 0.0, 1.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Blue must be between 0 and 1. You provided 1.5.

    """
    r, g, b = [float(v) for v in rgb]

    for name, v in {'Red': r, 'Green': g, 'Blue': b}.items():
        if not (0 - FLOAT_ERROR <= v <= 1 + FLOAT_ERROR):
            raise ValueError("%s must be between 0 and 1. You provided %r."
                             % (name, v))

    vmin = min(r, g, b) ## Min. value of RGB
    vmax = max(r, g, b) ## Max. value of RGB
    diff = vmax - vmin  ## Delta RGB value

    vsum = vmin + vmax

    l = vsum / 2

    if diff == 0.0: ## This is a gray, no chroma...
        return (0.0, 0.0, l)

    ##
    ## Chromatic data...
    ##

    ## Saturation
    if l < 0.5:
        s = diff / vsum
    else:
        s = diff / (2.0 - vsum)

    dr = (((vmax - r) / 6 ) + (diff / 2)) / diff
    dg = (((vmax - g) / 6 ) + (diff / 2)) / diff
    db = (((vmax - b) / 6 ) + (diff / 2)) / diff

    if r == vmax:
        h = db - dg
    elif g == vmax:
        h = (1.0/3) + dr - db
    elif b == vmax:
        h = (2.0/3) + dg - dr

    if h < 0: h += 1
    if h > 1: h -= 1

    return (h, s, l)


def _hue2rgb(v1, v2, vH):
    """Private helper function (Do not call directly)

    :param vH: rotation around the chromatic circle (between 0..1)

    """

    while vH < 0: vH += 1
    while vH > 1: vH -= 1

    if 6 * vH < 1: return v1 + (v2 - v1) * 6 * vH
    if 2 * vH < 1: return v2
    if 3 * vH < 2: return v1 + (v2 - v1) * ((2.0 / 3) - vH) * 6

    return v1


def rgb2hex(rgb, force_long=False):
    """Transform RGB tuple to hex RGB representation

    :param rgb: RGB 3-uple of float between 0 and 1
    :rtype: 3 hex char or 6 hex char string representation

    Usage
    -----

    >>> from colour import rgb2hex

    >>> rgb2hex((0.0,1.0,0.0))
    '#0f0'

    Rounding try to be as natural as possible:

    >>> rgb2hex((0.0,0.999999,1.0))
    '#0ff'

    And if not possible, the 6 hex char representation is used:

    >>> rgb2hex((0.23,1.0,1.0))
    '#3bffff'

    >>> rgb2hex((0.0,0.999999,1.0), force_long=True)
    '#00ffff'

    """

    hx = '#' + ''.join(["%02x" % int(c*255 + 0.5 - FLOAT_ERROR) for c in rgb])

    if force_long == False and \
        hx[1] == hx[2] and \
        hx[3] == hx[4] and \
        hx[5] == hx[6]:
        return '#' + hx[1] + hx[3] + hx[5]

    return hx


def hex2rgb(str_rgb):
    """Transform hex RGB representation to RGB tuple

    :param rgb: 3 hex char or 6 hex char string representation
    :rtype: RGB 3-uple of float between 0 and 1

    >>> from colour import hex2rgb

    >>> hex2rgb('#00ff00')
    (0.0, 1.0, 0.0)

    >>> hex2rgb('#0f0')
    (0.0, 1.0, 0.0)

    >>> hex2rgb('#aaa')  # doctest: +ELLIPSIS
    (0.66..., 0.66..., 0.66...)

    >>> hex2rgb('#aa')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Invalid value '#aa' provided for rgb color.

    """

    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color."
                         % str_rgb)

    return tuple([float(int(v, 16))/255 for v in (r, g, b)])


def hex2web(hex):
    """Converts HEX representation to WEB

    :param rgb: 3 hex char or 6 hex char string representation
    :rtype: web string representation (human readable if possible)

    WEB representation uses X11 rgb.txt to define convertion
    between RGB and english color names.

    Usage
    =====

    >>> from colour import hex2web

    >>> hex2web('#ff0000')
    'red'

    >>> hex2web('#aaaaaa')
    '#aaa'

    >>> hex2web('#abc')
    '#abc'

    >>> hex2web('#acacac')
    '#acacac'

    """
    dec_rgb = " ".join(["%3d" % int(v * 255) for v in hex2rgb(hex)])
    with open(RGB_FILE) as f:
        for line in f:
            if line.startswith(dec_rgb):
                return line[13:-1]

    # Hex format is verified by hex2rgb function. And should be 3 or 6 digit
    if len(hex) == 7:
        if hex[1] == hex[2] and \
           hex[3] == hex[4] and \
           hex[5] == hex[6]:
            return '#' + hex[1] + hex[3] + hex[5]
    return hex

def web2hex(web, force_long=False):
    """Converts WEB representation to HEX

    :param rgb: web string representation (human readable if possible)
    :rtype: 3 hex char or 6 hex char string representation

    WEB representation uses X11 rgb.txt to define convertion
    between RGB and english color names.

    Usage
    =====

    >>> from colour import web2hex

    >>> web2hex('red')
    '#f00'

    >>> web2hex('#aaa')
    '#aaa'

    >>> web2hex('#foo')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: '#foo' is not in web format. Need 3 or 6 hex digit.

    >>> web2hex('#aaa', force_long=True)
    '#aaaaaa'

    >>> web2hex('#aaaaaa')
    '#aaaaaa'

    >>> web2hex('#aaaa')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: '#aaaa' is not in web format. Need 3 or 6 hex digit.

    >>> web2hex('pinky')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: 'pinky' is not a recognized color.

    """
    if web.startswith('#'):
        if LONG_HEX_COLOR.match(web) or (
            SHORT_HEX_COLOR.match(web) and not force_long):
            return web.lower()
        elif SHORT_HEX_COLOR.match(web) and force_long:
            return '#' + ''.join([("%s" % (t,)) * 2 for t in web[1:]])
        raise AttributeError("%r is not in web format. Need 3 or 6 hex digit." % web)

    result = None
    with open(RGB_FILE) as f:
        for line in f:
            if line.endswith(web + '\n'):
                result = line[0:11]
                break

    if result == None:
        raise ValueError("%r is not a recognized color." % web)

    ## convert dec to hex:

    r, g, b = result[0:3], result[4:7], result[8:11]
    return rgb2hex([float(int(v))/255 for v in (r, g, b)], force_long)


def color_scale(begin_hsl, end_hsl, nb):
    """Returns a list of nb color HSL tuples between begin_hsl and end_hsl

    >>> from colour import color_scale

    >>> [rgb2hex(hsl2rgb(hsl)) for hsl in color_scale((0, 1, 0.5),
    ...                                               (1, 1, 0.5), 3)]
    ['#f00', '#0f0', '#00f', '#f00']

    >>> [rgb2hex(hsl2rgb(hsl)) for hsl in color_scale((0, 0, 0), (0, 0, 1), 15)]
    ['#000', '#111', '#222', '#333', '#444', '#555', '#666', '#777', '#888', '#999', '#aaa', '#bbb', '#ccc', '#ddd', '#eee', '#fff']

    """

    step = tuple([float(end_hsl[i] - begin_hsl[i])/nb for i in range(0, 3)])

    def mul(step, value):
        return tuple([v * value for v in step])

    def add_v(step, step2):
        return tuple([v + step2[i] for i, v in enumerate(step)])


    return [add_v(begin_hsl, mul(step, r)) for r in range(0, nb + 1)]

##
## All purpose object
##


class Color(object):
    """Abstraction of a color object

    Color object keeps information of a color. It can input/output to different
    format (HSL, RGB, HEX, WEB) and their partial representation.

        >>> from colour import Color, HSL

        >>> b = Color()
        >>> b.hsl = HSL.BLUE

    Access values
    -------------

        >>> b.hue  # doctest: +ELLIPSIS
        0.66...
        >>> b.saturation
        1.0
        >>> b.luminance
        0.5

        >>> b.red
        0.0
        >>> b.blue
        1.0
        >>> b.green
        0.0

        >>> b.rgb
        (0.0, 0.0, 1.0)
        >>> b.hsl  # doctest: +ELLIPSIS
        (0.66..., 1.0, 0.5)
        >>> b.hex
        '#00f'

    Change values
    -------------

    Let's change Hue toward red tint:

        >>> b.hue = 0.0
        >>> b.hex
        '#f00'

        >>> b.hue = 2.0/3
        >>> b.hex
        '#00f'

    In the other way round:

        >>> b.hex = '#f00'
        >>> b.hsl
        (0.0, 1.0, 0.5)

    Long hex can be accessed directly:

        >>> b.hex_l = '#123456'
        >>> b.hex_l
        '#123456'
        >>> b.hex
        '#123456'

        >>> b.hex_l = '#ff0000'
        >>> b.hex_l
        '#ff0000'
        >>> b.hex
        '#f00'

    Convenience
    -----------

        >>> c = Color('blue')
        >>> c
        <Color blue>
        >>> c.hue = 0
        >>> c
        <Color red>

        >>> c.saturation = 0.0
        >>> c.hsl  # doctest: +ELLIPSIS
        (..., 0.0, 0.5)
        >>> c.rgb
        (0.5, 0.5, 0.5)
        >>> c.hex
        '#7f7f7f'
        >>> c
        <Color #7f7f7f>

        >>> c.luminance = 0.0
        >>> c
        <Color black>

        >>> c.hex
        '#000'

        >>> c.green = 1.0
        >>> c.blue = 1.0
        >>> c.hex
        '#0ff'
        >>> c
        <Color cyan>

        >>> c = Color('blue', luminance=0.75)
        >>> c
        <Color #7f7fff>

        >>> c = Color('red', red=0.5)
        >>> c
        <Color #7f0000>

        >>> print(c)
        #7f0000

    You can try to query unexisting attributes:

        >>> c.lightness  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        AttributeError: 'lightness' not found

    TODO: could add HSV, CMYK, YUV conversion.

#     >>> b.hsv
#     >>> b.value
#     >>> b.cyan
#     >>> b.magenta
#     >>> b.yellow
#     >>> b.key
#     >>> b.cmyk


    Check recursive init
    --------------------

    To support blind convertion of web strings (or already converted object),
    the Color object supports instanciation with another Color object.

        >>> Color(Color(Color('red')))
        <Color red>

    """

    _hsl = None   ## internal representation

    def __init__(self, color=None, **kwargs):

        if isinstance(color, Color):
            self.web = color.web
        else:
            self.web = color if color else 'black'

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, label):
        if ('get_' + label) in self.__class__.__dict__:
            return getattr(self, 'get_' + label)()
        raise AttributeError("'%s' not found" % label)

    def __setattr__(self, label, value):
        if label != "_hsl":
            fc = getattr(self, 'set_' + label)
            fc(value)
        else:
            self.__dict__[label] = value

    ##
    ## Get
    ##

    def get_hsl(self):
        return tuple(self._hsl)

    def get_hex(self):
        return rgb2hex(self.rgb)

    def get_hex_l(self):
        return rgb2hex(self.rgb, force_long=True)

    def get_rgb(self):
        return hsl2rgb(self.hsl)

    def get_hue(self):
        return self.hsl[0]

    def get_saturation(self):
        return self.hsl[1]

    def get_luminance(self):
        return self.hsl[2]

    def get_red(self):
        return self.rgb[0]

    def get_green(self):
        return self.rgb[1]

    def get_blue(self):
        return self.rgb[2]

    def get_web(self):
        return hex2web(self.hex)


    ##
    ## Set
    ##

    def set_hsl(self, value):
        self._hsl = list(value)

    def set_rgb(self, value):
        self.hsl = rgb2hsl(value)

    def set_hue(self, value):
        self._hsl[0] = value

    def set_saturation(self, value):
        self._hsl[1] = value

    def set_luminance(self, value):
        self._hsl[2] = value

    def set_red(self, value):
        r, g, b = self.rgb
        r = value
        self.rgb = (r, g, b)

    def set_green(self, value):
        r, g, b = self.rgb
        g = value
        self.rgb = (r, g, b)

    def set_blue(self, value):
        r, g, b = self.rgb
        b = value
        self.rgb = (r, g, b)

    def set_hex(self, value):
        self.rgb = hex2rgb(value)

    set_hex_l = set_hex

    def set_web(self, value):
        self.hex = web2hex(value)

    ## range of color generation

    def range_to(self, value, steps):
        for hsl in color_scale(self._hsl, Color(value).hsl, steps - 1):
            yield Color(hsl=hsl)

    ##
    ## Convenience
    ##

    def __str__(self):
        return "%s" % self.web

    def __repr__(self):
        return "<Color %s>" % self.web

