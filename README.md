# PIL-dimensions

Add a bit more versatility to an already versatile module, allowing the user to dimension drawings, with antialiasing as required and add dashed lines.
For those in a hurry and your python version is newer than 3.7, use the module DimLinesDC which requires a dataclass, otherwise use the module
DimLinesAA which is very similar. If antialiasing is not necessary use the module DimLinesPIL. All modules with annotations are found in the **scripts** directory.

## See the working copy

[Read the Docs](https://pil-dimensions.readthedocs.io/en/latest/index.html)

1. Contributors
    * Contact
2. Dimensions
    * Introduction Dimensions
    * Line Dimension
        * Dimension Properties
        * Arrow and Arrowshape Attributes
        * Create Dimension Script
    * Changes to Line Dimension
        * Changed Properties Line Dimension
        * Change Dimension Script
    * Angled Text
        * Angled Text Properties
        * Create Angled Text
    * Inner Dimension
        * Inner Dimension Properties
    * Thickness Dimension
        * Properties Thickness Dimension
    * Angle Dimension
        * Angle Dimension Properties
        * Create Angled Dimension
    * Extension Lines
    * Outer Dimensions
        * Outer Dimension Properties
    * Slanting Dimension
        * Slanting Dimension Properties
    * Level Dimensions
        * Level Properties
    * Leaders
        * Leader Properties
3. Dashed Lines
    * Dashed Lines Introduction
    * Line Example
        * Naive Lines and Gap
        * Enforce Correct Line and Gap Sizes
    * Line and Gap Array
    * Using Linspace
    * Convert to a Function
    * Line Length
    * Different Orientations
    * Different Line Patterns
        * Changes to Script
    * Revisit Line Lengths
    * Resampling Antialiasing
4. Rasterization Lines and Circles
    * Bresenham Algorithm
    * Line Rasterization
    * Pro-Active Antialiasing
    * Thick Lines
    * Thick Antialiased Lines
        * Antialias Limits
        * Reduce Antialias Duplication
        * Allow for other Colour Fills
    * Dashed Lines and Rasterization
        * Base Dashed Line
        * Adjust for Slope
        * Adding Antialiasing
    * Circles
        * Mid-Point Algorithm
        * Alois Zigl Algorithms
    * Thick Circles
        * Two Pixel Thick Circles Compared
        * Thicker Antialiased Circles
    * Antialiased Arc
5. Antialiased Dimensions
    * Introduction Antialiased Dimensions
    * AA Line Dimension
        * AA Dimension Attributes
        * AA Arrow and Arrowshape Attributes
        * Create dimension_aa Script
    * Inner AA Dimension
        * Inner AA Dimension Attributes
    * Thickness AA Dimension
        * Properties Thickness AA Dimension
    * Arc AA Dimension
        * Arc AA Dimension Properties
        * Create Arc AA Dimension
    * AA Extension Lines
    * Outer AA Dimensions
        * Outer AA Dimension Attributes
    * Slanting AA Dimension
        * Slanting AA Dimension Properties
    * Level AA Dimensions
    * Inner and Outer Levels
    * AA Leaders
        * AA Leader Properties
    * Dataclasses
        * Dimension Scripts used in DimLinesDC
        * Auxiliary DC Functions
    * Attributes (attrs)
        * attr Attributes
6. General
    * Classes
        * Classic Classes
        * Dataclass
        * Attrs
        * Applying dataclass and attrs
7. Sources for Documentation
    * Dimensions for PIL
        * DimLinesPIL package
    * AA Dimensions with PIL
        * DimLinesAA package
    * AA Dimensions with PIL and Dataclass
        * DimLinesDC package
    * AA Dimensions with atr
        * DimLinesattr package
