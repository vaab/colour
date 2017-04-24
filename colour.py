# -*- coding: utf-8 -*-
"""Color Library

.. :doctest:

This module defines several color formats that can be converted to one or
another.

Usage
-----

Several function exists to convert from one format to another. But all
convertion function are not written from all format towards all formats.
By using Color object, you'll silently use all available function, sometime
chained, to give you a convertion from any format to any other.

Please see the documentation of this object for more information.

"""

from __future__ import with_statement, print_function

import collections
import hashlib
import re
import sys
import traceback
import inspect


##
## Convenience function
##

def with_metaclass(mcls):
    def decorator(cls):
        body = vars(cls).copy()
        # clean out class body
        body.pop('__dict__', None)
        body.pop('__weakref__', None)
        return mcls(cls.__name__, cls.__bases__, body)
    return decorator

##
## Some Constants
##

## Soften inequalities and some rounding issue based on float
FLOAT_ERROR = 0.0000005


RGB_TO_COLOR_NAMES = {
    (0, 0, 0): ['Black'],
    (0, 0, 128): ['Navy', 'NavyBlue'],
    (0, 0, 139): ['DarkBlue'],
    (0, 0, 205): ['MediumBlue'],
    (0, 0, 255): ['Blue'],
    (0, 100, 0): ['DarkGreen'],
    (0, 128, 0): ['Green'],
    (0, 139, 139): ['DarkCyan'],
    (0, 191, 255): ['DeepSkyBlue'],
    (0, 206, 209): ['DarkTurquoise'],
    (0, 250, 154): ['MediumSpringGreen'],
    (0, 255, 0): ['Lime'],
    (0, 255, 127): ['SpringGreen'],
    (0, 255, 255): ['Cyan', 'Aqua'],
    (25, 25, 112): ['MidnightBlue'],
    (30, 144, 255): ['DodgerBlue'],
    (32, 178, 170): ['LightSeaGreen'],
    (34, 139, 34): ['ForestGreen'],
    (46, 139, 87): ['SeaGreen'],
    (47, 79, 79): ['DarkSlateGray', 'DarkSlateGrey'],
    (50, 205, 50): ['LimeGreen'],
    (60, 179, 113): ['MediumSeaGreen'],
    (64, 224, 208): ['Turquoise'],
    (65, 105, 225): ['RoyalBlue'],
    (70, 130, 180): ['SteelBlue'],
    (72, 61, 139): ['DarkSlateBlue'],
    (72, 209, 204): ['MediumTurquoise'],
    (75, 0, 130): ['Indigo'],
    (85, 107, 47): ['DarkOliveGreen'],
    (95, 158, 160): ['CadetBlue'],
    (100, 149, 237): ['CornflowerBlue'],
    (102, 205, 170): ['MediumAquamarine'],
    (105, 105, 105): ['DimGray', 'DimGrey'],
    (106, 90, 205): ['SlateBlue'],
    (107, 142, 35): ['OliveDrab'],
    (112, 128, 144): ['SlateGray', 'SlateGrey'],
    (119, 136, 153): ['LightSlateGray', 'LightSlateGrey'],
    (123, 104, 238): ['MediumSlateBlue'],
    (124, 252, 0): ['LawnGreen'],
    (127, 255, 0): ['Chartreuse'],
    (127, 255, 212): ['Aquamarine'],
    (128, 0, 0): ['Maroon'],
    (128, 0, 128): ['Purple'],
    (128, 128, 0): ['Olive'],
    (128, 128, 128): ['Gray', 'Grey'],
    (132, 112, 255): ['LightSlateBlue'],
    (135, 206, 235): ['SkyBlue'],
    (135, 206, 250): ['LightSkyBlue'],
    (138, 43, 226): ['BlueViolet'],
    (139, 0, 0): ['DarkRed'],
    (139, 0, 139): ['DarkMagenta'],
    (139, 69, 19): ['SaddleBrown'],
    (143, 188, 143): ['DarkSeaGreen'],
    (144, 238, 144): ['LightGreen'],
    (147, 112, 219): ['MediumPurple'],
    (148, 0, 211): ['DarkViolet'],
    (152, 251, 152): ['PaleGreen'],
    (153, 50, 204): ['DarkOrchid'],
    (154, 205, 50): ['YellowGreen'],
    (160, 82, 45): ['Sienna'],
    (165, 42, 42): ['Brown'],
    (169, 169, 169): ['DarkGray', 'DarkGrey'],
    (173, 216, 230): ['LightBlue'],
    (173, 255, 47): ['GreenYellow'],
    (175, 238, 238): ['PaleTurquoise'],
    (176, 196, 222): ['LightSteelBlue'],
    (176, 224, 230): ['PowderBlue'],
    (178, 34, 34): ['Firebrick'],
    (184, 134, 11): ['DarkGoldenrod'],
    (186, 85, 211): ['MediumOrchid'],
    (188, 143, 143): ['RosyBrown'],
    (189, 183, 107): ['DarkKhaki'],
    (192, 192, 192): ['Silver'],
    (199, 21, 133): ['MediumVioletRed'],
    (205, 92, 92): ['IndianRed'],
    (205, 133, 63): ['Peru'],
    (208, 32, 144): ['VioletRed'],
    (210, 105, 30): ['Chocolate'],
    (210, 180, 140): ['Tan'],
    (211, 211, 211): ['LightGray', 'LightGrey'],
    (216, 191, 216): ['Thistle'],
    (218, 112, 214): ['Orchid'],
    (218, 165, 32): ['Goldenrod'],
    (219, 112, 147): ['PaleVioletRed'],
    (220, 20, 60): ['Crimson'],
    (220, 220, 220): ['Gainsboro'],
    (221, 160, 221): ['Plum'],
    (222, 184, 135): ['Burlywood'],
    (224, 255, 255): ['LightCyan'],
    (230, 230, 250): ['Lavender'],
    (233, 150, 122): ['DarkSalmon'],
    (238, 130, 238): ['Violet'],
    (238, 221, 130): ['LightGoldenrod'],
    (238, 232, 170): ['PaleGoldenrod'],
    (240, 128, 128): ['LightCoral'],
    (240, 230, 140): ['Khaki'],
    (240, 248, 255): ['AliceBlue'],
    (240, 255, 240): ['Honeydew'],
    (240, 255, 255): ['Azure'],
    (244, 164, 96): ['SandyBrown'],
    (245, 222, 179): ['Wheat'],
    (245, 245, 220): ['Beige'],
    (245, 245, 245): ['WhiteSmoke'],
    (245, 255, 250): ['MintCream'],
    (248, 248, 255): ['GhostWhite'],
    (250, 128, 114): ['Salmon'],
    (250, 235, 215): ['AntiqueWhite'],
    (250, 240, 230): ['Linen'],
    (250, 250, 210): ['LightGoldenrodYellow'],
    (253, 245, 230): ['OldLace'],
    (255, 0, 0): ['Red'],
    (255, 0, 255): ['Magenta', 'Fuchsia'],
    (255, 20, 147): ['DeepPink'],
    (255, 69, 0): ['OrangeRed'],
    (255, 99, 71): ['Tomato'],
    (255, 105, 180): ['HotPink'],
    (255, 127, 80): ['Coral'],
    (255, 140, 0): ['DarkOrange'],
    (255, 160, 122): ['LightSalmon'],
    (255, 165, 0): ['Orange'],
    (255, 182, 193): ['LightPink'],
    (255, 192, 203): ['Pink'],
    (255, 215, 0): ['Gold'],
    (255, 218, 185): ['PeachPuff'],
    (255, 222, 173): ['NavajoWhite'],
    (255, 228, 181): ['Moccasin'],
    (255, 228, 196): ['Bisque'],
    (255, 228, 225): ['MistyRose'],
    (255, 235, 205): ['BlanchedAlmond'],
    (255, 239, 213): ['PapayaWhip'],
    (255, 240, 245): ['LavenderBlush'],
    (255, 245, 238): ['Seashell'],
    (255, 248, 220): ['Cornsilk'],
    (255, 250, 205): ['LemonChiffon'],
    (255, 250, 240): ['FloralWhite'],
    (255, 250, 250): ['Snow'],
    (255, 255, 0): ['Yellow'],
    (255, 255, 224): ['LightYellow'],
    (255, 255, 240): ['Ivory'],
    (255, 255, 255): ['White']
}

## Building inverse relation
COLOR_NAME_TO_RGB = dict(
    (name.lower(), rgb)
    for rgb, names in RGB_TO_COLOR_NAMES.items()
    for name in names)


##
## Color Type Factory machinery
##


class FormatRegistry(list):

    def get(self, label, default=None):
        for f in self:
            if label == str(f):
                return f
        return default

    def find(self, label):
        f = self.get(label, None)
        if f is not None:
            return f, None
        return self.get_by_attr(label)

    def get_by_attr(self, label):
        if "_" in label:
            format, label = label.split("_", 1)
            f = self.get(format, None)
            formats = [] if f is None else [f]
        else:
            formats = list(self)
        ret = []
        for f in formats:
            for attr in getattr(f, "_fields", []):
                if label == attr:
                    ret.append(f)
        if len(ret) > 1:
            raise ValueError(
                "Ambiguous attribute %r. Try one of: %s"
                % (label, ", ".join("%s_%s" % (f, label) for f in ret)))
        elif len(ret) == 1:
            return ret[0], label
        else:  ## len(ret) == 0:
            return None, None


def register_format(registry):
    def wrap(f):
        registry.append(f)
        return f
    return wrap


class MetaFormat(type):

    def __getattr__(self, value):
        label = value.lower()
        if label in COLOR_NAME_TO_RGB:
            return RGB(
                tuple(v / 255. for v in COLOR_NAME_TO_RGB[label])
                ).convert(self)
        raise AttributeError("%s instance has no attribute %r"
                             % (self.__class__, value))

    def __repr__(self):
        return "<Format %s>" % (self.__name__, )

    def __str__(self):
        return self.__name__.lower()


@with_metaclass(MetaFormat)
class Format(object):

    def convert(self, dst_format, converter_registry=None):
        converter_registry = converter_registry or Converters
        src_format = type(self)
        ret = converter_registry.convert_fun(
            src_format, dst_format)(self)
        return ret


def Tuple(*a):
    """Create a simpler named tuple type, inheriting from ``Format``

    Usage
    -----

        >>> Tuple("a", "b", "c")
        <Format Tuple(a, b, c)>

    This can conveniently be used as a parent class for formats, with
    an easy declaration::

        >>> class MyFormat(Tuple("a", "b", "c")): pass

    .. sensible representation::

        >>> MyFormat(1, 2, 3)
        MyFormat(a=1, b=2, c=3)

    .. and the ability to take a real tuple upon initialisation::

        >>> MyFormat((1, 2, 3))
        MyFormat(a=1, b=2, c=3)

    .. keeping the awesome feature of namedtuples, a partial argument
    and keyword list::

        >>> MyFormat(1, b=2, c=3)
        MyFormat(a=1, b=2, c=3)

    Of course, these are subclasses of ``Format``::

        >>> isinstance(MyFormat((1, 2, 3)), Format)
        True

    """

    class klass(collections.namedtuple("_Anon", a), Format):
        ## Allow the support of instanciating with a single tuple.
        def __new__(cls, *a, **kw):
            if len(a) == 1 and isinstance(a[0], tuple) and \
                   len(a[0]) == len(cls._fields):
                return cls.__new__(cls, *a[0], **kw)
            return super(klass, cls).__new__(cls, *a, **kw)

        ## Force namedtuple to read the actual name of the class
        def __repr__(self):
            return ('%s(%s)'
                    % (self.__class__.__name__,
                       ", ".join("%s=%r" % (f, getattr(self, f))
                                 for f in self._fields)))

    ## Provide a sensible name
    klass.__name__ = "Tuple(%s)" % (", ".join(a), )

    return klass


class String(str, Format):
    """Defines a Format based on python string

    A default validation will be done on the class attribute
    regex::

        >>> class MyFormat(String):
        ...     regex = re.compile('(red|blue|green)')

        >>> MyFormat('invalid')
        Traceback (most recent call last):
        ...
        ValueError: Invalid string specifier 'invalid' format for MyFormat format.

        >>> red = MyFormat('red')

    Notice that the representation of this object is invisible as it
    is a subclass of string::

        >>> red
        'red'

    Although::

        >>> type(MyFormat('red'))
        <Format MyFormat>

    You can avoid setting ``regex`` if you have no use of this check::

        >>> class MyFormat(String): pass
        >>> MyFormat('red')
        'red'

    """

    default = None  ## no value
    regex = None

    def __new__(cls, s, **kwargs):
        if s is None and cls.default is not None:
            s = cls.default
        s = cls._validate(s)
        return super(String, cls).__new__(cls, s)

    @classmethod
    def _validate(cls, s):
        if cls.regex:
            if not cls.regex.match(s):
                raise ValueError(
                    'Invalid string specifier %r format for %s format.'
                    % (s, cls.__name__))
        return s


##
## Converters function
##

class ConverterRegistry(list):
    """Provides helper functions to get and combine converters function

    First, this object acts as a registry, storing in a list the available
    converters. Converters are special annotated functions::

        >>> cr = ConverterRegistry()

    Registering should be done thanks to ``register_converter`` decorator::

        >>> @register_converter(cr, src="hex", dst="dec")
        ... def hex2dec(x): return int(x, 16)

    Or equivalently::

        >>> register_converter(cr, src="dec", dst="hex")(
        ...     lambda x: hex(x))  ## doctest: +ELLIPSIS
        <function <lambda> at ...>
        >>> register_converter(cr, src="dec", dst="bin")(
        ...     lambda x: bin(x))  ## doctest: +ELLIPSIS
        <function <lambda> at ...>

    Then we can expect simply converting between available path::

        >>> cr.convert_fun("hex", "dec")("15")
        21

    Note that this is provided directly by only one converter, in the following
    2 converters will be used to get to the answer::

        >>> cr.convert_fun("hex", "bin")("15")
        '0b10101'

    When source and destination format are equivalent, this will make not change
    on the output::

        >>> cr.convert_fun("hex", "hex")("15")
        '15'

    And if no path exists it'll cast an exception::

        >>> cr.convert_fun("bin", "hex")("0101")
        Traceback (most recent call last):
        ...
        ValueError: No convertion path found from bin to hex format.

    Note that if the functions have already been annotated, then you
    can instantiate directly a new ``ConverterRegistry``::

        >>> new_cr = ConverterRegistry(cr)
        >>> new_cr.convert_fun("hex", "bin")("15")
        '0b10101'

    """

    def __init__(self, converters=None):
        if converters is None:
            converters = []
        super(ConverterRegistry, self).__init__(converters)

    def get(self, src):
        return {cv.dst: (cv, cv.conv_kwargs)
                for cv in self
                if cv.src is src}

    def find_path(self, src, dst):
        visited = [src]
        nexts = [(([], n), t[0], t[1])
                 for n, t in self.get(src).items()
                 if n not in visited]
        while len(nexts) != 0:
            (path, next), fun, dct = nexts.pop()
            visited.append(next)
            new_path = path + [fun]
            dsts = self.get(next)
            if dst is next:
                return new_path
            nexts.extend([((new_path, n), t[0], t[1])
                          for n, t in dsts.items() if n not in visited])

    def convert_fun(self, src_format, dst_format):
        def _path_to_callable(path):
            def _f(value):
                for fun in path:
                    value = fun(value)
                    if callable(fun.dst):
                        value = fun.dst(value)
                return value
            return _f
        if src_format is dst_format or src_format == dst_format:
            return lambda x: x
        path = self.find_path(src_format, dst_format)
        if path:
            return _path_to_callable(path)
        raise ValueError(
            "No convertion path found from %s to %s format."
            % (src_format, dst_format))


def register_converter(registry, src, dst, **kwargs):

    def decorator(f):
        f.src = src
        f.dst = dst
        f.conv_kwargs = kwargs
        registry.append(f)
        return f
    return decorator


def color_scale(begin_hsl, end_hsl, nb):
    """Returns a list of nb color HSL tuples between begin_hsl and end_hsl

        >>> from colour import color_scale

        >>> [HSL(hsl).convert(HexS) for hsl in color_scale((0, 1, 0.5),
        ...                                                (1, 1, 0.5), 3)]
        ['#f00', '#0f0', '#00f', '#f00']

        >>> [HSL(hsl).convert(HexS)
        ...  for hsl in color_scale((0, 0, 0),
        ...                         (0, 0, 1),
        ...                         15)]  # doctest: +ELLIPSIS
        ['#000', '#111', '#222', ..., '#ccc', '#ddd', '#eee', '#fff']

    Of course, asking for negative values is not supported:

        >>> color_scale((0, 1, 0.5), (1, 1, 0.5), -2)
        Traceback (most recent call last):
        ...
        ValueError: Unsupported negative number of colors (nb=-2).

    """

    if nb < 0:
        raise ValueError(
            "Unsupported negative number of colors (nb=%r)." % nb)

    step = tuple([float(end_hsl[i] - begin_hsl[i]) / nb for i in range(0, 3)]) \
           if nb > 0 else (0, 0, 0)

    def mul(step, value):
        return tuple([v * value for v in step])

    def add_v(step, step2):
        return tuple([v + step2[i] for i, v in enumerate(step)])

    return [add_v(begin_hsl, mul(step, r)) for r in range(0, nb + 1)]


##
## Color Pickers
##

def RGB_color_picker(obj):
    """Build a color representation from the string representation of an object

    This allows to quickly get a color from some data, with the
    additional benefit that the color will be the same as long as the
    (string representation of the) data is the same::

        >>> from colour import RGB_color_picker, Color

    Same inputs produce the same result::

        >>> RGB_color_picker("Something") == RGB_color_picker("Something")
        True

    ... but different inputs produce different colors::

        >>> RGB_color_picker("Something") != RGB_color_picker("Something else")
        True

    In any case, we still get a ``Color`` object::

        >>> isinstance(RGB_color_picker("Something"), Color)
        True

    """

    ## Turn the input into a by 3-dividable string. SHA-384 is good because it
    ## divides into 3 components of the same size, which will be used to
    ## represent the RGB values of the color.
    digest = hashlib.sha384(str(obj).encode('utf-8')).hexdigest()

    ## Split the digest into 3 sub-strings of equivalent size.
    subsize = int(len(digest) / 3)
    splitted_digest = [digest[i * subsize: (i + 1) * subsize]
                       for i in range(3)]

    ## Convert those hexadecimal sub-strings into integer and scale them down
    ## to the 0..1 range.
    max_value = float(int("f" * subsize, 16))
    components = (
        int(d, 16)     ## Make a number from a list with hex digits
        / max_value    ## Scale it down to [0.0, 1.0]
        for d in splitted_digest)

    return Color(rgb2hex(components))  ## Profit!


def hash_or_str(obj):
    try:
        return hash((type(obj).__name__, obj))
    except TypeError:
        ## Adds the type name to make sure two object of different type but
        ## identical string representation get distinguished.
        return "\0".join([type(obj).__name__, str(obj)])

##
## All purpose object
##

def mkDataSpace(formats, converters, picker=None,
                internal_format=None,
                input_formats=[],
                repr_format=None,
                string_format=None):
    """Returns a DataSpace provided a format registry and converters

    To create a data space you'll need a format registry, as this one::

        >>> fr = FormatRegistry()

        >>> @register_format(fr)
        ... class Dec(int, Format): pass
        >>> @register_format(fr)
        ... class Hex(String): pass
        >>> @register_format(fr)
        ... class Bin(String): pass

    To create a data space you'll need a converter registry, as this one::

        >>> cr = ConverterRegistry()

        >>> @register_converter(cr, Hex, Dec)
        ... def h2d(x): return int(x, 16)
        >>> @register_converter(cr, Dec, Hex)
        ... def d2h(x): return hex(x)
        >>> @register_converter(cr, Dec, Bin)
        ... def d2b(x): return bin(x)

    Then you can create the data space::

        >>> class Numeric(mkDataSpace(fr, cr)): pass


    Instantiation
    =============

    You can instatiate by explicitely giving the input format:

        >>> Numeric(dec=1)
        <Numeric 1>
        >>> Numeric(hex='0xc')
        <Numeric 12>

    Similarily, you can let the ``DataSpace`` object figure
    it out if you provide an already instantiated value:

        >>> Numeric(Dec(1))
        <Numeric 1>
        >>> Numeric(Hex('0xc'))
        <Numeric 12>

    And you can instantiate a DataSpace object with an other instance of
    it self::

        >>> Numeric(Numeric(1))
        <Numeric 1>

    You can also let the dataspace try to figure it out thanks to
    ``input_formats`` which is covered in the next section.

    And, finally, using the ``pick_for`` attribute, you can ask an
    automatic value for any type of python object. This value would
    then identify and should be always the same for the same object.
    This is covered in ``picker`` section.


    input_formats
    -------------

    A dataspace can be instantiated with any type of object, in the
    case the object is not an instance of a format listed in the
    format registry, it'll have to try to try to instantiate one of
    these internal format with the value you have provided.  This is
    where the ``input_formats`` list will be used. Note that if it was
    not specified it will be the ``repr_format`` alone and if not
    specified, it'll fallback on the first available format alone in
    the format registry:

        >>> class Numeric(mkDataSpace(fr, cr)): pass
        >>> Numeric(1)
        <Numeric 1>

    But notice that hex value will be refused, as the only input format
    specified was (by default) the first one in the registry ``Dec``::

        >>> Numeric('0xc')
        Traceback (most recent call last):
        ...
        ValueError: No input formats are able to read '0xc' (tried Dec)

    So if you want, you can specify the list of input formats, they will be
    tried in the given order...

        >>> class Numeric(mkDataSpace(fr, cr, input_formats=[Dec, Hex])): pass
        >>> Numeric(1)
        <Numeric 1>
        >>> Numeric('0xc')
        <Numeric 12>

    Note also that if you don't want to specify ``input_formats``, using keyword
    can be allowed for one-time access::

        >>> class Numeric(mkDataSpace(fr, cr)): pass
        >>> Numeric(1)
        <Numeric 1>
        >>> Numeric(hex='0xc')
        <Numeric 12>


    picker
    ------

    By default, the picker mecanism is not operational::

        >>> class Numeric(mkDataSpace(fr, cr)): pass
        >>> Numeric(pick_for=object())
        Traceback (most recent call last):
        ...
        ValueError: Can't pick value as no picker was defined.

    You must define a ``picker``, a function that will output a value
    that could be instantiated by the ``DataSpace`` object::

        >>> class Numeric(mkDataSpace(fr, cr, picker=lambda x: 1)): pass
        >>> Numeric(pick_for=object())
        <Numeric 1>

    Of course, this is a dummy example, you should probably use
    ``hash`` or ``id`` or the string representation of your object to
    reliably give a different value to different object while having
    the same value for the same object.


    Output formats
    ==============

    Dataspace will have mainly 2 output formats to follow python conventions::
    - a repr output
    - a string output
    These are manageable independantly if needed.


    object representation
    ---------------------

    There's a ``repr_format`` keyword to set the python repr format, by
    default it will fallback to the first format available in the format
    registry::

        >>> class Numeric(mkDataSpace(fr, cr, repr_format=Hex)): pass
        >>> Numeric('0xc')
        <Numeric 0xc>

    Notice that the input format by default is the ``repr_format``. So:

        >>> class Numeric(mkDataSpace(fr, cr,
        ...     repr_format=Hex, input_formats=[Dec, ])): pass
        >>> Numeric(12)
        <Numeric 0xc>


    object string output
    --------------------

    There's a ``string_format`` keyword to set the python string
    output used by ``%s`` or ``str()``, by default it will fallback to
    the ``repr_format`` value if defined and if not to the first
    format available in the format registry::

        >>> class Numeric(mkDataSpace(fr, cr, string_format=Hex)): pass
        >>> str(Numeric(12))
        '0xc'


    Internal Format
    ===============

    ``DataSpace`` instance have an internal format which is the format
    that is effectively used to store the value. This format may be fixed
    of variable. By default it is variable, and this means that the value
    stored can change format any time.

    In some case you might want to use a fixed format to store your value.

    This will not change any visible behavior, the value being converted
    back and forth to the expected format anyway::

        >>> class Numeric(mkDataSpace(fr, cr, internal_format=Hex)): pass
        >>> Numeric(1)
        <Numeric 1>
        >>> Numeric(1).hex
        '0x1'

    In our example, we only have a path to convert from ``Dec`` to ``Bin`` and
    not the reverse::

        >>> class Numeric(mkDataSpace(fr, cr, internal_format=Bin)): pass
        >>> x = Numeric(15)
        >>> x.bin
        '0b1111'

    Instanciation, attribute acces was okay, but::

        >>> x
        Traceback (most recent call last):
        ...
        ValueError: No convertion path found from bin to dec format.

    Because representaiton of the object should be in ``Dec`` format.


    Attribute
    =========

    There are 2 different type of magic attribute usable on
    ``DataSpace`` instances:
    - attributes that uses the format names and aims at setting
      or getting conversion in other formats.
    - attributes that uses subcomponent name of namedtuple

    Format's name
    -------------

    Each ``DataSpace`` instance will provide attributes following the name
    of every format of the format registry that is reachable thanks to the
    converters.

        >>> class Numeric(mkDataSpace(fr, cr)): pass
        >>> Numeric(1).hex
        '0x1'
        >>> Numeric(1).bin
        '0b1'

    These attribute are read/write, so you can set the value of the instance
    easily::

        >>> x = Numeric(12)
        >>> x
        <Numeric 12>
        >>> x.hex = '0x12'
        >>> x
        <Numeric 18>
        >>> x.bin = '0b10101'

    We didn't provide any way to convert from binary to dec, which is
    the representation format here, so:

        >>> x
        Traceback (most recent call last):
        ...
        ValueError: No convertion path found from bin to dec format.

    Notice that this only makes an error upon usage, because the
    internal format (see section) is not fixed, and will thus follow
    blindly the last attribute assignation's format.

    subcomponent attribute
    ----------------------

    This is a very special feature geared toward the usage of
    namedtuple formats.

    Most dataspace usage are used as reference systems translation
    between multi-dimensional data. Let's take for instance
    translation between polar coordinates and cartesian
    coordinates::

        >>> import math
        >>> fr2 = FormatRegistry()

        >>> @register_format(fr2)
        ... class Cartesian(Tuple("x", "y")): pass
        >>> @register_format(fr2)
        ... class Polar(Tuple("radius", "angle")): pass

        >>> cr2 = ConverterRegistry()

        >>> @register_converter(cr2, Cartesian, Polar)
        ... def c2p(v): return math.sqrt(v.x**2 + v.y**2), math.atan2(v.y, v.x)
        >>> @register_converter(cr2, Polar, Cartesian)
        ... def p2c(p):
        ...     return (p.radius * math.cos(p.angle),
        ...             p.radius * math.sin(p.angle))

        >>> class Point2D(mkDataSpace(fr2, cr2)): pass

        >>> point = Point2D((1, 0))
        >>> point
        <Point2D Cartesian(x=1, y=0)>

    The names of the subcomponent of the tuple are directly accessible
    (if there are no ambiguity)::

        >>> point.x
        1

        >>> point.angle = math.pi
        >>> point.x
        -1.0

    In case of ambiguity, you can prefix your attribute label with the
    format names as such:

        >>> point.cartesian_y = 0.0
        >>> point.cartesian_x = 1.0
        >>> point.polar_angle
        0.0

    Here is such a case:

        >>> fr3 = FormatRegistry()

        >>> @register_format(fr3)
        ... class Normal(Tuple("x", "y")): pass
        >>> @register_format(fr3)
        ... class Inverted(Tuple("x", "y")): pass

        >>> cr3 = ConverterRegistry()

        >>> @register_converter(cr3, Normal, Inverted)
        ... def n2i(v): return v.y, v.x
        >>> @register_converter(cr3, Inverted, Normal)
        ... def i2n(v): return v.y, v.x

    In this case, we don't expect attribute ``x`` to be found::

        >>> class Point2D(mkDataSpace(fr3, cr3)): pass
        >>> Point2D((1, 2)).x = 2
        Traceback (most recent call last):
        ...
        ValueError: Ambiguous attribute 'x'. Try one of: normal_x, inverted_x

        >>> Point2D((1, 2)).x
        Traceback (most recent call last):
        ...
        ValueError: Ambiguous attribute 'x'. Try one of: normal_x, inverted_x


    incorrect attribute
    -------------------

    Of course, referring to an attribute label that can't be infered
    following the above rules then it'll cast an attribute error::

        >>> class Numeric(mkDataSpace(fr, cr)): pass
        >>> Numeric(1).foo
        Traceback (most recent call last):
        ...
        AttributeError: 'foo' not found

    You can't read it and can't set it::

        >>> Numeric(1).foo = 2
        Traceback (most recent call last):
        ...
        AttributeError: foo


    Edge cases
    ==========

    If you provide an empty format registry, it'll complain:

        >>> mkDataSpace(FormatRegistry(), ConverterRegistry(), None)
        Traceback (most recent call last):
        ...
        ValueError: formats registry provided is empty.

    """

    if len(formats) == 0:
        raise ValueError("formats registry provided is empty.")

    ## defaults
    repr_format = repr_format or formats[0]
    string_format = string_format or repr_format
    input_formats = input_formats or [repr_format]

    class DataSpace(object):
        """Relative Element in multi-representation data

        This object holds an internal representation of a data in a
        format (fixed or variable) and provide means to translate the
        data in available formats thanks to a set of converter functions.

        """

        _internal = None

        def __init__(self, value=None, pick_for=None, pick_key=hash_or_str,
                     picker=None, **kwargs):

            if pick_key is None:
                pick_key = lambda x: x

            if pick_for is not None:
                if not (picker or self._picker):
                    raise ValueError(
                        "Can't pick value as no picker was defined.")
                value = (picker or self._picker)(pick_key(pick_for))

            if isinstance(value, DataSpace):
                value_if_name = str(type(value._internal))
                setattr(self, value_if_name,
                        getattr(value, value_if_name))
            elif isinstance(value, tuple(formats)):
                self._internal = value.convert(self._internal_format, converters) \
                                 if self._internal_format else value
            else:
                for f in input_formats:
                    try:
                        setattr(self, str(f), value)
                        break
                    except (ValueError, TypeError):
                        continue
                else:
                    ## maybe keyword values were used
                    if len(set(kwargs.keys()) &
                           set(str(f) for f in self._formats)) == 0:
                        raise ValueError(
                            "No input formats are able to read %r (tried %s)"
                            % (value,
                               ", ".join(f.__name__ for f in input_formats)))

            self.equality = RGB_equivalence

            for k, v in kwargs.items():
                setattr(self, k, v)

        def __getattr__(self, label):
            f, attr = self._formats.find(label)
            if f is not None:
                if attr is not None:
                    return getattr(
                        getattr(self, str(f)),
                        attr)
                return self._internal.convert(f, self._converters)
            raise AttributeError("'%s' not found" % label)

        def __setattr__(self, label, value):
            if label.startswith("_") or label == "equality":
                self.__dict__[label] = value
                return

            f, attr = self._formats.find(label)
            if f is None:
                raise AttributeError(label)
            elif attr is None:
                if not isinstance(value, f):
                    try:
                        value = f(value)
                    except:
                        msg = format_last_exception()
                        raise ValueError(
                            "Instantiation of %s failed with given value %s."
                            "\n%s"
                            % (type(value).__name__, value, msg))
                if self._internal_format:
                    value = value.convert(self._internal_format,
                                          self._converters)
                self._internal = value
            else:  ## attr is not None
                setattr(self, str(f),
                        getattr(self, str(f))._replace(**{attr: value}))

        def __str__(self):
            return "%s" % (getattr(self, str(self._string_format)), )

        def __repr__(self):
            return "<%s %s>" % (self.__class__.__name__,
                                getattr(self, str(self._repr_format)))

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.equality(self, other)
            return NotImplemented

        if sys.version_info[0] == 2:
            ## Note: intended to be a backport of python 3 behavior
            def __ne__(self, other):
                equal = self.__eq__(other)
                return equal if equal is NotImplemented else not equal

    frame = inspect.currentframe()
    argvalues = inspect.getargvalues(frame)
    for k in argvalues.args:
        value = argvalues.locals[k]
        if k == "picker" and value:
            value = staticmethod(value)
        setattr(DataSpace, "_%s" % k, value)
    return DataSpace

##
## Color equivalence
##

RGB_equivalence = lambda c1, c2: c1.hex == c2.hex
HSL_equivalence = lambda c1, c2: c1.hsl == c2.hsl


##
## Module wide color object
##


def make_color_factory(**kwargs_defaults):

    def ColorFactory(*args, **kwargs):
        new_kwargs = kwargs_defaults.copy()
        new_kwargs.update(kwargs)
        return Color(*args, **new_kwargs)
    return ColorFactory


##
## Convenience
##

def format_last_exception(prefix="  | "):
    """Format the last exception for display it in tests.

    This allows to raise custom exception, without loosing the context of what
    caused the problem in the first place:

        >>> def f():
        ...     raise Exception("Something terrible happened")
        >>> try:  ## doctest: +ELLIPSIS
        ...     f()
        ... except Exception:
        ...     formated_exception = format_last_exception()
        ...     raise ValueError('Oups, an error occured:\\n%s'
        ...         % formated_exception)
        Traceback (most recent call last):
        ...
        ValueError: Oups, an error occured:
          | Traceback (most recent call last):
        ...
          | Exception: Something terrible happened

    """

    return '\n'.join(
        str(prefix + line)
        for line in traceback.format_exc().strip().split('\n'))


##
## Color Formats
##

## Global module wide registry
Formats = FormatRegistry()


@register_format(Formats)
class Web(String):
    """string object with english color names or use short or long hex repr

    This format is used most notably in HTML/CSS for its ease of use.

    ex: 'red', '#123456', '#fff' are all web representation.

        >>> Web('white')
        'white'
        >>> Web.white
        'white'

        >>> Web('foo')
        Traceback (most recent call last):
        ...
        ValueError: 'foo' is not a recognized color for Web format.

        >>> Web('#foo')
        Traceback (most recent call last):
        ...
        ValueError: Invalid hex string specifier '#foo' for Web format

    Web has a default value to 'blue'::

        >>> Web(None)
        'blue'

    """

    default = 'blue'

    @classmethod
    def _validate(cls, s):
        if s.startswith('#'):
            if not HexS.regex.match(s):
                raise ValueError(
                    "Invalid hex string specifier '%s' for Web format"
                    % s)
            return s
        web = s.lower()
        if web not in COLOR_NAME_TO_RGB:
            raise ValueError(
                "%r is not a recognized color for Web format."
                % web)
        return web


@register_format(Formats)
class HSL(Tuple("hue", "saturation", "luminance")):
    """3-uple of Hue, Saturation, Lightness all between 0.0 and 1.0

    As all ``Format`` subclass, it can instantiate color based on the X11
    color names::

        >>> HSL.white
        HSL(hue=0.0, saturation=0.0, luminance=1.0)

    """


@register_format(Formats)
class RGB(Tuple("red", "green", "blue")):
    """3-uple of Red, Green, Blue all values between 0.0 and 1.0

    As all ``Format`` subclass, it can instantiate color based on the X11
    color names::

        >>> RGB.darkcyan  ## doctest: +ELLIPSIS
        RGB(red=0.0, green=0.545..., blue=0.545...)
        >>> RGB.WHITE
        RGB(red=1.0, green=1.0, blue=1.0)
        >>> RGB.BLUE
        RGB(red=0.0, green=0.0, blue=1.0)

        >>> RGB.DOESNOTEXIST  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        AttributeError: ... has no attribute 'DOESNOTEXIST'

    """


@register_format(Formats)
class Hex(String):
    """7-chars string starting with '#' and with red, green, blue values

    Each color is expressed in 2 hex digit each.

    Note: This format accept only 6-dex digit

    Example: '#ffffff'

    As all ``Format`` subclass, it can instantiate color based on the X11
    color names::

        >>> Hex.WHITE
        '#ffffff'
        >>> type(Hex.WHITE)
        <Format Hex>
        >>> Hex.BLUE
        '#0000ff'

    """

    regex = re.compile(r'^#[0-9a-fA-F]{6}$')


@register_format(Formats)
class HexS(String):
    """string starting with '#' and with red, green, blue values

    This format accept color in 3 or 6 value ex: '#fff' or '#ffffff'

    """

    regex = re.compile(r'^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$')


##
## Converters
##


## Module wide converters
Converters = ConverterRegistry()


@register_converter(Converters, HSL, RGB)
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
    g = _hue2rgb(v1, v2, h)
    b = _hue2rgb(v1, v2, h - (1.0 / 3))

    return r, g, b


@register_converter(Converters, RGB, HSL)
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

    Regression check upon very close values in every component of
    red, green and blue:

        >>> rgb2hsl((0.9999999999999999, 1.0, 0.9999999999999994))
        ...     ## doctest: +ELLIPSIS
        (0.0, 0.0, 0.999...)

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

    vmin = min(r, g, b)  ## Min. value of RGB
    vmax = max(r, g, b)  ## Max. value of RGB
    diff = vmax - vmin   ## Delta RGB value

    vsum = vmin + vmax

    l = vsum / 2

    if diff < FLOAT_ERROR:  ## This is a gray, no chroma...
        return 0.0, 0.0, l

    ##
    ## Chromatic data...
    ##

    ## Saturation
    if l < 0.5:
        s = diff / vsum
    else:
        s = diff / (2.0 - vsum)

    dr = (((vmax - r) / 6) + (diff / 2)) / diff
    dg = (((vmax - g) / 6) + (diff / 2)) / diff
    db = (((vmax - b) / 6) + (diff / 2)) / diff

    if r == vmax:
        h = db - dg
    elif g == vmax:
        h = (1.0 / 3) + dr - db
    else:  ##  b == vmax
        h = (2.0 / 3) + dg - dr

    if h < 0: h += 1
    if h > 1: h -= 1

    return h, s, l


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


@register_converter(Converters, Hex, HexS)
def hex2hexs(hex):
    """Shorten from 6 to 3 hex represention if possible

    Usage
    -----

        >>> from colour import hex2hexs

    Provided a long string hex format, it should shorten it when
    possible::

        >>> hex2hexs('#00ff00')
        '#0f0'

    In the following case, it is not possible to shorten, thus::

        >>> hex2hexs('#01ff00')
        '#01ff00'

    """

    if len(hex) == 7 and hex[1::2] == hex[2::2]:
        return "#" + ''.join(hex[1::2])
    return hex


@register_converter(Converters, HexS, Hex)
def hexs2hex(hex):
    """Enlarge possible short 3 hexgit to give full hex 6 char long

    Usage
    -----

        >>> from colour import hexs2hex

    Provided a short string hex format, it should enlarge it::

        >>> hexs2hex('#0f0')
        '#00ff00'

    In the following case, it is already enlargened, thus::

        >>> hexs2hex('#01ff00')
        '#01ff00'

    """
    if not Hex.regex.match(hex):
        return '#' + ''.join([("%s" % (t, )) * 2 for t in hex[1:]])
    return hex


@register_converter(Converters, RGB, Hex)
def rgb2hex(rgb):
    """Transform RGB tuple to hex RGB representation

    :param rgb: RGB 3-uple of float between 0 and 1
    :rtype: 3 hex char or 6 hex char string representation

    Usage
    -----

        >>> from colour import rgb2hex

        >>> rgb2hex((0.0, 1.0, 0.0))
        '#00ff00'

    Rounding try to be as natural as possible:

        >>> rgb2hex((0.0, 0.999999, 1.0))
        '#00ffff'

        >>> rgb2hex((0.5, 0.999999, 1.0))
        '#7fffff'

    """

    return "#" + ''.join(["%02x" % int(c * 255 + 0.5 - FLOAT_ERROR)
                          for c in rgb])


@register_converter(Converters, Hex, RGB)
def hex2rgb(str_rgb):
    """Transform hex RGB representation to RGB tuple

    :param str_rgb: 3 hex char or 6 hex char string representation
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
        ValueError: Invalid value '#aa' provided as hex color for rgb conversion.

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
        raise ValueError(
            "Invalid value %r provided as hex color for rgb conversion."
            % str_rgb)

    return tuple(float(int(v, 16)) / 255 for v in (r, g, b))


@register_converter(Converters, Hex, Web)
def hex2web(hex):
    """Converts Hex representation to Web

    :param rgb: 3 hex char or 6 hex char string representation
    :rtype: web string representation (human readable if possible)

    Web representation uses X11 rgb.txt to define convertion
    between RGB and english color names.

    Usage
    =====

        >>> from colour import hex2web

        >>> hex2web('#ff0000')
        'red'

        >>> hex2web('#aaaaaa')
        '#aaa'

        >>> hex2web('#acacac')
        '#acacac'

    """
    dec_rgb = tuple(int(v * 255) for v in hex2rgb(hex))
    if dec_rgb in RGB_TO_COLOR_NAMES:
        ## take the first one
        color_name = RGB_TO_COLOR_NAMES[dec_rgb][0]
        ## Enforce full lowercase for single worded color name.
        return color_name if len(re.sub(r"[^A-Z]", "", color_name)) > 1 \
               else color_name.lower()

    return hex2hexs(hex)


@register_converter(Converters, Web, Hex)
def web2hex(web):
    """Converts Web representation to Hex

    :param rgb: web string representation (human readable if possible)
    :rtype: 3 hex char or 6 hex char string representation

    Web representation uses X11 rgb.txt (converted in array in this file)
    to define convertion between RGB and english color names.

    As of https://www.w3.org/TR/css3-color/#svg-color, there are 147 names
    recognized.


    Usage
    =====

        >>> from colour import web2hex

        >>> web2hex('red')
        '#ff0000'

        >>> web2hex('#aaa')
        '#aaaaaa'

        >>> web2hex('#foo')  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        AttributeError: '#foo' is not in web format. Need 3 or 6 hex digit.

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

        And color names are case insensitive:

        >>> Color('RED')
        <Color red>

    """
    if web.startswith('#'):
        if Hex.regex.match(web):
            return web.lower()
        elif HexS.regex.match(web):
            return hexs2hex(web)
        raise AttributeError(
            "%r is not in web format. Need 3 or 6 hex digit." % web)

    web = web.lower()
    if web not in COLOR_NAME_TO_RGB:
        raise ValueError("%r is not a recognized color." % web)

    return rgb2hex([float(int(v)) / 255 for v in COLOR_NAME_TO_RGB[web]])


class Color(mkDataSpace(formats=Formats, converters=Converters,
                        picker=RGB_color_picker)):
    """Abstraction of a color object

    Color object keeps information of a color. It can input/output to
    different formats (the ones registered in Formats object) and
    their partial representation.

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
        RGB(red=0.0, green=0.0, blue=1.0)
        >>> b.hsl  # doctest: +ELLIPSIS
        HSL(hue=0.66..., saturation=1.0, luminance=0.5)
        >>> b.hex
        '#0000ff'

    Change values
    -------------

    Let's change Hue toward red tint:

        >>> b.hue = 0.0
        >>> b.hex
        '#ff0000'

        >>> b.hue = 2.0/3
        >>> b.hex
        '#0000ff'

    In the other way round:

        >>> b.hexs = '#f00'
        >>> b.hsl
        HSL(hue=0.0, saturation=1.0, luminance=0.5)

    Long hex can be accessed directly:

        >>> b.hex = '#123456'
        >>> b.hex
        '#123456'
        >>> b.hexs
        '#123456'

        >>> b.hex = '#ff0000'
        >>> b.hex
        '#ff0000'
        >>> b.hexs
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
        HSL(hue=..., saturation=0.0, luminance=0.5)
        >>> c.rgb
        RGB(red=0.5, green=0.5, blue=0.5)
        >>> c.hex
        '#7f7f7f'
        >>> c
        <Color #7f7f7f>

        >>> c.luminance = 0.0
        >>> c
        <Color black>

        >>> c.hex
        '#000000'

        >>> c.green = 1.0
        >>> c.blue = 1.0
        >>> c.hex
        '#00ffff'
        >>> c
        <Color cyan>

    Equivalently, in one go:

        >>> c.rgb = (1, 1, 0)
        >>> c
        <Color yellow>

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


    Recursive init
    --------------

    To support blind convertion of web strings (or already converted object),
    the Color object supports instantiation with another Color object.

        >>> Color(Color(Color('red')))
        <Color red>

    Equality support
    ----------------

    Default equality is RGB hex comparison:

        >>> Color('red') == Color('blue')
        False
        >>> Color('red') == Color('red')
        True
        >>> Color('red') != Color('blue')
        True
        >>> Color('red') != Color('red')
        False

    But this can be changed:

        >>> saturation_equality = lambda c1, c2: c1.luminance == c2.luminance
        >>> Color('red', equality=saturation_equality) == Color('blue')
        True


    Subclassing support
    -------------------

    You should be able to subclass ``Color`` object without any issues::

        >>> class Tint(Color):
        ...     pass

    And keep the internal API working::

        >>> Tint("red").hsl
        HSL(hue=0.0, saturation=1.0, luminance=0.5)

    """

    def range_to(self, value, steps):
        for hsl in color_scale(self.hsl, self.__class__(value).hsl, steps - 1):
            yield self.__class__(hsl=hsl)
