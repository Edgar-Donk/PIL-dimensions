======================
Different Orientations
======================

The examples so far worked for vertical lines, let's expand on this. Our line 
length appears to be sorted out, the next problem is the second linspace. The
start and finish points need to be calculated based on the change due to the 
length of the dash, but as we have seen this must be reduced by one, to 
account for the way a line is drawn::

    # make second part of the line array
    x2 = x0 + int_up(dash2 * cos(theta))
    y2 = y0 + int_up(dash2 * sin(theta))
    x3 = x1 + int_up(dash2 * cos(theta))
    y3 = y1 + int_up(dash2 * sin(theta))

Change the orientation to horizontal and check the dash and gap sizes. Oops
not what we want, it's a continuous line, check on the final array(fin_arr),
it hasn't been sorted::

    # sort along the column, where the maximum change occurs
    if abs(x1 -x0) > abs(y1 -y0):
        fin_arr = int_(both_arr[both_arr[:, 0].argsort()])
    else:
        fin_arr = int_(both_arr[both_arr[:, 1].argsort()])

When sorting along the column, select the appropriate column, the x or y one,
[:, 0] and [:, 1] respectively. Use the column that changes most.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 07dash_gap_function.py

    .. literalinclude:: ../examples/dashes/07dash_gap_function.py