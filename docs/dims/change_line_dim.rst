=========================
Changes to Line Dimension
=========================

Some of the other dimensions just arrows, not necessarily pointing outwards. 

Changed Properties Line Dimension
---------------------------------

* ptB 
    Finishing coordinates used on a line, optional, default None.
* angle
    Slope of arrow in degrees used when working just with arrows, optional,
    default None.

Change Dimension Script
-----------------------

We can use the line dimension to draw the arrows, we need its position, 
angle, shape and which way to point, add a default value to ptB. Use the 
start point (ptA)
for its position add an angle option, checking on the arrow part of the 
script we should have all that is needed::

    def dimension(dr, ptA, ptB=None, angle=None, width=1, fill=(0,0,0),
                arrowhead=(8, 10, 3), arrow='last'):
        
        # extract entries from tuples
        x0, y0 = ptA
        if angle is None and ptB:
            phi = atan2(y1-y0, x1-x0)
            dr.line((ptA,ptB), width=width, fill=fill)
            x1, y1 = ptB
            phi = radians(angle)
        elif ptB is None and isinstance(angle, int):
            x1, y1 = ptA
            phi = radians(angle)
        else:
            raise Exception('dimension: Either supply ptB {} or angle {} not both' \
                .format(ptB, angle))
        ....

There are no other changes required to the line dimension.

After all that we should have a script that looks something like

.. container:: toggle

    .. container:: header

        *Show/Hide Code* test_arrow_line.py

    .. literalinclude:: ../examples/dims/test_arrow_line.py

.. note:: One can test the dimension module DimLinesPIL by importing the
    relevant dimension directly and running just the main part of the script.