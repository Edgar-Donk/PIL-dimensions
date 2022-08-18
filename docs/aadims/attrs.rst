=========
attrs
=========

``attrs`` produces similar results to a dataclass, the methods are slightly
different and it enforces the class integrity more strongly than when using
a dataclass, nevertheless a lot of attribute duplication is 
avoided. With Python 3.9, or newer, all the variable types are directly 
accessible, otherwise import the types from **typing** and use a capital letter,
so **any** becomes **typing.Any** in the earlier versions.

Use the module DimLinesattr as opposed to the modules DimLinesAA or DimLinesDC. 
The 
testing programs are suffixed by **_attr**, so test_aa_dim.py becomes 
test_aa_dim_attr.py. The PIL image and drawing handles can be stored in 
the dataclass. Checks are made as the variables are changed, without too much
additional work.

.. note:: **Changing Variables**
    The variables in the dataclass dc are changed just by using a 
    construct like the following, which is like a simple class(no __init__)::
    
        im = Image.new('RGB', (80, 80), back)
        dc.image = im
        print(dc.back)
        >>> (255,255,255)
    
    attrs enforces the original class structure more strictly than in the
    dataclass, therefore any new data has to be loaded into an instance
    of the decorated class::
    
        aq = atr(100,100)
        print(atr.back)
        >>> <member 'back' of 'atr' objects>
        print(aq.back)
        >>> (255,255,255)

The results for drawing using DimLinesattr are
exactly the same as for DimLinesAA, the function names are similar. The 
major change is in the number of attributes used for each function, so taking 
the inner dimension as an example, call up the function with::

    inner_dim_attr(ptA, ptB, text=text, arrow='both')

which in turn calls up::

    dimension_attr(ptA, ptB)
    ....
    angled_text(aq.image, at, text, angle, font=aq.font, fill=aq.fill)

as opposed to::

    inner_dim(im, ptA, ptB, text=text, font=None, width=1, fill=(0,0,0),
              arrowhead=(8, 10, 3), arrow='both')

which calls up::

    dimension(im, ptA, ptB, width=width, fill=fill, arrowhead=arrowhead,
              arrow='both')
    ....
    angled_text(im, at, text, angle, font=font, fill=fill)

angled text is in the DimLinesPIL module, independant of attrs.

Changing data after initialisation is not easy, as any changed data
has to be included with the changing data, so to change the data one must
instantiate again, which means that previously changed data within the attr 
class reverts back to its default value, unless this is re-entered, which is
not really practicable inside the DimLinesattr module. 

This means that **arrow** is best left as a normal function attribute. 

The data **aall** changes less 
frequently within the module, but stays constant within a function, it is
possible therefore to have the opposite value from its own default, **aall**
need only be called if we wish to change the angled_text behaviour. Other
data will depend on the value at initialisation.

Taking advantage of attrs properties note that data input can be deferred 
until after initialisation. Set the PIL handles ``image`` and ``draw`` inside 
the attrs class, this means that the image **width** and **height** are 
part of the class with no default values, so these are set when the class is 
initialised. Once set image and draw are created from PIL Image and ImageDraw.

When initialised the data can be validated, using attr's built in validation.

attr Attributes
===============

.. raw:: html

   <details>
   <summary><a>Show/Hide <b>attr Attributes</b>  similar to dataclass</a></summary>

dimension_attr
--------------

* ptA
    Start coordinates
* ptB 
    Finishing line coordinates, default None
* angle
    Angle in degrees, default None
* arrow
    position of the arrow on the line, which influences the direction it 
    points, 'first', 'last' or 'both'

dims_attr
---------

External dimension

* ptA
    Start coordinates
* ptB 
    Finishing line coordinates
* extA
    Two integer tuple, giving the extension line size and gap next to start
* extB
    Two integer tuple, giving the extension line size and gap next to end, 
    optional if the same as extA   
* text
    Dimension text
* textorient
    Change text orientation, “h”, “horizontal”, “v”, “vertical”
* dimsorient
    confirm dimension orientation when extA and extB are unequal, 
    “h”, “horizontal”, “v”, “vertical”
* tail
    Show tails or arrows, default True
    
inner_dim_attr
--------------

* ptA
    Start coordinates
* ptB 
    Finishing line coordinates
* text
    Dimension text  

thickness_dim_attr
------------------

* ptA
    Start coordinates
* thick 
    Thickness of item
* angle
    Slope of Dimension, changes text position, default horizontal 0°    
* text
    Dimension text

arc_dim_attr
------------

* centre
    Arc’s circle centre
* radius
    Arc’s circle radius
* begin
    Starting angle, in degrees or enclosing line coordinates
* end
    Ending angle, in degrees or enclosing line coordinates
* text
    Dimension text    

slant_dim_attr
--------------

* ptA
    Start coordinates
* ptB
    Finishing coordinates, optional
* extA
    Two integer tuple, giving the extension line size and gap next to start
* angle
    Slope of dimension, optional
* length
    Dimension length, optional
* text
    Dimension text
* tail
    Show tails or arrows, default True

dim_level_attr
--------------

* at
    Coordinates at left tank wall level
* diam
    Tank diameter, pixels
* ldr
    Inclined leader length, default 20
* dash
    Tuple giving dash pattern, dash length then gap default (10, 4)
* text
    Dimension text

leader_attr
-----------

* at
    Coordinates on object
* angle
    Angle of first extension line, changes leader orientation, default 315°
* extA
    Length inclined extension line, default 20
* extB
    Length inclined extension line, default 20
* text
    Dimension text 

.. raw:: html

   </details>

|
