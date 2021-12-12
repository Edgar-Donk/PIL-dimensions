import sys
sys.path.append('../dims')

from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import angled_text, DashedLine
from DimLinesDC import dc, slant_dim_dc, WideLineDC, dims_dc

dc.font = ImageFont.truetype('consola.ttf', 15)
dc.image = Image.new('RGB', (300, 160), '#FFFFDD')
dc.draw = ImageDraw.Draw(dc.image)

a = (30, 100)
c = (186, 100)
f = (236, 50)
e = (236, 100)
d = (276, 100)

WideLineDC(f, a, width=2)
WideLineDC(a, c, width=2)
WideLineDC(c, f, width=2)

DashedLine(dc.draw, c, d, dash=(5,5), width = 2, fill='black')
DashedLine(dc.draw, e, f, dash=(5,5), width = 1, fill='black')
slant_dim_dc(a, f, extA=(8, 2), text='d2')
dims_dc(a, c, extA=(-8,-2), text='d1')
dims_dc(f, e, extA=(8,2), text='d3', textorient='horizontal')

angled_text(dc.image, (a[0]-7, a[1]), text='A', angle=0, font=dc.font, fill='black')
angled_text(dc.image, (f[0]+10, f[1]-12), text='F', angle=0, font=dc.font, fill='black')
angled_text(dc.image, (e[0], e[1]+12), text='E', angle=0, font=dc.font, fill='black')
angled_text(dc.image, (c[0] -7, c[1]-10), text='C', angle=0, font=dc.font, fill='black')


#dc.image.save('../figures/draw_arrow.png')
dc.image.show()
