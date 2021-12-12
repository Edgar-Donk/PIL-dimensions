from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import slant_dim, dims, DashedLine, angled_text

Font = ImageFont.truetype('consola.ttf', 15)
image2 = Image.new('RGB', (300, 160), '#FFFFDD')
sdraw = ImageDraw.Draw(image2)

a = (30, 100)
c = (186, 100)
f = (236, 50)
e = (236, 100)
d = (276, 100)

sdraw.line([a, c, f, a], fill='black', width=2)

DashedLine(sdraw, c, d, dash=(5,5), width = 2, fill='black')
DashedLine(sdraw, e, f, dash=(5,5), width = 1, fill='black')
slant_dim(image2,sdraw, a, f, extA=(8, 2), fill='black', width=1, text='d2', font=Font)
dims(image2,sdraw, a, c, extA=(-8,-2), text='d1', font=Font)
dims(image2,sdraw, f, e, extA=(-8,-2), text='d3', font=Font)

angled_text(image2, (a[0]-7, a[1]), text='A', angle=0, font=Font, fill='black')
angled_text(image2, (f[0]+10, f[1]-12), text='F', angle=0, font=Font, fill='black')
angled_text(image2, (e[0], e[1]+12), text='E', angle=0, font=Font, fill='black')
angled_text(image2, (c[0] -7, c[1]-10), text='C', angle=0, font=Font, fill='black')

image2.show()
#image2.save('../figures/draw_arrow.png') 
