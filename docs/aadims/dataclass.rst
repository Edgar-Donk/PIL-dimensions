=========
Dataclass
=========

If you have Python 3.6 or newer take advantage of dataclasses, it
reduces the number of attributes that need to be applied from a top
level function down to those within the module. The dataclass is accessible
to all those modules within its own directory without any module linking 
necessary. A lot of attribute duplication is 
avoided. With Python 3.9, or newer, all the variable types are directly 
accessible, otherwise import the types from **typing** and use a capital letter,
so **any** is **typing.Any** in the earlier versions.

Use the module DimLinesDC as opposed to the module DimLinesAA. The 
testing programs are suffixed by **_dc**, so test_aa_dim.py becomes 
test_aa_dim_dc.py. Even the PIL image and drawing handles can be created and 
stored in the dataclass. 

.. note:: **Changing Variables**
    The variables in the dataclass dc are easily changed just by using a 
    construct like the following::
    
        im = Image.new('RGB', (80, 80), back)
        dc.image = im

The main problem is when an immediate check on variables is
required, ``def __post_init__(self)`` checks the dataclass only when  
all the variables are updated together and not for each individual entry.

The results for drawing using DimLinesDC as opposed to DimLinesAA are
exactly the same, the names of the functions are similar. The major
change is in the number of attributes used for each function, so taking 
the inner dimension as an example, call up the function with::

    inner_dim_dc(ptA, ptB, text=text)

which in turn called up::

    dimension_dc(ptA, ptB)
    ....
    angled_text(dc.image, at, text, angle, font=dc.font, fill=dc.fill)

as opposed to::

    inner_dim(im, ptA, ptB, text=text, font=None, width=1, fill=(0,0,0),
              arrowhead=(8, 10, 3), arrow='both')

which calls up::

    dimension(im, ptA, ptB, width=width, fill=fill, arrowhead=arrowhead,
              arrow='both')
    ....
    angled_text(im, at, text, angle, font=font, fill=fill)

angled text is in the module DimLinesPIL, not yet tied into the dataclass.

When there is an attribute that changes occassionally the parent function 
changes the dataclass, calls the child function then resets the dataclass,
as done in the leader_dc function::

    ....
    dc.arrow = 'first'
    dimension_dc(at, ptB)
    dc.arrow = 'both'
    ....

Normally PIL programs
require to know the handle for PIL.Image and the handle for PIL.ImageDraw.
The handle for PIL.Image (image) which needs the image size (height and 
width) and the background colour (back). In turn the handle for PIL.ImageDraw
(image) needs the handle for PIL.Image. When initialising an instance of the 
dataclass provide the image size and the rest happens automatically. If one
or more default values is unsuitable change it here by adding the data name
equal to its new default value. The instance ``d`` is only used for 
initialisation, otherwise work directly with the the dataclass as shown above. 
In the module DimLinesDC find the 
dataclass **dc**, just after its definition find the lines::

    ######################################
    # Change dc initialisation values here
    wi = 200    # image width
    hi = 200    # image height
    d = dc(wi, hi)
    ######################################

alter the values 200 to those required, add any changes to the defaults as
needed::

    ######################################
    # Change dc initialisation values here
    wi = 160    # image width
    hi = 100    # image height
    d = dc(wi, hi, back=(0,0,0)
    ######################################

remember to save, then in the calling program ensure 
that the DimLinesDC module imports ``dc``::

    from DimLinesDC import ..., dc, ...

Dimension Scripts used in DimLinesDC
=====================================

.. raw:: html

   <details>
   <summary><a>Show/Hide <b>Dataclass Attributes</b> similar to antialias</a></summary>

dimension_dc
------------

* ptA
    Start coordinates
* ptB 
    Finishing line coordinates, default None
* angle
    Angle in degrees, default None

dims_dc
-------

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
    
inner_dim_dc
------------

* ptA
    Start coordinates
* ptB 
    Finishing line coordinates
* text
    Dimension text  

thickness_dim_dc
----------------

* ptA
    Start coordinates
* thick 
    Thickness of item
* angle
    Slope of Dimension, changes text position, default horizontal 0°    
* text
    Dimension text

arc_dim_dc
----------

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

slant_dim_dc
------------

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

dim_level_dc
------------

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

leader_dc
---------

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

Auxiliary DC Functions
======================

These will be similar to the functions found in the antialiased dimensions
except that the number of attributes have been reduced. The naming is also 
similar, just that the suffix is changed.

.. raw:: html

   <details>
   <summary><a>Show/Hide <b>Dataclass Auxiliary Functions</b> similar to antialias</a></summary>

DashedLineDC
------------

* pta
    Starting point of line 
* ptb
    Finishing point of line 
* dash
    Size of dash and gaps, default (5,5)
* adjust
    Alter dash and gap size relative to slope, default False

WideLineDC
----------

* pta
    Starting point of line 
* ptb
    Finishing point of line 
* width
    width in pixels, default 1

LineDC
------

Always 1 pixel wide

* pta
    Starting point of line 
* ptb
    Finishing point of line 

polyDC
------

Filled antialiased polygon default

* xy
    List of point tuples
* outline
    rgb tuple if an unfilled polygon is required

make_arc_dc
-----------

* centre
    Arc circle centre
* radius
    Arc circle radius
* start
    Arc starting angle, degrees
* finish
    Arc finishing angle, degrees

.. raw:: html

   </details>