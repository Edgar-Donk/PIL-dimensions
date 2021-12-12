==============
AA Dimensions
==============

Most of the PIL dimensions can be used as a template for the antialiased
scripts, angled text can be 
taken over with no change, other than the arrow needs especial attention 
as it is to be antialiased.

Some utility functions will be needed that are part of the DimLinesPIL 
module, so ensure that these can be accessed by an appropriate 
sys.path.append, in my case it was in the subdirectory **dims** 
so the antialiasing subdirecory **aadims** had a common parent **examples**.
When drawing antialiased dimensions, lines, arcs or circles use the module 
DimLinesAA.

The examples shown in the following dimensions include the coding from which 
the module DimLinesAA is built upon, compare to the original scripts in
PIL dimensions.

Often we require both the PIL drawing and image handles, this will fall away
once a dataclass or attr class is used.

.. toctree::
   :caption: PIL Dimensions...
   :maxdepth: 1
   
   intro_aadims
   line_aadim
   inner_aadim
   thick_aadim
   angle_aadim
   aaextenders
   outer_aadim
   slanted_aadim
   level_aadim
   aaleader
   dataclass
   attrs