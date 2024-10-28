=====================
Convert to a Function
=====================

If we change our script into a function we need to know the start and finish 
of the line together with a knowledge of the dash and gap sizes. Use a tuple 
similar to the system from tkinter canvas. So the function's heading will be 
like::

    def line_dashed(im, start_pos, end_pos, dash=(5,5), width = 1, fill='black'):

Where ``im`` is the PIL Image alias.

.. sidebar:: Line Length

    The true line length can easily be determined by the built-in math
    function ``dist``. Simply include the start and end coordinates::
    
        line_length = dist(start_pos, end_pos)

Separate the function parts from the main function in the previous example. 
Extract the tuple 
information, compute the length of a single dash and the following gap, 
derive the line length, from these find out how many times the pattern is 
repeated, and insert into the linspace functions. 
Assume for the moment that we are only dealing with vertical lines and add
the length of a dash to the y part of the start and end coordinates. Then 
there should be a script like the following.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 05dash_gap_function.py

    .. literalinclude:: ../examples/dashes/05dash_gap_function.py

It should match up to the previous array.

There are several shortcomings in the script.

#. Line length
    Accommodate lines that do not finish exactly at the pattern end.

#. Change orientation
    The examples so far were with vertical lines.
    
#. Different line patterns
    The dash tuple so far only had 2 entries

#. Revisit line lengths
    With more complex patterns the lines may go beyond the end position.

As we go along other problems will undoubtedly raise their heads.
