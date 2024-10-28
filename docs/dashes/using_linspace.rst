
Using Linspace
--------------

.. sidebar:: Linspace Parameters

    Linspace uses start and end parameters, with a third parameter showing
    how many intervals we want. By default the start and end are included in
    the resulting array. The size of the number of generated samples (num) 
    is inclusive, so add 1 to the 
    difference between end and start to calculate num::     

        linspace(start, end, num)

Next generate the array using start and end points of our coordinate pairs.
Use numpy's linspace function, this provides values at equal spacing.
Linspace can work with coordinate sets to produce equally spaced coordinates.
Use two linspace functions, the first to work with the start of the
coordinate pairs, the second to work with the finish of the coordinate pairs.
Join the two arrays produced by both linspaces using concatenate. 
Finally sort this final array. Use argsort which produces results directly 
as the desired column of coordinates::

    start_arr = linspace((30, 10), (30, 70), 3)
    end_arr = linspace((30, 24), (30, 84), 3)
    
    both_arr = concatenate([start_arr, end_arr], axis=0)

    arr = int_(both_arr[both_arr[:, 1].argsort()])

..

.. topic:: Sorting in Numpy

    Both np.sort and np.argsort can sort two dimensional arrays::

        >>> arr = np.array([[30, 10],
            [30, 24],
            [30, 40],
            [30, 54],
            [30, 70],
            [30, 84]])
    
        >>> np.sort(arr, axis=1)
        array([[10, 30],
            [24, 30],
            [30, 40],
            [30, 54],
            [30, 70],
            [30, 84]])

    Notice how the second row has been switched, as you see it is correct
    but not what is needed. Only one column or the other requires sorting::
    
        >>> arr[arr[:,1].sort()] # sorting on the 2nd column
        array([[[30, 10],
            [30, 24],
            [30, 40],
            [30, 54],
            [30, 70],
            [30, 84]]])
    
    The sort order can be changed by inverting the array::
    
        >>> arr[::-1]
        array([[30, 84],
            [30, 70],
            [30, 54],
            [30, 40],
            [30, 24],
            [30, 10]])

..

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 04line_start_finish_linspace.py

    .. literalinclude:: ../examples/dashes/04line_start_finish_linspace.py

The result should look exactly the same as with our array.
