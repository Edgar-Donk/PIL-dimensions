from PIL import Image, ImageDraw
from DimLinesPIL import dimension

image2 = Image.new('RGB', (120, 120), '#FFFFDD')
sdraw = ImageDraw.Draw(image2)

arrowhead=(8, 10, 3)
fill='black'
width=1
ptA=(10,110)
ptB=(10,10)
dimension(sdraw, ptA, ptB, width=width, fill=fill, arrowhead=arrowhead,
                arrow='both')
ptC=(20,10)
ptD=(110,110)
dimension(sdraw, ptC, ptD, width=width, fill=fill, arrowhead=arrowhead,
                arrow='both')

image2.show()
#image2.save('../../temp/dimension_2 arrows.png')