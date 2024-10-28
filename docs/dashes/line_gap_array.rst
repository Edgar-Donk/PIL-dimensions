==================
Line and Gap Array
==================

Now create an array to replace the coordinates, and draw the line usng a 
``for loop`` and ``range``. Start the range at 0 and run using the array size, 
but at intervals of 2, so that every pair of coordinates draws the line from the 
start of the coordinate pair to the next coordinate pair. Arrange as a list
comprehension method.

.. sidebar:: List Comprehension

   The expression is enclosed in square brackets, if round brackets had been 
   used it would have created a generator expression, which needs a different
   method to give results.

::

    nr_lines = len(arr)
    [draw.line([tuple(arr[n]), tuple(arr[n+1])], width=1, fill='black')
            for n in range(0, nr_lines, 2)]

If all goes correctly the output should look the same as the previous script,
in particular the line and gap sizes.  

 .. figure:: ../figures/dashes/line_start_finish2.png
    :width: 779
    :height: 720
    :align: center

    Drawing three lines and two gaps using an array

..

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 03line_start_finish_array.py

    .. literalinclude:: ../examples/dashes/03line_start_finish_array.py