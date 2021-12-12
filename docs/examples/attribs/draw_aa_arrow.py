import sys
sys.path.append('../dims')

#from PIL import Image, ImageDraw, ImageFont
from DimLinesPIL import angled_text, DashedLine
from DimLinesattr import aq, slant_dim_attr, WideLineATTR, dims_attr

print(aq.width,aq.height)
#print(a.draw)
#ft = ImageFont.truetype('consola.ttf', 15)
#im = Image.new('RGB', (300, 160), (255,255,221))
#a = atr(im, font=ft)

ap = (30, 100)
cp = (186, 100)
fp = (236, 50)
ep = (236, 100)
dp = (276, 100)

WideLineATTR(fp, ap, width=2)
WideLineATTR(ap, cp, width=2)
WideLineATTR(cp, fp, width=2)

DashedLine(aq.draw, cp, dp, dash=(5,5), width = 2, fill=aq.fill)
DashedLine(aq.draw, ep, fp, dash=(5,5), width = 1, fill=aq.fill)
slant_dim_attr(ap, fp, extA=(8, 2), text='d2')
dims_attr(ap, cp, extA=(-8,-2), text='d1')
dims_attr(fp, ep, extA=(8,2), text='d3', textorient='horizontal')

angled_text(aq.image, (ap[0]-7, ap[1]), text='A', angle=0, font=aq.font, fill=aq.fill)
angled_text(aq.image, (fp[0]+10, fp[1]-12), text='F', angle=0, font=aq.font, fill=aq.fill)
angled_text(aq.image, (ep[0], ep[1]+12), text='E', angle=0, font=aq.font, fill=aq.fill)
angled_text(aq.image, (cp[0] -7, cp[1]-10), text='C', angle=0, font=aq.font, fill=aq.fill)


#dc.image.save('../figures/draw_arrow.png')
aq.image.show()
