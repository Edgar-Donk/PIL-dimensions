=========================
Dashed Lines Introduction
=========================

PIL (Pillow) has no inbuilt function for drawing dashed lines in its Draw 
module, necessary for many sketches or drawings. This 
module was based on a program seen in `*Code Review*
<https://codereview.stackexchange.com/questions/70143/drawing-a-dashed-line-with-pygame>`_
where a simple case of drawing a dashed line with an equal number of spaces 
was shown (thankyou Richard Weiss).

There was a variable in the original script that allowed one to start with a
space rather than a dash, this is similar to 
the **dashoffset**, used in the Canvas, where dash patterns are started after 
a specified distance. Both these were not thought to be strictly necessary.

We will be using the ``dash`` tuple to make various patterns, see later 
:ref:`dash tuple<Different Line Patterns>`

One of the innate problems is that a line drawn on one of the major axes is
1.4 times shorter than the line at 45°. The user usually gives the begin and 
end points, so how the line changes is not remarked. To start with  
geometrical solutions are given, finally the problem is tackled using 
Bresenham's algorithm to draw a line which worked better. Extending this 
method the lines can be antialiased.