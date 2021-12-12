===================
Outer AA Dimensions
===================

.. |lefto| image:: ../figures/aadims/dims_aa(60,40)-(60,80).png
    :width: 120
    :height: 120

.. |righto| image:: ../figures/aadims/dims_aa(60,80)-(60,40).png
    :width: 120
    :height: 120

.. |aboveo| image:: ../figures/aadims/dims_aa(80,60)-(40,60).png
    :width: 120
    :height: 120

.. |belowo| image:: ../figures/aadims/dims_aa(40,60)-(80,60).png
    :width: 120
    :height: 120

,,

    +----------------+-----------------+-----------------+-----------------+
    |   **Vertical Dimension**         |      **Horizontal Dimension**     |
    +================+=================+=================+=================+
    |  |lefto|       |  |righto|       |  |aboveo|       |  |belowo|       |
    +----------------+-----------------+-----------------+-----------------+
    | Left position  | Right position  | Upper position  | Lower position  |
    +----------------+-----------------+-----------------+-----------------+
    | Negative 270°  |  Positive 90°   |  Positive 0°    |  Negative 180°  |
    +----------------+-----------------+-----------------+-----------------+

Outer AA Dimension Attributes
-----------------------------

.. raw:: html

   <details>
   <summary><a>Show/Hide <b>dims_aa</b> properties</a></summary>

# im 
    PIL image handle, link to the calling program
# ptA
    Start coordinates
# ptB 
    Finishing coordinates
# extA
    Two integer tuple, giving the extension line size and gap next to start,
# extB
    Two integer tuple, giving the extension line size and gap next to end,
    optional if the same as extA
# text
    Dimension text
# font
    Font of the text
# textorient
    Change text orientation, "h", "horizontal", "v", "vertical" 
# fill
    Line colour, RGB tuple
# back
    Background colour, RGB tuple  
# tail
    Show tails or arrows, default **True**
# arrowhead
    Three integer tuple describing the shape and size of the arrow
# arrow
    position of the arrow on the line, which influences the direction it 
    points.

.. raw:: html

   </details>

|

Dimensions taken to the outside of an item will have extension lines and 
text, often there are several dimensions chained one to another plus one 
overall dimension positioned outside of the chained dimensions. If the chained
dimensions have arrows the effect can be rather cluttered, and if they have 
short tails the effect can look better. Which method to use is a matter of 
taste or what is considered standard. 

These dimensions are vertical or horizontal, for slanting dimensions see the
next section. The text on vertical dimensions runs vertically, 
whilst horizontal dimensions have horizontal text. If the default text 
orientation needs changing use **textorient**
to change its orientation (horizontal or vertical).

It is assumed that the 
dimensions lie to the right of the item or above it, when using dimensions to
the left of an item or below the item use negative extension sizes. When
both extension lines are the same the second extender **extB** can be left 
without a value.
If the object is not linear over the dimension, use different sizes for the 
extensions, **extA** and **extB**. Extension line lengths are given as a 
tuple of two integers, 
the first shows the drawn line length and the next the space between the 
object and drawn line, if no gap is required use a single integer.


Confirm that we are dealing with vertical or horizontal dimensions.
Several positioning properties depend on the orientation, so the extension 
lines are horizontal on vertical dimensions and vertical on the horizontal 
dimensions. 

.. note:: The outer dimension is based on its own coordinates, ptA and ptB.
   Position the dimension away from the object using the extension line 
   lengths .

The extension lines 
are drawn according to the lengths given. Then either add the two 45" stubs 
or add arrows to the dimension line , finally add the angled text.

At the end you should have something like the following.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* test_aa_dim.py

    .. literalinclude:: ../examples/aadims/test_aa_dim.py
