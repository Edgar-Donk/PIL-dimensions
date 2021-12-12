=============
Rasterization
=============

Drawing lines on a monitor involves rasterization, Bresenham is one of the
best known methods. A similar algorithm, based on Zigl, evaluates the line 
errors or differences
between the theoretical and actual line. This leads to a pro-active
method of antialiasing.

Similarly rasterized circle algorithms from Bresenham and Zigl led to 
antialiased circles. PIL already has a normal arc, therefore there is no 
need to duplicate this, 
but there is no antialiased arc, which will be derived from the 
antialiased circle. 

.. toctree::
   :caption: Rasterization...
   :maxdepth: 1
   
   bresen
   line_errors
   better_anti_alias
   thick_line
   thick_anti
   dash_lines
   circle
   thick_circles
   arc