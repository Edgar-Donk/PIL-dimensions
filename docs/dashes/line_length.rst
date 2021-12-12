
===========
Line Length
===========

Our examples so far have been too simplistic, what happens if the start and 
end points do 
not fit nicely into the length of the pattern, linspace will be 
unphased and produce an array of floating values, which after converting to 
integers will not coincide with the sizes required. If a user feeds in a 
pattern it is of secondary importance that the line finishes 
exactly at the end point. What should concern us is that the dashes and gaps
are accurate, so ensure that the correct information is fed into the 
linspace functions.

Change the end position so that the dash gap pattern finishes at the 
highest multiple of the pattern length that fits into the pattern length. 
With an eye on orientation, make this so it suits any angle::

    theta = atan2(y1 - y0, x1 - x0)
    
    if line_length % dash_gap_length != 0:
        factor = line_length//dash_gap_length 
        line_length = factor * dash_gap_length
        x1 = int(x0 + line_length * cos(theta) + 0.5)
        y1 = int(y0 + line_length * sin(theta) + 0.5)

Once the above changes are made run the script with an end position of say
(30, 90). It should fit into the old framework.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 06dash_gap_function.py

    .. literalinclude:: ../examples/dashes/06dash_gap_function.py
